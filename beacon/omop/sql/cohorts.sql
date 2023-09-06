-- name: get_cohort_count$
-- Get gender count
select count(*)
from cdm.person p

-- name: get_age_range^
-- Get age min-max
select min(date_part('year', age( now(), p.birth_datetime)))::int min_age, max(date_part('year', age( now(), p.birth_datetime)))::int max_age
from cdm.person p

-- name: get_gender_count
-- Get gender count
select c.concept_name, count(*)
from cdm.person p
inner join vocabularies.concept c on c.concept_id = p.gender_concept_id
group by concept_name

-- name: get_achilles_gender_count
-- Get gender count
select aa.analysis_name, c.vocabulary_id, c.concept_code, c.concept_name, ar.count_value
from achilles_analysis aa
inner join achilles_results ar on aa.analysis_id = ar.analysis_id
inner join vocabularies.concept c on c.concept_id = ar.stratum_1::int
where aa.analysis_id = 2

-- name: get_year_of_birth_count
-- Get year_of_birth count
select p.year_of_birth, count(*)
from cdm.person p
group by p.year_of_birth
order by year_of_birth

-- name: get_achilles_year_of_birth_count
-- Get year_of_birth count
select aa.analysis_name, aa.stratum_1_name, ar.stratum_1, ar.count_value
from achilles_analysis aa
inner join achilles_results ar on aa.analysis_id = ar.analysis_id
where aa.analysis_id = 3

-- name: get_condition_count
-- Get condtion concept count
select c.concept_code, c.vocabulary_id, concept_name, count(distinct person_id) count_value
from cdm.condition_occurrence co
inner join vocabularies.concept c on c.concept_id = co.condition_concept_id
group by c.concept_code, c.vocabulary_id, concept_name
order by count_value desc

-- name: get_achilles_condition_count
-- Get condtion concept count
select aa.analysis_name, c.vocabulary_id, c.concept_code, c.concept_name, ar.count_value
from achilles_analysis aa
inner join achilles_results ar on aa.analysis_id = ar.analysis_id
inner join vocabularies.concept c on c.concept_id = ar.stratum_1::int
where aa.analysis_id = 400
order by count_value desc

-- name: get_procedure_count
-- Get procedure concept count
select c.concept_code, c.vocabulary_id, concept_name, count(distinct person_id) count_value
from cdm.procedure_occurrence po
inner join vocabularies.concept c on c.concept_id = po.procedure_concept_id
group by c.concept_code, c.vocabulary_id, concept_name
order by count_value desc


-- name: get_achilles_procedure_count
-- Get procedure concept count
select aa.analysis_name, c.vocabulary_id, c.concept_code, c.concept_name, ar.count_value
from achilles_analysis aa
inner join achilles_results ar on aa.analysis_id = ar.analysis_id
inner join vocabularies.concept c on c.concept_id = ar.stratum_1::int
where aa.analysis_id = 600
order by count_value desc

-- name: get_drug_count
-- Get drug concept count
select c.concept_code, c.vocabulary_id, concept_name, count(distinct person_id) count_value
from cdm.drug_exposure de
inner join vocabularies.concept c on c.concept_id = de.drug_concept_id
group by c.concept_code, c.vocabulary_id, concept_name
order by count_value desc

-- name: get_achilles_drug_count
-- Get drug concept count
select aa.analysis_name, c.vocabulary_id, c.concept_code, c.concept_name, ar.count_value
from achilles_analysis aa
inner join achilles_results ar on aa.analysis_id = ar.analysis_id
inner join vocabularies.concept c on c.concept_id = ar.stratum_1::int
where aa.analysis_id = 700
order by count_value desc