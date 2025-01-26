-- Test Personas Migration

-- 1. Technical Professional (Emily Zhang)
INSERT INTO users (id, email, name, password)
VALUES (
    gen_random_uuid(),
    'emily.zhang@example.com',
    'Emily Zhang',
    'test_password'
)
ON CONFLICT (email) DO UPDATE 
SET name = EXCLUDED.name;

UPDATE users 
SET personality_traits = '{
    "traits": [
        "analytical",
        "precise",
        "intellectual",
        "curious",
        "systematic"
    ]
}'::jsonb,
    communication_style = '{
        "message_length": {
            "preferred_word_count": 150,
            "range_tolerance": 50,
            "description": "Prefers comprehensive responses that thoroughly explain concepts"
        },
        "technical_depth": {
            "level": 4.8,
            "scale_info": "1-5 where 5 is most technical",
            "description": "Expects technical terminology and precise explanations"
        },
        "question_frequency": {
            "questions_per_response": 1,
            "description": "Prefers focused, single follow-up questions that probe deeper into technical aspects"
        },
        "reasoning_visibility": {
            "level": 4.5,
            "scale_info": "1-5 where 5 shows all reasoning",
            "description": "Wants to see the logical steps and technical considerations behind suggestions"
        },
        "formality_level": {
            "level": 4.0,
            "scale_info": "1-5",
            "description": "Professional tone with technical precision, but not overly formal"
        },
        "response_structure": {
            "type": "structured",
            "elements": ["context", "technical explanation", "practical application", "follow-up"],
            "description": "Prefers well-organized responses with clear sections"
        },
        "code_examples": {
            "frequency": "high",
            "detail_level": 4.5,
            "scale_info": "1-5",
            "description": "Appreciates detailed code examples when relevant"
        }
    }'::jsonb,
    demographic = '{
        "age_range": "28-35",
        "profession": "Senior Systems Architect",
        "interests": ["distributed systems", "quantum computing", "mathematics"]
    }'::jsonb
WHERE email = 'emily.zhang@example.com';

-- Emily's interests
INSERT INTO interests (id, user_id, name, summary) VALUES
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'emily.zhang@example.com'), 'Distributed Systems', 'Fascinated by scalable architecture and system design'),
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'emily.zhang@example.com'), 'Quantum Computing', 'Following developments in quantum algorithms and applications'),
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'emily.zhang@example.com'), 'Mathematics', 'Particularly interested in category theory and its applications to CS');

-- Emily's social circle
INSERT INTO people (id, user_id, name, relationship, demographic, notes) VALUES
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'emily.zhang@example.com'), 'Dr. Chen', 'Mentor', 
    '{"profession": "Professor", "interests": ["quantum computing", "theoretical CS"], "met": "2020-09"}'::jsonb,
    'PhD advisor, brilliant researcher in quantum algorithms. Weekly research discussions.'),
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'emily.zhang@example.com'), 'Marcus', 'Colleague', 
    '{"profession": "Software Architect", "interests": ["distributed systems", "cloud computing"], "met": "2022-03"}'::jsonb,
    'Lead architect at work, great technical discussions about system design.');

-- 2. Emotional Support Seeker (Sophie Martinez)
INSERT INTO users (id, email, name, password)
VALUES (
    gen_random_uuid(),
    'sophie.m@example.com',
    'Sophie Martinez',
    'test_password'
)
ON CONFLICT (email) DO UPDATE 
SET name = EXCLUDED.name;

UPDATE users 
SET personality_traits = '{
    "traits": [
        "empathetic",
        "emotional",
        "introspective",
        "sensitive",
        "caring"
    ]
}'::jsonb,
    communication_style = '{
        "message_length": {
            "preferred_word_count": 100,
            "range_tolerance": 30,
            "description": "Prefers concise but emotionally attuned responses"
        },
        "empathy_level": {
            "level": 4.8,
            "scale_info": "1-5 where 5 is most empathetic",
            "description": "Needs strong emotional validation and understanding"
        },
        "question_frequency": {
            "questions_per_response": 2,
            "type": "reflective",
            "description": "Appreciates questions that help explore feelings and perspectives"
        },
        "personal_examples": {
            "frequency": "high",
            "relevance_required": 4.5,
            "scale_info": "1-5",
            "description": "Values relatable examples and scenarios"
        },
        "validation_style": {
            "explicit_validation": true,
            "validation_first": true,
            "description": "Start with emotional validation before suggestions"
        },
        "formality_level": {
            "level": 2.0,
            "scale_info": "1-5",
            "description": "Warm and personal, like talking to a friend"
        },
        "response_structure": {
            "type": "flowing",
            "elements": ["validation", "exploration", "gentle suggestions"],
            "description": "Natural, conversational flow rather than structured responses"
        }
    }'::jsonb,
    demographic = '{
        "age_range": "25-30",
        "profession": "Social Worker",
        "interests": ["psychology", "relationships", "self-improvement"]
    }'::jsonb
WHERE email = 'sophie.m@example.com';

-- Sophie's interests
INSERT INTO interests (id, user_id, name, summary) VALUES
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'sophie.m@example.com'), 'Psychology', 'Understanding human behavior and relationships'),
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'sophie.m@example.com'), 'Self-Help', 'Personal growth and emotional well-being'),
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'sophie.m@example.com'), 'Meditation', 'Finding inner peace and emotional balance');

-- Sophie's social circle and relationship dynamics
INSERT INTO people (id, user_id, name, relationship, demographic, notes) VALUES
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'sophie.m@example.com'), 'Jake', 'Ex-boyfriend', 
    '{"profession": "Marketing Manager", "interests": ["travel", "music"], "met": "2021-06"}'::jsonb,
    'Complex relationship, still processing the breakup. Difficulty with boundaries.'),
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'sophie.m@example.com'), 'Lisa', 'Best Friend', 
    '{"profession": "Therapist", "interests": ["psychology", "yoga"], "met": "2019-01"}'::jsonb,
    'Always there for emotional support, but sometimes feel like I burden her too much.');

-- 3. University Student (Tom Chen)
INSERT INTO users (id, email, name, password)
VALUES (
    gen_random_uuid(),
    'tom.chen@example.com',
    'Tom Chen',
    'test_password'
)
ON CONFLICT (email) DO UPDATE 
SET name = EXCLUDED.name;

UPDATE users 
SET personality_traits = '{
    "traits": [
        "adaptable",
        "enthusiastic",
        "social",
        "sometimes anxious",
        "creative"
    ]
}'::jsonb,
    communication_style = '{
        "message_length": {
            "preferred_word_count": 80,
            "range_tolerance": 20,
            "description": "Prefers shorter, clear messages with key points highlighted"
        },
        "formality_level": {
            "level": 1.5,
            "scale_info": "1-5",
            "description": "Very casual, using current slang and informal language"
        },
        "encouragement_level": {
            "level": 4.5,
            "scale_info": "1-5",
            "description": "Needs frequent positive reinforcement and confidence boosting"
        },
        "question_frequency": {
            "questions_per_response": 1,
            "type": "guiding",
            "description": "Simple, direct questions that help break down complex topics"
        },
        "examples_style": {
            "type": "relatable",
            "context": "student life",
            "description": "Uses examples from academic and campus life contexts"
        },
        "response_structure": {
            "type": "casual",
            "elements": ["main point", "quick explanation", "relatable example"],
            "description": "Keep it simple and easy to follow"
        },
        "emoji_usage": {
            "frequency": "moderate",
            "description": "Occasional emojis to maintain engagement"
        }
    }'::jsonb,
    demographic = '{
        "age_range": "19-22",
        "profession": "University Student",
        "interests": ["computer science", "gaming", "anime"]
    }'::jsonb
WHERE email = 'tom.chen@example.com';

-- Tom's interests and academic life
INSERT INTO interests (id, user_id, name, summary) VALUES
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'tom.chen@example.com'), 'Computer Science', 'Major, struggling with algorithms but loving web dev'),
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'tom.chen@example.com'), 'Gaming', 'Competitive eSports, part of university team'),
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'tom.chen@example.com'), 'Anime', 'Active in anime club, organizing conventions');

-- Tom's university life and friends
INSERT INTO people (id, user_id, name, relationship, demographic, notes) VALUES
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'tom.chen@example.com'), 'Prof. Williams', 'Professor', 
    '{"profession": "CS Professor", "interests": ["algorithms", "teaching"], "met": "2023-09"}'::jsonb,
    'Algorithms professor, intimidating but trying to get help during office hours.'),
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'tom.chen@example.com'), 'Emma', 'Study Partner', 
    '{"profession": "Student", "interests": ["computer science", "mathematics"], "met": "2023-09"}'::jsonb,
    'Smart classmate, might have a crush on her but afraid to say anything.');

-- 4. Conflict Navigator (Michael Ross)
INSERT INTO users (id, email, name, password)
VALUES (
    gen_random_uuid(),
    'michael.r@example.com',
    'Michael Ross',
    'test_password'
)
ON CONFLICT (email) DO UPDATE 
SET name = EXCLUDED.name;

UPDATE users 
SET personality_traits = '{
    "traits": [
        "assertive",
        "strong-willed",
        "direct",
        "passionate",
        "defensive"
    ]
}'::jsonb,
    communication_style = '{
        "message_length": {
            "preferred_word_count": 120,
            "range_tolerance": 30,
            "description": "Direct and comprehensive enough to address points of conflict"
        },
        "directness_level": {
            "level": 4.8,
            "scale_info": "1-5",
            "description": "Very direct communication with clear statements"
        },
        "perspective_offering": {
            "frequency": "high",
            "balance_level": 4.5,
            "scale_info": "1-5",
            "description": "Regularly offer alternative viewpoints and perspectives"
        },
        "question_frequency": {
            "questions_per_response": 2,
            "type": "challenging",
            "description": "Questions that challenge assumptions and promote reflection"
        },
        "solution_focus": {
            "level": 4.0,
            "scale_info": "1-5",
            "description": "Emphasis on practical solutions and action steps"
        },
        "response_structure": {
            "type": "analytical",
            "elements": ["situation analysis", "multiple perspectives", "actionable steps"],
            "description": "Structured analysis with clear conclusions"
        }
    }'::jsonb,
    demographic = '{
        "age_range": "30-35",
        "profession": "Project Manager",
        "interests": ["leadership", "politics", "debate"]
    }'::jsonb
WHERE email = 'michael.r@example.com';

-- Michael's interests
INSERT INTO interests (id, user_id, name, summary) VALUES
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'michael.r@example.com'), 'Leadership', 'Developing management skills and team dynamics'),
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'michael.r@example.com'), 'Politics', 'Strong political views and activism'),
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'michael.r@example.com'), 'Debate', 'Enjoys intellectual arguments and discussions');

-- Michael's complex relationships
INSERT INTO people (id, user_id, name, relationship, demographic, notes) VALUES
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'michael.r@example.com'), 'Karen', 'Team Lead', 
    '{"profession": "Senior Manager", "interests": ["management", "agile"], "met": "2022-01"}'::jsonb,
    'Constant disagreements about project management style. Feels like she undermines my authority.'),
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'michael.r@example.com'), 'John', 'Brother', 
    '{"profession": "Lawyer", "interests": ["politics", "debate"], "met": "1990-01"}'::jsonb,
    'Opposite political views, family gatherings are tense. Want to maintain relationship despite differences.');

-- 5. Self-Discovery Journey (Maya Patel)
INSERT INTO users (id, email, name, password)
VALUES (
    gen_random_uuid(),
    'maya.p@example.com',
    'Maya Patel',
    'test_password'
)
ON CONFLICT (email) DO UPDATE 
SET name = EXCLUDED.name;

UPDATE users 
SET personality_traits = '{
    "traits": [
        "curious",
        "reflective",
        "indecisive",
        "creative",
        "searching"
    ]
}'::jsonb,
    communication_style = '{
        "message_length": {
            "preferred_word_count": 200,
            "range_tolerance": 50,
            "description": "Enjoys exploratory, thoughtful responses that consider multiple angles"
        },
        "question_frequency": {
            "questions_per_response": 3,
            "type": "exploratory",
            "description": "Open-ended questions that promote self-reflection"
        },
        "perspective_variety": {
            "level": 4.5,
            "scale_info": "1-5",
            "description": "Appreciates multiple viewpoints and possibilities"
        },
        "guidance_style": {
            "directiveness": 2.0,
            "scale_info": "1-5 where 1 is least directive",
            "description": "Gentle suggestions rather than direct advice"
        },
        "metaphor_usage": {
            "frequency": "high",
            "description": "Appreciates metaphors and analogies for self-discovery"
        },
        "response_structure": {
            "type": "exploratory",
            "elements": ["reflection", "possibilities", "gentle guidance", "open questions"],
            "description": "Flowing structure that encourages exploration"
        },
        "validation_balance": {
            "encouragement": 4.0,
            "challenge": 3.0,
            "scale_info": "1-5",
            "description": "Balance between supporting current feelings and encouraging growth"
        }
    }'::jsonb,
    demographic = '{
        "age_range": "24-28",
        "profession": "Freelance Writer",
        "interests": ["writing", "philosophy", "art"]
    }'::jsonb
WHERE email = 'maya.p@example.com';

-- Maya's diverse interests
INSERT INTO interests (id, user_id, name, summary) VALUES
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'maya.p@example.com'), 'Creative Writing', 'Exploring different genres and styles'),
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'maya.p@example.com'), 'Philosophy', 'Questions about purpose and meaning'),
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'maya.p@example.com'), 'Photography', 'Visual storytelling and expression'),
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'maya.p@example.com'), 'Environmental Activism', 'Passionate but unsure how to contribute'),
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'maya.p@example.com'), 'Digital Art', 'Learning new medium of expression');

-- Maya's supportive network
INSERT INTO people (id, user_id, name, relationship, demographic, notes) VALUES
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'maya.p@example.com'), 'Sarah', 'Writing Mentor', 
    '{"profession": "Author", "interests": ["writing", "teaching"], "met": "2022-08"}'::jsonb,
    'Helps with writing projects, encourages exploration of different styles.'),
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'maya.p@example.com'), 'Raj', 'Friend', 
    '{"profession": "Environmental Scientist", "interests": ["activism", "sustainability"], "met": "2023-02"}'::jsonb,
    'Inspires me with his clear sense of purpose and dedication to environmental causes.');

-- 6. Social Navigator (Jordan Taylor)
INSERT INTO users (id, email, name, password)
VALUES (
    gen_random_uuid(),
    'jordan.t@example.com',
    'Jordan Taylor',
    'test_password'
)
ON CONFLICT (email) DO UPDATE 
SET name = EXCLUDED.name;

UPDATE users 
SET personality_traits = '{
    "traits": [
        "friendly",
        "anxious",
        "caring",
        "overthinking",
        "people-pleasing"
    ]
}'::jsonb,
    communication_style = '{
        "message_length": {
            "preferred_word_count": 90,
            "range_tolerance": 20,
            "description": "Concise messages to avoid overthinking"
        },
        "reassurance_level": {
            "level": 4.5,
            "scale_info": "1-5",
            "frequency": "high",
            "description": "Regular reassurance and validation of social interpretations"
        },
        "question_frequency": {
            "questions_per_response": 1,
            "type": "clarifying",
            "description": "Simple, clear questions to avoid ambiguity"
        },
        "suggestion_style": {
            "directiveness": 3.5,
            "scale_info": "1-5",
            "options_count": 2,
            "description": "Clear options with pros and cons for social situations"
        },
        "social_interpretation": {
            "detail_level": 4.0,
            "scale_info": "1-5",
            "description": "Help interpret social cues and others perspectives"
        },
        "response_structure": {
            "type": "supportive",
            "elements": ["validation", "interpretation", "clear suggestions"],
            "description": "Structured to reduce anxiety and provide clear guidance"
        },
        "tone_consistency": {
            "level": 4.8,
            "scale_info": "1-5",
            "description": "Very consistent, predictable tone to reduce anxiety"
        }
    }'::jsonb,
    demographic = '{
        "age_range": "20-24",
        "profession": "Marketing Assistant",
        "interests": ["social media", "fashion", "relationships"]
    }'::jsonb
WHERE email = 'jordan.t@example.com';

-- Jordan's interests
INSERT INTO interests (id, user_id, name, summary) VALUES
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'jordan.t@example.com'), 'Social Media', 'Understanding online communication and trends'),
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'jordan.t@example.com'), 'Fashion', 'Expression through style'),
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'jordan.t@example.com'), 'Psychology', 'Understanding people and relationships');

-- Jordan's complex social network
INSERT INTO people (id, user_id, name, relationship, demographic, notes) VALUES
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'jordan.t@example.com'), 'Alex', 'Crush', 
    '{"profession": "Graphic Designer", "interests": ["art", "music"], "met": "2023-06"}'::jsonb,
    'Work in same building, trying to find ways to talk more. Unsure if feelings are reciprocated.'),
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'jordan.t@example.com'), 'Taylor', 'Best Friend', 
    '{"profession": "Teacher", "interests": ["education", "travel"], "met": "2020-09"}'::jsonb,
    'Sometimes feel like they are drifting away since they started teaching. Want to maintain closeness.'),
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'jordan.t@example.com'), 'Friend Group', 'Friends', 
    '{"size": "6 people", "common_interests": ["movies", "board games"], "met": "2021-03"}'::jsonb,
    'Complex group dynamics, trying to navigate different personalities and maintain harmony.');

-- Add some stories for each user to provide context for their situations
INSERT INTO stories (id, user_id, title, description, location, timestamp, tags) VALUES
    -- Emily's technical achievements
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'emily.zhang@example.com'),
    'Quantum Algorithm Breakthrough',
    'Successfully implemented a novel quantum algorithm optimization. Dr. Chen provided crucial insights during our weekly meeting.',
    'Research Lab',
    '2023-11-15',
    ARRAY['quantum computing', 'research', 'achievement']),

    -- Sophie's relationship challenges
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'sophie.m@example.com'),
    'Difficult Conversation with Jake',
    'Had to set boundaries about post-breakup communication. Lisa helped prepare for the conversation.',
    'Local Coffee Shop',
    '2023-12-01',
    ARRAY['relationships', 'personal growth', 'boundaries']),

    -- Tom's university experiences
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'tom.chen@example.com'),
    'First Algorithm Assignment',
    'Struggled with the complexity analysis but Emma helped explain it. Need to build confidence to ask Prof. Williams more questions.',
    'University Library',
    '2023-10-20',
    ARRAY['study', 'computer science', 'collaboration']),

    -- Michael's workplace conflicts
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'michael.r@example.com'),
    'Project Management Dispute',
    'Karen overrode my decision about sprint planning without discussion. Team seems caught in the middle.',
    'Office',
    '2023-11-28',
    ARRAY['work', 'conflict', 'leadership']),

    -- Maya's exploration
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'maya.p@example.com'),
    'First Photography Exhibition',
    'Displayed my work at local gallery. Sarah encouraged me to submit despite my doubts. Mixed feelings about the reception.',
    'Art Gallery',
    '2023-12-05',
    ARRAY['art', 'personal growth', 'creativity']),

    -- Jordan's social situations
    (gen_random_uuid(), (SELECT id FROM users WHERE email = 'jordan.t@example.com'),
    'Group Dinner Planning',
    'Trying to organize friend group dinner. Worried about seating arrangements and making sure everyone feels included.',
    'Restaurant',
    '2023-12-10',
    ARRAY['social', 'friendship', 'anxiety']); 