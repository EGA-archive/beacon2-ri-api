# LocalEGA testsuite

The tests use [BATS](https://github.com/bats-core/bats-core).

We use curl to query the beacon endpoints, and compare the results with manually curated responses.

In this directory, if the beacon is setup (including the IdP and permissions server), you can run 

	bats .
	
The output should look like:

	$ bats .
	✓ Permissions - GVariants - Anonymous
	✓ Filter by registered dataset - Anonymous
	✓ Filters - 1
	✓ Filters - 2
	✓ Filters - 3
	✓ Filters - 4
	✓ Filters - 5
	✓ Info
	✓ Info - Schema
	✓ Service info
	✓ Info - Model
	✓ Biosamples
	✓ Biosamples - SAMEA4806673
	✓ Biosamples - SAMEA4806673 - individuals
	✓ Biosamples - SAMEA4806673 - g_variants
	✓ Individuals
	✓ Individuals - NA24631
	✓ Individuals - NA24631 - biosamples
	✓ Individuals - NA24631 - g_variants
	✓ GVariants
	✓ GVariants - 1
	✓ GVariants - 1 - biosamples
	✓ GVariants - 1 - individuals
	✓ Datasets
	✓ Filtering Terms
	✓ Variants SNP query
	✓ Biosamples by SNP
	✓ Individuals by SNP
	✓ Variants region query
	
	29 tests, 0 failures

