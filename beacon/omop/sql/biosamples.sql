
-- name: sql_get_biosamples
-- Get biosamples
SELECT specimen_id
FROM cdm.specimen
LIMIT :limit
OFFSET :offset

-- name: sql_get_biosample_id^
-- Get biosample by id
SELECT DISTINCT specimen_id
FROM cdm.specimen
WHERE specimen_id = :specimen_id

-- name: get_count_specimen$
-- Get specimen count
SELECT count(*)
FROM cdm.specimen

-- name: sql_get_specimen
-- Get gender and race by id
SELECT person_id, disease_status_concept_id, anatomic_site_concept_id,
    specimen_date::text, specimen_datetime::text
FROM cdm.specimen
WHERE specimen_id = :specimen_id


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


-- name: sql_filtering_terms_biosample
-- Get all the observation filtering terms for individual
select distinct CONCAT(vocabulary_id,':',concept_code) as uri, c.concept_name
from vocabularies.concept as c
join cdm.specimen as con
    on con.disease_status_concept_id=c.concept_id or con.anatomic_site_concept_id=c.concept_id