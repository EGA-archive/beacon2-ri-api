#!/usr/bin/env bats

load helpers

@test "Genomic SNP [GRCh37] Y: 2655179 G > A (ALL)" {

    query='/genomic_snp?referenceName=Y&start=2655179&assemblyId=GRCh37&referenceBases=G&alternateBases=A&includeDatasetResponses=ALL'
    response="genomic_snp-simple.json"
    pattern=.

    run compare ${query} ${response} ${pattern}

    [[ "$status" = 0 ]]

}

@test "Genomic SNP [GRCh37] Y: 2655179 G > A (ALL) + Variant model: GA4GH" {

    query='/genomic_snp?referenceName=Y&start=2655179&assemblyId=GRCh37&referenceBases=G&alternateBases=A&includeDatasetResponses=ALL&- variant=ga4gh-variant-representation-v0.1'
    response="genomic_snp-variant_version.json"
    pattern=.

    run compare ${query} ${response} ${pattern}

    [[ "$status" = 0 ]]

}
