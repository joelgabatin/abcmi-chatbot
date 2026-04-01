-- Migration: Expand counseling_type values for chatbot scheduling flow
-- Run this in the Supabase SQL Editor if counseling_requests already exists

ALTER TABLE counseling_requests
    DROP CONSTRAINT IF EXISTS counseling_requests_counseling_type_check;

ALTER TABLE counseling_requests
    ADD CONSTRAINT counseling_requests_counseling_type_check
    CHECK (counseling_type IN ('face-to-face', 'online', 'call', 'video-call'));
