from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional, Text

from supabase import create_client

from config import NEXT_PUBLIC_SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY
from rasa.core.brokers.broker import EventBroker
from rasa.core.tracker_stores.tracker_store import TrackerStore
from rasa.shared.core.domain import Domain
from rasa.shared.core.events import SessionStarted
from rasa.shared.core.trackers import DialogueStateTracker, EventVerbosity


class SupabaseTrackerStore(TrackerStore):
    """Persist conversation trackers in Supabase using a single JSON row per sender."""

    VISITORS_TABLE = "visitors"
    CHAT_SESSIONS_TABLE = "chat_sessions"
    CHAT_MESSAGES_TABLE = "chat_messages"

    def __init__(
        self,
        domain: Optional[Domain] = None,
        host: Optional[Text] = None,
        event_broker: Optional[EventBroker] = None,
        table_name: Text = "rasa_trackers",
        **kwargs: Dict[Text, Any],
    ) -> None:
        super().__init__(domain, event_broker, **kwargs)
        supabase_url = host or NEXT_PUBLIC_SUPABASE_URL
        self.client = create_client(supabase_url, SUPABASE_SERVICE_ROLE_KEY)
        self.table_name = table_name

    def _warn(self, action: Text, error: Exception) -> None:
        print(
            f"[WARN] Supabase tracker store could not {action} using table "
            f"'{self.table_name}': {error}"
        )

    @staticmethod
    def _events_since_last_session_start(events: List[Dict[Text, Any]]) -> List[Dict[Text, Any]]:
        events_after_session_start: List[Dict[Text, Any]] = []
        for event in reversed(events):
            events_after_session_start.append(event)
            if event.get("event") == SessionStarted.type_name:
                break
        return list(reversed(events_after_session_start))

    def _build_payload(self, tracker: DialogueStateTracker) -> Dict[Text, Any]:
        state = tracker.current_state(EventVerbosity.ALL)
        events = state.get("events", [])
        now_iso = datetime.now(timezone.utc).isoformat()
        return {
            "sender_id": tracker.sender_id,
            "tracker_state": state,
            "events": events,
            "last_event_timestamp": events[-1].get("timestamp") if events else None,
            "updated_at": now_iso,
        }

    @staticmethod
    def _timestamp_to_iso(timestamp: Optional[float]) -> Text:
        if timestamp is None:
            return datetime.now(timezone.utc).isoformat()
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()

    @staticmethod
    def _default_session_id(sender_id: Text, timestamp: Optional[float]) -> Text:
        session_suffix = int(timestamp) if timestamp else "default"
        return f"{sender_id}-{session_suffix}"

    @staticmethod
    def _get_event_metadata(event: Dict[Text, Any]) -> Dict[Text, Any]:
        metadata = event.get("metadata")
        return metadata if isinstance(metadata, dict) else {}

    @staticmethod
    def _extract_message_text(event: Dict[Text, Any]) -> Optional[Text]:
        if event.get("event") == "user":
            return event.get("text")

        if event.get("event") != "bot":
            return None

        text = event.get("text")
        if text:
            return text

        data = event.get("data") or {}
        if isinstance(data, dict):
            if data.get("text"):
                return data["text"]
            if data:
                return json.dumps(data, ensure_ascii=True)

        return None

    def _get_existing_tracker_row(self, sender_id: Text) -> Optional[Dict[Text, Any]]:
        try:
            response = (
                self.client.table(self.table_name)
                .select("events,current_session_id")
                .eq("sender_id", sender_id)
                .limit(1)
                .execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            self._warn("read existing tracker state", e)
            return None

    def _upsert_visitor(self, sender_id: Text, timestamp: Optional[float]) -> None:
        try:
            self.client.table(self.VISITORS_TABLE).upsert(
                {
                    "visitor_id": sender_id,
                    "updated_at": self._timestamp_to_iso(timestamp),
                },
                on_conflict="visitor_id",
            ).execute()
        except Exception as e:
            self._warn("upsert visitor", e)

    def _close_session(self, session_id: Optional[Text], ended_at: Optional[float]) -> None:
        if not session_id:
            return
        try:
            (
                self.client.table(self.CHAT_SESSIONS_TABLE)
                .update({"ended_at": self._timestamp_to_iso(ended_at)})
                .eq("session_id", session_id)
                .is_("ended_at", "null")
                .execute()
            )
        except Exception as e:
            self._warn("close chat session", e)

    def _ensure_session(
        self,
        sender_id: Text,
        session_id: Text,
        started_at: Optional[float],
    ) -> None:
        try:
            self.client.table(self.CHAT_SESSIONS_TABLE).upsert(
                {
                    "session_id": session_id,
                    "visitor_id": sender_id,
                    "started_at": self._timestamp_to_iso(started_at),
                },
                on_conflict="session_id",
            ).execute()
        except Exception as e:
            self._warn("upsert chat session", e)

    def _insert_chat_message(
        self,
        sender_id: Text,
        session_id: Text,
        event: Dict[Text, Any],
    ) -> None:
        message_text = self._extract_message_text(event)
        if not message_text:
            return

        sender_type = "user" if event.get("event") == "user" else "bot"
        try:
            self.client.table(self.CHAT_MESSAGES_TABLE).insert(
                {
                    "session_id": session_id,
                    "visitor_id": sender_id,
                    "sender": sender_type,
                    "message_text": message_text,
                    "created_at": self._timestamp_to_iso(event.get("timestamp")),
                }
            ).execute()
        except Exception as e:
            self._warn("insert chat message", e)

    def _sync_chat_history(
        self,
        sender_id: Text,
        all_events: List[Dict[Text, Any]],
        previous_events: List[Dict[Text, Any]],
        previous_session_id: Optional[Text],
    ) -> Optional[Text]:
        self._upsert_visitor(
            sender_id,
            all_events[-1].get("timestamp") if all_events else None,
        )

        current_session_id = previous_session_id
        new_events = (
            all_events[len(previous_events):]
            if len(all_events) >= len(previous_events)
            else all_events
        )

        if not new_events and not current_session_id and all_events:
            current_session_id = self._default_session_id(
                sender_id,
                all_events[0].get("timestamp"),
            )
            self._ensure_session(sender_id, current_session_id, all_events[0].get("timestamp"))

        for event in new_events:
            metadata = self._get_event_metadata(event)
            requested_session_id = metadata.get("session_id")

            if event.get("event") == SessionStarted.type_name:
                self._close_session(current_session_id, event.get("timestamp"))
                current_session_id = requested_session_id or self._default_session_id(
                    sender_id,
                    event.get("timestamp"),
                )
                self._ensure_session(sender_id, current_session_id, event.get("timestamp"))
                continue

            if not current_session_id:
                current_session_id = requested_session_id or self._default_session_id(
                    sender_id,
                    event.get("timestamp"),
                )
                self._ensure_session(sender_id, current_session_id, event.get("timestamp"))
            elif requested_session_id and requested_session_id != current_session_id:
                self._close_session(current_session_id, event.get("timestamp"))
                current_session_id = requested_session_id
                self._ensure_session(sender_id, current_session_id, event.get("timestamp"))

            if event.get("event") in {"user", "bot"}:
                self._insert_chat_message(sender_id, current_session_id, event)

        return current_session_id

    async def save(self, tracker: DialogueStateTracker) -> None:
        await self.stream_events(tracker)
        payload = self._build_payload(tracker)
        existing_row = self._get_existing_tracker_row(tracker.sender_id) or {}
        previous_events = existing_row.get("events") or []
        payload["current_session_id"] = self._sync_chat_history(
            tracker.sender_id,
            payload["events"],
            previous_events,
            existing_row.get("current_session_id"),
        )
        try:
            self.client.table(self.table_name).upsert(payload, on_conflict="sender_id").execute()
        except Exception as e:
            self._warn("save tracker state", e)

    async def retrieve(self, sender_id: Text) -> Optional[DialogueStateTracker]:
        return await self._retrieve(sender_id, fetch_all_sessions=False)

    async def retrieve_full_tracker(
        self, conversation_id: Text
    ) -> Optional[DialogueStateTracker]:
        return await self._retrieve(conversation_id, fetch_all_sessions=True)

    async def _retrieve(
        self, sender_id: Text, fetch_all_sessions: bool
    ) -> Optional[DialogueStateTracker]:
        try:
            response = (
                self.client.table(self.table_name)
                .select("events")
                .eq("sender_id", sender_id)
                .limit(1)
                .execute()
            )
        except Exception as e:
            self._warn("retrieve tracker state", e)
            return None

        if not response.data:
            return None

        events = response.data[0].get("events") or []
        if not fetch_all_sessions:
            events = self._events_since_last_session_start(events)

        if not events:
            return None

        return DialogueStateTracker.from_dict(sender_id, events, self.domain.slots)

    async def delete(self, sender_id: Text) -> None:
        try:
            self.client.table(self.table_name).delete().eq("sender_id", sender_id).execute()
        except Exception as e:
            self._warn("delete tracker state", e)

    async def keys(self) -> Iterable[Text]:
        try:
            response = self.client.table(self.table_name).select("sender_id").execute()
            return [row["sender_id"] for row in response.data or [] if row.get("sender_id")]
        except Exception as e:
            self._warn("list tracker keys", e)
            return []

    async def update(
        self, tracker: DialogueStateTracker, apply_deletion_only: bool = True
    ) -> None:
        await self.save(tracker)
