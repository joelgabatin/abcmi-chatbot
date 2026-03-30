-- Migration: Create church_founders table
-- Run this in the Supabase SQL Editor

CREATE TABLE IF NOT EXISTS church_founders (
    id          SERIAL PRIMARY KEY,
    name        TEXT NOT NULL,
    title       TEXT,
    role        TEXT NOT NULL DEFAULT 'Founder',
    description TEXT,
    sort_order  INT  NOT NULL DEFAULT 0
);

-- Seed data
INSERT INTO church_founders (name, title, role, sort_order) VALUES
    ('Marino S. Coyoy', 'Rev.', 'Founder',   1),
    ('Elizabeth L. Coyoy', NULL,  'Foundress', 2);
