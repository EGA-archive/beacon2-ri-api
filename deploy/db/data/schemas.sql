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


---------------------------
------- V2.0 TABLES -------
---------------------------

-- Tables related to the services endpoint
-- Create tables
CREATE TABLE organization_table (
  id SERIAL NOT NULL PRIMARY KEY,
  stable_id text NOT NULL,
  name text,
  description text,
  address text,
  welcome_url text,
  contact_url text,
  logo_url text,
  info text
);

CREATE TABLE service_table (
  id SERIAL NOT NULL PRIMARY KEY,
  stable_id text NOT NULL,
  name text NOT NULL,
  service_type text NOT NULL,
  api_version text NOT NULL,
  service_url text NOT NULL,
  entry_point boolean NOT NULL,
  organization_id INT REFERENCES organization_table (id) NOT NULL,
  description text,
  version text,
  open boolean NOT NULL,
  welcome_url text,
  alternative_url  text,
  create_date_time timestamp(6) without time zone,
  update_date_time timestamp(6) without time zone
);


-- Insert mock data
INSERT INTO organization_table (stable_id, name, description, address, welcome_url, contact_url, logo_url, info) VALUES ('org.example', 'Org-Example', 'This is an example', '123 Street', 'welcome.com', 'contact@me', 'logo.com', 'extra_info');
INSERT INTO organization_table (stable_id, name, description, address, welcome_url, contact_url, logo_url, info) VALUES ('org.example2', 'Org-Example2', 'This is an example2', '321 Street', 'welcome2.com', 'contact2@me', 'logo2.com', 'extra_info2');


INSERT INTO service_table (stable_id, name, service_type, api_version, service_url, entry_point, organization_id, description, version, open, welcome_url, alternative_url, create_date_time, update_date_time) VALUES ('BA1', 'BA1', 'GA4GHBeaconAggregator', 'v1', 'BA1.com', true, '1', 'BA1 description', 'v2', true, 'BA1-welcome.com', 'BA1-alternative.com', '2019-09-26', '2019-09-26');
INSERT INTO service_table (stable_id, name, service_type, api_version, service_url, entry_point, organization_id, description, version, open, welcome_url, alternative_url, create_date_time, update_date_time) VALUES ('BA2', 'BA2', 'GA4GHBeaconAggregator', 'v1', 'BA2.com', true, '2', 'BA2 description', 'v2', true, 'BA2-welcome.com', 'BA2-alternative.com', '2019-09-26', '2019-09-26');
INSERT INTO service_table (stable_id, name, service_type, api_version, service_url, entry_point, organization_id, description, version, open, welcome_url, alternative_url, create_date_time, update_date_time) VALUES ('R1', 'R1', 'GA4GHRegistry', 'v1', 'R1.com', false, '1', 'R1 description', 'v2', true, 'R1-welcome.com', 'R1-alternative.com', '2019-09-26', '2019-09-26');

-- Create view
CREATE VIEW service AS
SELECT 
  s.id,
  s.stable_id as service_stable_id,
  s.name as service_name,
  s.service_type,
  s.api_version,
  s.service_url,
  s.entry_point,
  s.description as service_description,
  s.version,
  s.open,
  s.welcome_url as service_welcome_url,
  s.alternative_url,
  s.create_date_time,
  s.update_date_time,
  o.id as organization_id,
  o.stable_id as organization_stable_id,
  o.name as organization_name,
  o.description as organization_description,
  o.address,
  o.welcome_url as organization_welcome_url,
  o.contact_url,
  o.logo_url,
  o.info
  FROM service_table s
  JOIN organization_table o ON s.organization_id=o.id;

-- Add columns to beacon_sample_table
ALTER TABLE beacon_sample_table
ADD COLUMN sex text,
ADD COLUMN tissue text,
ADD COLUMN description text, 
ADD CONSTRAINT sex_constraint CHECK (LOWER(sex) = ANY(ARRAY['female'::text,'male'::text,'other'::text,'unknown'::text]));



-- Tables related to the samples endpoint
-- Create patient table
CREATE TABLE patient_table (
  id SERIAL NOT NULL PRIMARY KEY,
  stable_id text,
  sex text,
  age_of_onset int,
  disease text,
  CONSTRAINT sex_constraint CHECK (LOWER(sex) = ANY(ARRAY['female'::text,'male'::text,'other'::text,'unknown'::text]))
);

-- Add patient column to beacon_sample_table
ALTER TABLE public.beacon_sample_table
ADD COLUMN patient_id  INT REFERENCES patient_table (id);

-- Insert mock data into patient_table
INSERT INTO public.patient_table (stable_id, sex, age_of_onset, disease) VALUES ('patient1', 'female', '61', 'Lung cancer');
INSERT INTO public.patient_table (stable_id, sex, age_of_onset, disease) VALUES ('patient2', 'male', '70', 'Kidney cancer');
INSERT INTO public.patient_table (stable_id, sex, age_of_onset) VALUES ('patient3', 'female', '45');
INSERT INTO public.patient_table (stable_id, sex, age_of_onset, disease) VALUES ('patient4', 'male', '82', 'Hepatitis');
INSERT INTO public.patient_table (stable_id, sex, age_of_onset, disease) VALUES ('patient5', 'male', '65', 'Lung cancer');


-- Tables related to the access_levels endpoint
-- Create table
CREATE TABLE public.dataset_access_level_table (
    dataset_id integer REFERENCES public.beacon_dataset_table(id),
    parent_field text,
    field text,
    access_level text NOT NULL CHECK (access_level = ANY (ARRAY['NOT_SUPPORTED'::text, 'PUBLIC'::text, 'REGISTERED'::text, 'CONTROLLED'::text])),
    CONSTRAINT dataset_access_level_table_pkey PRIMARY KEY (dataset_id, parent_field, field)
);


-- Tables related to the filtering terms
-- Create table
CREATE TABLE public.ontology_term_table (
    id SERIAL NOT NULL PRIMARY KEY,
    ontology text NOT NULL,
    term text NOT NULL,
    target_table text NOT NULL,
    column_name text NOT NULL,
    column_value text,
    additional_comments text,
    label text
);

-- Insert mock data
INSERT INTO public.ontology_term_table (id, ontology, term, target_table, column_name, column_value, additional_comments, label) VALUES 
  (1,E'sex',E'1',E'public.beacon_sample_table',E'sex',E'female',NULL,E'Female'),
  (2,E'sex',E'2',E'public.beacon_sample_table',E'sex',E'male',NULL,E'Male'),
  (3,E'tissue',E'1',E'public.beacon_sample_table',E'tissue',E'liver',NULL,E'Liver sample'),
  (4,E'tissue',E'2',E'public.beacon_sample_table',E'tissue',E'lung',NULL,E'Lung sample'),
  (5,E'tissue',E'3',E'public.beacon_sample_table',E'tissue',E'kidney',NULL,E'Kidney sample'),
  (6,E'disease',E'1',E'public.patient_table',E'disease',E'lung cancer',NULL,E'Lung cancer'),
  (7,E'disease',E'2',E'public.patient_table',E'disease',E'kidney cancer',NULL,E'Kidney cancer'),
  (8,E'disease',E'3',E'public.patient_table',E'disease',E'hepatitis',NULL,E'Hepatitis'),
  (9,E'GO',E'0030237',E'public.beacon_sample_table',E'sex',E'female',NULL,E'Female'),
  (10,E'GO',E'0030238',E'public.beacon_sample_table',E'sex',E'male',NULL,E'Male'),
  (11,E'HPO',E'0009726',E'public.patient_table',E'disease',E'kidney cancer',NULL,E'Kidney cancer'),
  (12,E'HPO',E'0100526',E'public.patient_table',E'disease',E'lung cancer',NULL,E'Lung cancer'),
  (13,E'HPO',E'0012115',E'public.patient_table',E'disease',E'hepatitis',NULL,E'Hepatitis');

-- Create views
CREATE VIEW public.ontology_term_column_correspondance AS
SELECT id, ontology, term, target_table, column_name, column_value, additional_comments FROM public.ontology_term_table;

CREATE VIEW public.ontology_term AS
SELECT id, ontology, term, label FROM public.ontology_term_table;
