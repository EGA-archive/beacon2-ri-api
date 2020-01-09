#!/usr/bin/env bats

BEACON_URL=${BEACON_URL:-"http://localhost:5050"}

@test "gVariant (SNP) [GRCh37] Y: 2655179 G > A (ALL)" {
    
    query="${BEACON_URL}/gVariant?referenceName=Y&start=2655179&assemblyId=GRCh37&referenceBases=G&alternateBases=A&includeDatasetResponses=ALL"
    response="${BATS_TEST_DIRNAME}/responses/genomic_snp-simple.json"

    run diff -y \
	<(curl "${query}" | jq -S 'walk(if type == "object" then del(.variantAnnotations) else . end)') \
	<(jq -S 'walk(if type == "object" then del(.variantAnnotations) else . end)' $response)

    [[ "$status" = 0 ]]

}

@test "gVariant (SNP) [GRCh37] Y: 2655179 G > A (ALL) + Variant model: GA4GH" {

    query="${BEACON_URL}/gVariant?referenceName=Y&start=2655179&assemblyId=GRCh37&referenceBases=G&alternateBases=A&includeDatasetResponses=ALL&variant=ga4gh-variant-representation-v0.1"
    response="${BATS_TEST_DIRNAME}/responses/genomic_snp-variant_version.json"

    run diff -y \
	<(curl "${query}" | jq -S 'walk(if type == "object" then del(.variantAnnotations) else . end)') \
	<(jq -S 'walk(if type == "object" then del(.variantAnnotations) else . end)' $response)

    [[ "$status" = 0 ]]

}

@test "gVariant (Region) [GRCh37] Y: 2655179-2656125 (ALL)" {

    query="${BEACON_URL}/gVariant?referenceName=Y&start=2655179&end=2656125&assemblyId=GRCh37&includeDatasetResponses=ALL"
    response="genomic_region-simple.json"

    run diff \
	<(curl "${query}" | jq -S 'walk(if type == "object" then del(.variantAnnotations) else . end)') \
	<(get_response $response 'walk(if type == "object" then del(.variantAnnotations) else . end)')
    [[ "$status" = 0 ]]

}
