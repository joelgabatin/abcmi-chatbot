import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from database import Database, SiteSettings, ChurchHistory, StatementOfBelief, ChurchCoreValues, ChurchBranch, Pastor

db = Database()


class ActionGetBranches(Action):
    """Multi-turn branch finder: region → branch → details"""

    def name(self) -> Text:
        return "action_get_branches"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        db.connect()
        intent = tracker.latest_message.get("intent", {}).get("name")
        region_id = tracker.get_slot("selected_region_id")
        region_name = tracker.get_slot("selected_region_name")

        # Step 1: User asked about branches — list regions
        if intent == "ask_branches" or (not region_id):
            regions = ChurchBranch.get_all_regions(db)
            if regions:
                lines = ["Which region are you looking for? Here are our available regions:\n"]
                for i, r in enumerate(regions, 1):
                    lines.append(f"{i}. {r['name']}")
                lines.append("\nPlease type the region name or its number.")
                dispatcher.utter_message(text="\n".join(lines))
            else:
                dispatcher.utter_message(text="Sorry, I couldn't retrieve the regions right now.")
            return []

        # Step 2: User selected a region — list its branches
        if intent == "select_region" and region_id and not tracker.get_slot("selected_branch_id"):
            branches = ChurchBranch.get_branches_by_region(db, int(region_id))
            if branches:
                lines = [f"Here are the branches in {region_name}:\n"]
                for i, b in enumerate(branches, 1):
                    lines.append(f"{i}. {b['name']} — {b['location']}")
                lines.append("\nWhich branch would you like to know more about?")
                dispatcher.utter_message(text="\n".join(lines))
            else:
                dispatcher.utter_message(text=f"Sorry, no active branches found in {region_name}.")
            return []

        dispatcher.utter_message(text="Please tell me which region you are looking for.")
        return []


class ActionGetTotalBranches(Action):

    def name(self) -> Text:
        return "action_get_total_branches"

    def run(self, dispatcher, tracker, domain):
        db.connect()
        total = ChurchBranch.get_total_count(db)
        if total is not None:
            dispatcher.utter_message(text=f"ABCMI currently has {total} active branch(es) in total.")
        else:
            dispatcher.utter_message(text="Sorry, I couldn't retrieve the branch count right now.")
        return []


class ActionGetLocalBranches(Action):

    def name(self) -> Text:
        return "action_get_local_branches"

    def run(self, dispatcher, tracker, domain):
        db.connect()
        user_msg = tracker.latest_message.get("text", "").lower()
        local = ChurchBranch.get_local_branches(db)
        if local is not None:
            if "how many" in user_msg or "count" in user_msg or "total" in user_msg or "number" in user_msg:
                dispatcher.utter_message(text=f"ABCMI has {len(local)} local branch(es) across the Philippines.")
            else:
                lines = [f"Here are the local branches of ABCMI ({len(local)} total):\n"]
                for i, b in enumerate(local, 1):
                    lines.append(f"{i}. {b['name']} — {b['location']}")
                dispatcher.utter_message(text="\n".join(lines))
        else:
            dispatcher.utter_message(text="Sorry, I couldn't retrieve local branch information right now.")
        return []


class ActionGetInternationalBranches(Action):

    def name(self) -> Text:
        return "action_get_international_branches"

    def run(self, dispatcher, tracker, domain):
        db.connect()
        user_msg = tracker.latest_message.get("text", "").lower()
        intl = ChurchBranch.get_international_branches(db)
        if intl is not None:
            if "how many" in user_msg or "count" in user_msg or "total" in user_msg or "number" in user_msg:
                dispatcher.utter_message(text=f"ABCMI has {len(intl)} international branch(es).")
            else:
                if not intl:
                    dispatcher.utter_message(text="There are currently no active international branches.")
                else:
                    lines = [f"Here are the international branches of ABCMI ({len(intl)} total):\n"]
                    for i, b in enumerate(intl, 1):
                        lines.append(f"{i}. {b['name']} — {b['location']}")
                    dispatcher.utter_message(text="\n".join(lines))
        else:
            dispatcher.utter_message(text="Sorry, I couldn't retrieve international branch information right now.")
        return []


class ActionGetMission(Action):

    def name(self) -> Text:
        return "action_get_mission"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        db.connect()
        mission = SiteSettings.get_mission(db)
        if mission:
            dispatcher.utter_message(text=f"Our mission: {mission}")
        else:
            dispatcher.utter_message(
                text="Sorry, I couldn't retrieve the mission right now."
            )
        return []


class ActionGetVision(Action):

    def name(self) -> Text:
        return "action_get_vision"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        db.connect()
        vision = SiteSettings.get_vision(db)
        if vision:
            dispatcher.utter_message(text=f"Our vision: {vision}")
        else:
            dispatcher.utter_message(
                text="Sorry, I couldn't retrieve the vision right now."
            )
        return []


class ActionGetHistory(Action):

    def name(self) -> Text:
        return "action_get_history"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        db.connect()
        history = ChurchHistory.get_all(db)
        if history:
            lines = ["Here is the history of our church:\n"]
            for item in history:
                lines.append(f"• {item['year']}: {item['event']}")
            dispatcher.utter_message(text="\n".join(lines))
        else:
            dispatcher.utter_message(
                text="Sorry, I couldn't retrieve the church history right now."
            )
        return []


class ActionGetStatementOfBelief(Action):

    def name(self) -> Text:
        return "action_get_statement_of_belief"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        db.connect()
        statements = StatementOfBelief.get_all(db)
        if statements:
            lines = ["Here is what ABCMI Church believes:\n"]
            for item in statements:
                lines.append(f"{item['item_number']}. {item['statement']}")
            dispatcher.utter_message(text="\n".join(lines))
        else:
            dispatcher.utter_message(
                text="Sorry, I couldn't retrieve the statement of belief right now."
            )
        return []


class ActionGetDrivingForce(Action):

    def name(self) -> Text:
        return "action_get_driving_force"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        db.connect()
        driving_force = SiteSettings.get_driving_force(db)
        if driving_force:
            dispatcher.utter_message(text=driving_force)
        else:
            dispatcher.utter_message(
                text="Sorry, I couldn't retrieve the driving force right now."
            )
        return []


class ActionGetCoreValues(Action):

    def name(self) -> Text:
        return "action_get_core_values"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        db.connect()
        core_values = ChurchCoreValues.get_all(db)
        if core_values:
            lines = ["Here are the core values of ABCMI Church:\n"]
            for i, item in enumerate(core_values, 1):
                lines.append(f"{i}. {item['title']}")
            dispatcher.utter_message(text="\n".join(lines))
        else:
            dispatcher.utter_message(
                text="Sorry, I couldn't retrieve the core values right now."
            )
        return []


class ActionGetAllPastors(Action):

    def name(self) -> Text:
        return "action_get_all_pastors"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        db.connect()
        pastors = Pastor.get_all_with_branches(db)
        if pastors:
            lines = ["Here are the pastors of ABCMI Church:\n"]
            for p in pastors:
                branch = p.get("branches")
                branch_name = branch["name"] if branch else "Unassigned"
                lines.append(f"• {p['name']} ({p['role']}) — {branch_name}")
            dispatcher.utter_message(text="\n".join(lines))
        else:
            dispatcher.utter_message(
                text="Sorry, I couldn't retrieve the list of pastors right now."
            )
        return []


class ActionFindPastor(Action):

    def name(self) -> Text:
        return "action_find_pastor"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        db.connect()
        pastor_name = next(tracker.get_latest_entity_values("pastor_name"), None)
        if not pastor_name:
            dispatcher.utter_message(
                text="Could you please tell me the name of the pastor you're looking for?"
            )
            return []

        pastors = Pastor.find_by_name(db, pastor_name)
        if pastors:
            p = pastors[0]
            branch = p.get("branches")
            branch_name = branch["name"] if branch else "an ABCMI branch"
            branch_id = p.get("branch_id")
            dispatcher.utter_message(
                text=f"Yes! {p['name']} is one of our pastors. "
                     f"He/She serves as {p['role']} at {branch_name}."
            )
            return [
                SlotSet("last_pastor_name", p["name"]),
                SlotSet("last_branch_id", float(branch_id) if branch_id else None),
                SlotSet("last_branch_name", branch_name),
            ]
        else:
            dispatcher.utter_message(
                text=f"No, {pastor_name} is not listed as a pastor in our records."
            )
            return [
                SlotSet("last_pastor_name", None),
                SlotSet("last_branch_id", None),
                SlotSet("last_branch_name", None),
            ]


class ActionGetPastorBranchSchedule(Action):

    def name(self) -> Text:
        return "action_get_pastor_branch_schedule"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        db.connect()
        branch_id = tracker.get_slot("last_branch_id")
        branch_name = tracker.get_slot("last_branch_name")

        if not branch_id:
            dispatcher.utter_message(
                text="I don't have a branch in context yet. "
                     "Please first ask about a specific pastor so I know which branch to look up."
            )
            return []

        schedules = Pastor.get_branch_schedule(db, int(branch_id))
        if schedules:
            lines = [f"Here is the service schedule for {branch_name}:\n"]
            for s in schedules:
                desc = f" — {s['description']}" if s.get("description") else ""
                lines.append(f"• {s['day']} at {s['time']} ({s['type']}){desc}")
            dispatcher.utter_message(text="\n".join(lines))
        else:
            dispatcher.utter_message(
                text=f"Sorry, I couldn't find a service schedule for {branch_name} right now."
            )
        return []
