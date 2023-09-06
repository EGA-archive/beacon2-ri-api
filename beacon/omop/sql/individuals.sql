
-- name: sql_get_individuals
-- Get individuals
SELECT person_id
FROM cdm.person
LIMIT :limit
OFFSET :offset

-- name: cohort_individuals
-- Get individuals
SELECT subject_id as person_id
FROM cdm.cohort
where cohort_definition_id = :cohort_id
LIMIT :limit
OFFSET :offset

-- name: count_cohort_individuals$
-- Get individuals count
SELECT count(*)
FROM cdm.cohort
where cohort_definition_id = :cohort_id

-- name: count_individuals$
-- Get individuals count
SELECT count(*)
FROM cdm.person

-- name: sql_get_individual_id^
-- Get individual by id
SELECT DISTINCT person_id
FROM cdm.person
WHERE person_id = :person_id

-- name: sql_get_person
-- Get gender and race by id
SELECT gender_concept_id, race_concept_id
FROM cdm.person
WHERE person_id = :person_id

-- name: sql_get_condition
-- Get condition properties by id
SELECT condition_concept_id,
    extract(Year from age(condition_start_date, birth_datetime)) condition_ageOfOnset
FROM cdm.person as p,
    cdm.condition_occurrence as c
WHERE p.person_id = :person_id and p.person_id = c.person_id

-- name: sql_get_procedure
-- Get procedure properties by id
SELECT procedure_concept_id,
    extract(Year from age(procedure_date, birth_datetime)) procedure_ageOfOnset,
    to_char(procedure_date, 'YYYY-MM-DD')
FROM cdm.person as p,
    cdm.procedure_occurrence as c
WHERE p.person_id = :person_id and p.person_id=c.person_id

-- name: sql_get_measure
-- Get measure properties by id
Select measurement_concept_id,
    extract(Year from age(measurement_date, birth_datetime)) measurement_ageOfOnset,
    to_char(measurement_date, 'YYYY-MM-DD'),
    unit_concept_id,
    value_source_value
FROM cdm.person as p,
    cdm.measurement c
WHERE p.person_id = :person_id and p.person_id=c.person_id

-- name: sql_get_exposure
-- Get exposure properties by id
Select observation_concept_id,
    extract(Year from age(observation_date, birth_datetime)) observation_ageOfOnset,
    to_char(observation_date, 'YYYY-MM-DD')
FROM cdm.person as p,
    cdm.observation c
WHERE p.person_id = :person_id and p.person_id=c.person_id

-- name: sql_get_descendants
-- Get descendants from concept_id
SELECT descendant_concept_id
FROM vocabularies.concept_ancestor 
WHERE ancestor_concept_id = :concept_id

-- name: sql_get_concept_domain
-- Get OMOP concept_id and domain of the concept
SELECT concept_id, domain_id
FROM vocabularies.concept
WHERE vocabulary_id = :vocabulary_id and concept_code = :concept_code

-- name: sql_get_ontology^
-- Get ontology 
SELECT concept_name as label,
    vocabulary_id || ':' || concept_code as id
FROM vocabularies.concept 
WHERE concept_id = :concept_id

-- name: sql_filtering_terms_race_gender
-- Get all the race and gender filtering terms for individual
select distinct CONCAT(vocabulary_id,':',concept_code) as uri, c.concept_name
from vocabularies.concept as c
join cdm.person as p on p.race_concept_id=c.concept_id or p.gender_concept_id=c.concept_id

-- name: sql_filtering_terms_condition
-- Get all the condition_occurrence filtering terms for individual
select distinct CONCAT(vocabulary_id,':',concept_code) as uri, c.concept_name
from vocabularies.concept as c
join cdm.condition_occurrence as con on con.condition_occurrence_id=c.concept_id

-- name: sql_filtering_terms_measurement
-- Get all the measurement filtering terms for individual
select distinct CONCAT(vocabulary_id,':',concept_code) as uri, c.concept_name
from vocabularies.concept as c
join cdm.measurement as con on con.measurement_concept_id=c.concept_id

-- name: sql_filtering_terms_procedure
-- Get all the procedure_occurrence filtering terms for individual
select distinct CONCAT(vocabulary_id,':',concept_code) as uri, c.concept_name
from vocabularies.concept as c
join cdm.procedure_occurrence as con on con.procedure_concept_id=c.concept_id

-- name: sql_filtering_terms_observation
-- Get all the observation filtering terms for individual
select distinct CONCAT(vocabulary_id,':',concept_code) as uri, c.concept_name
from vocabularies.concept as c
join cdm.observation as con on con.observation_concept_id=c.concept_id
