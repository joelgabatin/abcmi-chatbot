-- Migration: Create church_events table
-- Run this in the Supabase SQL Editor

CREATE TABLE IF NOT EXISTS church_events (
    id               SERIAL PRIMARY KEY,
    name             TEXT        NOT NULL,
    description      TEXT,
    event_date       DATE,
    event_time       TIME,
    location         TEXT,
    slots_available  INT,
    registration_url TEXT,
    status           TEXT        NOT NULL DEFAULT 'upcoming',
    sort_order       INT         NOT NULL DEFAULT 0
);

-- Sample data
INSERT INTO church_events (name, description, event_date, event_time, location, slots_available, registration_url, status, sort_order) VALUES
    ('Youth Camp 2026',       'Annual youth gathering and fellowship',      '2026-04-15', '08:00', 'ABCMI Main Branch, Baguio City', 100, 'https://abcmi.org/events/youth-camp-2026',       'upcoming', 1),
    ('Easter Celebration',    'Church-wide Easter Sunday service',          '2026-04-20', '09:00', 'ABCMI Main Branch, Baguio City', 500, 'https://abcmi.org/events/easter-2026',           'upcoming', 2),
    ('Leadership Conference', 'Annual leadership and ministry conference',  '2026-05-10', '08:00', 'ABCMI Convention Hall',          200, 'https://abcmi.org/events/leadership-conf-2026', 'upcoming', 3);
