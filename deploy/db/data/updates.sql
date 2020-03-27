-- Insert mock data into beacon_sample_table
\! echo 'Updating beacon_sample_table';


-- abnormal sample EFO:0009655
-- liver UBERON:0002107
-- hepatic sinusoid UBERON:0001281
-- Kupffer cell CL:0000091
-- biopsy NCIT:C15189
-- Primary Malignant Neoplasm NCIT:C84509
-- tumor grade 2, general grading system MONDO:0024492

UPDATE public.beacon_sample_table
SET patient_id=1,
    --description=,
    biosample_status='abnormal sample',
    individual_age_at_collection_age='P12Y5M1D',
    individual_age_at_collection_age_group='Adolescent',
    organ='liver',
    tissue='hepatic sinusoid',
    cell_type='Kupffer cell',
    obtention_procedure='Biopsy',
    tumor_progression='Primary Malignant Neoplasm',
    tumor_grade='tumor grade 2, general grading system'
WHERE id%4=0;

UPDATE public.beacon_sample_table
SET patient_id=2,
    --description=,
    biosample_status='abnormal sample',
    individual_age_at_collection_age='P25Y9M18D',
    individual_age_at_collection_age_group='Adult',
    organ='liver',
    tissue='hepatic sinusoid',
    cell_type='Kupffer cell',
    obtention_procedure='Biopsy',
    tumor_progression='Primary Malignant Neoplasm',
    tumor_grade='tumor grade 2, general grading system'
WHERE id%3=0;

UPDATE public.beacon_sample_table
SET patient_id=3,
    --description=,
    biosample_status='abnormal sample',
    individual_age_at_collection_age='P56Y2M26D',
    individual_age_at_collection_age_group='Adult',
    organ='liver',
    tissue='hepatic sinusoid',
    cell_type='Kupffer cell',
    obtention_procedure='Biopsy',
    tumor_progression='Primary Malignant Neoplasm',
    tumor_grade='tumor grade 2, general grading system'
WHERE id%7=0;

UPDATE public.beacon_sample_table
SET patient_id=4,
    --description=,
    biosample_status='abnormal sample',
    individual_age_at_collection_age='P72Y6M11D',
    individual_age_at_collection_age_group='Adult',
    organ='liver',
    tissue='hepatic sinusoid',
    cell_type='Kupffer cell',
    obtention_procedure='Biopsy',
    tumor_progression='Primary Malignant Neoplasm',
    tumor_grade='tumor grade 2, general grading system'
WHERE tissue is null;

\! echo 'End';