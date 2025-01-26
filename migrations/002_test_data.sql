-- Test Data Migration

-- Create test user if not exists
INSERT INTO users (id, email, name, password, communication_style, personality_traits, demographic)
VALUES (
    gen_random_uuid(),
    'test@example.com',
    'Alex Chen',
    'test_password',
    '{
        "word_count": {
            "target": 150,
            "tolerance": 50
        },
        "technical_level": 4.8,
        "questions_per_response": 1,
        "reasoning_detail": 4.5,
        "formality_level": 4.0,
        "response_structure": ["context", "analysis", "suggestion"],
        "code_examples": {
            "frequency": "high",
            "detail_level": 4.5
        }
    }',
    '{
        "analytical": 4.8,
        "curious": 4.5,
        "technical": 4.7,
        "empathetic": 3.8,
        "detail_oriented": 4.6
    }',
    '{
        "age_range": "25-35",
        "interests": ["technology", "science", "philosophy"],
        "profession": "Software Engineer"
    }'
)
ON CONFLICT (email) DO UPDATE 
SET name = EXCLUDED.name,
    communication_style = EXCLUDED.communication_style,
    personality_traits = EXCLUDED.personality_traits,
    demographic = EXCLUDED.demographic;

-- Update test user profile
UPDATE users 
SET personality_traits = '{
    "traits": [
        "analytical",
        "curious",
        "tech-savvy",
        "empathetic",
        "detail-oriented"
    ]
}'::jsonb,
    communication_style = '{
        "style_description": "Prefers detailed technical discussions with clear examples",
        "formality": {
            "level": 3.5,
            "context_dependent": true
        },
        "detail_preference": "high",
        "example_preference": "frequent",
        "depth_preference": "in-depth",
        "interaction_style": "exploratory"
    }'::jsonb,
    demographic = '{
        "age_range": "25-35",
        "profession": "Software Engineer",
        "interests": ["technology", "science", "philosophy"]
    }'::jsonb
WHERE email = 'test@example.com';

-- Add interests
INSERT INTO interests (id, user_id, name, summary) VALUES
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'test@example.com'), 'Machine Learning', 'Deep interest in neural networks and AI applications'),
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'test@example.com'), 'AI Ethics', 'Concerned about responsible AI development and societal impact'),
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'test@example.com'), 'Philosophy', 'Particularly interested in ethics and epistemology'),
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'test@example.com'), 'Rock Climbing', 'Indoor and outdoor climbing, particularly bouldering'),
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'test@example.com'), 'Science Fiction', 'Enjoys exploring technological and social implications in fiction');

-- Add people
INSERT INTO people (id, user_id, name, relationship, notes) VALUES
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'test@example.com'), 'Sarah', 'Colleague', 'Met at AI Ethics conference. Regular discussions about ML and ethics. Very knowledgeable about neural networks.'),
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'test@example.com'), 'David', 'Climbing Partner', 'Weekly climbing sessions. Great at breaking down complex climbing problems.'),
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'test@example.com'), 'Maria', 'Book Club Friend', 'Leads monthly sci-fi book club. Fascinating perspectives on technology in literature.');

-- Add stories
INSERT INTO stories (id, user_id, title, description, location, timestamp) VALUES
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'test@example.com'), 'First ML Project Success', 'Successfully implemented a computer vision model for identifying plant diseases. Sarah provided crucial guidance on model architecture.', 'Tech Hub Office', '2023-09-15'),
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'test@example.com'), 'Ethics Panel Discussion', 'Participated in AI ethics panel with Sarah. Discussed implications of AI in healthcare and privacy concerns.', 'University Conference Center', '2023-11-20'),
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'test@example.com'), 'V5 Boulder Problem', 'Finally solved the challenging overhang problem at the climbing gym. David suggested a key beta for the crux move.', 'Boulder Gym', '2023-12-05');

-- Connect stories with people
INSERT INTO story_people (story_id, person_id)
SELECT s.id, p.id
FROM stories s
CROSS JOIN people p
WHERE s.title = 'First ML Project Success' AND p.name = 'Sarah'
   OR s.title = 'Ethics Panel Discussion' AND p.name = 'Sarah'
   OR s.title = 'V5 Boulder Problem' AND p.name = 'David';

-- Connect people with interests
INSERT INTO person_interests (person_id, interest_id)
SELECT p.id, i.id
FROM people p, interests i
WHERE p.name = 'Sarah' AND i.name IN ('Machine Learning', 'AI Ethics')
UNION
SELECT p.id, i.id
FROM people p, interests i
WHERE p.name = 'David' AND i.name = 'Rock Climbing'
UNION
SELECT p.id, i.id
FROM people p, interests i
WHERE p.name = 'Maria' AND i.name IN ('Science Fiction', 'Philosophy'); 