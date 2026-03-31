-- Migration: Create readable chat history tables
-- Run this in the Supabase SQL Editor

CREATE TABLE IF NOT EXISTS visitors (
    id         BIGSERIAL PRIMARY KEY,
    visitor_id VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS chat_sessions (
    id         BIGSERIAL PRIMARY KEY,
    session_id VARCHAR(100) NOT NULL UNIQUE,
    visitor_id VARCHAR(100) NOT NULL,
    started_at TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    ended_at   TIMESTAMPTZ,
    CONSTRAINT fk_chat_sessions_visitor_id
        FOREIGN KEY (visitor_id) REFERENCES visitors(visitor_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS chat_messages (
    id           BIGSERIAL PRIMARY KEY,
    session_id   VARCHAR(100) NOT NULL,
    visitor_id   VARCHAR(100) NOT NULL,
    sender       VARCHAR(10)  NOT NULL CHECK (sender IN ('user', 'bot')),
    message_text TEXT         NOT NULL,
    created_at   TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_chat_messages_session_id
        FOREIGN KEY (session_id) REFERENCES chat_sessions(session_id) ON DELETE CASCADE,
    CONSTRAINT fk_chat_messages_visitor_id
        FOREIGN KEY (visitor_id) REFERENCES visitors(visitor_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_chat_sessions_visitor_id
    ON chat_sessions (visitor_id);

CREATE INDEX IF NOT EXISTS idx_chat_messages_session_id
    ON chat_messages (session_id);

CREATE INDEX IF NOT EXISTS idx_chat_messages_visitor_id
    ON chat_messages (visitor_id);
