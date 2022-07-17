--
-- PostgreSQL database dump
--

-- Dumped from database version 12.9 (Ubuntu 12.9-0ubuntu0.20.04.1)
-- Dumped by pg_dump version 12.9 (Ubuntu 12.9-0ubuntu0.20.04.1)

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

--
-- Name: adminpack; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS adminpack WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION adminpack; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION adminpack IS 'administrative functions for PostgreSQL';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.history (
    id bigint NOT NULL,
    from_id bigint NOT NULL,
    to_id bigint NOT NULL,
    from_word_id bigint NOT NULL,
    to_word_id bigint NOT NULL,
    send_time timestamp with time zone NOT NULL
);


ALTER TABLE public.history OWNER TO postgres;

--
-- Name: history_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.history ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: ignore; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ignore (
    id bigint NOT NULL,
    string_text character varying NOT NULL,
    replace character varying,
    node_id bigint NOT NULL,
    ignore boolean NOT NULL
);


ALTER TABLE public.ignore OWNER TO postgres;

--
-- Name: ignore_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.ignore ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.ignore_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: nodes; Type: TABLE; Schema: public; Owner: tg_parser_server
--

CREATE TABLE public.nodes (
    id bigint NOT NULL,
    node_name character varying NOT NULL
);


ALTER TABLE public.nodes OWNER TO tg_parser_server;

--
-- Name: nodes_id_seq; Type: SEQUENCE; Schema: public; Owner: tg_parser_server
--

ALTER TABLE public.nodes ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.nodes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: recipients; Type: TABLE; Schema: public; Owner: tg_parser_server
--

CREATE TABLE public.recipients (
    id bigint NOT NULL,
    tg_id bigint NOT NULL,
    tg_name character varying NOT NULL,
    node_id bigint NOT NULL
);


ALTER TABLE public.recipients OWNER TO tg_parser_server;

--
-- Name: recipients_id_seq; Type: SEQUENCE; Schema: public; Owner: tg_parser_server
--

ALTER TABLE public.recipients ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.recipients_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: sources; Type: TABLE; Schema: public; Owner: tg_parser_server
--

CREATE TABLE public.sources (
    id bigint NOT NULL,
    tg_id bigint,
    tg_name character varying NOT NULL,
    node_id bigint NOT NULL
);


ALTER TABLE public.sources OWNER TO tg_parser_server;

--
-- Name: sources_id_seq; Type: SEQUENCE; Schema: public; Owner: tg_parser_server
--

ALTER TABLE public.sources ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.sources_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: history history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.history
    ADD CONSTRAINT history_pkey PRIMARY KEY (id);


--
-- Name: ignore ignore_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ignore
    ADD CONSTRAINT ignore_pkey PRIMARY KEY (id);


--
-- Name: nodes node_name; Type: CONSTRAINT; Schema: public; Owner: tg_parser_server
--

ALTER TABLE ONLY public.nodes
    ADD CONSTRAINT node_name UNIQUE (node_name);


--
-- Name: nodes nodes_pkey; Type: CONSTRAINT; Schema: public; Owner: tg_parser_server
--

ALTER TABLE ONLY public.nodes
    ADD CONSTRAINT nodes_pkey PRIMARY KEY (id);


--
-- Name: recipients recipients_pkey; Type: CONSTRAINT; Schema: public; Owner: tg_parser_server
--

ALTER TABLE ONLY public.recipients
    ADD CONSTRAINT recipients_pkey PRIMARY KEY (id);


--
-- Name: sources sources_pkey; Type: CONSTRAINT; Schema: public; Owner: tg_parser_server
--

ALTER TABLE ONLY public.sources
    ADD CONSTRAINT sources_pkey PRIMARY KEY (id);


--
-- Name: recipients node_id; Type: FK CONSTRAINT; Schema: public; Owner: tg_parser_server
--

ALTER TABLE ONLY public.recipients
    ADD CONSTRAINT node_id FOREIGN KEY (node_id) REFERENCES public.nodes(id) NOT VALID;


--
-- Name: sources node_id; Type: FK CONSTRAINT; Schema: public; Owner: tg_parser_server
--

ALTER TABLE ONLY public.sources
    ADD CONSTRAINT node_id FOREIGN KEY (node_id) REFERENCES public.nodes(id) NOT VALID;


--
-- Name: ignore node_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ignore
    ADD CONSTRAINT node_id FOREIGN KEY (node_id) REFERENCES public.nodes(id);


--
-- PostgreSQL database dump complete
--

