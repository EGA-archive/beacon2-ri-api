#!/usr/bin/env bats

load helpers

@test "Genomic Region [GRCh37] Y: 2655179-2656125 (ALL)" {

    query='/genomic_region?referenceName=Y&start=2655179&end=2656125&assemblyId=GRCh37&includeDatasetResponses=ALL'
    response="genomic_region-simple.json"
    pattern=.

    run compare ${query} ${response} ${pattern}

    [[ "$status" = 0 ]]

}
