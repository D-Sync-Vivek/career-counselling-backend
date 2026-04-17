--
-- PostgreSQL database dump
--


-- Dumped from database version 17.8 (a48d9ca)
-- Dumped by pg_dump version 17.9 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

-- CRITICAL: Add this to support your mentor expertise vectors
CREATE EXTENSION IF NOT EXISTS vector;

ALTER TABLE IF EXISTS ONLY public.user_skills DROP CONSTRAINT IF EXISTS user_skills_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.user_skills DROP CONSTRAINT IF EXISTS user_skills_skill_id_fkey;
ALTER TABLE IF EXISTS ONLY public.student_insights DROP CONSTRAINT IF EXISTS student_insights_student_id_fkey;
ALTER TABLE IF EXISTS ONLY public.student_insights DROP CONSTRAINT IF EXISTS student_insights_recommended_career_id_fkey;
ALTER TABLE IF EXISTS ONLY public.roadmaps DROP CONSTRAINT IF EXISTS roadmaps_student_id_fkey;
ALTER TABLE IF EXISTS ONLY public.results DROP CONSTRAINT IF EXISTS results_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.results DROP CONSTRAINT IF EXISTS results_test_id_fkey;
ALTER TABLE IF EXISTS ONLY public.psychometric_profiles DROP CONSTRAINT IF EXISTS psychometric_profiles_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.profiles DROP CONSTRAINT IF EXISTS profiles_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.parent_student_links DROP CONSTRAINT IF EXISTS parent_student_links_student_id_fkey;
ALTER TABLE IF EXISTS ONLY public.parent_student_links DROP CONSTRAINT IF EXISTS parent_student_links_parent_id_fkey;
ALTER TABLE IF EXISTS ONLY public.parent_feedback DROP CONSTRAINT IF EXISTS parent_feedback_student_id_fkey;
ALTER TABLE IF EXISTS ONLY public.parent_feedback DROP CONSTRAINT IF EXISTS parent_feedback_parent_id_fkey;
ALTER TABLE IF EXISTS ONLY public.mentors DROP CONSTRAINT IF EXISTS mentors_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.mentor_feedback DROP CONSTRAINT IF EXISTS mentor_feedback_student_id_fkey;
ALTER TABLE IF EXISTS ONLY public.mentor_feedback DROP CONSTRAINT IF EXISTS mentor_feedback_session_id_fkey;
ALTER TABLE IF EXISTS ONLY public.mentor_feedback DROP CONSTRAINT IF EXISTS mentor_feedback_mentor_id_fkey;
ALTER TABLE IF EXISTS ONLY public.mentor_availability DROP CONSTRAINT IF EXISTS mentor_availability_mentor_id_fkey;
ALTER TABLE IF EXISTS ONLY public.lifestyle_profiles DROP CONSTRAINT IF EXISTS lifestyle_profiles_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.roadmap_tasks DROP CONSTRAINT IF EXISTS fk_phase;
ALTER TABLE IF EXISTS ONLY public.financial_profiles DROP CONSTRAINT IF EXISTS financial_profiles_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.chat_messages DROP CONSTRAINT IF EXISTS chat_messages_student_id_fkey;
ALTER TABLE IF EXISTS ONLY public.chat_messages DROP CONSTRAINT IF EXISTS chat_messages_sender_id_fkey;
ALTER TABLE IF EXISTS ONLY public.chat_messages DROP CONSTRAINT IF EXISTS chat_messages_mentor_id_fkey;
ALTER TABLE IF EXISTS ONLY public.career_skills DROP CONSTRAINT IF EXISTS career_skills_skill_id_fkey;
ALTER TABLE IF EXISTS ONLY public.career_skills DROP CONSTRAINT IF EXISTS career_skills_career_id_fkey;
ALTER TABLE IF EXISTS ONLY public.aspiration_profiles DROP CONSTRAINT IF EXISTS aspiration_profiles_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.academic_profiles DROP CONSTRAINT IF EXISTS academic_profiles_user_id_fkey;
DROP INDEX IF EXISTS public.ix_users_email;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_pkey;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_invite_code_key;
ALTER TABLE IF EXISTS ONLY public.user_skills DROP CONSTRAINT IF EXISTS user_skills_pkey;
ALTER TABLE IF EXISTS ONLY public.tests DROP CONSTRAINT IF EXISTS tests_pkey;
ALTER TABLE IF EXISTS ONLY public.student_insights DROP CONSTRAINT IF EXISTS student_insights_student_id_key;
ALTER TABLE IF EXISTS ONLY public.student_insights DROP CONSTRAINT IF EXISTS student_insights_pkey;
ALTER TABLE IF EXISTS ONLY public.skills DROP CONSTRAINT IF EXISTS skills_pkey;
ALTER TABLE IF EXISTS ONLY public.skills DROP CONSTRAINT IF EXISTS skills_name_key;
ALTER TABLE IF EXISTS ONLY public.sessions DROP CONSTRAINT IF EXISTS sessions_pkey;
ALTER TABLE IF EXISTS ONLY public.roadmaps DROP CONSTRAINT IF EXISTS roadmaps_student_id_key;
ALTER TABLE IF EXISTS ONLY public.roadmaps DROP CONSTRAINT IF EXISTS roadmaps_pkey;
ALTER TABLE IF EXISTS ONLY public.roadmap_tasks DROP CONSTRAINT IF EXISTS roadmap_tasks_pkey;
ALTER TABLE IF EXISTS ONLY public.roadmap_phases DROP CONSTRAINT IF EXISTS roadmap_phases_pkey;
ALTER TABLE IF EXISTS ONLY public.results DROP CONSTRAINT IF EXISTS results_pkey;
ALTER TABLE IF EXISTS ONLY public.psychometric_profiles DROP CONSTRAINT IF EXISTS psychometric_profiles_user_id_key1;
ALTER TABLE IF EXISTS ONLY public.psychometric_profiles DROP CONSTRAINT IF EXISTS psychometric_profiles_pkey1;
ALTER TABLE IF EXISTS ONLY public.profiles DROP CONSTRAINT IF EXISTS profiles_user_id_key;
ALTER TABLE IF EXISTS ONLY public.profiles DROP CONSTRAINT IF EXISTS profiles_pkey;
ALTER TABLE IF EXISTS ONLY public.parent_student_links DROP CONSTRAINT IF EXISTS parent_student_links_pkey;
ALTER TABLE IF EXISTS ONLY public.parent_feedback DROP CONSTRAINT IF EXISTS parent_feedback_pkey;
ALTER TABLE IF EXISTS ONLY public.mentorship_requests DROP CONSTRAINT IF EXISTS mentorship_requests_pkey;
ALTER TABLE IF EXISTS ONLY public.mentors DROP CONSTRAINT IF EXISTS mentors_user_id_key;
ALTER TABLE IF EXISTS ONLY public.mentors DROP CONSTRAINT IF EXISTS mentors_pkey;
ALTER TABLE IF EXISTS ONLY public.mentor_feedback DROP CONSTRAINT IF EXISTS mentor_feedback_pkey;
ALTER TABLE IF EXISTS ONLY public.mentor_availability DROP CONSTRAINT IF EXISTS mentor_availability_pkey;
ALTER TABLE IF EXISTS ONLY public.lifestyle_profiles DROP CONSTRAINT IF EXISTS lifestyle_profiles_user_id_key;
ALTER TABLE IF EXISTS ONLY public.lifestyle_profiles DROP CONSTRAINT IF EXISTS lifestyle_profiles_pkey;
ALTER TABLE IF EXISTS ONLY public.financial_profiles DROP CONSTRAINT IF EXISTS financial_profiles_user_id_key;
ALTER TABLE IF EXISTS ONLY public.financial_profiles DROP CONSTRAINT IF EXISTS financial_profiles_pkey;
ALTER TABLE IF EXISTS ONLY public.chat_messages DROP CONSTRAINT IF EXISTS chat_messages_pkey;
ALTER TABLE IF EXISTS ONLY public.careers DROP CONSTRAINT IF EXISTS careers_title_key;
ALTER TABLE IF EXISTS ONLY public.careers DROP CONSTRAINT IF EXISTS careers_pkey;
ALTER TABLE IF EXISTS ONLY public.career_skills DROP CONSTRAINT IF EXISTS career_skills_pkey;
ALTER TABLE IF EXISTS ONLY public.aspiration_profiles DROP CONSTRAINT IF EXISTS aspiration_profiles_user_id_key;
ALTER TABLE IF EXISTS ONLY public.aspiration_profiles DROP CONSTRAINT IF EXISTS aspiration_profiles_pkey;
ALTER TABLE IF EXISTS ONLY public.academic_profiles DROP CONSTRAINT IF EXISTS academic_profiles_user_id_key;
ALTER TABLE IF EXISTS ONLY public.academic_profiles DROP CONSTRAINT IF EXISTS academic_profiles_pkey;
DROP TABLE IF EXISTS public.users;
DROP TABLE IF EXISTS public.user_skills;
DROP TABLE IF EXISTS public.tests;
DROP TABLE IF EXISTS public.student_insights;
DROP TABLE IF EXISTS public.skills;
DROP TABLE IF EXISTS public.sessions;
DROP TABLE IF EXISTS public.roadmaps;
DROP TABLE IF EXISTS public.roadmap_tasks;
DROP TABLE IF EXISTS public.roadmap_phases;
DROP TABLE IF EXISTS public.results;
DROP TABLE IF EXISTS public.psychometric_profiles;
DROP TABLE IF EXISTS public.profiles;
DROP TABLE IF EXISTS public.parent_student_links;
DROP TABLE IF EXISTS public.parent_feedback;
DROP TABLE IF EXISTS public.mentorship_requests;
DROP TABLE IF EXISTS public.mentors;
DROP TABLE IF EXISTS public.mentor_feedback;
DROP TABLE IF EXISTS public.mentor_availability;
DROP TABLE IF EXISTS public.lifestyle_profiles;
DROP TABLE IF EXISTS public.financial_profiles;
DROP TABLE IF EXISTS public.chat_messages;
DROP TABLE IF EXISTS public.careers;
DROP TABLE IF EXISTS public.career_skills;
DROP TABLE IF EXISTS public.aspiration_profiles;
DROP TABLE IF EXISTS public.academic_profiles;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: academic_profiles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.academic_profiles (
    id uuid NOT NULL,
    user_id uuid,
    overall_percentage_band text,
    strongest_subject text,
    weakest_subject text,
    favorite_subject text,
    learning_style text,
    study_hours_home text,
    homework_completion text,
    achievements text,
    updated_at timestamp with time zone,
    field_configs jsonb
);


--
-- Name: aspiration_profiles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.aspiration_profiles (
    id uuid NOT NULL,
    user_id uuid,
    dream_career text,
    life_direction text,
    ten_year_vision text,
    updated_at timestamp with time zone,
    field_configs jsonb
);


--
-- Name: career_skills; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.career_skills (
    career_id uuid NOT NULL,
    skill_id uuid NOT NULL,
    weight integer
);


--
-- Name: careers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.careers (
    id uuid NOT NULL,
    title character varying NOT NULL,
    description text,
    base_success_probability double precision
);


--
-- Name: chat_messages; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.chat_messages (
    id uuid NOT NULL,
    student_id uuid NOT NULL,
    mentor_id uuid NOT NULL,
    sender_id uuid NOT NULL,
    message text NOT NULL,
    sent_at timestamp with time zone DEFAULT now()
);


--
-- Name: financial_profiles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.financial_profiles (
    id uuid NOT NULL,
    user_id uuid,
    family_structure text,
    income_band text,
    father_education text,
    mother_education text,
    affordability_level text,
    coaching_access text,
    updated_at timestamp with time zone
);


--
-- Name: lifestyle_profiles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.lifestyle_profiles (
    id uuid NOT NULL,
    user_id uuid,
    study_hours text,
    screen_time text,
    routine_consistency text,
    sleep_quality text,
    distraction_level text,
    task_completion text,
    reaction_to_failure text,
    stress_level text,
    pressure_handling text,
    social_preference text,
    focus_ability text,
    biggest_distraction text,
    focus_score double precision,
    updated_at timestamp with time zone,
    field_configs jsonb
);


--
-- Name: mentor_availability; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mentor_availability (
    id uuid NOT NULL,
    mentor_id uuid,
    day_of_week integer NOT NULL,
    start_time time without time zone NOT NULL,
    end_time time without time zone NOT NULL,
    is_booked boolean
);


--
-- Name: mentor_feedback; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mentor_feedback (
    id uuid NOT NULL,
    session_id uuid,
    mentor_id uuid,
    student_id uuid,
    notes text,
    action_items text,
    submitted_at timestamp with time zone DEFAULT now()
);


--
-- Name: mentors; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mentors (
    id uuid NOT NULL,
    user_id uuid,
    expertise character varying NOT NULL,
    expertise_vector public.vector(384),
    bio text,
    years_experience integer,
    rating double precision,
    is_verified boolean
);


--
-- Name: mentorship_requests; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mentorship_requests (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    student_id uuid NOT NULL,
    mentor_id uuid NOT NULL,
    availability_id uuid,
    message text,
    status character varying(20) DEFAULT 'pending'::character varying,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    request_type character varying(20) DEFAULT 'session'::character varying
);


--
-- Name: parent_feedback; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.parent_feedback (
    id uuid NOT NULL,
    parent_id uuid,
    student_id uuid,
    behavior_insights text,
    study_habits text,
    logged_at timestamp with time zone DEFAULT now()
);


--
-- Name: parent_student_links; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.parent_student_links (
    id uuid NOT NULL,
    parent_id uuid NOT NULL,
    student_id uuid NOT NULL,
    linked_at timestamp with time zone DEFAULT now()
);


--
-- Name: profiles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.profiles (
    id uuid NOT NULL,
    user_id uuid,
    full_name text NOT NULL,
    dob text,
    gender text,
    current_class text,
    school_type text,
    state text,
    area_type text,
    medium_of_learning text,
    updated_at timestamp with time zone DEFAULT now(),
    field_configs jsonb
);


--
-- Name: psychometric_profiles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.psychometric_profiles (
    id uuid NOT NULL,
    user_id uuid,
    personality_type text,
    riasec_code text,
    work_environment text,
    work_style text,
    biggest_strength text,
    biggest_weakness text,
    motivation_driver text,
    updated_at timestamp with time zone
);


--
-- Name: results; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.results (
    id uuid NOT NULL,
    user_id uuid,
    test_id uuid,
    overall_score double precision,
    speed_score double precision,
    accuracy_score double precision,
    consistency_score double precision,
    weakness_mapping jsonb,
    status character varying(20) NOT NULL,
    partial_answers jsonb,
    completed_at timestamp with time zone DEFAULT now()
);


--
-- Name: roadmap_phases; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.roadmap_phases (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    roadmap_id uuid NOT NULL,
    sequence integer NOT NULL,
    title character varying(255) NOT NULL,
    status character varying(50) DEFAULT 'Not Started'::character varying,
    progress_percentage double precision DEFAULT 0.0
);


--
-- Name: roadmap_tasks; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.roadmap_tasks (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    phase_id uuid NOT NULL,
    sequence integer NOT NULL,
    title character varying(255) NOT NULL,
    description text,
    status character varying(50) DEFAULT 'Not Started'::character varying
);


--
-- Name: roadmaps; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.roadmaps (
    id uuid NOT NULL,
    student_id uuid,
    title character varying NOT NULL,
    description text,
    status character varying,
    progress_percentage double precision,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


--
-- Name: sessions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sessions (
    id uuid NOT NULL,
    student_id uuid,
    mentor_id uuid,
    scheduled_at timestamp with time zone NOT NULL,
    duration_minutes integer NOT NULL,
    status character varying,
    meeting_url character varying,
    dyte_meeting_id character varying
);


--
-- Name: skills; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.skills (
    id uuid NOT NULL,
    name character varying NOT NULL,
    category character varying
);


--
-- Name: student_insights; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.student_insights (
    id uuid NOT NULL,
    student_id uuid,
    ai_summary text,
    recommended_career_id uuid,
    success_probability double precision,
    feasibility_score double precision,
    passion_skill_gap double precision,
    generated_at timestamp with time zone DEFAULT now()
);


--
-- Name: tests; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tests (
    id uuid NOT NULL,
    title character varying NOT NULL,
    type character varying NOT NULL,
    total_questions integer
);


--
-- Name: user_skills; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_skills (
    user_id uuid NOT NULL,
    skill_id uuid NOT NULL,
    score double precision,
    updated_at timestamp with time zone DEFAULT now()
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id uuid NOT NULL,
    email character varying,
    hashed_password character varying NOT NULL,
    full_name character varying,
    role character varying NOT NULL,
    profile_photo_url character varying,
    invite_code character varying(6),
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    academic_data jsonb,
    apti_data jsonb,
    personality_data jsonb,
    lifestyle_data jsonb,
    financial_data jsonb,
    passion_strength_data jsonb,
    aspiration_data jsonb,
    career_interest_data jsonb,
    profile_data jsonb
);


--
-- Data for Name: academic_profiles; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.academic_profiles (id, user_id, overall_percentage_band, strongest_subject, weakest_subject, favorite_subject, learning_style, study_hours_home, homework_completion, achievements) 
VALUES ('4495dee8-0a9e-4c6b-b6b5-de94887fc961', NULL, 'What was your overall percentage...', 'Which subject...', 'Which subject...', 'Regardless of...', 'Do you learn best...', 'On average...', 'How often...', 'List any...');


--
-- Data for Name: aspiration_profiles; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.aspiration_profiles (id, user_id, dream_career, life_direction, ten_year_vision, updated_at, field_configs) FROM stdin;
a413e96c-ef12-4433-b7a5-6868856d30aa	\N	If you had no fear of failure, what is the one career you would pursue?	What is the current primary focus or direction of your life right now?	Describe exactly where you want to be and what you want to be doing in 10 years.	\N	\N
\.


--
-- Data for Name: career_skills; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.career_skills (career_id, skill_id, weight) FROM stdin;
71ddb3f8-420a-4a51-9295-18c4d501336b	d8936321-b131-4bf5-8a97-9e926c7510bf	9
71ddb3f8-420a-4a51-9295-18c4d501336b	83becb2c-8b8a-41da-b393-e1c92f3feec5	8
71ddb3f8-420a-4a51-9295-18c4d501336b	0f2d3099-1877-4ce1-b9c4-925e96faa80f	7
71ddb3f8-420a-4a51-9295-18c4d501336b	9dabfaf9-1048-4fe7-8b21-65611a814de4	9
71ddb3f8-420a-4a51-9295-18c4d501336b	b85174dd-9469-4a1a-858b-ab967f3228dd	8
6bd90417-9677-4bac-b41b-1183b8f4571b	3903fb6a-3ea1-4f48-9756-0aebb3e3458a	8
6bd90417-9677-4bac-b41b-1183b8f4571b	8ebfdf63-8eb9-4e02-8361-b38c44f26736	9
6bd90417-9677-4bac-b41b-1183b8f4571b	0b198e98-1fe3-4630-b2ab-06e516dc819d	9
6bd90417-9677-4bac-b41b-1183b8f4571b	ea1755d2-fa1a-4d15-be7e-5360a3c2aa60	8
6bd90417-9677-4bac-b41b-1183b8f4571b	b85174dd-9469-4a1a-858b-ab967f3228dd	7
\.


--
-- Data for Name: careers; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.careers (id, title, description, base_success_probability) FROM stdin;
71ddb3f8-420a-4a51-9295-18c4d501336b	Data Analyst	This career leverages your strong mathematics and logical problem-solving skills while requiring minimal public speaking. Many data analyst roles can be learned through free online courses and certifications, making it highly accessible despite financial constraints. The work is detail-oriented and analytical, perfectly matching your aptitude profile.	0.85
6bd90417-9677-4bac-b41b-1183b8f4571b	Web Developer	This career leverages your strong logical problem-solving through coding while requiring minimal public speaking. With abundant free resources (freeCodeCamp, YouTube tutorials) and the ability to build a portfolio from home, this is highly achievable despite financial constraints. The demand for web developers continues to grow, offering remote work possibilities that suit your rural location.	0.85
b3032e92-5e1a-456b-9a6d-c106a475e104	Music Producer/Sound Engineer	AI recommended path for Music Producer/Sound Engineer	0.7
f74854b2-4b84-4177-9e52-064bcfcc784a	Actuarial Science/Quantitative Risk Analyst	AI recommended path for Actuarial Science/Quantitative Risk Analyst	0.7
b67353b7-46a1-4b15-aafd-11b16aba68d1	Content Strategist / Creative Director	AI recommended path for Content Strategist / Creative Director	0.7
305268f0-5a2b-47c6-8853-517cf192226c	Corporate Communications Specialist	AI recommended path for Corporate Communications Specialist	0.7
0714e7a1-d549-4726-9a35-d5c59d036056	Content Strategy Manager / Technical Writer	AI recommended path for Content Strategy Manager / Technical Writer	0.7
36aac0c7-808b-4d09-90f9-07e908a14611	Marketing Analyst / Digital Marketing Specialist	AI recommended path for Marketing Analyst / Digital Marketing Specialist	0.7
a98de095-1b58-4cf9-bd34-bb6c10b4e8bb	Technical Writer in Tech/Finance	AI recommended path for Technical Writer in Tech/Finance	0.7
c9cc9b05-ec9e-40db-92cb-5105652540ea	Financial Communications Specialist	AI recommended path for Financial Communications Specialist	0.7
4a9918ce-6697-4db3-a72c-4793b7988e08	E-sports Operations/Event Manager	AI recommended path for E-sports Operations/Event Manager	0.7
96e07513-1899-4072-93af-ea626bf96834	Government Services Officer	AI recommended path for Government Services Officer	0.7
f8680cab-c381-4f0b-954b-65783592b3be	Civil Services (Government Administration)	AI recommended path for Civil Services (Government Administration)	0.7
\.


--
-- Data for Name: chat_messages; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.chat_messages (id, student_id, mentor_id, sender_id, message, sent_at) FROM stdin;
\.


--
-- Data for Name: financial_profiles; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.financial_profiles (id, user_id, family_structure, income_band, father_education, mother_education, affordability_level, coaching_access, updated_at) FROM stdin;
6bf6888f-6b87-4592-9fbe-5227c5b03959	\N	What is your family structure? (Nuclear Family, Joint Family, Single Parent Household, Other)	What is your family's approximate annual household income? (Below ₹3 LPA, ₹3–5 LPA, ₹5–10 LPA, ₹10–20 LPA, Above ₹20 LPA)	What is the highest level of education completed by your father/guardian? (Below 10th, 10th/SSC, 12th/HSC, Diploma/ITI, Graduate, Post-Graduate or higher)	What is the highest level of education completed by your mother/guardian? (Below 10th, 10th/SSC, 12th/HSC, Diploma/ITI, Graduate, Post-Graduate or higher)	How would you describe your family's ability to afford educational resources and coaching? (Need affordable options, Can stretch a little, Can invest in quality education)	What is your current access to coaching or tuition? (Yes, in a coaching institute, No, but considering it, No, self-study, No, online resources)	\N
\.


--
-- Data for Name: lifestyle_profiles; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.lifestyle_profiles (id, user_id, study_hours, screen_time, routine_consistency, sleep_quality, distraction_level, task_completion, reaction_to_failure, stress_level, pressure_handling, social_preference, focus_ability, biggest_distraction, focus_score, updated_at, field_configs) FROM stdin;
24d3a359-2edb-46c2-b61d-2d69bc8de172	\N	How many hours of uninterrupted "Deep Work" can you achieve in a day?	What is your average daily screen time for entertainment (Social Media/Gaming)?	On a scale of 1-10, how strictly do you follow a fixed daily routine?	How many hours of restful sleep do you get, and do you feel energized upon waking?	How easily do you get distracted by notifications or surroundings while studying?	\N	How do you typically handle a setback or bad grade?	\N	How do you mentally handle high-pressure situations like surprise tests or deadlines?	Do you prefer group study or solo focus?	What is the maximum duration you can stay focused on a single difficult task?	What is the #1 thing that breaks your focus?	\N	\N	\N
\.


--
-- Data for Name: mentor_availability; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mentor_availability (id, mentor_id, day_of_week, start_time, end_time, is_booked) FROM stdin;
4b99def6-e01b-4447-a90c-84115608c3ff	ede1faa2-6900-4ab5-b30b-9e7cb982751b	3	16:00:00	17:00:00	t
48718498-bbaf-4ce5-8bb3-d11204f4cd7d	ede1faa2-6900-4ab5-b30b-9e7cb982751b	3	19:00:00	20:00:00	t
7475e501-fe9c-4b20-8994-1a6ceb5ee85e	ede1faa2-6900-4ab5-b30b-9e7cb982751b	4	15:00:00	16:00:00	t
d50c0afb-0091-4beb-9480-76043f539684	ede1faa2-6900-4ab5-b30b-9e7cb982751b	4	16:00:00	17:00:00	t
2bb00dee-df0d-41b0-bd2a-249d5e359600	ede1faa2-6900-4ab5-b30b-9e7cb982751b	4	17:00:00	18:00:00	t
73be3e8a-fcbc-4f56-b22b-8c3ffa5457c8	ede1faa2-6900-4ab5-b30b-9e7cb982751b	4	18:00:00	19:00:00	t
d1ab9700-c9e2-4a40-ad77-307f4dc69884	ede1faa2-6900-4ab5-b30b-9e7cb982751b	5	12:00:00	13:00:00	t
\.


--
-- Data for Name: mentor_feedback; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mentor_feedback (id, session_id, mentor_id, student_id, notes, action_items, submitted_at) FROM stdin;
\.


--
-- Data for Name: mentors; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mentors (id, user_id, expertise, expertise_vector, bio, years_experience, rating, is_verified) FROM stdin;
ede1faa2-6900-4ab5-b30b-9e7cb982751b	5bc65df5-4139-4086-be70-eb9c59499af2	Government Services	[-0.08446608,-0.038327005,0.030793196,-0.023974108,-0.046560314,0.026745241,0.09674096,-0.025932224,-0.006134786,0.02134982,-0.0118882395,0.020364655,-0.019788675,-0.011648314,0.0030232763,-0.047143824,0.04008805,0.003237857,-0.088547386,-0.039796732,-0.0033267147,0.046160754,-0.12129131,0.034678824,-0.031010708,0.062399987,-0.076808825,-0.052544795,-0.00413018,-0.06291946,0.032214727,-0.01838302,0.024769548,0.008659174,0.037768316,0.082819685,0.08803928,-0.016847597,0.043051653,0.0082816295,-0.031120136,-0.047074873,-0.0070758956,-0.027291093,-0.018540593,-0.003424103,0.040722936,-0.010694231,-0.0077551813,-0.06297897,0.0025471542,-0.027389634,0.04556552,0.06264125,0.018095626,-0.089598894,-0.006123863,0.015450119,-0.084685385,-0.05071094,-0.016199341,0.016520448,-0.055670734,0.023957273,0.0794005,0.0632783,-0.06562999,-0.009680791,0.015603056,-0.18671894,-0.061540768,-0.033027463,0.056782786,0.053228382,0.020095287,-0.040151734,0.047402922,0.039614927,0.11015922,-0.1445904,0.04042696,-0.015835565,-0.0035638302,0.13507812,-0.0057138344,-0.029960483,-0.07060868,-0.024879698,0.009473768,-0.008225202,0.02109809,-0.026607445,0.054356504,-0.026879616,-0.059865847,0.0019855853,0.045662023,-0.08149208,-0.02574522,0.18709591,-0.008993038,0.022898259,0.03365682,0.00066189916,-0.015381023,-0.020939836,-0.097026326,0.012016102,0.0148731135,0.048457548,-0.007707479,-0.0069154324,-0.04846076,0.021879615,0.015919635,-0.044843983,0.007965666,0.025420416,0.044883378,-0.012818678,-0.00962681,0.034795836,-0.04143678,-0.025474478,-0.020458266,-0.008759241,0.0386289,-4.9656235e-33,-0.06042033,0.019753387,0.05669153,0.018208722,-0.009893089,0.002463502,-0.029174924,0.003919084,0.005405827,0.10320879,-0.01289608,0.111887686,0.045456704,-0.014910947,0.06774599,0.02033155,-0.06161787,0.037723627,-0.0027246166,0.0392057,-0.043707184,0.039477527,0.034858596,-0.0061852997,0.1201575,-0.03971338,0.016686723,-0.006001984,0.14234261,0.005858843,0.059409108,0.07270749,0.01622516,-0.010503837,0.006026879,0.02256999,0.02371627,-0.08540456,0.006008175,-0.087325685,-0.052175418,0.0065514627,0.045250185,0.08340666,-0.000712875,0.017631289,0.031667136,0.005403757,0.029754288,0.046334833,0.011950092,0.023687165,-0.08958811,-0.017089982,-0.0035866783,-0.01279266,0.056424268,0.0061947927,0.017325815,-0.053301908,0.060108438,-0.0791721,-0.051248305,-0.004587777,0.01685861,-0.05189822,-0.010712272,-0.017227855,0.10134296,-0.025195489,-0.061135065,0.01565148,0.116244584,0.06495198,-0.024620809,0.010356728,0.012672905,-0.04123087,-0.032547846,0.02804844,-0.024408495,-0.023401173,0.03413862,0.027600171,0.1496716,0.025344165,-0.01981614,-0.022808569,0.046593986,-0.056677874,-0.15784061,-0.008530907,0.0009794723,0.10617729,-0.0038572543,2.2543234e-33,-0.038553875,-0.086070344,-0.030159358,0.036668424,0.0046276255,0.058161955,-0.028366003,-0.08609837,0.056638822,0.08123851,-0.020277249,-0.028862817,0.061453726,0.08120872,0.012731586,-0.048377004,-0.051698476,-0.04642614,0.0027602208,0.024132913,-0.030164191,0.091249436,0.022374462,0.06458499,-0.05289174,0.028007826,-0.12110326,-0.10840842,0.06120132,-0.0021758038,-0.009435166,-0.05325642,-0.047570612,-0.0022693274,-0.13536963,0.01802733,0.07118643,-0.00965483,-0.04987105,0.018368192,0.025218751,-0.072764784,0.013055938,0.023427479,-0.09821277,-0.030038897,-0.08316646,0.047767423,-0.05508245,-0.055475224,-0.09221324,-0.023423662,-0.0515657,-0.021334479,0.0062369066,0.019499298,-0.004598899,-0.014227367,-0.058316305,-0.006825778,0.03010927,0.010080234,-0.061100964,0.043842867,-0.02106778,-0.02658101,0.006019178,-0.06501513,0.04309523,-0.013053131,0.06890516,-0.03267099,-0.05379958,0.038068626,-0.0543143,-0.017392708,-0.05724225,-0.012060024,-0.0033282614,0.0008814667,0.07204627,-0.08026463,-0.013192613,0.0025643455,-0.018679537,-0.0022211897,0.17143716,-0.05002168,0.02727835,-0.029566,-0.09368275,-0.030758627,0.020003678,0.060873307,0.056266572,-1.3175408e-08,0.041352283,0.043111872,-0.042419404,-0.013588396,-0.070463225,-0.048029564,-0.028404938,0.08281273,-0.025143221,0.014347123,0.05663671,0.012737804,-0.0089446865,-0.016637025,0.023181906,-0.03316002,0.026314454,0.0033382203,0.0036332875,0.063217774,0.023107233,0.028357344,-0.0146906,0.019885436,0.009558111,0.019379282,0.052495006,0.10301725,0.052605305,0.08678174,-0.029946506,0.025194699,0.054189175,-0.020278743,-0.009568807,0.019408768,-0.028350227,-0.044762954,0.022582201,-0.054000624,0.010724613,0.03573282,-0.020176377,-0.0062979623,0.07197665,0.04174558,0.027406665,0.034054812,0.09791384,-0.10841145,-0.0024777167,-0.009786242,0.031275474,0.014422953,0.019167554,-0.07248121,0.006833532,0.0078092087,-0.033333883,0.057761654,0.005560038,-0.028046086,0.07248441,-0.026137678]	With a deep understanding of the administrative landscape, I provide actionable insights to help aspirants navigate complex syllabi and interviews. My mission is to bridge the gap between ambition and a successful career in government service.	5	0	t
0d1bb49f-9d5b-4879-9378-e60eccb6ba8c	ddf51f2a-ea2c-4713-8aea-eb35d5c985ab	Music	[0.019252112,-0.024731405,-0.0046656653,-0.005162896,-0.09804203,0.099218234,0.11092683,-0.041055474,0.06495716,0.003137613,-0.000251227,0.0019003686,0.03517607,-0.053048324,-0.03215236,0.02203371,0.019198148,0.019650422,-0.054413546,-0.05798826,-0.09929195,0.040736757,-0.052437853,0.045902416,0.0021240325,0.11100396,-0.036223456,0.07501271,-0.001920026,-0.09847799,0.0052889627,0.08739189,0.07946173,-0.049189515,-0.14084236,-0.020189961,-0.016267128,-0.033013586,-0.0035659352,-0.002956224,-0.0035619927,0.00416955,0.023496062,-0.042382672,-0.03891265,-0.03200501,-0.016281597,-0.016593946,0.0017470825,0.082750864,-0.0048819478,0.04258236,-0.05260766,0.057169475,-0.024472501,-0.050992932,0.018292055,0.09273775,0.05662992,0.016926033,0.006151935,-0.058501262,-0.026099967,-0.015435537,0.071951985,-0.014721819,0.0021068726,0.0656542,-0.012808995,-0.0045685167,0.029309154,-0.0038851076,0.043352872,0.027354054,0.06857328,-0.022438956,-0.010824696,-0.06594368,-0.012600889,-0.04673702,0.055291317,-0.06476129,-0.0817718,-0.09327944,-0.0032691853,-0.026254704,-0.017071467,0.03163438,-0.07394633,-0.024718719,-0.07037735,-0.009809461,-0.032146767,0.022211967,-0.030306775,0.07837039,-0.00961963,-0.07923688,-0.01589575,0.22051999,0.043764554,0.0699073,0.043655235,0.045647826,-0.021047486,-0.0873994,-0.02412225,0.11125342,0.00933266,-0.04938595,0.009985575,-0.0057944744,-0.051437143,0.0067586396,0.048378192,0.029970434,0.043328624,0.0580385,0.030433262,0.0031075408,-0.007722495,-0.032950174,-0.035731107,0.0014904577,-0.06404116,-0.04051379,-0.04840777,-3.18489e-33,0.046071224,-0.11433462,0.07313232,0.040109932,0.07043424,-0.025386384,-0.058715273,-0.013814642,0.014715954,0.08078192,0.041528534,0.025261434,-0.03474701,0.007032045,0.0995586,-0.060934883,-0.06885799,0.06256658,-0.010142994,0.005895431,-0.040349938,0.018094957,0.03611496,0.07657333,0.023972413,-0.025236642,0.033624012,-0.115153424,0.04174684,-0.020961083,-0.004595607,0.029162286,0.048245445,-0.030153325,-0.024123272,-0.0009600044,-0.02126284,-0.023702273,0.054054677,-0.062027514,-0.008649723,0.019513864,-0.0699701,-0.018621815,-0.010148489,0.034356456,0.046003688,0.05517131,-0.042948198,0.051001396,0.014367031,0.019873878,-0.003028826,0.04117189,0.04726823,0.016900178,0.031882875,0.012401083,0.027878774,-0.019213852,0.113674454,0.10592882,0.018590832,-0.08770832,0.016155327,0.024639891,0.057435907,-0.050698746,0.08944771,-0.04453371,-0.09408777,-0.0281011,0.027569814,-0.019170767,-0.017785504,0.01586824,-0.012052674,-0.08115268,-0.018250246,0.020701105,-0.05754646,0.012553133,0.0017713227,0.033058178,-0.018477311,0.04764418,-0.03135668,-0.13356945,-0.030812271,0.016493393,-0.14461029,-0.00980187,0.028851375,0.016579868,-0.006303487,2.3646547e-33,-0.0077168033,0.029302925,0.04955205,0.03009709,0.047437225,0.026526712,-0.010838697,-0.01650799,0.025449382,0.082704976,-0.04389025,-0.034575023,0.06791466,0.0024702281,-0.06196313,-0.026064938,0.04681484,0.053185474,0.052849054,0.024202181,-0.085603386,-0.017440759,0.04033014,-0.045135085,-0.07489534,0.01200931,0.0010285786,0.008874175,-0.03929066,0.019193748,0.06259948,-0.02178475,-0.008830254,-0.11390209,-0.0010683734,0.0751928,0.0985416,0.035702776,-0.047485743,-0.019956604,-0.017059572,0.044986416,0.09342412,0.12839808,-0.020657599,-0.0056538885,-0.037966978,0.16428061,-0.04268567,-0.019600352,0.03112704,-0.0262909,0.029530901,-0.102747865,-0.030400867,0.028048785,-0.066821754,-0.060780194,-0.01267808,0.045414127,0.013861431,0.049621098,-0.08045584,-0.030082706,-0.04753408,0.08407653,0.026319042,-0.0045627607,-0.029693311,0.048075028,0.058825113,0.0460355,-0.016761176,0.020173276,-0.101547234,-0.002920447,-0.08315379,-0.010594545,0.016209582,-0.062310386,0.03618365,0.0044423947,-0.050258607,-0.022163466,-0.046075333,0.020356087,0.09770143,-0.0014757448,-0.02310721,-0.017713921,0.050947405,0.013131559,-0.054437287,-0.0014572678,-0.052118633,-1.2067495e-08,-0.011834481,-0.0104805445,-0.04372664,-0.06548369,0.015506185,0.06628355,0.094178274,-0.038012706,0.021334754,0.017188398,0.019513797,-0.023155008,0.030499598,0.044500254,0.037080955,-0.035136376,-0.0118236365,0.04016096,-0.050265156,0.010577784,0.039289977,0.027214278,0.04574244,-0.033781905,-0.017139021,-0.00014185076,0.109147705,0.05528032,0.035615165,0.063105,-0.028865935,0.03284117,-0.0132607315,-0.059933845,0.0108562615,-0.07655214,0.028839657,-0.10141702,-0.051322486,-0.012896435,0.004614698,0.07901464,0.04798714,-0.049255297,-0.07668156,-0.0358022,0.0842631,-0.008859607,-0.016000625,0.016515905,-0.08970372,-0.019650528,-0.004275633,0.034010787,0.03250029,0.017169785,-0.05277395,0.094794735,-0.079629526,0.030391088,0.021826489,-0.00862065,0.07042971,0.022453714]	Love music!!!!!!!	2	0	t
9c0c33f1-a25d-49d5-9b49-e389d8ece997	f532cff2-555b-489c-bfaf-3ef569532bb7	Sport Teacher	[-0.022868255,0.04673007,-0.012168242,-0.012036614,-0.028983135,0.0049716146,0.08810605,0.029131876,0.03889116,0.13486536,-0.013038738,0.019937402,-0.0750313,0.08482716,0.042703554,0.08371835,0.038292788,0.046039812,-0.03553297,-0.08910086,-0.03237617,0.07334706,-0.004882945,0.043661654,-0.005401043,0.048607778,-0.002252683,0.017322524,-0.08995149,-0.065586105,-0.0867698,-0.089033216,-0.0015032144,0.07893364,-0.026736403,0.04864941,0.031448934,0.08734618,-0.070354395,0.042194657,-0.04198386,-0.04277279,0.017550515,0.0417461,0.0063043386,0.041384224,0.039448157,-0.028594257,0.030982703,-0.016081518,-0.004376885,-0.062222388,-0.029535709,-0.06943957,0.12883101,0.037068836,-0.01537358,0.06675306,-0.004141963,0.016273554,0.024149178,0.020689588,-0.07774415,0.06714114,-0.031248393,-0.047947787,-0.10289417,0.08372571,0.011949407,-0.04429165,0.044347476,0.0065056174,0.030643908,-0.0051523405,0.091295175,-0.009956478,-0.002442165,-0.018073263,0.062289823,0.004280661,-0.0045329635,-0.119884804,-0.0035800396,9.1505666e-05,0.05276224,-0.033744596,0.021540381,0.023774391,0.04803318,0.016876014,-0.069529064,-0.00044358592,0.016989565,0.029286575,-0.049321037,0.06657872,-0.05561266,-0.018173715,-0.046424072,0.12906219,-0.01564171,0.041368518,0.0155956205,0.098007694,-0.013685502,-0.007325442,-0.029847253,0.020767877,0.045189016,0.08862302,0.0073698927,0.011169979,-0.07222274,0.06307863,0.0008888609,0.095297255,0.060757473,0.032709323,-0.10009861,0.02121644,-0.0075272107,0.01442461,-0.038613126,0.029537348,-0.018687645,-0.052926224,0.010146534,-2.9301204e-33,0.01113001,-0.011391438,0.04987898,0.059597507,-0.050698075,0.012180522,0.05976347,-0.04352137,0.022923915,-0.032349136,0.033409577,0.058765367,-0.0049132453,0.0043547316,0.04494391,0.06141168,-0.07511405,-0.008499367,-0.031144947,0.07715457,0.053289626,0.014872902,-0.02291389,0.012694914,-0.042085465,0.029045284,0.07147978,-0.048291735,0.080542356,0.021336628,-0.013396426,-0.040244497,-0.08712413,-0.060184773,0.103410594,-0.048851557,-0.017616604,-0.042878132,0.036360037,0.043145586,0.048786785,-0.06321605,0.049293004,-0.07908295,-0.025858054,0.035008423,0.09566943,0.06514082,0.005132738,0.013957901,-0.051993318,-0.059477706,0.040746912,-0.062411122,0.01439925,-0.029490784,0.04035726,0.06005846,-0.08083356,-0.02231537,-0.004887005,0.10427693,-0.014784351,0.040638812,-0.029307691,-0.056332752,-0.01153211,-0.022794597,0.06659255,-0.053881556,-0.0019939407,0.034660485,-0.063650765,0.013788193,-0.047427975,-0.019554378,0.02632658,-0.055538327,-0.09474492,-0.0332009,0.03674934,-0.033283155,-0.008476394,-0.037370715,-0.019453494,-0.031451575,-0.040258806,-0.08524796,0.077110544,0.045797773,-0.073558666,-0.018776022,-0.058092695,0.124483034,-0.0531451,1.7423875e-33,-0.025957556,-0.023653619,-0.0137648005,0.05748544,0.101392016,-0.008187473,0.06995746,0.056356575,0.052043,0.0137325525,0.01658807,-0.07619896,-0.052393142,0.02081121,-0.016009966,0.009155186,-0.04853619,-0.034343436,-0.07064935,-0.06862519,-0.001527232,0.047851402,-0.00031191978,-0.03701267,0.00020530632,-0.006911216,0.0036197894,0.025303453,-0.08847954,0.05758144,0.030185465,-0.0039970116,0.08744065,0.034416113,-0.107861385,0.11119926,0.03913526,-0.01760566,-0.01763182,0.03670566,0.07148845,-0.103637025,-0.020418547,0.0160783,0.04964235,-0.023587042,0.037840102,0.031372964,0.00042276765,0.0004597554,-0.053812243,-0.012389872,-0.0020692989,-0.025105137,0.10193764,-0.015546761,0.045429025,-0.08238621,-0.04788524,-0.03644247,0.015060133,-0.0025030202,-0.03581251,0.09357842,0.0121294,0.014991287,-0.061057433,0.005616939,-0.11248763,-0.00505858,0.0010272237,0.06601135,-0.012878508,-0.022808675,-0.07941035,0.04460812,-0.0033754725,0.07054594,0.0133577585,0.051992428,-0.057987005,-0.081017874,0.02371596,0.048343193,0.03208602,0.051780768,0.036100376,0.015169756,0.019325959,-0.05513556,0.08881069,0.08769017,0.054517716,-0.06420192,-0.023673894,-1.11295995e-08,-0.035336673,-0.022074364,-0.043506354,-0.046733946,-0.028035523,0.055506878,-0.008609644,-0.060486156,0.011684424,0.0039259186,0.0021324174,-0.01635667,0.05977628,-0.010575687,0.087070115,-0.022245374,-0.0028368211,0.07093974,-0.04089169,0.039728552,0.07142324,-0.014501586,-0.0147052165,0.017844684,-0.03568978,-0.12129195,-0.03221192,0.027976288,-0.02740144,0.019985935,-0.051068332,0.055638697,0.01936126,-0.1031148,0.0059111794,0.031219728,0.041443568,-0.06371947,-0.0769497,0.050700318,-0.09882855,0.035779938,0.041823816,-0.00799096,0.08239199,0.014711852,0.033989023,-0.062910505,-0.000546579,0.018570198,-0.051039238,0.015020335,0.02146578,-0.06004735,-0.036748808,0.049101207,-0.077954635,-0.07395148,-0.12842172,-0.059699684,0.018927393,-0.0759043,-0.0053904834,0.06693293]	e-sport!?	1	0	t
\.


--
-- Data for Name: mentorship_requests; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mentorship_requests (id, student_id, mentor_id, availability_id, message, status, created_at, updated_at, request_type) FROM stdin;
7c23cf29-546b-4cbf-ae17-ffdac83fe08c	988b1973-77e2-40b7-b609-c3550812d1cb	0dcbdb98-b93f-4f1f-9305-73f18e3aecfa	17628882-15f6-433f-844a-e36499296e97	dont know what this does	approved	2026-03-30 20:28:24.177029+05:30	2026-03-30 20:28:24.177029+05:30	session
6df50016-fa6a-4875-affc-ba930b487928	11f04294-3486-48b7-a118-7dde0e6146cf	0dcbdb98-b93f-4f1f-9305-73f18e3aecfa	2c2d3d29-92c3-4d9e-8bd0-a86f0e21db96		pending	2026-04-01 19:39:27.520126+05:30	2026-04-01 19:39:27.520126+05:30	session
f8bf6813-aafc-4193-86df-ef773c18d1b2	73c4b680-2d95-43a2-bee3-39f351ac955d	3d715f81-3703-47fc-ac63-6a290ca5614d	\N	I would like to request mentorship from you.	accepted	2026-04-11 14:38:00.252124+05:30	2026-04-11 14:42:00.717346+05:30	connection
8bdf199e-3dd2-46f0-be9b-da95ed33171c	73c4b680-2d95-43a2-bee3-39f351ac955d	0dcbdb98-b93f-4f1f-9305-73f18e3aecfa	56ced3f4-e827-4d4d-adcf-1a3a769cfc1c		pending	2026-04-02 13:46:35.671481+05:30	2026-04-02 13:46:35.671481+05:30	session
2d47982e-b60d-4cd3-a974-395863f36daa	3b4a166e-51c4-4a3e-b388-79d916f84714	3d715f81-3703-47fc-ac63-6a290ca5614d	\N	I would like to request mentorship from you.	accepted	2026-04-11 13:13:02.795226+05:30	2026-04-11 14:47:45.721369+05:30	connection
77a7fdad-0702-4422-bf93-919cf7f3a2de	73c4b680-2d95-43a2-bee3-39f351ac955d	d406ecd6-89ce-48f0-8529-68c00477bc4d	bcea72dc-7c5f-45aa-9230-96f2d3bf034a		approved	2026-04-12 16:51:03.438373+05:30	2026-04-12 16:51:26.820297+05:30	session
5390105f-1fb7-4090-a9a3-b05003fe675d	73c4b680-2d95-43a2-bee3-39f351ac955d	d406ecd6-89ce-48f0-8529-68c00477bc4d	acbf878b-6728-49f5-8b67-4666eff4eb10		approved	2026-04-13 15:45:56.072592+05:30	2026-04-13 15:46:09.33509+05:30	session
8b28bac2-d298-40cf-8796-17f3a4deebc6	3b4a166e-51c4-4a3e-b388-79d916f84714	c7a401b6-5b27-4fbe-842a-fa5746907996	610bf122-ced3-4cc8-8265-9c7b2ac63714	I would like to book this session.	approved	2026-04-14 00:30:28.836066+05:30	2026-04-14 00:30:57.432296+05:30	session
a4dcd9b9-29ef-424f-871d-0607221ea821	3b4a166e-51c4-4a3e-b388-79d916f84714	c7a401b6-5b27-4fbe-842a-fa5746907996	7b8c3123-072c-40ba-a00b-f364cfe8a074	I would like to book this session.	approved	2026-04-14 00:45:57.120105+05:30	2026-04-14 00:48:47.744063+05:30	session
6f4cfef3-168b-4294-bec8-7b9b3904da61	42da0e64-54b6-420e-b8d6-a0058e06c0e3	3d715f81-3703-47fc-ac63-6a290ca5614d	2ad49ad8-d712-4cda-94f9-b24f3a1ebf30	avs	approved	2026-04-05 01:52:59.007831+05:30	2026-04-05 01:52:59.007831+05:30	session
1db70d59-8d7a-44b6-9020-a0f7ac002f5c	42da0e64-54b6-420e-b8d6-a0058e06c0e3	3d715f81-3703-47fc-ac63-6a290ca5614d	a28efc7b-819c-4fc9-acab-6041438a8485	sdfgn	approved	2026-04-05 01:54:02.788914+05:30	2026-04-05 01:54:02.788914+05:30	session
487259df-9a36-4084-ae60-360c41f5688f	3b4a166e-51c4-4a3e-b388-79d916f84714	3d715f81-3703-47fc-ac63-6a290ca5614d	de23d8ad-1687-420c-b4cc-3bf4b61a520b	I would like to book this session.	approved	2026-04-14 01:06:36.561049+05:30	2026-04-14 01:07:20.01852+05:30	session
fd4864ec-46c1-4044-a04f-67ef2d53515b	73c4b680-2d95-43a2-bee3-39f351ac955d	0dcbdb98-b93f-4f1f-9305-73f18e3aecfa	\N		pending	2026-04-06 18:13:46.012681+05:30	2026-04-06 18:13:46.012681+05:30	connection
11be09d5-bd8c-4c64-9301-fc470aa7ed08	73c4b680-2d95-43a2-bee3-39f351ac955d	d406ecd6-89ce-48f0-8529-68c00477bc4d	\N		accepted	2026-04-06 18:14:04.031011+05:30	2026-04-06 18:14:39.248226+05:30	connection
ec11bdab-99c8-4b49-9a42-4871f7e90642	3e985aa2-346b-4eda-8322-59ff77dc4ae5	d406ecd6-89ce-48f0-8529-68c00477bc4d	\N		accepted	2026-04-06 22:39:47.951412+05:30	2026-04-06 22:40:35.449636+05:30	connection
f02950ec-d5d2-45a9-bc6c-4cd4d7e6fa9b	73c4b680-2d95-43a2-bee3-39f351ac955d	d406ecd6-89ce-48f0-8529-68c00477bc4d	7b46fd3f-8f6d-41fa-b179-b94a34eb471e		approved	2026-04-07 18:42:19.734147+05:30	2026-04-07 18:42:46.127194+05:30	session
1332e5cb-70c2-4555-9325-897b437d941a	73c4b680-2d95-43a2-bee3-39f351ac955d	d406ecd6-89ce-48f0-8529-68c00477bc4d	c34540e2-663d-455f-be72-eb78669a4dd2	just checking	approved	2026-04-08 13:42:54.374636+05:30	2026-04-08 13:45:48.644729+05:30	session
5805a9f8-1b3c-416a-9b37-e5cebf906057	3b4a166e-51c4-4a3e-b388-79d916f84714	d406ecd6-89ce-48f0-8529-68c00477bc4d	\N	I would like to request mentorship from you.	pending	2026-04-09 16:59:00.394876+05:30	2026-04-09 16:59:00.394876+05:30	connection
d54e16c1-c8b7-48e5-862d-7b084a791f95	3b4a166e-51c4-4a3e-b388-79d916f84714	0dcbdb98-b93f-4f1f-9305-73f18e3aecfa	\N	I would like to request mentorship from you.	pending	2026-04-09 17:11:32.979214+05:30	2026-04-09 17:11:32.979214+05:30	connection
8b809fab-d764-48a6-a6f3-82ea3d620298	3b4a166e-51c4-4a3e-b388-79d916f84714	b6953716-070f-4074-837b-a695dcb63838	\N	I would like to request mentorship from you.	pending	2026-04-11 13:07:31.117982+05:30	2026-04-11 13:07:31.117982+05:30	connection
856ba781-ab7d-4644-b265-d0766d972dd3	3b4a166e-51c4-4a3e-b388-79d916f84714	c7a401b6-5b27-4fbe-842a-fa5746907996	\N	I would like to request mentorship from you.	accepted	2026-04-09 16:50:45.713051+05:30	2026-04-11 14:12:50.071529+05:30	connection
0e36c951-e7a2-40de-b271-0744e2f94823	3b4a166e-51c4-4a3e-b388-79d916f84714	c7a401b6-5b27-4fbe-842a-fa5746907996	97bbca6f-8957-44a3-a4d2-7db0c0e9f23f	I would like to book this session.	approved	2026-04-14 02:08:15.194784+05:30	2026-04-14 02:08:55.401264+05:30	session
aef990fe-dc01-4073-b030-d4d6f9230e87	42bfcb92-4801-40aa-bafc-b8b7a6be0913	ede1faa2-6900-4ab5-b30b-9e7cb982751b	\N	I would like to request mentorship from you.	accepted	2026-04-15 14:42:45.150016+05:30	2026-04-15 14:44:19.559456+05:30	connection
458b3d01-49b4-497e-83a8-9f04695daa0b	42bfcb92-4801-40aa-bafc-b8b7a6be0913	ede1faa2-6900-4ab5-b30b-9e7cb982751b	4b99def6-e01b-4447-a90c-84115608c3ff	I would like to book this session.	approved	2026-04-15 14:45:27.85621+05:30	2026-04-15 14:47:44.905905+05:30	session
2287f5c1-f6a6-49c0-9e31-aad4395ef43a	42bfcb92-4801-40aa-bafc-b8b7a6be0913	0d1bb49f-9d5b-4879-9378-e60eccb6ba8c	\N	I would like to request mentorship from you.	pending	2026-04-15 16:10:58.154721+05:30	2026-04-15 16:10:58.154721+05:30	connection
0f48a67e-a9cb-4ee0-8b69-1a11f53ec93d	42bfcb92-4801-40aa-bafc-b8b7a6be0913	ede1faa2-6900-4ab5-b30b-9e7cb982751b	48718498-bbaf-4ce5-8bb3-d11204f4cd7d		approved	2026-04-15 18:23:22.381638+05:30	2026-04-15 18:23:40.421558+05:30	session
365f255c-3e61-4cab-bece-890aa3cad455	42bfcb92-4801-40aa-bafc-b8b7a6be0913	9c0c33f1-a25d-49d5-9b49-e389d8ece997	\N	I would like to request mentorship from you.	accepted	2026-04-15 16:05:20.701119+05:30	2026-04-16 14:16:46.998284+05:30	connection
67805bc5-e29b-440c-8d11-5ddba67cc073	42bfcb92-4801-40aa-bafc-b8b7a6be0913	ede1faa2-6900-4ab5-b30b-9e7cb982751b	7475e501-fe9c-4b20-8994-1a6ceb5ee85e	I would like to book this session.	approved	2026-04-16 14:42:41.538444+05:30	2026-04-16 15:01:44.252459+05:30	session
a3cbf449-eb9b-4193-9bc3-2ccc3182fff6	42bfcb92-4801-40aa-bafc-b8b7a6be0913	ede1faa2-6900-4ab5-b30b-9e7cb982751b	d50c0afb-0091-4beb-9480-76043f539684	I would like to book this session.	approved	2026-04-16 15:40:55.864231+05:30	2026-04-16 15:41:29.08191+05:30	session
6c9f8add-b29f-4df5-b6dd-10e51d723dbb	42bfcb92-4801-40aa-bafc-b8b7a6be0913	ede1faa2-6900-4ab5-b30b-9e7cb982751b	2bb00dee-df0d-41b0-bd2a-249d5e359600	I would like to book this session.	approved	2026-04-16 16:03:22.77792+05:30	2026-04-16 16:03:43.156852+05:30	session
60a9aa3b-8504-4752-8dd6-da34954e6c2c	42bfcb92-4801-40aa-bafc-b8b7a6be0913	ede1faa2-6900-4ab5-b30b-9e7cb982751b	73be3e8a-fcbc-4f56-b22b-8c3ffa5457c8	I would like to book this session.	approved	2026-04-16 17:24:24.19052+05:30	2026-04-16 17:24:44.951381+05:30	session
57db0214-e8e2-4673-bce4-f8818e8f3eba	42bfcb92-4801-40aa-bafc-b8b7a6be0913	ede1faa2-6900-4ab5-b30b-9e7cb982751b	d1ab9700-c9e2-4a40-ad77-307f4dc69884	I would like to book this session.	approved	2026-04-17 11:55:17.705056+05:30	2026-04-17 11:55:36.878746+05:30	session
\.


--
-- Data for Name: parent_feedback; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.parent_feedback (id, parent_id, student_id, behavior_insights, study_habits, logged_at) FROM stdin;
\.


--
-- Data for Name: parent_student_links; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.parent_student_links (id, parent_id, student_id, linked_at) FROM stdin;
a8aa0942-b74e-4bc8-886c-148436fa7935	b0cb04e9-2036-438d-b770-1c418e30619d	42bfcb92-4801-40aa-bafc-b8b7a6be0913	2026-04-15 14:36:51.581733+05:30
627c694c-992a-4918-ae89-13fd4b4092c8	4e6b35fb-dd45-4a68-88f0-2a4ace030fd8	42bfcb92-4801-40aa-bafc-b8b7a6be0913	2026-04-16 14:19:46.904051+05:30
\.


--
-- Data for Name: profiles; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.profiles (id, user_id, full_name, dob, gender, current_class, school_type, state, area_type, medium_of_learning, updated_at, field_configs) FROM stdin;
59807314-fa51-4be7-a6d5-2468ef19d708	\N	What is your legal full name as per school records?	What is your date of birth (DD/MM/YYYY)?	How do you identify your gender?	Which academic grade or class are you currently enrolled in?	Is your school a Government, Private, or International institution?	In which state or territory of India do you currently reside?	\N	What is the primary language used for teaching in your school?	\N	\N
\.


--
-- Data for Name: psychometric_profiles; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.psychometric_profiles (id, user_id, personality_type, riasec_code, work_environment, work_style, biggest_strength, biggest_weakness, motivation_driver, updated_at) FROM stdin;
\.


--
-- Data for Name: results; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.results (id, user_id, test_id, overall_score, speed_score, accuracy_score, consistency_score, weakness_mapping, status, partial_answers, completed_at) FROM stdin;
\.


--
-- Data for Name: roadmap_phases; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.roadmap_phases (id, roadmap_id, sequence, title, status, progress_percentage) FROM stdin;
d67feb75-5aad-4dd7-ba29-c641d8dcf1df	7112faa4-9546-40fa-bbd0-f47225ac40ec	1	Foundations of Financial Communications	Active	91.66666666666666
59bd9479-c544-4317-ae70-ceeba0ff12c9	179bac3b-87e4-4488-a4ba-047564e6790b	2	Communication and Interpersonal Skills	Not Started	0
dded2fc2-cfa0-45c3-819b-e3af5a87ff15	7112faa4-9546-40fa-bbd0-f47225ac40ec	2	Financial Data Analysis and Visualization	Not Started	0
fb0a9488-b5e5-4299-b945-b70f621dc688	7112faa4-9546-40fa-bbd0-f47225ac40ec	3	Financial Communications and Storytelling	Not Started	0
ad986496-d433-4652-96e4-b64552c50243	7112faa4-9546-40fa-bbd0-f47225ac40ec	4	Financial Communications Strategy and Planning	Not Started	0
faed7907-e3ab-44ac-8e06-450eda3aac78	7112faa4-9546-40fa-bbd0-f47225ac40ec	5	Financial Communications Specialization and Portfolio Development	Not Started	0
be0865f5-9bc6-4f7d-ae28-0b0f24555a76	179bac3b-87e4-4488-a4ba-047564e6790b	3	Data Analysis and Problem-Solving	Not Started	0
43578e1e-f551-482f-8ebe-92aa9d62e7e9	179bac3b-87e4-4488-a4ba-047564e6790b	4	Leadership and Management	Not Started	0
72b804b0-4b0c-41c5-babc-22c17569748c	179bac3b-87e4-4488-a4ba-047564e6790b	5	Capstone Project	Not Started	0
8ba6dd4a-2a2f-49af-9abd-c592a948958e	179bac3b-87e4-4488-a4ba-047564e6790b	1	Foundational Knowledge	Active	16.666666666666664
b051e108-742a-452d-88c8-5b14cdad163a	433b1435-50cc-4815-862f-a869def4faa1	2	Analytical and Critical Thinking	Not Started	0
e7d225f3-8d83-43ed-b59b-b7fefb0d72c4	433b1435-50cc-4815-862f-a869def4faa1	3	Communication and Leadership	Not Started	0
2e55ffb4-c2c3-4b17-897d-49e5353ab27d	433b1435-50cc-4815-862f-a869def4faa1	4	Specialized Knowledge	Not Started	0
04d7c018-0515-43d7-bdf2-45dbcdd702f4	433b1435-50cc-4815-862f-a869def4faa1	5	Preparation for Civil Services Examination	Not Started	0
bf46e895-d264-4053-830a-73e2d2bfbdfb	c18b7246-d210-4d6c-b77f-8bec79847631	3	E-sports Operations and Management	Not Started	0
343461b7-11b7-4d8d-8470-74bd90d44242	c18b7246-d210-4d6c-b77f-8bec79847631	4	E-sports Event Execution and Evaluation	Not Started	0
3431c541-1e78-45e5-8d36-cca22e20b8d2	b00bf3ce-5dcb-4c29-a07b-b767047f95b1	2	Programming and Data Analysis	Not Started	0
c55f67d4-84cb-4b41-bafc-f60ef016f926	b00bf3ce-5dcb-4c29-a07b-b767047f95b1	3	Actuarial Science Fundamentals	Not Started	0
59c4d9f2-0759-4719-b464-f5316db477a8	b00bf3ce-5dcb-4c29-a07b-b767047f95b1	4	Quantitative Risk Analysis	Not Started	0
b088df3c-7977-4f3b-8959-a1307d616fd2	b00bf3ce-5dcb-4c29-a07b-b767047f95b1	5	Capstone Project and Career Preparation	Not Started	0
ebef3b5d-101d-4960-a3e5-27652defc04b	b00bf3ce-5dcb-4c29-a07b-b767047f95b1	1	Foundations of Mathematics and Statistics	Active	0
3bd81b64-4bd2-4bce-a28e-c8ace2b7465d	433b1435-50cc-4815-862f-a869def4faa1	1	Foundational Knowledge	Active	66.66666666666666
d7990979-cc76-41e4-a2bd-206f75f6e4f8	c18b7246-d210-4d6c-b77f-8bec79847631	5	E-sports Venture Planning and Launch	Not Started	0
d47d4b5e-3736-4df2-9840-0f13248ffc94	c18b7246-d210-4d6c-b77f-8bec79847631	2	E-sports Event Management	Active	16.666666666666664
6f3b63de-82cf-4261-b913-c1fbfda4c506	c18b7246-d210-4d6c-b77f-8bec79847631	1	Foundations of E-sports Operations	Active	50
\.


--
-- Data for Name: roadmap_tasks; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.roadmap_tasks (id, phase_id, sequence, title, description, status) FROM stdin;
a0ad4336-e4bc-4f4e-a4af-db5459043344	dded2fc2-cfa0-45c3-819b-e3af5a87ff15	0	Week 5: Learn advanced data analysis concepts using online resources	\N	Not Started
710efd4d-6c72-4f42-a7bc-61c2a8a0895f	dded2fc2-cfa0-45c3-819b-e3af5a87ff15	1	Week 5: Practice analyzing financial data using Python	\N	Not Started
47390990-2725-4bc4-873d-9a332d81d35a	dded2fc2-cfa0-45c3-819b-e3af5a87ff15	2	Week 5: Create a financial data analysis report	\N	Not Started
a6ff81f6-5feb-49b4-81fb-0867429553da	dded2fc2-cfa0-45c3-819b-e3af5a87ff15	10	Week 6: Learn data visualization concepts using online resources	\N	Not Started
451b9b8a-f654-4024-aa65-817e81d55c77	dded2fc2-cfa0-45c3-819b-e3af5a87ff15	11	Week 6: Practice creating visualizations using Tableau	\N	Not Started
9bf66d8f-2377-43e2-a865-f9b6ea75b9c0	dded2fc2-cfa0-45c3-819b-e3af5a87ff15	12	Week 6: Create a financial dashboard	\N	Not Started
64b942b7-90c4-41ca-9e70-e634651ae4a3	dded2fc2-cfa0-45c3-819b-e3af5a87ff15	20	Week 7: Learn effective reporting skills using online resources	\N	Not Started
78e38428-0387-47cb-a17c-b016fd2b7eec	dded2fc2-cfa0-45c3-819b-e3af5a87ff15	21	Week 7: Practice writing a financial report	\N	Not Started
4c79fce8-3d2e-4bb8-9a6b-8225a146d60f	dded2fc2-cfa0-45c3-819b-e3af5a87ff15	22	Week 7: Create a comprehensive financial report	\N	Not Started
ef369fea-ad76-4ebf-9df8-a8bdd7620ad4	dded2fc2-cfa0-45c3-819b-e3af5a87ff15	30	Week 8: Analyze financial case studies using online resources	\N	Not Started
546bd3f3-07a1-4d1e-8699-0890ba684833	dded2fc2-cfa0-45c3-819b-e3af5a87ff15	31	Week 8: Create a case study report	\N	Not Started
9e780969-d3c0-43dc-88bf-2ed620f76bbc	dded2fc2-cfa0-45c3-819b-e3af5a87ff15	32	Week 8: Present the case study findings	\N	Not Started
0c4e8512-5f9a-4ef3-9281-ee18ae78d2ad	fb0a9488-b5e5-4299-b945-b70f621dc688	0	Week 9: Learn effective financial communications skills using online resources	\N	Not Started
21b2018e-f1d1-4ce4-95c4-499ed46b999b	fb0a9488-b5e5-4299-b945-b70f621dc688	1	Week 9: Practice writing a financial press release	\N	Not Started
ce734214-1ca6-419c-973d-b80fe73cf859	fb0a9488-b5e5-4299-b945-b70f621dc688	2	Week 9: Create a financial communications plan	\N	Not Started
90503c1d-5099-4cb3-8d80-8af277342c67	fb0a9488-b5e5-4299-b945-b70f621dc688	10	Week 10: Learn storytelling concepts using online resources	\N	Not Started
93d9f9ed-9bb8-4554-9796-2c0a3324ceb8	fb0a9488-b5e5-4299-b945-b70f621dc688	11	Week 10: Practice creating a financial story	\N	Not Started
eb6f9312-01fb-4778-92ba-affecf12309b	fb0a9488-b5e5-4299-b945-b70f621dc688	12	Week 10: Create a financial narrative	\N	Not Started
7fbbd1e1-4d43-4568-94de-e4cf820be082	fb0a9488-b5e5-4299-b945-b70f621dc688	20	Week 11: Learn effective presentation skills using online resources	\N	Not Started
aea4fa00-1df5-4e59-b58a-a2f6a334c21b	fb0a9488-b5e5-4299-b945-b70f621dc688	21	Week 11: Practice presenting financial information	\N	Not Started
d9219d76-f44f-47b0-b82f-97e52b9fbe29	fb0a9488-b5e5-4299-b945-b70f621dc688	22	Week 11: Create a financial presentation	\N	Not Started
781c6159-506c-432a-bd54-e0d7e86f1df2	fb0a9488-b5e5-4299-b945-b70f621dc688	30	Week 12: Analyze financial case studies using online resources	\N	Not Started
86e4dc75-24ac-417b-a257-f0603822b9c6	fb0a9488-b5e5-4299-b945-b70f621dc688	31	Week 12: Create a case study report	\N	Not Started
f943520a-18be-4a6a-8df3-f753a9341174	fb0a9488-b5e5-4299-b945-b70f621dc688	32	Week 12: Present the case study findings	\N	Not Started
7bb2f750-0aff-4729-97d8-9ec76cfeb366	ad986496-d433-4652-96e4-b64552c50243	0	Week 13: Learn financial communications strategy concepts using online resources	\N	Not Started
3ef87c8b-6f5b-4cbb-8dab-4cf4536ccff0	ad986496-d433-4652-96e4-b64552c50243	1	Week 13: Practice creating a financial communications strategy	\N	Not Started
fda681e8-9085-402d-b516-87eb5e65d2c8	ad986496-d433-4652-96e4-b64552c50243	2	Week 13: Create a financial communications plan	\N	Not Started
63953273-27b8-45db-94fa-9bf234fad911	d67feb75-5aad-4dd7-ba29-c641d8dcf1df	12	Week 2: Practice using financial terminology in sentences	\N	Completed
7cc3456e-06f0-4c34-9818-699a819df44a	d67feb75-5aad-4dd7-ba29-c641d8dcf1df	11	Week 2: Create flashcards for key terms	\N	Completed
18c77509-fd14-42ab-9826-1b9448b8acc7	d67feb75-5aad-4dd7-ba29-c641d8dcf1df	20	Week 3: Learn basic data analysis concepts using online resources	\N	Completed
795335a6-2d9d-4dbc-8f41-31cd62b0bfc8	d67feb75-5aad-4dd7-ba29-c641d8dcf1df	21	Week 3: Practice analyzing financial data using Excel	\N	Completed
7df76eed-f7c9-4afa-9325-95a9207b0325	d67feb75-5aad-4dd7-ba29-c641d8dcf1df	30	Week 4: Learn effective communication skills using online resources	\N	Completed
271b6cfb-0b67-48a3-a5ce-cd0d2bd8433c	d67feb75-5aad-4dd7-ba29-c641d8dcf1df	0	Week 1: Read the Wikipedia article on financial communications	\N	Completed
59011450-6fea-4db8-ab91-23f29d28884c	d67feb75-5aad-4dd7-ba29-c641d8dcf1df	1	Week 1: Watch a YouTube video on financial communications basics	\N	Completed
d0546d65-66bf-438e-99f0-bedbaee4ddda	d67feb75-5aad-4dd7-ba29-c641d8dcf1df	2	Week 1: Take notes on key concepts	\N	Completed
0a14119b-ca08-43f2-bdcd-6b15ec740aa5	d67feb75-5aad-4dd7-ba29-c641d8dcf1df	10	Week 2: Study financial terminology using online resources	\N	Completed
6befb0ce-17a0-4a47-aad1-09bb83169c28	d67feb75-5aad-4dd7-ba29-c641d8dcf1df	32	Week 4: Record a video presenting financial information	\N	Completed
6a793261-0285-4d6d-a154-b6ade963e7c5	d67feb75-5aad-4dd7-ba29-c641d8dcf1df	31	Week 4: Practice writing a financial report	\N	Not Started
4e0bcaf5-3b88-417f-8739-bbc222673de4	d67feb75-5aad-4dd7-ba29-c641d8dcf1df	22	Week 3: Create a simple financial report	\N	Completed
00ca8d2b-a79f-4b2e-a82e-ed882a91a6e1	ad986496-d433-4652-96e4-b64552c50243	10	Week 14: Learn planning concepts using online resources	\N	Not Started
32ebe55e-dbf9-4f90-9b86-8528e0e6cab5	ad986496-d433-4652-96e4-b64552c50243	11	Week 14: Practice creating a financial plan	\N	Not Started
f5d2b919-5b6c-4b04-a9ac-947657aea1ea	ad986496-d433-4652-96e4-b64552c50243	12	Week 14: Create a comprehensive financial plan	\N	Not Started
cbb5469c-147c-4afe-9e11-051e1beeb4bd	ad986496-d433-4652-96e4-b64552c50243	20	Week 15: Learn budgeting concepts using online resources	\N	Not Started
2880517c-89e8-430e-9417-737ff75e680c	ad986496-d433-4652-96e4-b64552c50243	21	Week 15: Practice creating a financial budget	\N	Not Started
a51108f6-8769-4193-a3a6-5146429e9ade	ad986496-d433-4652-96e4-b64552c50243	22	Week 15: Create a comprehensive financial budget	\N	Not Started
d55f23ea-ecb7-4f94-83ef-92912ee93587	ad986496-d433-4652-96e4-b64552c50243	30	Week 16: Analyze financial case studies using online resources	\N	Not Started
2df889fc-48e3-4912-886a-b7910214a07a	ad986496-d433-4652-96e4-b64552c50243	31	Week 16: Create a case study report	\N	Not Started
b764ce99-563b-46f8-929c-822513d3b163	ad986496-d433-4652-96e4-b64552c50243	32	Week 16: Present the case study findings	\N	Not Started
2fbec3d9-c67e-4928-b5ab-68fc520300bc	faed7907-e3ab-44ac-8e06-450eda3aac78	0	Week 17: Learn specialized financial communications concepts using online resources	\N	Not Started
6b74cda4-523c-4968-8aca-45c3236c3d77	faed7907-e3ab-44ac-8e06-450eda3aac78	1	Week 17: Practice creating specialized financial communications content	\N	Not Started
ddc72476-7b9c-45d9-8022-8a8a41b6c954	faed7907-e3ab-44ac-8e06-450eda3aac78	2	Week 17: Create a specialized financial communications plan	\N	Not Started
811a1a76-16d0-44b5-9d06-0260f0bb2cdf	faed7907-e3ab-44ac-8e06-450eda3aac78	10	Week 18: Learn portfolio development concepts using online resources	\N	Not Started
87522459-5d49-46ac-83cd-7a4a88d33359	faed7907-e3ab-44ac-8e06-450eda3aac78	11	Week 18: Practice creating a financial communications portfolio	\N	Not Started
0340d718-1b17-4ca0-9b3d-18e601863669	faed7907-e3ab-44ac-8e06-450eda3aac78	12	Week 18: Create a comprehensive financial communications portfolio	\N	Not Started
a54bfe69-a8a6-46ee-bfb6-afae61252068	faed7907-e3ab-44ac-8e06-450eda3aac78	20	Week 19: Learn networking concepts using online resources	\N	Not Started
ade88e65-ead6-43fc-b15c-b3891cef00b8	faed7907-e3ab-44ac-8e06-450eda3aac78	21	Week 19: Practice networking with financial communications professionals	\N	Not Started
d7a64897-f263-4fa4-9e7c-b9cf74f52a53	faed7907-e3ab-44ac-8e06-450eda3aac78	22	Week 19: Create a networking plan	\N	Not Started
3dafc685-a61e-41c0-8b69-4148edc8801e	faed7907-e3ab-44ac-8e06-450eda3aac78	30	Week 20: Analyze financial case studies using online resources	\N	Not Started
3c2b3e00-be00-4782-848d-fb774dd9d412	faed7907-e3ab-44ac-8e06-450eda3aac78	31	Week 20: Create a case study report	\N	Not Started
1e466632-3c40-4405-b8e1-91681f642d17	faed7907-e3ab-44ac-8e06-450eda3aac78	32	Week 20: Present the case study findings	\N	Not Started
b1d558ee-7176-4983-a4b8-94c90c03c5ac	d7990979-cc76-41e4-a2bd-206f75f6e4f8	12	Week 32: Write a 1-page report on marketing strategy	\N	Not Started
e386d5c9-ae86-4518-b00a-b9c1863b3c65	8ba6dd4a-2a2f-49af-9abd-c592a948958e	1	Week 1: Watch YouTube videos on public administration principles	\N	Not Started
cff1decc-64f6-4fc0-9b4b-c064079d31b7	8ba6dd4a-2a2f-49af-9abd-c592a948958e	2	Week 1: Take notes on key concepts and terminology	\N	Not Started
85523844-6f0d-4809-8fd5-5b2c0fadce00	8ba6dd4a-2a2f-49af-9abd-c592a948958e	10	Week 2: Research and analyze government policies and procedures	\N	Not Started
6190b6f2-73b9-48a8-b862-d8bae5046650	8ba6dd4a-2a2f-49af-9abd-c592a948958e	11	Week 2: Create a mind map to visualize the relationships between policies and procedures	\N	Not Started
67c01e98-cae7-4338-b3ab-d3b8ace0917a	8ba6dd4a-2a2f-49af-9abd-c592a948958e	12	Week 2: Write a short essay on the importance of policies and procedures in government services	\N	Not Started
63bc298a-80c9-409a-a77b-821185668769	59bd9479-c544-4317-ae70-ceeba0ff12c9	0	Week 9: Watch TED talks on effective communication	\N	Not Started
3e5ebb74-c901-4ae4-b487-e3895a52defa	59bd9479-c544-4317-ae70-ceeba0ff12c9	1	Week 9: Practice active listening and asking questions	\N	Not Started
8bba44a7-e65d-4154-8da6-c8ed62743487	59bd9479-c544-4317-ae70-ceeba0ff12c9	2	Week 9: Write a reflective journal on personal communication style	\N	Not Started
27340b99-19fb-46e0-95c5-2d02cf025511	59bd9479-c544-4317-ae70-ceeba0ff12c9	10	Week 10: Participate in online forums on public administration to practice interacting with others	\N	Not Started
083ddc61-0cd5-474d-9e4f-b42ed48559b4	59bd9479-c544-4317-ae70-ceeba0ff12c9	11	Week 10: Role-play different scenarios to develop conflict resolution skills	\N	Not Started
5af52478-94a8-4448-8e6a-35746628cfe3	59bd9479-c544-4317-ae70-ceeba0ff12c9	12	Week 10: Create a personal development plan to improve interpersonal skills	\N	Not Started
8f9c7341-40ea-47f4-8b3a-907dbd227704	be0865f5-9bc6-4f7d-ae28-0b0f24555a76	0	Week 17: Watch tutorials on data analysis software	\N	Not Started
605c7028-9c7b-4556-8d9f-717cc4044025	be0865f5-9bc6-4f7d-ae28-0b0f24555a76	1	Week 17: Practice analyzing datasets on government services	\N	Not Started
f107308b-b8a4-4372-bcfa-3d7072772ff1	be0865f5-9bc6-4f7d-ae28-0b0f24555a76	2	Week 17: Create a report on findings and recommendations	\N	Not Started
1c165298-b7de-4daf-8468-431cd51a4396	be0865f5-9bc6-4f7d-ae28-0b0f24555a76	10	Week 18: Participate in online challenges on problem-solving	\N	Not Started
aea420d4-0f01-43c5-9d7e-33fd57773924	be0865f5-9bc6-4f7d-ae28-0b0f24555a76	11	Week 18: Create a case study on a government services problem	\N	Not Started
2082eb6a-b8d5-454d-b771-4617e344e728	be0865f5-9bc6-4f7d-ae28-0b0f24555a76	12	Week 18: Develop a proposal for a solution	\N	Not Started
ff82f4df-5053-48a5-b683-c7bd5a2db14e	43578e1e-f551-482f-8ebe-92aa9d62e7e9	0	Week 25: Watch TED talks on leadership	\N	Not Started
149ca63a-f66c-484e-9578-a7b3355cf43f	43578e1e-f551-482f-8ebe-92aa9d62e7e9	1	Week 25: Read case studies on leadership in government services	\N	Not Started
824fbb82-c8f9-4190-b8ae-b437502d0852	ebef3b5d-101d-4960-a3e5-27652defc04b	0	Week 1: Watch video lectures on probability theory	\N	Not Started
f2f2c041-bca0-4173-8b98-ae86f4aee50c	ebef3b5d-101d-4960-a3e5-27652defc04b	1	Week 1: Practice problems on conditional probability	\N	Not Started
e177134b-cd38-4202-91de-0140461a1d67	ebef3b5d-101d-4960-a3e5-27652defc04b	2	Week 1: Read chapters 1-2 of 'Probability and Statistics' by Jim Henley	\N	Not Started
dddaffff-7c7b-424f-9f1c-b7f3e1702812	ebef3b5d-101d-4960-a3e5-27652defc04b	10	Week 2: Watch video lectures on calculus theory	\N	Not Started
8ecd6850-f19b-48fc-ad12-500f31eb8c59	ebef3b5d-101d-4960-a3e5-27652defc04b	11	Week 2: Practice problems on limits and derivatives	\N	Not Started
15f50a44-77b4-4327-9b0a-af30a208c16f	ebef3b5d-101d-4960-a3e5-27652defc04b	12	Week 2: Read chapters 3-4 of 'Calculus' by Michael Spivak	\N	Not Started
3cb724a0-d82e-42f8-a9ba-7e6d51c3677e	3431c541-1e78-45e5-8d36-cca22e20b8d2	0	Week 1: Complete Python tutorials on Codecademy	\N	Not Started
e4da14ba-fdd6-4414-b680-9d9d1ed1bd4a	3431c541-1e78-45e5-8d36-cca22e20b8d2	1	Week 1: Practice problems on Python basics	\N	Not Started
c111233e-d3a6-4d21-8ef0-89eb5e63d1d8	3431c541-1e78-45e5-8d36-cca22e20b8d2	2	Week 1: Read chapters 1-2 of 'Python Crash Course' by Eric Matthes	\N	Not Started
c8d8a43e-aef7-4a27-9a7d-a586137c7534	43578e1e-f551-482f-8ebe-92aa9d62e7e9	2	Week 25: Create a personal leadership development plan	\N	Not Started
145d2769-c781-440a-a3b9-1617056d8c7c	43578e1e-f551-482f-8ebe-92aa9d62e7e9	10	Week 26: Participate in online forums on management in government services	\N	Not Started
51ce33d5-19b5-4f85-90eb-42e6a060652f	43578e1e-f551-482f-8ebe-92aa9d62e7e9	11	Week 26: Create a project plan for a government services project	\N	Not Started
c2aeda5d-6daf-458d-8798-d19bfccb3f19	43578e1e-f551-482f-8ebe-92aa9d62e7e9	12	Week 26: Develop a team building strategy	\N	Not Started
4e042dc8-d038-4367-ac38-d46d9357c8c9	72b804b0-4b0c-41c5-babc-22c17569748c	0	Week 33: Create a project plan for a government services project	\N	Not Started
4faa636e-e295-489c-bdbe-682b48ad5aa7	72b804b0-4b0c-41c5-babc-22c17569748c	1	Week 33: Develop a stakeholder engagement strategy	\N	Not Started
41f42a91-02b9-4bb5-b327-efd1d347d70c	72b804b0-4b0c-41c5-babc-22c17569748c	2	Week 33: Establish a project timeline	\N	Not Started
dbc7338b-12c6-4a64-b13a-f3b3b28dd28a	72b804b0-4b0c-41c5-babc-22c17569748c	10	Week 34: Implement the project plan	\N	Not Started
8ab05d8f-ef34-481c-8d04-024d1cbced72	3431c541-1e78-45e5-8d36-cca22e20b8d2	10	Week 2: Watch video lectures on Pandas and data analysis	\N	Not Started
a3ec1071-c30a-4ad2-a69e-f716cb751cd1	3431c541-1e78-45e5-8d36-cca22e20b8d2	11	Week 2: Practice problems on data manipulation and analysis	\N	Not Started
8894a071-e0c6-4540-8c25-ef106a1ce422	3431c541-1e78-45e5-8d36-cca22e20b8d2	12	Week 2: Read chapters 3-4 of 'Python Data Science Handbook' by Jake VanderPlas	\N	Not Started
5d38d595-9474-42f2-8dc7-a4f8d03c0dd2	c55f67d4-84cb-4b41-bafc-f60ef016f926	0	Week 1: Watch video lectures on insurance theory	\N	Not Started
a85682e2-0ec4-4e36-af44-90afb3f928dd	c55f67d4-84cb-4b41-bafc-f60ef016f926	1	Week 1: Practice problems on insurance calculations	\N	Not Started
deaefbf3-39d5-4a1b-82cd-22a628bcef34	c55f67d4-84cb-4b41-bafc-f60ef016f926	2	Week 1: Read chapters 1-2 of 'Insurance: Concepts and Coverage' by Kenneth Black	\N	Not Started
8dee8e92-e2cb-44ee-8d01-ccf90f736379	c55f67d4-84cb-4b41-bafc-f60ef016f926	10	Week 2: Watch video lectures on risk management theory	\N	Not Started
3a0e6491-63ac-4cc8-9845-52b75d1d8696	c55f67d4-84cb-4b41-bafc-f60ef016f926	11	Week 2: Practice problems on risk assessment and mitigation	\N	Not Started
3e9fe009-f3cb-484c-8ca9-d1e4d0a2f1c7	c55f67d4-84cb-4b41-bafc-f60ef016f926	12	Week 2: Read chapters 3-4 of 'Risk Management and Insurance' by Harold D. Skipper	\N	Not Started
ac8bd17b-343f-4cf4-951f-83740156d83f	59c4d9f2-0759-4719-b464-f5316db477a8	0	Week 1: Watch video lectures on stochastic processes theory	\N	Not Started
e54bfd76-61a6-44b0-bd2d-4f71b0f226c4	59c4d9f2-0759-4719-b464-f5316db477a8	1	Week 1: Practice problems on stochastic processes calculations	\N	Not Started
27bb77dc-3a39-48e2-9a43-bd8f75369dee	59c4d9f2-0759-4719-b464-f5316db477a8	2	Week 1: Read chapters 1-2 of 'Stochastic Processes' by Robert M. Gray	\N	Not Started
bf2fc7c9-a8f8-4cc5-a615-ae605ef7f294	59c4d9f2-0759-4719-b464-f5316db477a8	10	Week 2: Watch video lectures on time series analysis theory	\N	Not Started
2c35999a-fd50-409d-8105-e44a98a29129	59c4d9f2-0759-4719-b464-f5316db477a8	11	Week 2: Practice problems on time series analysis calculations	\N	Not Started
f0ce0aa7-fa57-4192-8cec-39b9718d86cc	59c4d9f2-0759-4719-b464-f5316db477a8	12	Week 2: Read chapters 3-4 of 'Time Series Analysis' by James D. Hamilton	\N	Not Started
60741717-8ecf-4c4d-abac-a4f0b507fc33	b088df3c-7977-4f3b-8959-a1307d616fd2	0	Week 1: Define a capstone project topic and scope	\N	Not Started
4afe6860-1b10-473b-8331-10733bc042dc	b088df3c-7977-4f3b-8959-a1307d616fd2	1	Week 1: Conduct research and gather data for the project	\N	Not Started
307cdec5-c2da-4fc3-84ce-6f7a74e39165	b088df3c-7977-4f3b-8959-a1307d616fd2	2	Week 1: Develop a project plan and timeline	\N	Not Started
3fd5dd28-c2cf-45b6-b3ae-8b25bf69959c	b088df3c-7977-4f3b-8959-a1307d616fd2	10	Week 2: Update resume and online profiles	\N	Not Started
63b7078c-f78a-4f2c-b04d-d9e61988ecb9	b088df3c-7977-4f3b-8959-a1307d616fd2	11	Week 2: Practice interview skills and prepare for common actuarial science interview questions	\N	Not Started
aa128ffa-21f3-4226-a635-0e6cd2fbbc3c	b088df3c-7977-4f3b-8959-a1307d616fd2	12	Week 2: Network with professionals in the actuarial science field	\N	Not Started
3b86a8bb-eb4e-4b0d-8f8a-7ffd4bc79b66	6f3b63de-82cf-4261-b913-c1fbfda4c506	10	Week 2: Create a basic event plan template	\N	Not Started
31c9d7e6-ce3c-42de-835c-35e567d11f99	6f3b63de-82cf-4261-b913-c1fbfda4c506	11	Week 2: Research 3 successful e-sports events	\N	Not Started
f954b356-2cdf-4376-8e74-31277278a1b7	6f3b63de-82cf-4261-b913-c1fbfda4c506	12	Week 2: Write a 1-page report on event planning	\N	Not Started
6b9e336c-15a6-435f-ad7c-48f2b33cf5ff	d47d4b5e-3736-4df2-9840-0f13248ffc94	0	Week 9: Research 2 e-sports event venues	\N	Not Started
8f625bdb-ed50-4e0a-aaf7-8a3b7f3b4f49	d47d4b5e-3736-4df2-9840-0f13248ffc94	1	Week 9: Create a logistics plan for a small e-sports event	\N	Not Started
465026de-20ac-48e7-9aef-15088f04c0ac	d47d4b5e-3736-4df2-9840-0f13248ffc94	10	Week 10: Create a social media marketing plan for an e-sports event	\N	Not Started
e801949b-3e7e-444f-93b0-525dd3fcfc8a	d47d4b5e-3736-4df2-9840-0f13248ffc94	11	Week 10: Research 2 successful e-sports marketing campaigns	\N	Not Started
f279c14d-4a38-4ff3-aa06-0c642d813cf9	d47d4b5e-3736-4df2-9840-0f13248ffc94	12	Week 10: Write a 1-page report on marketing strategy	\N	Not Started
64b8226a-29b7-499d-a08d-6241de78af01	bf46e895-d264-4053-830a-73e2d2bfbdfb	0	Week 17: Research 2 successful e-sports teams	\N	Not Started
e04e365e-647c-4da9-881e-a93a24a8e67e	bf46e895-d264-4053-830a-73e2d2bfbdfb	1	Week 17: Create a team management plan for a small e-sports team	\N	Not Started
904c1270-dd20-4f6a-908c-2986bf45a167	bf46e895-d264-4053-830a-73e2d2bfbdfb	2	Week 17: Write a 1-page report on team management	\N	Not Started
6c1e2356-7b42-4f91-9225-f143e2de6a62	bf46e895-d264-4053-830a-73e2d2bfbdfb	10	Week 18: Create a player management plan for a small e-sports team	\N	Not Started
b0b4843d-d876-4e09-b3d8-b6e34b571666	bf46e895-d264-4053-830a-73e2d2bfbdfb	11	Week 18: Research 2 successful e-sports player management strategies	\N	Not Started
db0305f0-c2a3-4b45-8a79-e8510af7acd7	bf46e895-d264-4053-830a-73e2d2bfbdfb	12	Week 18: Write a 1-page report on player management	\N	Not Started
53db3957-3f43-4f3f-9fc4-850969c3a420	343461b7-11b7-4d8d-8470-74bd90d44242	0	Week 25: Research 2 e-sports event setup strategies	\N	Not Started
bae31614-81b7-45d5-877e-e9508edae7b6	343461b7-11b7-4d8d-8470-74bd90d44242	1	Week 25: Create an event setup plan for a small e-sports event	\N	Not Started
ce02146a-189b-4ecc-adf5-75acf32bc4eb	343461b7-11b7-4d8d-8470-74bd90d44242	2	Week 25: Write a 1-page report on event setup	\N	Not Started
9412afe4-4aac-446b-b89a-595d6a222502	343461b7-11b7-4d8d-8470-74bd90d44242	10	Week 26: Create an event execution plan for a small e-sports event	\N	Not Started
f3e1c9b2-804f-4095-abf2-7efcc7451622	343461b7-11b7-4d8d-8470-74bd90d44242	11	Week 26: Research 2 successful e-sports event execution strategies	\N	Not Started
f1c97af1-475e-48c1-8d72-ab6bc48731c9	343461b7-11b7-4d8d-8470-74bd90d44242	12	Week 26: Write a 1-page report on event execution	\N	Not Started
07bed813-2d37-4d20-88a7-71afe67e5b9c	d7990979-cc76-41e4-a2bd-206f75f6e4f8	0	Week 31: Research 2 successful e-sports business plans	\N	Not Started
d4f9850b-8a03-41af-a5b7-d4d93c31adea	d7990979-cc76-41e4-a2bd-206f75f6e4f8	1	Week 31: Create a business plan for an e-sports venture	\N	Not Started
c212c76a-6f35-4ef7-916b-8057828b0a10	d7990979-cc76-41e4-a2bd-206f75f6e4f8	2	Week 31: Write a 1-page report on business planning	\N	Not Started
5a3b812e-89ba-4bab-8e62-a29ea5517109	d7990979-cc76-41e4-a2bd-206f75f6e4f8	10	Week 32: Create a marketing plan for an e-sports venture	\N	Not Started
0dd23d1a-dd26-43eb-85a3-13160c84da1d	d7990979-cc76-41e4-a2bd-206f75f6e4f8	11	Week 32: Research 2 successful e-sports marketing campaigns	\N	Not Started
ea18917f-4fb1-488f-97d5-dc3532c5204d	6f3b63de-82cf-4261-b913-c1fbfda4c506	1	Week 1: Read 2 articles on the e-sports industry	\N	Completed
05448e34-25a4-46ec-9453-c8164dbf51a5	6f3b63de-82cf-4261-b913-c1fbfda4c506	2	Week 1: Create a list of 10 key e-sports terms	\N	Completed
536e5c56-a480-421a-9a21-082c7bff8333	6f3b63de-82cf-4261-b913-c1fbfda4c506	0	Week 1: Watch 5 hours of e-sports tournaments	\N	Completed
1af5d13c-be27-420f-bb76-959daec2c5a2	d47d4b5e-3736-4df2-9840-0f13248ffc94	2	Week 9: Write a 1-page report on logistics planning	\N	Completed
9167c99d-2d39-4cb1-8d69-18d99d6863f7	72b804b0-4b0c-41c5-babc-22c17569748c	11	Week 34: Monitor and evaluate progress	\N	Not Started
b650bbf6-f4af-40bc-a5d5-e033207d1021	72b804b0-4b0c-41c5-babc-22c17569748c	12	Week 34: Adjust the project plan as needed	\N	Not Started
6f30f29e-7263-4374-ba3c-57ecff11a85e	8ba6dd4a-2a2f-49af-9abd-c592a948958e	0	Week 1: Read the official government website to understand the role of a Government Services Officer	\N	Completed
51a1c368-0e4a-4fa2-b4d7-bcc598e466a4	3bd81b64-4bd2-4bce-a28e-c8ace2b7465d	11	Week 2: Analyze case studies of governance models	\N	Not Started
7886654c-2da4-41cf-8b64-7b8657995243	3bd81b64-4bd2-4bce-a28e-c8ace2b7465d	12	Week 2: Create a mind map of key concepts	\N	Not Started
467aa764-9e2c-4bd9-8d70-6619399f18fb	b051e108-742a-452d-88c8-5b14cdad163a	0	Week 9: Practice data analysis using Excel	\N	Not Started
5979adf4-05db-4b6e-b1f5-a7f554add27b	b051e108-742a-452d-88c8-5b14cdad163a	1	Week 9: Watch video lectures on data visualization	\N	Not Started
1f23d3ab-8be9-44bb-8eae-771041619c27	b051e108-742a-452d-88c8-5b14cdad163a	2	Week 9: Create a dashboard to visualize data	\N	Not Started
d40b8ade-c650-43dc-a9a9-19fa2d2f9dd0	b051e108-742a-452d-88c8-5b14cdad163a	10	Week 10: Solve logical reasoning puzzles	\N	Not Started
491030cb-f1b6-4fef-931f-9cbc1415e266	b051e108-742a-452d-88c8-5b14cdad163a	11	Week 10: Participate in online debates	\N	Not Started
b71154cc-2c2a-43e4-b15c-c7bdf78ff455	b051e108-742a-452d-88c8-5b14cdad163a	12	Week 10: Create a case study on a complex issue	\N	Not Started
7546f677-ac6e-4dc3-9f02-dce6f4f6d328	e7d225f3-8d83-43ed-b59b-b7fefb0d72c4	0	Week 17: Practice public speaking using TED Talks	\N	Not Started
dc5e0b47-d123-42e3-a7b7-803646282fef	e7d225f3-8d83-43ed-b59b-b7fefb0d72c4	1	Week 17: Create a presentation on a policy issue	\N	Not Started
b5d477d9-f5c8-423d-8731-d859716a6a75	e7d225f3-8d83-43ed-b59b-b7fefb0d72c4	2	Week 17: Record and review a presentation	\N	Not Started
fb2d0bc8-2eca-4f5d-86cb-ba22e317c5d5	e7d225f3-8d83-43ed-b59b-b7fefb0d72c4	10	Week 18: Write a policy brief	\N	Not Started
ebc6b04c-448a-4b71-877b-c9df33cb4326	e7d225f3-8d83-43ed-b59b-b7fefb0d72c4	11	Week 18: Edit and review a written piece	\N	Not Started
82c89831-1eea-4a74-8fea-f7e08a866177	e7d225f3-8d83-43ed-b59b-b7fefb0d72c4	12	Week 18: Create a writing schedule	\N	Not Started
a9def286-f822-473f-8d4a-6981e587276b	2e55ffb4-c2c3-4b17-897d-49e5353ab27d	0	Week 25: Read economic policy reports	\N	Not Started
1d39a349-fd07-45e4-9142-68145f240a9f	2e55ffb4-c2c3-4b17-897d-49e5353ab27d	1	Week 25: Analyze economic data	\N	Not Started
eda84c43-ff03-48d0-ba14-acd0fc487a37	2e55ffb4-c2c3-4b17-897d-49e5353ab27d	2	Week 25: Create a policy brief on economic issues	\N	Not Started
97f33c17-24e2-465f-95b4-1bdeb9266c96	2e55ffb4-c2c3-4b17-897d-49e5353ab27d	10	Week 26: Research social policy frameworks	\N	Not Started
8edefc84-5d8b-4e61-8920-c132ab9946ad	2e55ffb4-c2c3-4b17-897d-49e5353ab27d	11	Week 26: Analyze case studies of social programs	\N	Not Started
66be3834-5a35-42c0-8cff-f75b28079a3d	2e55ffb4-c2c3-4b17-897d-49e5353ab27d	12	Week 26: Create a policy brief on social issues	\N	Not Started
d19d78fb-40fe-45d7-99b2-31d7c6b77a58	04d7c018-0515-43d7-bdf2-45dbcdd702f4	0	Week 33: Create a study plan	\N	Not Started
10455e93-f63e-4b82-b4ca-123301d1cabb	04d7c018-0515-43d7-bdf2-45dbcdd702f4	1	Week 33: Practice mock tests	\N	Not Started
2afcac2e-5a86-4866-a712-2854531381cb	04d7c018-0515-43d7-bdf2-45dbcdd702f4	2	Week 33: Review and analyze question papers	\N	Not Started
0b77855c-feb2-436d-9c71-b324fa743960	04d7c018-0515-43d7-bdf2-45dbcdd702f4	10	Week 34: Practice time management techniques	\N	Not Started
8b9e788d-0e11-4854-ba98-d06ab11b2a8c	04d7c018-0515-43d7-bdf2-45dbcdd702f4	11	Week 34: Analyze question papers	\N	Not Started
5826d859-4133-42a1-80ae-1979129b9d28	04d7c018-0515-43d7-bdf2-45dbcdd702f4	12	Week 34: Create a question paper analysis template	\N	Not Started
22be4824-b3fb-48b3-8853-8c15e3fa5916	3bd81b64-4bd2-4bce-a28e-c8ace2b7465d	1	Week 1: Watch YouTube lectures on government administration	\N	Completed
a42f5a20-2c19-4e8c-b6ca-401392c71a4e	3bd81b64-4bd2-4bce-a28e-c8ace2b7465d	2	Week 1: Take notes on key concepts	\N	Completed
866f2feb-29c8-4d86-b9a6-ebae176bdd29	3bd81b64-4bd2-4bce-a28e-c8ace2b7465d	0	Week 1: Read the Constitution of India	\N	Completed
ab41161d-aff1-4d6a-988f-f82ea73942c3	3bd81b64-4bd2-4bce-a28e-c8ace2b7465d	10	Week 2: Research public policy frameworks	\N	Completed
\.


--
-- Data for Name: roadmaps; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.roadmaps (id, student_id, title, description, status, progress_percentage, created_at, updated_at) FROM stdin;
433b1435-50cc-4815-862f-a869def4faa1	42bfcb92-4801-40aa-bafc-b8b7a6be0913	Civil Services (Government Administration)	Level: BEGINNER | Duration: 6 months	Active	13.333333333333332	2026-04-15 14:34:27.244185+05:30	2026-04-16 14:11:21.340946+05:30
\.


--
-- Data for Name: sessions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.sessions (id, student_id, mentor_id, scheduled_at, duration_minutes, status, meeting_url, dyte_meeting_id) FROM stdin;
b4ff9a09-d130-4080-a928-a624eba780a6	988b1973-77e2-40b7-b609-c3550812d1cb	0dcbdb98-b93f-4f1f-9305-73f18e3aecfa	2026-04-06 16:30:00+05:30	60	scheduled	\N	\N
f4260bfd-a5f2-46e7-b133-54f9de0f6913	73c4b680-2d95-43a2-bee3-39f351ac955d	d406ecd6-89ce-48f0-8529-68c00477bc4d	2026-04-06 05:30:00+05:30	60	scheduled	\N	\N
3dc81a52-33b0-4841-bc91-dc2787015c2e	73c4b680-2d95-43a2-bee3-39f351ac955d	d406ecd6-89ce-48f0-8529-68c00477bc4d	2026-04-02 22:30:00+05:30	60	completed	\N	\N
b7c97e93-daaa-4e2f-881d-214348fd3059	73c4b680-2d95-43a2-bee3-39f351ac955d	d406ecd6-89ce-48f0-8529-68c00477bc4d	2026-04-02 23:30:00+05:30	60	scheduled	\N	\N
ba8e763c-dfa0-4dfb-9978-5ffb99c7c909	73c4b680-2d95-43a2-bee3-39f351ac955d	d406ecd6-89ce-48f0-8529-68c00477bc4d	2026-04-03 07:30:00+05:30	60	scheduled	\N	\N
ce6bf04c-e679-45a9-a123-179cc03f85ff	73c4b680-2d95-43a2-bee3-39f351ac955d	d406ecd6-89ce-48f0-8529-68c00477bc4d	2026-04-03 17:00:00+05:30	60	scheduled	\N	\N
265e36ca-2195-410c-b54c-fa8f80ad5f2a	73c4b680-2d95-43a2-bee3-39f351ac955d	d406ecd6-89ce-48f0-8529-68c00477bc4d	2026-04-03 15:57:32.12258+05:30	60	completed	\N	\N
74cfb13b-b1dc-4003-85c6-f0e0cf1e4000	73c4b680-2d95-43a2-bee3-39f351ac955d	d406ecd6-89ce-48f0-8529-68c00477bc4d	2026-04-03 18:00:00+05:30	60	completed	\N	\N
a224d4ff-6bb4-41a6-a822-4d0ceb25b3b5	73c4b680-2d95-43a2-bee3-39f351ac955d	d406ecd6-89ce-48f0-8529-68c00477bc4d	2026-04-03 19:00:00+05:30	60	completed	\N	\N
430f6479-0302-482a-a48e-23a1078e1ea1	73c4b680-2d95-43a2-bee3-39f351ac955d	d406ecd6-89ce-48f0-8529-68c00477bc4d	2026-04-03 19:00:00+05:30	60	completed	\N	\N
981460a2-fb37-4638-bbcd-884b737f23e4	73c4b680-2d95-43a2-bee3-39f351ac955d	d406ecd6-89ce-48f0-8529-68c00477bc4d	2026-04-04 10:00:00+05:30	60	scheduled	\N	bbbcb4f8-311c-4fb5-85f1-401f33abce8e
b3190258-c0ab-49a8-a15e-c48034d8e204	73c4b680-2d95-43a2-bee3-39f351ac955d	d406ecd6-89ce-48f0-8529-68c00477bc4d	2026-04-04 11:00:00+05:30	60	scheduled	\N	bbb970f0-3356-43f5-953f-7b1281370cad
d31a2f96-991e-4391-af62-525e6125737c	42da0e64-54b6-420e-b8d6-a0058e06c0e3	3d715f81-3703-47fc-ac63-6a290ca5614d	2026-04-05 03:00:00+05:30	60	scheduled	\N	\N
3904b645-edd4-4cb9-b369-8035db5553b5	42da0e64-54b6-420e-b8d6-a0058e06c0e3	3d715f81-3703-47fc-ac63-6a290ca5614d	2026-04-05 02:00:00+05:30	60	scheduled	\N	\N
0fede97c-19c4-4f8b-95c9-bc2052715ad0	73c4b680-2d95-43a2-bee3-39f351ac955d	d406ecd6-89ce-48f0-8529-68c00477bc4d	2026-04-06 16:00:00+05:30	60	scheduled	\N	bbb52740-584f-47f0-ae12-99dee43198eb
bb48e277-453e-415c-bc6c-f1d859e88c4a	73c4b680-2d95-43a2-bee3-39f351ac955d	d406ecd6-89ce-48f0-8529-68c00477bc4d	2026-04-07 19:00:00+05:30	60	scheduled	\N	bbb4cf70-20d0-42cd-a42c-00edf5f7c28d
83fb98ab-8aa9-42e0-a1cb-df3a5704d337	73c4b680-2d95-43a2-bee3-39f351ac955d	d406ecd6-89ce-48f0-8529-68c00477bc4d	2026-04-13 10:00:00+05:30	60	scheduled	\N	bbbbd453-ef33-4ab2-852e-b7be5f55ab03
6a8868d5-1089-4ba8-b118-7dcaad3fe3e9	73c4b680-2d95-43a2-bee3-39f351ac955d	d406ecd6-89ce-48f0-8529-68c00477bc4d	2026-04-12 17:00:00+05:30	60	scheduled	\N	bbbb6812-4d4a-4881-8b07-56180e625085
5b3a3d93-b773-449e-bd45-3b626e10b9c8	73c4b680-2d95-43a2-bee3-39f351ac955d	d406ecd6-89ce-48f0-8529-68c00477bc4d	2026-04-13 16:00:00+05:30	60	scheduled	\N	bbbeb36d-e701-4113-851e-ccf4bb9a9dc3
5f63b760-a4a6-4ff7-a2a2-d01d9386a79f	3b4a166e-51c4-4a3e-b388-79d916f84714	c7a401b6-5b27-4fbe-842a-fa5746907996	2026-04-14 09:00:00+05:30	60	scheduled	\N	bbbbae4c-75b7-4730-8cf3-ad87744b933c
f138ced7-df0b-414c-a256-8583d0851b10	3b4a166e-51c4-4a3e-b388-79d916f84714	c7a401b6-5b27-4fbe-842a-fa5746907996	2026-04-15 00:00:00+05:30	60	scheduled	\N	bbb9b94d-835b-4606-bdd9-448726f89d36
81a95ce2-197e-4624-84ca-90bc51f1cfc8	3b4a166e-51c4-4a3e-b388-79d916f84714	3d715f81-3703-47fc-ac63-6a290ca5614d	2026-04-14 10:00:00+05:30	60	scheduled	\N	bbb4c9bf-663e-4c0a-8bec-6bafc4086d30
7807f73e-9199-4e3d-9acc-189187c6ee29	3b4a166e-51c4-4a3e-b388-79d916f84714	c7a401b6-5b27-4fbe-842a-fa5746907996	2026-04-14 02:10:00+05:30	60	scheduled	\N	bbb661d1-8788-49f5-8337-af087bece4ad
55a1bb94-e009-4d73-a77c-3b3ea388175d	42bfcb92-4801-40aa-bafc-b8b7a6be0913	ede1faa2-6900-4ab5-b30b-9e7cb982751b	2026-04-15 16:00:00+05:30	60	scheduled	\N	bbb9a583-5bb8-45a4-bf0d-6f5a8de33b83
cfa3e1e1-9748-4119-9b41-c0d499ffa0bd	42bfcb92-4801-40aa-bafc-b8b7a6be0913	ede1faa2-6900-4ab5-b30b-9e7cb982751b	2026-04-16 15:00:00+05:30	60	completed	\N	bbb8f1a9-2d04-4111-8826-c98839bf9d2b
9e34892c-1000-4484-845e-bf83b38c32ea	42bfcb92-4801-40aa-bafc-b8b7a6be0913	ede1faa2-6900-4ab5-b30b-9e7cb982751b	2026-04-16 18:00:00+05:30	60	scheduled	\N	bbb9cd09-75c9-4360-9602-0e94323c28dc
34966a18-63f9-4c93-bb16-a1d08c01595d	42bfcb92-4801-40aa-bafc-b8b7a6be0913	ede1faa2-6900-4ab5-b30b-9e7cb982751b	2026-04-16 16:05:00+05:30	60	completed	\N	bbb43db4-5ecf-47c0-a2f1-de77af3ba2c1
39a8535b-9ed0-48dc-b545-f241557e7c02	42bfcb92-4801-40aa-bafc-b8b7a6be0913	ede1faa2-6900-4ab5-b30b-9e7cb982751b	2026-04-16 17:28:00+05:30	60	scheduled	\N	bbbe673d-80a6-493f-ae5d-115a63cb483e
1a60288a-0f14-4e49-b6d0-d68a5b1f1c5a	42bfcb92-4801-40aa-bafc-b8b7a6be0913	ede1faa2-6900-4ab5-b30b-9e7cb982751b	2026-04-17 14:46:00+05:30	60	completed	\N	bbb14a8a-69ae-4b78-895d-e5e82f65c542
2be6bddb-d650-4508-9010-b2e8e8279c40	42bfcb92-4801-40aa-bafc-b8b7a6be0913	ede1faa2-6900-4ab5-b30b-9e7cb982751b	2026-04-17 11:55:00+05:30	60	completed	\N	bbb205cd-7fe2-406d-8338-2b3dd7685ff8
\.


--
-- Data for Name: skills; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.skills (id, name, category) FROM stdin;
d8936321-b131-4bf5-8a97-9e926c7510bf	Statistical Analysis	technical
83becb2c-8b8a-41da-b393-e1c92f3feec5	Excel/Spreadsheets	technical
0f2d3099-1877-4ce1-b9c4-925e96faa80f	Data Visualization	technical
9dabfaf9-1048-4fe7-8b21-65611a814de4	Logical Reasoning	cognitive
b85174dd-9469-4a1a-858b-ab967f3228dd	Attention to Detail	cognitive
3903fb6a-3ea1-4f48-9756-0aebb3e3458a	HTML/CSS	technical
8ebfdf63-8eb9-4e02-8361-b38c44f26736	JavaScript Programming	technical
0b198e98-1fe3-4630-b2ab-06e516dc819d	Logical Problem Solving	cognitive
ea1755d2-fa1a-4d15-be7e-5360a3c2aa60	Self-Learning Ability	soft
\.


--
-- Data for Name: student_insights; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.student_insights (id, student_id, ai_summary, recommended_career_id, success_probability, feasibility_score, passion_skill_gap, generated_at) FROM stdin;
5df62d81-cf80-422e-b6ed-6a5e2ddcd15a	42bfcb92-4801-40aa-bafc-b8b7a6be0913	\N	f8680cab-c381-4f0b-954b-65783592b3be	\N	\N	\N	2026-04-15 14:34:12.274263+05:30
\.


--
-- Data for Name: tests; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tests (id, title, type, total_questions) FROM stdin;
\.


--
-- Data for Name: user_skills; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.user_skills (user_id, skill_id, score, updated_at) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (id, email, hashed_password, full_name, role, profile_photo_url, invite_code, created_at, updated_at, academic_data, apti_data, personality_data, lifestyle_data, financial_data, passion_strength_data, aspiration_data, career_interest_data, profile_data) FROM stdin;
ba1e0065-bab3-4f33-8835-2715652b836d	user@example.com	$2b$12$Q8i2Iq5WPPWXNVHTxZRl1Oho.wxfb7bj4lQt4ne1Uj6JcUAJvLU1q	string	student	\N	\N	2026-04-15 12:47:33.469055+05:30	2026-04-15 12:47:33.469055+05:30	\N	\N	\N	\N	\N	\N	\N	\N	\N
42bfcb92-4801-40aa-bafc-b8b7a6be0913	me@gmail.com	$2b$12$e2zKMbRRYG58itaGRmmSrOW3ji92lffnwHonijvu88ZX7osD.U54G	me	student	\N	BSRAYL	2026-04-14 18:23:22.499376+05:30	2026-04-15 14:36:04.600161+05:30	{"achievements": "s", "learning_style": "ss", "weakest_subject": "s", "favorite_subject": "s", "study_hours_home": "s", "strongest_subject": "ss", "homework_completion": "s", "overall_percentage_band": "h"}	{"0f93c6f4-42d9-493e-b6f4-77d48ed2eeda": "B", "1502d90b-f81d-418e-a25a-8e9a9f3ce89d": "B", "23d341d3-044d-489e-a1c0-18a28019291a": "B", "2cc7de55-5c05-4129-8fe8-90b3aa727cb4": "B", "2f3d9a85-c0a7-4092-86ee-5f9f36f7aecb": "B", "314770eb-34fc-4599-8bc6-8d933f078a52": "B", "3609b258-cdbb-4103-bbe8-3dc7bad050a0": "B", "3882738e-bf2f-45b9-8713-31c4a74318cb": "B", "44b81742-d754-442d-823a-b5b79a0142e4": "B", "462733ac-e470-40b9-95c2-60294d600644": "B", "46b06c12-012b-4450-838f-e86ff9501213": "B", "4f364ab0-73bf-448c-b100-405af2fbfe34": "B", "5636ef2d-2b1f-4f2d-afe7-88a6aaef24a9": "B", "5a68b7b4-a23f-4e8d-9668-de11b2ee8c06": "B", "5a9a2594-7ff2-4532-9de2-702e7ae9a39a": "B", "5ffda759-ffd4-490e-9317-13c3e78974ed": "B", "62854d6e-cc9a-40e8-afe2-0906fd15c70e": "B", "635d4ea6-a7f2-439c-94aa-dce67d95e8d8": "B", "6524d79d-5eac-4219-b33a-0160d8e63eb0": "B", "661fdb2e-79ef-4a7d-93db-1f61af5f8a2c": "B", "6d354098-129b-4544-a76f-9be8d8ba1098": "B", "7a2063b7-3758-4a77-9c96-675d8dbd2219": "B", "7c60f66d-d94c-464a-875a-a7507719fb9d": "B", "81d8bf84-ac8e-4ac4-b415-27cf84238968": "B", "837e4636-3b8c-42e6-9432-a3ae7990fb96": "B", "84b22aee-3925-45c3-9bcc-1c93359bbf4f": "B", "8c2fb2a5-6a78-4358-a573-e745c7bef32c": "B", "8f426477-3f9e-4f65-9e71-1f88c4570b4c": "B", "95d60555-bc6e-405a-b9b2-ba3b969e5a6e": "B", "977c9ed9-db1b-46af-a70a-79c8d234b67c": "B", "9ec004be-fad9-4556-8de7-dc7c6328b8ca": "B", "a1f4de27-f1ed-4bf4-865a-246edab7d30b": "B", "d2382b54-72db-45d0-9282-bb31d8b6a8a1": "B", "d55861fa-c6e8-43dd-86ee-e6d8cafd61d1": "B", "d62870be-6f28-4442-8010-8f37f559f7e9": "B", "d686d388-50a7-493f-bd57-1cef50890943": "B", "e804009d-161e-4410-a585-3b356ef39d67": "B", "f1ca4450-a735-4a2d-9af5-97e3bdc50232": "B", "f313f0c3-a93f-4517-bb4b-ca6924d74e1e": "B", "f4b6fe46-82d8-4448-94fe-8d0590977acb": "B", "f5aedd71-39de-4358-b785-ca3a4fd1c49c": "B", "f7e196a8-928b-4366-9863-a94b84bcb323": "B", "f9b972da-c81a-4901-845b-3d7faa7d6249": "B", "fb2a331c-e2a4-4f36-a913-7ab26b96ab44": "B", "fedeb497-8165-46f5-8d28-da8ff44bd23b": "B"}	{"C1": 2, "C3": 4, "C4": 4, "C5": 2, "C6": 4, "C7": 2, "C8": 4, "D1": 4, "D2": 4, "D3": 2, "D4": 5, "D5": 2, "D7": 2, "D8": 4, "E1": 2, "E2": 2, "E3": 4, "E4": 2, "E6": 2, "E7": 4, "E8": 4, "H1": 4, "H2": 4, "H3": 2, "H5": 4, "H6": 2, "H7": 4, "H8": 2, "S2": 4, "S3": 4, "S4": 4, "S5": 2, "S6": 2, "S7": 2, "S8": 4}	{"screen_time": "ss", "study_hours": "ss", "focus_ability": "s", "sleep_quality": "s", "distraction_level": "s", "pressure_handling": "s", "social_preference": "s", "biggest_distraction": "s", "reaction_to_failure": "s", "routine_consistency": "s"}	{"income_band": "ss", "coaching_access": "s", "family_structure": "ss", "father_education": "s", "mother_education": "ss", "affordability_level": "s"}	{"effort_level": "Minimal", "easiest_tasks": "sss", "curiosity_level": 4, "biggest_strength": "ss", "biggest_weakness": "ss", "motivation_driver": "Money", "confidence_trigger": "s", "free_time_activity": "hiis", "natural_strength_area": "Creativity", "most_exciting_activity": "s", "most_satisfying_success": "s", "what_people_praise_you_for": "s"}	{"dream_career": "s", "life_direction": "s", "ten_year_vision": "s"}	{"creativity": 1, "leadership": 2, "work_style": "Team", "helping_nature": 4, "interest_domain": "Art", "biggest_strength": "s", "biggest_weakness": "s", "career_awareness": "Medium", "data_orientation": 4, "work_environment": "Outdoor", "physical_activity": 4, "preferred_activity": "s", "research_inclination": 5, "preferred_career_type": "Private"}	{"dob": "2", "state": "dd", "gender": "Female", "full_name": "Aditi", "school_type": "Private", "current_class": "11th", "medium_of_learning": "English"}
92d61dc2-c5da-4295-afec-bb308562d99e	choudharyyash614@gmail.com	$2b$12$uJOP3uWlSzvtvjL/0Oyw7eG1WzSZcT/qm7ZdNJIw8nX9QhBAjLlyy	Yash Choudhary	student	\N	PY9D4C	2026-04-15 12:57:04.952122+05:30	2026-04-15 13:51:33.007134+05:30	{"achievements": "nothing", "learning_style": "Auditory (Lectures & Podcasts)", "weakest_subject": "history", "favorite_subject": "computer science", "study_hours_home": "1–2 hours/day", "strongest_subject": "physics", "homework_completion": "Always (90–100%)", "overall_percentage_band": "40–60%"}	{"_status": "in_progress", "_answers": {"0": "B", "1": "B", "2": "C", "3": "C", "4": "C", "5": "D", "6": "C", "7": "B"}, "_current_index": 7, "_session_questions": [{"answer": "B", "options": ["A) 4-14-7", "B) 4-15-7", "C) 3-15-7", "D) 4-14-6"], "category": "Logical Reasoning", "question": "If CAT = 3-1-20, what is DOG?", "difficulty": "Easy", "explanation": "Using A=1, B=2… D=4, O=15, G=7. DOG = 4-15-7."}, {"answer": "B", "options": ["A) 50 km/h", "B) 60 km/h", "C) 70 km/h", "D) 80 km/h"], "category": "Quantitative Aptitude", "question": "A train travels 180 km in 3 hours. What is its speed?", "difficulty": "Easy", "explanation": "Speed = Distance / Time = 180 / 3 = 60 km/h."}, {"answer": "C", "options": ["A) Bold", "B) Strong", "C) Cowardly", "D) Fierce"], "category": "Verbal Ability", "question": "What is the antonym of 'BRAVE'?", "difficulty": "Easy", "explanation": "Brave means courageous. Its antonym is cowardly, meaning lacking courage."}, {"answer": "C", "options": ["A) 30", "B) 34", "C) 36", "D) 49"], "category": "Logical Reasoning", "question": "Find the next term: 1, 4, 9, 16, 25, ?", "difficulty": "Medium", "explanation": "These are perfect squares: 1², 2², 3², 4², 5², 6² = 36."}, {"answer": "C", "options": ["A) 100 cm²", "B) 121 cm²", "C) 144 cm²", "D) 169 cm²"], "category": "Quantitative Aptitude", "question": "The perimeter of a square is 48 cm. What is its area?", "difficulty": "Medium", "explanation": "Side = Perimeter / 4 = 48 / 4 = 12 cm. Area = 12² = 144 cm²."}, {"answer": "B", "options": ["A) Artist", "B) Museum", "C) Canvas", "D) Colour"], "category": "Verbal Ability", "question": "Analogy — Book : Library :: Painting : ?", "difficulty": "Medium", "explanation": "Books are kept in a library; paintings are kept in a museum."}, {"answer": "C", "options": ["A) 0", "B) 4", "C) 8", "D) 16"], "category": "Logical Reasoning", "question": "A cube is painted blue on all faces, then cut into 64 equal smaller cubes. How many small cubes have no face painted?", "difficulty": "Hard", "explanation": "A 4×4×4 cube has an inner 2×2×2 core with no paint. 2³ = 8 unpainted cubes."}, {"answer": "A", "options": ["A) 18", "B) 23", "C) 28", "D) 33"], "category": "Quantitative Aptitude", "question": "A number when divided by 5 leaves remainder 3, and when divided by 7 leaves remainder 4. What is the smallest such number?", "difficulty": "Hard", "explanation": "We need x ≡ 3 (mod 5) and x ≡ 4 (mod 7). Testing: 18/5 = rem 3 ✓, 18/7 = rem 4 ✓. Answer = 18."}, {"answer": "B", "options": ["A) Animals are falling from the sky", "B) It is raining heavily", "C) The weather is pleasant", "D) There is a storm coming"], "category": "Verbal Ability", "question": "What does the idiom 'it's raining cats and dogs' mean?", "difficulty": "Easy", "explanation": "'Raining cats and dogs' is an idiom meaning it is raining very heavily."}, {"answer": "D", "options": ["A) 90°", "B) 120°", "C) 150°", "D) 180°"], "category": "Logical Reasoning", "question": "A clock shows 6:00. What is the angle between the hour and minute hands?", "difficulty": "Hard", "explanation": "At 6:00, the hour hand points to 6 (180°) and the minute hand to 12 (0°). Angle = 180°."}]}	\N	{"screen_time": "Less than 1 hr/day", "study_hours": "2–4 hrs of deep work", "focus_ability": "Less than 20 minutes", "sleep_quality": "Less than 6 hrs (poor)", "distraction_level": "Somewhat distracted", "pressure_handling": "Handle with moderate stress", "social_preference": "Solo focus (independent deep work)", "biggest_distraction": "girls", "reaction_to_failure": "Feel bad, but try again later", "routine_consistency": "7"}	{"income_band": "₹5–10 LPA", "coaching_access": "Yes, in a coaching institute", "family_structure": "Nuclear Family", "father_education": "12th / HSC", "mother_education": "12th / HSC", "affordability_level": "Need affordable options"}	\N	{"dream_career": "software engineer", "life_direction": "boosting the growth of my startup", "ten_year_vision": "on the top"}	{"creativity": "Not particularly creative", "leadership": "Yes, I love leading and organizing", "work_style": "Team-based & collaborative", "helping_nature": "Somewhat fulfilling", "interest_domain": "Technology & Computers", "biggest_strength": "problem solving", "biggest_weakness": "public speaking", "career_awareness": "High – I know exactly what I want", "data_orientation": "Somewhat comfortable with data", "work_environment": "Indoor / Office / Lab setting", "physical_activity": "No preference", "preferred_activity": "coding", "research_inclination": "Yes, I love deep research", "preferred_career_type": "Own Business / Entrepreneurship"}	{"dob": "2005-12-02", "state": "delhi", "gender": "Male", "full_name": "Yash Choudhary", "school_type": "Private", "current_class": "8th", "medium_of_learning": "English"}
b0cb04e9-2036-438d-b770-1c418e30619d	parent@gmail.com	$2b$12$2T2sh0XWbUxaC8TEhjncm.1zwMKEnUfZG0lhHd6ZqcPQiGofXusey	parent	parent	\N	\N	2026-04-15 14:36:34.377916+05:30	2026-04-15 14:36:34.377916+05:30	\N	\N	\N	\N	\N	\N	\N	\N	\N
5bc65df5-4139-4086-be70-eb9c59499af2	mentor@gmail.com	$2b$12$sVMM9wVwwc0tBwaaSjTUOedwU8w58UDLqkDASHyQ71pcxk0yLwvAu	Sir	mentor	\N	\N	2026-04-15 14:39:48.813302+05:30	2026-04-15 14:39:48.813302+05:30	\N	\N	\N	\N	\N	\N	\N	\N	\N
ddf51f2a-ea2c-4713-8aea-eb35d5c985ab	sir@gmail.com	$2b$12$f3dtoo24Df9axOdTzLJryOlUX7biC9vMx4//R0lcrykV6dP3MlINy	New	mentor	\N	\N	2026-04-15 14:46:31.593771+05:30	2026-04-15 14:46:31.593771+05:30	\N	\N	\N	\N	\N	\N	\N	\N	\N
f532cff2-555b-489c-bfaf-3ef569532bb7	bat@gmail.com	$2b$12$EH1FVxS6EHf6/KH7FvHApeaQMWsQ3sT7.gWBOMNsV8I6G2tncZIyG	BatMan	mentor	\N	\N	2026-04-15 14:48:29.181506+05:30	2026-04-15 14:48:29.181506+05:30	\N	\N	\N	\N	\N	\N	\N	\N	\N
f956a026-afdb-40a9-9efc-b2554deecf0f	newme@gmail.com	$2b$12$T68rePlDjzlKC180kkDXvuKYSFx4NoQE9pTqMspk0bvyN0hmRQZjS	newme	student	\N	\N	2026-04-15 16:54:21.49483+05:30	2026-04-15 16:59:22.943475+05:30	\N	\N	{"C1": 2, "C2": 2, "C3": 4, "C5": 2, "C6": 4, "C7": 4, "C8": 1, "D1": 2, "D2": 1, "D3": 2, "D4": 4, "D6": 4, "D7": 4, "D8": 4, "E1": 2, "E2": 4, "E3": 4, "E4": 4, "E6": 2, "E7": 2, "E8": 2, "H1": 4, "H3": 2, "H4": 5, "H5": 4, "H6": 1, "H7": 4, "H8": 2, "S1": 4, "S2": 2, "S3": 2, "S5": 4, "S6": 4, "S7": 2, "S8": 4}	{"screen_time": "g", "study_hours": "g", "focus_ability": "gg", "sleep_quality": "g", "distraction_level": "g", "pressure_handling": "g", "social_preference": "g", "biggest_distraction": "g", "reaction_to_failure": "gt", "routine_consistency": "g"}	{"income_band": "f", "coaching_access": "f", "family_structure": "f", "father_education": "f", "mother_education": "f", "affordability_level": "f"}	{"effort_level": "Maximum", "easiest_tasks": "gg", "curiosity_level": 2, "biggest_strength": "g", "biggest_weakness": "g", "motivation_driver": "Success", "confidence_trigger": "gg", "free_time_activity": "g", "natural_strength_area": "Studies", "most_exciting_activity": "g", "most_satisfying_success": "g", "what_people_praise_you_for": "g"}	{"dream_career": "s", "life_direction": "s", "ten_year_vision": "s"}	{"creativity": 4, "leadership": 2, "work_style": "Team", "helping_nature": 4, "interest_domain": "Business", "biggest_strength": "f", "biggest_weakness": "d", "career_awareness": "High", "data_orientation": 2, "work_environment": "Outdoor", "physical_activity": 1, "preferred_activity": "d", "research_inclination": 4, "preferred_career_type": "Govt"}	{"dob": "2", "state": "jj", "gender": "Male", "full_name": "a", "school_type": "Private", "current_class": "11th", "medium_of_learning": "Hindi"}
5e1f46ac-0403-4ae4-ad04-263858cd7a22	mridulbhardwaj13@gmail.com	$2b$12$7HmOD0CSPGl7LsZvabE0TufJoZRVSgbQssKc9DsooLMwuGzar4NNy	Aakash	student	\N	IJB3IP	2026-04-16 14:08:01.864342+05:30	2026-04-16 14:08:10.522136+05:30	\N	\N	\N	\N	\N	\N	\N	\N	\N
4e6b35fb-dd45-4a68-88f0-2a4ace030fd8	newp@gmail.coom	$2b$12$oDJgisNAWw5A09pjqmWeuevbH43CtZ12Im9QW1d7zHPj4/kIkLH6O	new	parent	\N	\N	2026-04-16 14:19:04.814372+05:30	2026-04-16 14:19:04.814372+05:30	\N	\N	\N	\N	\N	\N	\N	\N	\N
442c332d-0559-42dc-8311-f7df117da221	kumar.govind.iitdelhi@gmail.com	$2b$12$ncvA/i5w.bJMZIQZuCZKMOyqs1P72EYSMyDDIKaSi5Saiy.Xqz./i	kumar	student	\N	QY6B2R	2026-04-16 21:58:19.147139+05:30	2026-04-16 22:07:04.003506+05:30	{"achievements": "DISTRICT LEVEL BADMINTON CHAMPION", "learning_style": "Visual (Videos & Diagrams)", "weakest_subject": "CHEMISTRY ", "favorite_subject": "PHYSICS", "study_hours_home": "2–4 hours/day", "strongest_subject": "MATHS ,PHYSICS ", "homework_completion": "Sometimes (50–70%)", "overall_percentage_band": "75–90%"}	\N	\N	\N	\N	\N	\N	\N	{"dob": "1999-02-07", "state": "DELHI", "gender": "Male", "full_name": "KUMAR G", "school_type": "Private", "current_class": "11th", "medium_of_learning": "Mixed (English + Hindi)"}
\.


--
-- Name: academic_profiles academic_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.academic_profiles
    ADD CONSTRAINT academic_profiles_pkey PRIMARY KEY (id);


--
-- Name: academic_profiles academic_profiles_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.academic_profiles
    ADD CONSTRAINT academic_profiles_user_id_key UNIQUE (user_id);


--
-- Name: aspiration_profiles aspiration_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aspiration_profiles
    ADD CONSTRAINT aspiration_profiles_pkey PRIMARY KEY (id);


--
-- Name: aspiration_profiles aspiration_profiles_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aspiration_profiles
    ADD CONSTRAINT aspiration_profiles_user_id_key UNIQUE (user_id);


--
-- Name: career_skills career_skills_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.career_skills
    ADD CONSTRAINT career_skills_pkey PRIMARY KEY (career_id, skill_id);


--
-- Name: careers careers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.careers
    ADD CONSTRAINT careers_pkey PRIMARY KEY (id);


--
-- Name: careers careers_title_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.careers
    ADD CONSTRAINT careers_title_key UNIQUE (title);


--
-- Name: chat_messages chat_messages_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chat_messages
    ADD CONSTRAINT chat_messages_pkey PRIMARY KEY (id);


--
-- Name: financial_profiles financial_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.financial_profiles
    ADD CONSTRAINT financial_profiles_pkey PRIMARY KEY (id);


--
-- Name: financial_profiles financial_profiles_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.financial_profiles
    ADD CONSTRAINT financial_profiles_user_id_key UNIQUE (user_id);


--
-- Name: lifestyle_profiles lifestyle_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lifestyle_profiles
    ADD CONSTRAINT lifestyle_profiles_pkey PRIMARY KEY (id);


--
-- Name: lifestyle_profiles lifestyle_profiles_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lifestyle_profiles
    ADD CONSTRAINT lifestyle_profiles_user_id_key UNIQUE (user_id);


--
-- Name: mentor_availability mentor_availability_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mentor_availability
    ADD CONSTRAINT mentor_availability_pkey PRIMARY KEY (id);


--
-- Name: mentor_feedback mentor_feedback_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mentor_feedback
    ADD CONSTRAINT mentor_feedback_pkey PRIMARY KEY (id);


--
-- Name: mentors mentors_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mentors
    ADD CONSTRAINT mentors_pkey PRIMARY KEY (id);


--
-- Name: mentors mentors_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mentors
    ADD CONSTRAINT mentors_user_id_key UNIQUE (user_id);


--
-- Name: mentorship_requests mentorship_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mentorship_requests
    ADD CONSTRAINT mentorship_requests_pkey PRIMARY KEY (id);


--
-- Name: parent_feedback parent_feedback_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.parent_feedback
    ADD CONSTRAINT parent_feedback_pkey PRIMARY KEY (id);


--
-- Name: parent_student_links parent_student_links_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.parent_student_links
    ADD CONSTRAINT parent_student_links_pkey PRIMARY KEY (id);


--
-- Name: profiles profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.profiles
    ADD CONSTRAINT profiles_pkey PRIMARY KEY (id);


--
-- Name: profiles profiles_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.profiles
    ADD CONSTRAINT profiles_user_id_key UNIQUE (user_id);


--
-- Name: psychometric_profiles psychometric_profiles_pkey1; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.psychometric_profiles
    ADD CONSTRAINT psychometric_profiles_pkey1 PRIMARY KEY (id);


--
-- Name: psychometric_profiles psychometric_profiles_user_id_key1; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.psychometric_profiles
    ADD CONSTRAINT psychometric_profiles_user_id_key1 UNIQUE (user_id);


--
-- Name: results results_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.results
    ADD CONSTRAINT results_pkey PRIMARY KEY (id);


--
-- Name: roadmap_phases roadmap_phases_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roadmap_phases
    ADD CONSTRAINT roadmap_phases_pkey PRIMARY KEY (id);


--
-- Name: roadmap_tasks roadmap_tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roadmap_tasks
    ADD CONSTRAINT roadmap_tasks_pkey PRIMARY KEY (id);


--
-- Name: roadmaps roadmaps_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roadmaps
    ADD CONSTRAINT roadmaps_pkey PRIMARY KEY (id);


--
-- Name: roadmaps roadmaps_student_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roadmaps
    ADD CONSTRAINT roadmaps_student_id_key UNIQUE (student_id);


--
-- Name: sessions sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_pkey PRIMARY KEY (id);


--
-- Name: skills skills_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.skills
    ADD CONSTRAINT skills_name_key UNIQUE (name);


--
-- Name: skills skills_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.skills
    ADD CONSTRAINT skills_pkey PRIMARY KEY (id);


--
-- Name: student_insights student_insights_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.student_insights
    ADD CONSTRAINT student_insights_pkey PRIMARY KEY (id);


--
-- Name: student_insights student_insights_student_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.student_insights
    ADD CONSTRAINT student_insights_student_id_key UNIQUE (student_id);


--
-- Name: tests tests_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tests
    ADD CONSTRAINT tests_pkey PRIMARY KEY (id);


--
-- Name: user_skills user_skills_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_skills
    ADD CONSTRAINT user_skills_pkey PRIMARY KEY (user_id, skill_id);


--
-- Name: users users_invite_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_invite_code_key UNIQUE (invite_code);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: academic_profiles academic_profiles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.academic_profiles
    ADD CONSTRAINT academic_profiles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: aspiration_profiles aspiration_profiles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aspiration_profiles
    ADD CONSTRAINT aspiration_profiles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: career_skills career_skills_career_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.career_skills
    ADD CONSTRAINT career_skills_career_id_fkey FOREIGN KEY (career_id) REFERENCES public.careers(id) ON DELETE CASCADE;


--
-- Name: career_skills career_skills_skill_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.career_skills
    ADD CONSTRAINT career_skills_skill_id_fkey FOREIGN KEY (skill_id) REFERENCES public.skills(id) ON DELETE CASCADE;


--
-- Name: chat_messages chat_messages_mentor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chat_messages
    ADD CONSTRAINT chat_messages_mentor_id_fkey FOREIGN KEY (mentor_id) REFERENCES public.mentors(id) ON DELETE CASCADE;


--
-- Name: chat_messages chat_messages_sender_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chat_messages
    ADD CONSTRAINT chat_messages_sender_id_fkey FOREIGN KEY (sender_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: chat_messages chat_messages_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chat_messages
    ADD CONSTRAINT chat_messages_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: financial_profiles financial_profiles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.financial_profiles
    ADD CONSTRAINT financial_profiles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: roadmap_tasks fk_phase; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roadmap_tasks
    ADD CONSTRAINT fk_phase FOREIGN KEY (phase_id) REFERENCES public.roadmap_phases(id) ON DELETE CASCADE;


--
-- Name: lifestyle_profiles lifestyle_profiles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lifestyle_profiles
    ADD CONSTRAINT lifestyle_profiles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: mentor_availability mentor_availability_mentor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mentor_availability
    ADD CONSTRAINT mentor_availability_mentor_id_fkey FOREIGN KEY (mentor_id) REFERENCES public.mentors(id) ON DELETE CASCADE;


--
-- Name: mentor_feedback mentor_feedback_mentor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mentor_feedback
    ADD CONSTRAINT mentor_feedback_mentor_id_fkey FOREIGN KEY (mentor_id) REFERENCES public.mentors(id) ON DELETE CASCADE;


--
-- Name: mentor_feedback mentor_feedback_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mentor_feedback
    ADD CONSTRAINT mentor_feedback_session_id_fkey FOREIGN KEY (session_id) REFERENCES public.sessions(id) ON DELETE CASCADE;


--
-- Name: mentor_feedback mentor_feedback_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mentor_feedback
    ADD CONSTRAINT mentor_feedback_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: mentors mentors_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mentors
    ADD CONSTRAINT mentors_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: parent_feedback parent_feedback_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.parent_feedback
    ADD CONSTRAINT parent_feedback_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: parent_feedback parent_feedback_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.parent_feedback
    ADD CONSTRAINT parent_feedback_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: parent_student_links parent_student_links_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.parent_student_links
    ADD CONSTRAINT parent_student_links_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: parent_student_links parent_student_links_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.parent_student_links
    ADD CONSTRAINT parent_student_links_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: profiles profiles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.profiles
    ADD CONSTRAINT profiles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: psychometric_profiles psychometric_profiles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.psychometric_profiles
    ADD CONSTRAINT psychometric_profiles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: results results_test_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.results
    ADD CONSTRAINT results_test_id_fkey FOREIGN KEY (test_id) REFERENCES public.tests(id) ON DELETE CASCADE;


--
-- Name: results results_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.results
    ADD CONSTRAINT results_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: roadmaps roadmaps_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roadmaps
    ADD CONSTRAINT roadmaps_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: student_insights student_insights_recommended_career_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.student_insights
    ADD CONSTRAINT student_insights_recommended_career_id_fkey FOREIGN KEY (recommended_career_id) REFERENCES public.careers(id);


--
-- Name: student_insights student_insights_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.student_insights
    ADD CONSTRAINT student_insights_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: user_skills user_skills_skill_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_skills
    ADD CONSTRAINT user_skills_skill_id_fkey FOREIGN KEY (skill_id) REFERENCES public.skills(id) ON DELETE CASCADE;


--
-- Name: user_skills user_skills_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_skills
    ADD CONSTRAINT user_skills_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--


