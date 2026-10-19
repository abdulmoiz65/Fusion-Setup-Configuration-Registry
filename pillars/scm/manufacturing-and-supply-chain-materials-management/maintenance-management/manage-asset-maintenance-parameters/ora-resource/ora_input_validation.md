# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Data Loader request | Active Run Book task, published business object assetSystemOptions, and either a supplied setup-data artifact or an explicit supported parameter change | Stop before Data Loader preview | Select the configured task in the Run Book. When no artifact is supplied, have core.data-loader generate the live update XLSX sample. | Asset Maintenance Parameters create or update | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Business object | Require the exact published Data Loader REST business object assetSystemOptions | Every request | |
| Source data | When supplied, let core.data-loader validate the source-data format and registered-object template. When absent, generate the live assetSystemOptions update XLSX sample first. | Every request | |
| Explicit parameter change | Accept an explicit supported enable or disable request as the input for generated-workbook preparation; require the generated live-schema workbook before preview. | When no source artifact is supplied | |
| Direct REST request | Reject a request to construct a REST payload or call a Fusion REST write endpoint | Every request | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AAMP.VALIDATE_INPUT | step | 10 | validate_input | valid->AAMP.CHECK_RUNBOOK_SCOPE;missing_or_invalid->AAMP.MISSING_INPUT | none | stop | Asset Maintenance Parameters create or update |
