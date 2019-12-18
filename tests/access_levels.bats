#!/usr/bin/env bats

load helpers

@test "Access Levels Basic" {

    query='/access_levels'
    response="access_levels-basic.json"
    pattern=.

    run compare ${query} ${response} ${pattern}

    [[ "$status" = 0 ]]

}

@test "Access Levels 'includeFieldDetails=true'" {

    query='/access_levels?includeFieldDetails=true'
    response="access_levels-field_details.json"
    pattern=.

    run compare ${query} ${response} ${pattern}

    [[ "$status" = 0 ]]

}

@test "Access Levels 'displayDatasetDifferences=true'" {

    query='/access_levels?displayDatasetDifferences=true'
    response="access_levels-dataset_diff.json"
    pattern=.

    run compare ${query} ${response} ${pattern}

    [[ "$status" = 0 ]]

}

@test "Access Levels 'displayDatasetDifferences=true&includeFieldDetails=true'" {

    query='/access_levels?displayDatasetDifferences=true&includeFieldDetails=true'
    response="access_levels-det_and_diff.json"
    pattern=.

    run compare ${query} ${response} ${pattern}

    [[ "$status" = 0 ]]

}
