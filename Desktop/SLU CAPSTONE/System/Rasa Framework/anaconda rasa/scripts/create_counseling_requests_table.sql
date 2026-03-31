-- Migration: Create counseling_requests table
-- Run this in the Supabase SQL Editor

CREATE TABLE IF NOT EXISTS counseling_requests (
    id               BIGSERIAL PRIMARY KEY,
    full_name        TEXT        NOT NULL,
    contact_number   TEXT        NOT NULL,
    address          TEXT        NOT NULL DEFAULT 'Not provided via chatbot',
    facebook_account TEXT        NOT NULL DEFAULT 'Not provided',
    preferred_date   DATE        NOT NULL,
    preferred_time   TEXT        NOT NULL,
    counseling_type  TEXT        NOT NULL CHECK (counseling_type IN ('face-to-face', 'online')),
    is_member        BOOLEAN     NOT NULL DEFAULT FALSE,
    concern          TEXT        NOT NULL,
    status           TEXT        NOT NULL DEFAULT 'pending',
    admin_notes      TEXT,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
