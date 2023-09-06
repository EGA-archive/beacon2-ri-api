
# File for all the mappings from the Beacon v2 specification and the results of the SQL Queries

############################### Individual model  ####################################

def diseases_table_map(dictValues):
    return {
            'diseaseCode': dictValues["condition_concept_id"],
            'ageOfOnset': {'iso8601duration': dictValues["condition_ageOfOnset"]},
        }

def procedures_table_map(dictValues):
    return {
            'procedureCode': dictValues["procedure_concept_id"],
            'ageAtProcedure': {'iso8601duration': dictValues["procedure_ageOfOnset"]},
            'dateOfProcedure': dictValues["procedure_date"],
        }

def measures_table_map(dictValues):
    # TO DO
    # Make the return complex so depend on the type of data. It can be a unit/value, an ontology, referenceRange, complexValue, etc.
    return {
        'assayCode': dictValues["measurement_concept_id"],
        'date' : dictValues["measurement_date"],
        'measurementValue': {
            'unit': dictValues["unit_concept_id"],
            'value': dictValues["value_source_value"]
        },
        'observationMoment': {'iso8601duration':dictValues["measurement_ageOfOnset"]}
    }

def exposures_table_map(dictValues):
    return {
            'exposureCode': dictValues["observation_concept_id"],
            'ageAtExposure': {'iso8601duration': dictValues["observation_ageOfOnset"]},
            'date': dictValues["observation_date"],
        }