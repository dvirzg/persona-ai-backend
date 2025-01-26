-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create users table if it doesn't exist
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT NOT NULL UNIQUE,
    name TEXT,
    password TEXT NOT NULL,
    personality_traits JSONB DEFAULT NULL,
    communication_style JSONB DEFAULT NULL,
    demographic JSONB DEFAULT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
); 