-- Insert mock data into beacon_sample_table
\! echo 'Updating beacon_sample_table';

UPDATE beacon_sample_table SET sex='female' WHERE id IN (1,2,3);
UPDATE beacon_sample_table SET sex='male' WHERE id IN (4,5,6);

UPDATE beacon_sample_table SET tissue='kidney' WHERE id in (1,2);
UPDATE beacon_sample_table SET tissue='lung' WHERE id in (3,4);
UPDATE beacon_sample_table SET tissue='liver' WHERE id in (5,6);

UPDATE beacon_sample_table SET description='Lorem ipsum dolor sit, amet consectetur adipiscing elit, hendrerit et.' WHERE id IN (1,2,3,4,5,6);

UPDATE beacon_sample_table SET patient_id=1 WHERE id in (1,2);
UPDATE beacon_sample_table SET patient_id=2 WHERE id=3;
UPDATE beacon_sample_table SET patient_id=3 WHERE id=4;
UPDATE beacon_sample_table SET patient_id=4 WHERE id=5;
UPDATE beacon_sample_table SET patient_id=5 WHERE id=6;

\! echo 'End';