DROP VIEW IF EXISTS public.beacon_data_summary;
DROP VIEW IF EXISTS public.beacon_dataset;
DROP VIEW IF EXISTS public.beacon_dataset_consent_code;
DROP TABLE IF EXISTS public.beacon_dataset_consent_code_table CASCADE;
DROP TABLE IF EXISTS public.consent_code_table;
DROP TABLE IF EXISTS public.consent_code_category_table;
DROP TABLE IF EXISTS public.tmp_data_sample_table;
DROP TABLE IF EXISTS public.tmp_sample_table;
DROP TABLE IF EXISTS public.beacon_data_sample_table CASCADE;
DROP TABLE IF EXISTS public.beacon_dataset_sample_table CASCADE;
DROP TABLE IF EXISTS public.beacon_data_table;
DROP TABLE IF EXISTS public.beacon_sample_table;
DROP TABLE IF EXISTS public.beacon_dataset_table;

CREATE TABLE public.beacon_dataset_table
(
    id SERIAL NOT NULL PRIMARY KEY,
    stable_id character varying(50) NOT NULL,
    description character varying(800),
    access_type character varying(10),
    reference_genome character varying(50),
    variant_cnt bigint NOT NULL,
    call_cnt bigint,
    sample_cnt bigint NOT NULL,
    CONSTRAINT beacon_dataset_table_access_type_check CHECK (access_type = ANY (ARRAY['PUBLIC', 'REGISTERED', 'CONTROLLED']))
);

CREATE TABLE public.beacon_data_table (
    id SERIAL NOT NULL PRIMARY KEY,
    dataset_id integer NOT NULL REFERENCES public.beacon_dataset_table (id),
    chromosome character varying(2) NOT NULL,
    variant_id text,
    reference text NOT NULL,
    alternate text NOT NULL,
    start integer NOT NULL,
    "end" integer,
    type character varying(10),
    sv_length integer,
    variant_cnt integer,
    call_cnt integer,
    sample_cnt integer,
	matching_sample_cnt integer,
    frequency decimal

);

CREATE TABLE public.beacon_sample_table (
	id serial NOT NULL PRIMARY KEY,
	stable_id text NOT NULL
);

CREATE TABLE public.beacon_dataset_sample_table (
	id serial NOT NULL PRIMARY KEY,
	dataset_id int NOT NULL REFERENCES beacon_dataset_table(id),
	sample_id int NOT NULL REFERENCES beacon_sample_table(id),
	UNIQUE (dataset_id, sample_id)
);

CREATE TABLE public.beacon_data_sample_table (
	data_id int NOT NULL REFERENCES beacon_data_table(id),
	sample_id int NOT NULL REFERENCES beacon_sample_table(id),
	PRIMARY KEY (data_id, sample_id)
);

-- Temporary table for loading data into beacon_data_sample_table
CREATE TABLE public.tmp_data_sample_table (
  dataset_id integer NOT NULL REFERENCES public.beacon_dataset_table (id),
  chromosome character varying(2) NOT NULL,
  variant_id text,
  reference text NOT NULL,
  alternate text NOT NULL,
  start integer NOT NULL,
  type character varying(10),
  sample_ids text ARRAY[4] NOT NULL
);

CREATE TABLE tmp_sample_table (
  id serial NOT NULL,
	sample_stable_id text NOT NULL,
	dataset_id int NOT NULL REFERENCES beacon_dataset_table(id)
);

-----------------------------------
---------- CONSENT CODES ----------
-----------------------------------
CREATE TABLE consent_code_category_table (
	id serial PRIMARY KEY,
	name character varying(11)
);

INSERT INTO consent_code_category_table(name) VALUES ('PRIMARY');
INSERT INTO consent_code_category_table(name) VALUES ('SECONDARY');
INSERT INTO consent_code_category_table(name) VALUES ('REQUIREMENT');



CREATE TABLE consent_code_table (
	id serial PRIMARY KEY,
	name character varying(100) NOT NULL,
	abbr character varying(20) NOT NULL,
	description character varying(400) NOT NULL,
	additional_constraint_required boolean NOT NULL,
	category_id int NOT NULL REFERENCES consent_code_category_table(id)
);


INSERT INTO consent_code_table(name, abbr, description, additional_constraint_required, category_id) VALUES ('No restrictions', 'NRES', 'No restrictions on data use.', false, 1);
INSERT INTO consent_code_table(name, abbr, description, additional_constraint_required, category_id) VALUES ('General research use and clinical care', 'GRU(CC)', 'For health/medical/biomedical purposes, including the study of population origins or ancestry.', false, 1);
INSERT INTO consent_code_table(name, abbr, description, additional_constraint_required, category_id) VALUES ('Health/medical/biomedical research and clinical care', 'HMB(CC)', 'Use of the data is limited to health/medical/biomedical purposes; does not include the study of population origins or ancestry.', false, 1);
INSERT INTO consent_code_table(name, abbr, description, additional_constraint_required, category_id) VALUES ('Disease-specific research and clinical care', 'DS-[XX](CC)', 'Use of the data must be related to [disease].', true, 1);
INSERT INTO consent_code_table(name, abbr, description, additional_constraint_required, category_id) VALUES ('Population origins/ancestry research', 'POA', 'Use of the data is limited to the study of population origins or ancestry.', false, 1);
INSERT INTO consent_code_table(name, abbr, description, additional_constraint_required, category_id) VALUES ('Oher research-specific restrictions', 'RS-[XX]', 'Use of the data is limited to studies of [research type] (e.g., pediatric research).', true, 2);
INSERT INTO consent_code_table(name, abbr, description, additional_constraint_required, category_id) VALUES ('Research use only', 'RUO', 'Use of data is limited to research purposes (e.g., does not include its use in clinical care).', false, 2);
INSERT INTO consent_code_table(name, abbr, description, additional_constraint_required, category_id) VALUES ('No “general methods” research', 'NMDS', 'Use of the data includes methods development research (e.g., development of software or algorithms) ONLY within the bounds of other data use limitations.', false, 2);
INSERT INTO consent_code_table(name, abbr, description, additional_constraint_required, category_id) VALUES ('Genetic studies only', 'GSO', 'Use of the data is limited to genetic studies only (i.e., no “phenotype-only” research).', false, 2);
INSERT INTO consent_code_table(name, abbr, description, additional_constraint_required, category_id) VALUES ('Not-for-profit use only', 'NPU', 'Use of the data is limited to not-for-profit organizations.', false, 3);
INSERT INTO consent_code_table(name, abbr, description, additional_constraint_required, category_id) VALUES ('Publication required', 'PUB', 'Requestor agrees to make results of studies using the data available to the larger scientific community.', false, 3);
INSERT INTO consent_code_table(name, abbr, description, additional_constraint_required, category_id) VALUES ('Collaboration required', 'COL-[XX]', 'Requestor must agree to collaboration with the primary study investigator(s).', true, 3);
INSERT INTO consent_code_table(name, abbr, description, additional_constraint_required, category_id) VALUES ('Ethics approval required', 'IRB', 'Requestor must provide documentation of local IRB/REC approval.', false, 3);
INSERT INTO consent_code_table(name, abbr, description, additional_constraint_required, category_id) VALUES ('Geographical restrictions', 'GS-[XX]', 'Use of the data is limited to within [geographic region].', true, 3);
INSERT INTO consent_code_table(name, abbr, description, additional_constraint_required, category_id) VALUES ('Publication moratorium/embargo', 'MOR-[XX]', 'Requestor agrees not to publish results of studies until [date].', true, 3);
INSERT INTO consent_code_table(name, abbr, description, additional_constraint_required, category_id) VALUES ('Time limits on use', 'TS-[XX]', 'Use of data is approved for [x months].', true, 3);
INSERT INTO consent_code_table(name, abbr, description, additional_constraint_required, category_id) VALUES ('User-specific restrictions', 'US', 'Use of data is limited to use by approved users.', false, 3);
INSERT INTO consent_code_table(name, abbr, description, additional_constraint_required, category_id) VALUES ('Project-specific restrictions', 'PS', 'Use of data is limited to use within an approved project.', false, 3);
INSERT INTO consent_code_table(name, abbr, description, additional_constraint_required, category_id) VALUES ('Institution-specific restrictions', 'IS', 'Use of data is limited to use within an approved institution.', false, 3);



CREATE TABLE beacon_dataset_consent_code_table (
	dataset_id integer NOT NULL REFERENCES beacon_dataset_table(id),
	consent_code_id int NOT NULL REFERENCES consent_code_table(id),
	additional_constraint text,
	description text,
	version text,
	PRIMARY KEY (dataset_id, consent_code_id)
);

---------------------------
---------- VIEWS ----------
---------------------------
-- DROP VIEW public.beacon_data_summary;
CREATE OR REPLACE VIEW public.beacon_data_summary AS
SELECT dat.id AS dataset_id,
	d.variant_cnt,
	d.call_cnt,
	d.sample_cnt,
	COALESCE(COUNT(DISTINCT d_sam.sample_id),NULL) AS matching_sample_cnt,
	d.frequency
FROM beacon_data_table d
INNER JOIN beacon_dataset_table dat ON dat.id = d.dataset_id
LEFT JOIN beacon_data_sample_table d_sam ON d_sam.data_id=d.id
GROUP BY dat.id, d.variant_cnt, d.call_cnt, d.sample_cnt, d.frequency;

CREATE OR REPLACE VIEW beacon_dataset AS
SELECT
	d.id,
	d.stable_id,
	d.description,
	d.access_type,
	d.reference_genome,
	d.variant_cnt,
	d.call_cnt,
	d.sample_cnt
FROM beacon_dataset_table d
WHERE (d.access_type = ANY (ARRAY['PUBLIC', 'REGISTERED', 'CONTROLLED']))
AND d.variant_cnt > 0 AND d.reference_genome != '';

CREATE OR REPLACE VIEW beacon_dataset_consent_code AS
SELECT dc.dataset_id,
	cat.name AS category,
    code.abbr AS code,
    code.description AS description,
	dc.additional_constraint,
    dc.description AS additional_description,
    dc.version
FROM beacon_dataset_consent_code_table dc
INNER JOIN consent_code_table code ON code.id=dc.consent_code_id
INNER JOIN consent_code_category_table cat ON cat.id=code.category_id
ORDER BY dc.dataset_id, cat.id, code.id;
