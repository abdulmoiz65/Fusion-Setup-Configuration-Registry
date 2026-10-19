# Manage Channel Claim Reasons Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | ERP Financials Reference Data Set | Resolve exactly one existing ERP Financials reference data set before creating or identifying the claim reason to update. The SCM task must not create or alter the set. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| CJMCR.REFERENCE_DATA_SET | ERP Financials Reference Data Set | Yes | Every create or update request | Lookup | ERP Manage Reference Data Sets; supplied SetId uses setIdSets plus setIdSetsLOV confirmation, otherwise setIdSetsLOV, through the FSCR Run Book | resolve_reference_data_set | The set establishes record identity; update does not reassign the reason to another set. | Supply at least one exact existing SetId, SetCode or SetName; all supplied values must agree. SetId=0 is accepted after verification. Resolve missing, conflicting or ambiguous prerequisites before restarting the preview. | SetCode; SetName; supplied SetId retained as evidence only |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| DEPENDENCY_BLOCKER | The reference data set is missing or ambiguous | Lookup: yes; Create: no |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CJMCR.RESOLVE_REFERENCE_DATA_SET | decision | 2 | resolve_dependency | resolved->CJMCR.FIND_REFERENCE_DATA_SET;blocked->RETURN_ISSUES | CJMCR.VALIDATE_INPUT | stop | A validated channel claim reason create or update candidate requires one reference data set |
