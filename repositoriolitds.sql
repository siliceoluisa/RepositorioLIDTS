--
-- PostgreSQL database dump
--

-- Dumped from database version 16.8
-- Dumped by pg_dump version 16.8

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: files_repo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.files_repo (
    id_file integer NOT NULL,
    title character varying(255) NOT NULL,
    author character varying(100) NOT NULL,
    type_file character varying(50),
    editor character varying(100),
    place_publication character varying(250) NOT NULL,
    date_publication date NOT NULL,
    date_uploaded timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    description text,
    file_path character varying(100),
    id_user integer NOT NULL,
    id_materia integer NOT NULL,
    CONSTRAINT files_repo_type_file_check CHECK (((type_file)::text = ANY ((ARRAY['Tesis'::character varying, 'Artículo'::character varying, 'Libro'::character varying, 'Otro'::character varying])::text[])))
);


ALTER TABLE public.files_repo OWNER TO postgres;

--
-- Name: files_repo_id_file_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.files_repo_id_file_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.files_repo_id_file_seq OWNER TO postgres;

--
-- Name: files_repo_id_file_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.files_repo_id_file_seq OWNED BY public.files_repo.id_file;


--
-- Name: subjects; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subjects (
    id_materia integer NOT NULL,
    name character varying(150) NOT NULL,
    description text,
    semester smallint NOT NULL,
    CONSTRAINT subjects_semester_check CHECK (((semester >= 1) AND (semester <= 10)))
);


ALTER TABLE public.subjects OWNER TO postgres;

--
-- Name: subjects_id_materia_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.subjects_id_materia_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.subjects_id_materia_seq OWNER TO postgres;

--
-- Name: subjects_id_materia_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.subjects_id_materia_seq OWNED BY public.subjects.id_materia;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id_user integer NOT NULL,
    name character varying(100) NOT NULL,
    email character varying(255) NOT NULL,
    password text NOT NULL,
    type_user character varying(20),
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    profile_picture character varying(255)
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_user_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_user_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_user_seq OWNER TO postgres;

--
-- Name: users_id_user_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_user_seq OWNED BY public.users.id_user;


--
-- Name: files_repo id_file; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.files_repo ALTER COLUMN id_file SET DEFAULT nextval('public.files_repo_id_file_seq'::regclass);


--
-- Name: subjects id_materia; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subjects ALTER COLUMN id_materia SET DEFAULT nextval('public.subjects_id_materia_seq'::regclass);


--
-- Name: users id_user; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id_user SET DEFAULT nextval('public.users_id_user_seq'::regclass);


--
-- Data for Name: files_repo; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.files_repo (id_file, title, author, type_file, editor, place_publication, date_publication, date_uploaded, description, file_path, id_user, id_materia) FROM stdin;
1	Programando la interfaz gráfica con: XPCE/Prolog	Pau Sánchez Campello	Tesis	sin editor	sin lugar	2023-04-20	2025-04-01 12:37:48.600582	XPCE/Prolog es una forma de programar interfaces gráficas de usuario (GUI) utilizando la librería XPCE y el lenguaje de programación Prolog. 	uploads/2. xpcePROLOG.pdf	1	1
\.


--
-- Data for Name: subjects; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.subjects (id_materia, name, description, semester) FROM stdin;
1	Inteligencia Artificial	Introducción a algoritmos y técnicas de IA.	7
2	Sistemas Operativos	Estudio de la gestión de hardware y software del sistema.	7
3	Aplicaciones Web y Móviles	Desarrollo de aplicaciones para la web y dispositivos móviles.	7
4	Conmutadores y Redes Inalámbricas	Configuración y administración de redes avanzadas.	7
5	Seguridad en Cómputo	Principios y prácticas para proteger sistemas informáticos.	7
6	Análisis de Vulnerabilidades	Detección y mitigación de riesgos en sistemas.	7
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id_user, name, email, password, type_user, fecha_registro, profile_picture) FROM stdin;
1	Luisa Maria Santiago Siliceo	luisa.santiago98@unach.mx	hachi2024	Alumno	2025-03-29 14:00:04.802605	img/WhatsApp Image 2024-10-17 at 7.32.38 PM.jpeg
2	Alejandra Castellanos Cortez	alejandra.castellanos55@unach.mx	chocolate55	Alumno	2025-04-08 16:49:46.585945	/path/a/tu/imagen/WhatsApp Image 2025-04-08 at 4.49.18 PM.jpeg
\.


--
-- Name: files_repo_id_file_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.files_repo_id_file_seq', 1, true);


--
-- Name: subjects_id_materia_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.subjects_id_materia_seq', 6, true);


--
-- Name: users_id_user_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_user_seq', 2, true);


--
-- Name: files_repo files_repo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.files_repo
    ADD CONSTRAINT files_repo_pkey PRIMARY KEY (id_file);


--
-- Name: subjects subjects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subjects
    ADD CONSTRAINT subjects_pkey PRIMARY KEY (id_materia);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id_user);


--
-- Name: idx_files_repo_materia; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_files_repo_materia ON public.files_repo USING btree (id_materia);


--
-- Name: idx_files_repo_user; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_files_repo_user ON public.files_repo USING btree (id_user);


--
-- Name: files_repo files_repo_id_materia_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.files_repo
    ADD CONSTRAINT files_repo_id_materia_fkey FOREIGN KEY (id_materia) REFERENCES public.subjects(id_materia) ON DELETE CASCADE;


--
-- Name: files_repo files_repo_id_user_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.files_repo
    ADD CONSTRAINT files_repo_id_user_fkey FOREIGN KEY (id_user) REFERENCES public.users(id_user) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

