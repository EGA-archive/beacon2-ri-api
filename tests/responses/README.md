
`/query`
- localhost:5050/query?referenceName=Y&start=2655179&assemblyId=GRCh37&referenceBases=G&alternateBases=A&includeDatasetResponses=ALL

`/genomic_snp`
- localhost:5050/genomic_snp?referenceName=Y&start=2655179&assemblyId=GRCh37&referenceBases=G&alternateBases=A&includeDatasetResponses=ALL
- localhost:5050/genomic_snp?referenceName=Y&start=2655179&assemblyId=GRCh37&referenceBases=G&alternateBases=A&includeDatasetResponses=ALL&- variant=ga4gh-variant-representation-v0.1
> ignore value.variantsFound.variantAnnotations.default.value.info

`/genomic_region`
- localhost:5050/genomic_region?referenceName=Y&start=2655179&end=2656125&assemblyId=GRCh37&includeDatasetResponses=ALL
> ignore value.variantsFound.variantAnnotations.default.value.info

`/samples`
- localhost:5050/samples?filters=sex:1,tissue:2&referenceName=Y&alternateBases=A&referenceBases=G&start=2655179&assemblyId=GRCh37
- localhost:5050/samples?filters=sex:1,tissue:2
> ignore value.results[i].variantsFound

`/individuals`
- localhost:5050/individuals?filters=sex:1,tissue:2&referenceName=Y&alternateBases=A&referenceBases=G&start=2655179&assemblyId=GRCh37
- localhost:5050/individuals?filters=sex:1,tissue:2
> ignore value.results[i].variantsFound


`/`
- localhost:5050/ and localhost:5050/info
- localhost:5050/service-info
> ignore updateDateTime

`/filtering_terms`
- localhost:5050/filtering_terms
> it will be changing as the DB is updated, so we ignore it

`/access_levels`
- localhost:5050/access_levels
- localhost:5050/access_levels?includeFieldDetails=true
- localhost:5050/access_levels?displayDatasetDifferences=true
- localhost:5050/access_levels?displayDatasetDifferences=true&includeFieldDetails=true
> it depends on the access_levels.yaml, have in mind that any changes there will affect this endpoint

`/services`
- localhost:5050/services
> ignore updateDateTime