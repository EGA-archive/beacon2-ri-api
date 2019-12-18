#!/usr/bin/env bats

load helpers


@test "Samples Filters + [GRCh37] Y: 2655179 G > A (ALL)" {

    query='/genomic_region?referenceName=Y&start=2655179&end=2656125&assemblyId=GRCh37&includeDatasetResponses=ALL'
    response="samples-filters_and_variant.json"
    pattern=.

    run compare ${query} ${response} ${pattern}

    [[ "$status" = 0 ]]

}

@test "Samples Filters" {

    query='/genomic_region?referenceName=Y&start=2655179&end=2656125&assemblyId=GRCh37&includeDatasetResponses=ALL'
    response="samples-filters.json"
    pattern=.

    run compare ${query} ${response} ${pattern}

    [[ "$status" = 0 ]]

}
