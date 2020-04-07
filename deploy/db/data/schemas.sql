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

-- updated table for v2
-- the patient_id reference will be included after creting the patient_table
CREATE TABLE public.beacon_sample_table(
    id serial NOT NULL,
    stable_id text NOT NULL,
    -- patient_id integer REFERENCES public.patient_table(id),
    description text,
    biosample_status text,
    individual_age_at_collection_age text,
    individual_age_at_collection_age_group text,
    organ text,
    tissue text,
    cell_type text,
    obtention_procedure text,
    tumor_progression text,
    tumor_grade text,
    CONSTRAINT beacon_sample_table_pkey PRIMARY KEY (id),
    CONSTRAINT sample_unique UNIQUE (stable_id)
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


-- Tables related to the samples/individuals endpoints
-- Create patient table
CREATE TABLE public.patient_table
(
    id serial NOT NULL,
    stable_id text NOT NULL UNIQUE,
    sex text NOT NULL,
    ethnicity text,
    geographic_origin text,
    CONSTRAINT patient_table_pkey PRIMARY KEY (id),
    CONSTRAINT sex_constraint CHECK (lower(sex) = ANY (ARRAY['female'::text, 'male'::text, 'other'::text, 'unknown'::text]))
);

CREATE TABLE public.patient_disease_table(
    id serial NOT NULL PRIMARY KEY,
    patient_id integer NOT NULL REFERENCES public.patient_table(id),
    disease text NOT NULL,
    age text,
    age_group text,
    stage text NOT NULL,
    family_history boolean NOT NULL
);

CREATE TABLE public.pedigree_table(
    id serial NOT NULL PRIMARY KEY,
	stable_id text NOT NULL UNIQUE,
    description text NOT NULL
);

CREATE TABLE public.patient_pedigree_table(
    patient_id integer NOT NULL REFERENCES public.patient_table(id),
    pedigree_id integer NOT NULL REFERENCES public.pedigree_table(id),
    pedigree_role text NOT NULL,
    number_of_individuals_tested integer,
    disease text NOT NULL,
    PRIMARY KEY (patient_id, pedigree_id)
);

-- Add patient column to beacon_sample_table
ALTER TABLE public.beacon_sample_table
ADD COLUMN patient_id integer REFERENCES public.patient_table(id);

-- START Insert mock data

-- Latin American NCIT:C126531
-- European NCIT:C43851
-- African NCIT: C42331 
-- United States of America GAZ:00002459
-- Spain GAZ:00000591
-- Egypt GAZ:00003934
-- Democratic Republic of the Congo GAZ:00001086
INSERT INTO public.patient_table (id, stable_id, sex, ethnicity, geographic_origin) VALUES 
(1, 'patient1', 'female', 'Latin American', 'United States of America'),
(2, 'patient2', 'male', 'European', 'United States of America'),
(3, 'patient3', 'female', 'European', 'Spain'),
(4, 'patient4', 'male', 'African', 'Egypt'),
(5, 'patient5', 'male', 'African', 'Democratic Republic of the Congo');

-- Parkinson HP:0001300
-- Alzheimer HP:0002511
-- Lactose intolerance HP:0004789
-- Adolescent NCIT:C27954
-- Adult NCIT:C17600
-- Acute onset OGMS:0000119
INSERT INTO public.patient_disease_table (patient_id, disease, age, age_group, stage, family_history) VALUES
(1, 'Lactose intolerance', 'P12Y5M1D', 'Adolescent', 'Acute onset', false),
(1, 'Lactose intolerance', 'P12Y5M1D', 'Adolescent', 'Acute onset', true),
(2, 'Lactose intolerance', 'P25Y9M18D', 'Adult', 'Acute onset', false),
(3, 'Parkinson', 'P56Y2M26D', 'Adult', 'Acute onset', false),
(4, 'Alzheimer', 'P72Y6M11D', 'Adult', 'Acute onset', false);

INSERT INTO public.pedigree_table (id, stable_id, description) VALUES (1, 'PED001', 'Some pedigree');

-- identical twin relationship ERO:0002041
INSERT INTO public.patient_pedigree_table(patient_id, pedigree_id, pedigree_role, number_of_individuals_tested, disease) VALUES 
(1,1, 'identical twin relationship', 2, 'Lactose intolerance');

-- updates on the beacon_sample_table are done in updates.sql

-- END Insert mock data


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
    label text,
    target_table_alias text NOT NULL
);

-- Insert mock data
INSERT INTO public.ontology_term_table(ontology, term, label, target_table, column_name, column_value, target_table_alias) VALUES
-- patient_table
('NCIT','C17998','unknown','public.patient_table','sex','unknown','pat'),
('NCIT','C46113','female','public.patient_table','sex','female','pat'),
('NCIT','C46112','male','public.patient_table','sex','male','pat'),
('NCIT','C45908','other','public.patient_table','sex','other','pat'),
('NCIT','C126531','Latin American','public.patient_table','ethnicity','Latin American','pat'),
('NCIT','C43851','European','public.patient_table','ethnicity','European','pat'),
('NCIT','C42331','African','public.patient_table','ethnicity','African','pat'),
('GAZ','00002459','United States of America','public.patient_table','geographic_origin','United States of America','pat'),
('GAZ','00000591','Spain','public.patient_table','geogra
phic_origin','Spain','pat'),
('GAZ','00003934','Egypt','public.patient_table','geographic_origin','Egypt','pat'),
('GAZ','00001086','Democratic Republic of the Congo','public.patient_table','geographic_origin','Democratic Republic of the Congo','pat'),
-- patient_disease_table
('NCIT','C27954','Adolescent','public.patient_disease_table','age_group','Adolescent','pat_dis'),
('NCIT','C17600','Adult','public.patient_disease_table','age_group','Adult','pat_dis'),
('HP','0001300','Parkinson','public.patient_disease_table','disease','Parkinson','pat_dis'),
('HP','0002511','Alzheimer','public.patient_disease_table','disease','Alzheimer','pat_dis'),
('HP','0004789','Lactose intolerance','public.patient_disease_table','disease','Lactose intolerance','pat_dis'),
('OGMS','0000119','Acute onset','public.patient_disease_table','stage','Acute onset','pat_dis'),
-- patient_pedigree_table
('ERO','0002041','identical twin relationship','public.patient_pedigree_table','pedigree_role','identical twin relationship','pat_ped'),
('HP','0001300','Parkinson','public.patient_pedigree_table','disease','Parkinson','pat_ped'),
('HP','0002511','Alzheimer','public.patient_pedigree_table','disease','Alzheimer','pat_ped'),
('HP','0004789','Lactose intolerance','public.patient_pedigree_table','disease','Lactose intolerance','pat_ped'),
-- beacon_sample_table
('NCIT','C15189','biopsy','public.beacon_sample_table','obtention_procedure','biopsy','sam'),
('NCIT','C84509','Primary Malignant Neoplasm','public.beacon_sample_table','tumor_progression','Primary Malignant Neoplasm','sam'),
('EFO','0009655','abnormal sample','public.beacon_sample_table','biosample_status','abnormal sample','sam'),
('UBERON','0002107','liver','public.beacon_sample_table','organ','liver','sam'),
('UBERON','0001281','hepatic sinusoid','public.beacon_sample_table','tissue','hepatic sinusoid','sam'),
('CL','0000091','Kupffer cell','public.beacon_sample_table','cell_type','Kupffer cell','sam'),
('MONDO','0024492','tumor grade 2, general grading system','public.beacon_sample_table','tumor_grade','tumor grade 2, general grading system','sam'),
('NCIT','C27954','Adolescent','public.beacon_sample_table','individual_age_at_collection_age_group','Adolescent','sam'),
('NCIT','C17600','Adult','public.beacon_sample_table','individual_age_at_collection_age_group','Adult','sam')
;

-- Create views
CREATE VIEW public.ontology_term_column_correspondance AS
SELECT id, ontology, term, target_table, column_name, column_value, additional_comments FROM public.ontology_term_table;

CREATE OR REPLACE VIEW public.ontology_term AS
SELECT * FROM public.ontology_term_table;

CREATE OR REPLACE VIEW public.patient AS
SELECT * FROM public.patient_table;

-- DROP VIEW public.patient_w_ontology_terms;
CREATE OR REPLACE VIEW public.patient_w_ontology_terms AS
SELECT pat.id, 
	pat.stable_id, 
	pat.sex, 
	CASE WHEN ot_sex.id IS NOT NULL THEN ot_sex.ontology || ':' || ot_sex.term ELSE null::text END AS sex_ontology,
	pat.ethnicity, 
	CASE WHEN ot_ethnicity.id IS NOT NULL THEN ot_ethnicity.ontology || ':' || ot_ethnicity.term ELSE null::text END AS ethnicity_ontology,
	pat.geographic_origin,
	CASE WHEN ot_geo_origin.id IS NOT NULL THEN ot_geo_origin.ontology || ':' || ot_geo_origin.term ELSE null::text END AS geographic_origin_ontology
FROM public.patient_table pat
LEFT JOIN public.ontology_term ot_sex ON ot_sex.target_table='public.patient_table' AND ot_sex.column_name='sex' AND lower(ot_sex.column_value)=lower(pat.sex)
LEFT JOIN public.ontology_term ot_ethnicity ON ot_ethnicity.target_table='public.patient_table' AND ot_ethnicity.column_name='ethnicity' AND lower(ot_ethnicity.column_value)=lower(pat.ethnicity)
LEFT JOIN public.ontology_term ot_geo_origin ON ot_geo_origin.target_table='public.patient_table' AND ot_geo_origin.column_name='geographic_origin' AND lower(ot_geo_origin.column_value)=lower(pat.geographic_origin)
;

-- DROP VIEW public.patient_pedigree_w_ontology_terms;
CREATE OR REPLACE VIEW public.patient_pedigree_w_ontology_terms AS
SELECT pat_ped.patient_id, 
	pat_ped.pedigree_id, 
	pat_ped.pedigree_role, 
	CASE WHEN ot_role.id IS NOT NULL THEN ot_role.ontology || ':' || ot_role.term ELSE null::text END AS pedigree_role_ontology,
	pat_ped.number_of_individuals_tested, 
	pat_ped.disease,
	CASE WHEN ot_disease.id IS NOT NULL THEN ot_disease.ontology || ':' || ot_disease.term ELSE null::text END AS disease_ontology
FROM public.patient_pedigree_table pat_ped
LEFT JOIN public.ontology_term ot_role ON ot_role.target_table='public.patient_pedigree_table' AND ot_role.column_name='pedigree_role' AND lower(ot_role.column_value)=lower(pat_ped.pedigree_role)
LEFT JOIN public.ontology_term ot_disease ON ot_disease.target_table='public.patient_pedigree_table' AND ot_disease.column_name='disease' AND lower(ot_disease.column_value)=lower(pat_ped.disease)
;

CREATE OR REPLACE VIEW public.patient_disease_w_ontology_terms AS
SELECT pat_dis.id, 
	pat_dis.patient_id, 
	pat_dis.disease, 
	CASE WHEN ot_disease.id IS NOT NULL THEN ot_disease.ontology || ':' || ot_disease.term ELSE null::text END AS disease_ontology,
	pat_dis.age, 
	pat_dis.age_group, 
	CASE WHEN ot_age_group.id IS NOT NULL THEN ot_age_group.ontology || ':' || ot_age_group.term ELSE null::text END AS age_group_ontology,
	pat_dis.stage, 
	CASE WHEN ot_stage.id IS NOT NULL THEN ot_stage.ontology || ':' || ot_stage.term ELSE null::text END AS stage_ontology,
	pat_dis.family_history
FROM public.patient_disease_table pat_dis
LEFT JOIN public.ontology_term ot_disease ON ot_disease.target_table='public.patient_disease_table' AND ot_disease.column_name='disease' AND lower(ot_disease.column_value)=lower(pat_dis.disease)
LEFT JOIN public.ontology_term ot_age_group ON ot_age_group.target_table='public.patient_disease_table' AND ot_age_group.column_name='age_group' AND lower(ot_age_group.column_value)=lower(pat_dis.age_group)
LEFT JOIN public.ontology_term ot_stage ON ot_stage.target_table='public.patient_disease_table' AND ot_stage.column_name='stage' AND lower(ot_stage.column_value)=lower(pat_dis.stage)
;