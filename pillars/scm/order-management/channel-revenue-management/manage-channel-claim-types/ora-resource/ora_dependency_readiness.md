# Manage Channel Claim Types Dependency Readiness

## Required Dependency Order

Create rows retain the requirements below. For update, require the reference set for parent identity, but resolve a new Business Unit only when a non-null BusinessUnit change is requested. An AR-only child update does not require resupplying the BU name. Resolve existing parent and child identities through find_claim_type_by_code and find_existing_bu_mapping before current-value validation; do not create missing dependencies. Existing BUMappingCode and BusinessUnitId are identity evidence, never proposed replacements. A nullable BusinessUnit clear follows the explicit-clear contract and cannot be replaced by a guessed BU.

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Business-unit mapping shape | When child mappings are supplied, validate their parent discriminator, Business Unit ID or name, and BUMappingCode before preview. |
| 2 | Financials Business Unit identity | Resolve every supplied Business Unit ID or name to exactly one active BusinessUnitId through the Manage Business Unit resolver before building the final loader source. |
| 3 | ERP Financials Reference Data Set | Resolve one existing reference data set from any supplied SetId, SetCode or SetName before preview. The SCM task must not create or alter it. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| CJMCT.REFERENCE_DATA_SET | ERP Financials Reference Data Set | Yes | Every create or update, including child-only | Lookup | ERP Manage Reference Data Sets, resolved through the task's ID or code/name lookup in the FSCR Run Book | resolve_reference_data_set | The set identifies the parent | Supply SetId, SetCode or SetName; ID is optional and intake-only. Resolve one set and pass supported code/name fields to the loader | SetCode; SetName |
| CJMCT.BUSINESS_UNIT | Financials Business Unit identity | Conditional | Child create or a non-null requested BusinessUnit change on update | Lookup | ERP Financials Manage Business Unit resolver through finBusinessUnitsLOV | resolve_business_unit_identity | Resolve create ID or name to one active BU; cross-check both when supplied. Create removes helper names; update resolves only a proposed new name and retains writable BusinessUnit. | Create cross-checks supplied BusinessUnitId against the resolved BU; update cross-checks it against the existing mapping instead. AR-only updates need no new BU name. | BusinessUnitId; BusinessUnitName; ActiveFlag |
| CJMCT.BU_MAPPING | Business-unit level mapping | Conditional | Child create rows | Verify | Prepared Data Loader linkage and resolved Financials Business Unit identity | resolve_business_unit_identity | A new child belongs to its parent and resolved BU | Retain parent linkage and BUMappingCode; create uses resolved BusinessUnitId | Parent discriminator; BusinessUnitId; BUMappingCode |
| CJMCT.EXISTING_MAPPING | Existing child mapping | Conditional | Child update rows | Lookup | Existing mapping under resolved Fusion parent | find_existing_bu_mapping | Updates must target an existing child, not insert one | Supply existing mapping code or ID; preserve parentage | BusinessUnitLevelMappingId; ClaimTypeId; current values |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| DEPENDENCY_BLOCKER | The reference data set is missing or ambiguous | Lookup: yes; Create: no |
| DEPENDENCY_BLOCKER | A Business Unit ID or name has zero, multiple, inactive, inaccessible, or conflicting-identity matches | Lookup: yes; Create: no |
| INPUT_VALIDATION | A supplied business-unit mapping is incomplete or mis-parented | Lookup: no; Create: no |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CJMCT.RESOLVE_REFERENCE_DATA_SET | decision | 4 | resolve_dependency | resolved->CJMCT.FIND_REFERENCE_DATA_SET;blocked->RETURN_ISSUES | CJMCT.VALIDATE_CHILD_MAPPINGS,CJMCT.FIND_BUSINESS_UNIT | stop | A validated parent claim type and every supplied child mapping have resolved dependencies |
