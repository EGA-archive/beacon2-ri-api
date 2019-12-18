#!/usr/bin/env bats

load helpers

@test "Query [GRCh37] Y: 2655179 G > A (ALL)" {

    query=$'/query?referenceName=Y&start=2655179&assemblyId=GRCh37&referenceBases=G&alternateBases=A&includeDatasetResponses=ALL'
    response=$'query.json'
    pattern=$'.'

    compare ${query} ${response} ${pattern} > toto.txt

    run echo done
    
    [[ "$status" = 0 ]]

}
