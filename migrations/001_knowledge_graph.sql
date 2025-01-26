-- Knowledge Graph Schema Migration

-- Drop existing constraints if they exist
ALTER TABLE IF EXISTS interests DROP CONSTRAINT IF EXISTS unique_user_interest;
ALTER TABLE IF EXISTS people DROP CONSTRAINT IF EXISTS unique_user_person;

-- Interests Table
CREATE TABLE IF NOT EXISTS interests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    name TEXT NOT NULL,
    summary TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_interests_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- People Table
CREATE TABLE IF NOT EXISTS people (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    name TEXT NOT NULL,
    relationship TEXT,
    demographic JSONB,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_people_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Stories Table
CREATE TABLE IF NOT EXISTS stories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    location TEXT,
    timestamp TIMESTAMP,
    tags TEXT[],
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_stories_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Relationship Tables
CREATE TABLE IF NOT EXISTS story_people (
    story_id UUID NOT NULL,
    person_id UUID NOT NULL,
    PRIMARY KEY (story_id, person_id),
    CONSTRAINT fk_story_people_story FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE,
    CONSTRAINT fk_story_people_person FOREIGN KEY (person_id) REFERENCES people(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS person_interests (
    person_id UUID NOT NULL,
    interest_id UUID NOT NULL,
    PRIMARY KEY (person_id, interest_id),
    CONSTRAINT fk_person_interests_person FOREIGN KEY (person_id) REFERENCES people(id) ON DELETE CASCADE,
    CONSTRAINT fk_person_interests_interest FOREIGN KEY (interest_id) REFERENCES interests(id) ON DELETE CASCADE
);

-- Drop existing indexes if they exist
DROP INDEX IF EXISTS idx_interests_user_id;
DROP INDEX IF EXISTS idx_people_user_id;
DROP INDEX IF EXISTS idx_stories_user_id;
DROP INDEX IF EXISTS idx_stories_timestamp;

-- Create indexes
CREATE INDEX idx_interests_user_id ON interests(user_id);
CREATE INDEX idx_people_user_id ON people(user_id);
CREATE INDEX idx_stories_user_id ON stories(user_id);
CREATE INDEX idx_stories_timestamp ON stories(timestamp);

-- Add unique constraints
ALTER TABLE interests ADD CONSTRAINT unique_user_interest UNIQUE (user_id, name);
ALTER TABLE people ADD CONSTRAINT unique_user_person UNIQUE (user_id, name); 