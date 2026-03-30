-- Migration: Create prayer_requests table
-- Run this in the Supabase SQL Editor

CREATE TABLE IF NOT EXISTS prayer_requests (
    id             SERIAL PRIMARY KEY,
    name           TEXT        NOT NULL,
    phone_number   TEXT        NOT NULL,
    address        TEXT,
    prayer_request TEXT        NOT NULL,
    face_to_face   BOOLEAN     NOT NULL DEFAULT FALSE,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
