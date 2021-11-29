# How to implement a Beacon

## Framework & Model

## Types of beacon

You should decide which type of beacon you want:

| Granularity | Description                                                                                                   |
|-------------|---------------------------------------------------------------------------------------------------------------|
| boolean     | Only returns `exists: true` ('Yes') or `exists: false` ('No') to a given query.                               |
| count       | Returns `exists: true` or `exists: false` and the total number of positive results found (`numTotalResults`). |
| record      | Returns all of the previous information and adds details for every row.                                       |

> We recommend starting with a `boolean` beacon and the upgrading its capabilities.

## Endpoints

### Configuration endpoints

<details>
  <summary><b><code>/info</code></b> and also the root (<b><code>/</code></b>)</summary>

  It MUST return information (metadata) about the Beacon service and the organization supporting it.

  Response schema: [beaconInfoResponse.json](https://github.com/ga4gh-beacon/beacon-framework-v2/blob/main/responses/beaconInfoResponse.json)

  Example:
  ```json

  ```
</details>

<details>
  <summary><b><code>/service-info</code></b></summary>

  It returns the Beacon metadata in the GA4GH Service Info schema.

  Response schema: [ga4gh-service-info-1-0-0-schema.json](https://github.com/ga4gh-beacon/beacon-framework-v2/blob/main/responses/ga4gh-service-info-1-0-0-schema.json)

  Example:
  ```json

  ```
</details>

<details>
  <summary><b><code>/configuration</code></b></summary>

  It returns some configuration aspects and the definition of the entry types (e.g. genomic variants, biosamples, cohorts) implemented in that specific Beacon server or instance.

  Response schema: [beaconConfigurationSchema.json](https://github.com/ga4gh-beacon/beacon-framework-v2/blob/5361ace5edcc900ebf054e73ad4fd945b5bebed0/configuration/beaconConfigurationSchema.json)

  Example:
  ```json

  ```
</details>

<details>
  <summary><b><code>/entry_types</code></b></summary>

  It returns **only** the property `entryTypes` of the `/configuration` endpoint.

  Response schema: [beaconConfigurationSchema.json -> EntryTypes](https://github.com/ga4gh-beacon/beacon-framework-v2/blob/5361ace5edcc900ebf054e73ad4fd945b5bebed0/configuration/beaconConfigurationSchema.json#L44-L54)

  Example:
  ```json

  ```
</details>

<details>
  <summary><b><code>/map</code></b></summary>

  It returns a map (like a web sitemap) of the different endpoints implemented in that Beacon instance.

  Response schema: [beaconMapSchema.json](https://github.com/ga4gh-beacon/beacon-framework-v2/blob/main/configuration/beaconMapSchema.json)

  Example:
  ```json

  ```
</details>

<details>
  <summary><b><code>/filtering_terms</code></b></summary>

  It returns a list of the filtering terms accepted by that Beacon instance.

  Response schema: [filteringTermsSchema.json](https://github.com/ga4gh-beacon/beacon-framework-v2/blob/main/configuration/filteringTermsSchema.json)

  Example:
  ```json

  ```
</details>

<br>

> For more examples, visit: [https://github.com/ga4gh-beacon/beacon-framework-v2](https://github.com/ga4gh-beacon/beacon-framework-v2)

### Entities

| Entity             | Default Schemas                                                                                                                               | Endpoints                                                                                                                                                                                              |
|--------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Analyses           | [defaultSchema.json](https://github.com/ga4gh-beacon/beacon-v2-Models/blob/main/BEACON-V2-draft4-Model/analyses/defaultSchema.json)           | analyses <br>analyses/{id} <br>analyses/{id}/g_variants                                                                                                                                                |
| Biosamples         | [defaultSchema.json]( https://github.com/ga4gh-beacon/beacon-v2-Models/blob/main/BEACON-V2-draft4-Model/biosamples/defaultSchema.json)        | biosamples <br>biosamples/{id}		 <br>biosamples/{id}/g_variants <br>biosamples/{id}/analyses <br>biosamples/{id}/runs                                                                                    |
| Cohorts            | [defaultSchema.json]( https://github.com/ga4gh-beacon/beacon-v2-Models/blob/main/BEACON-V2-draft4-Model/cohorts/defaultSchema.json)           | cohorts <br>cohorts/{id} <br>cohorts/{id}/individuals <br>cohorts/{id}/filtering_terms <br>cohorts/{id}/runs	 <br>cohorts/{id}/analyses                                                                 |
| Datasets           | [defaultSchema.json]( https://github.com/ga4gh-beacon/beacon-v2-Models/blob/main/BEACON-V2-draft4-Model/datasets/defaultSchema.json)          | datasets <br>datasets/{id} <br>datasets/{id}/g_variants <br>datasets/{id}/biosamples <br>datasets/{id}/individuals <br>datasets/{id}/filtering_terms <br>datasets/{id}/runs <br>datasets/{id}/analyses |
| Genomic Variations | [defaultSchema.json]( https://github.com/ga4gh-beacon/beacon-v2-Models/blob/main/BEACON-V2-draft4-Model/genomicVariations/defaultSchema.json) | g_variants <br>g_variants/{id} <br>g_variants/{id}/biosamples <br>g_variants/{id}/individuals <br>g_variants/{id}/runs	 <br>g_variants/{id}/analyses                                                    |
| Individuals        | [defaultSchema.json]( https://github.com/ga4gh-beacon/beacon-v2-Models/blob/main/BEACON-V2-draft4-Model/individuals/defaultSchema.json)       | individuals <br>individuals/{id} <br>individuals/{id}/g_variants <br>individuals/{id}/biosamples <br>individuals/{id}/filtering_terms <br>individuals/{id}/runs <br>individuals/{id}/analysis          |
| Runs               | [defaultSchema.json]( https://github.com/ga4gh-beacon/beacon-v2-Models/blob/main/BEACON-V2-draft4-Model/runs/defaultSchema.json)              | runs	 <br>runs/{id}	 <br>runs/{id}/g_variants	 <br>runs/{id}/analyses                                                                                                                                     |
