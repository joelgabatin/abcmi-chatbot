-- Migration: Create rasa_trackers table for persistent Rasa tracker store
-- Run this in the Supabase SQL Editor

CREATE TABLE IF NOT EXISTS rasa_trackers (
    sender_id            TEXT PRIMARY KEY,
    tracker_state        JSONB       NOT NULL DEFAULT '{}'::jsonb,
    events               JSONB       NOT NULL DEFAULT '[]'::jsonb,
    current_session_id   TEXT,
    last_event_timestamp DOUBLE PRECISION,
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_rasa_trackers_updated_at
    ON rasa_trackers (updated_at DESC);
