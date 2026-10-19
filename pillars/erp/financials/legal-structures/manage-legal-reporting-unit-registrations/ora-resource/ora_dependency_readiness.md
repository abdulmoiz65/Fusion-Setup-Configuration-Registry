# Manage Legal Reporting Unit Registrations Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Target registration package | Bind current ASM, exact unchanged entity/LRU parents, registration header, and zero-row function child |
| 2 | Parent entity and LRU | Resolve both exact effective parents and prove ownership |
| 3 | Jurisdiction and legal address | Resolve one active compatible jurisdiction and one exact active internal address |
| 4 | Existing registration | Check exact LRU definition and sibling-LRU jurisdiction/number collision within entity |
| 5 | Authority/function scope | Require null authority values and zero function rows; enabled code lookup does not reopen scope |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| lrur_package | Current LRU-registration package shape | Yes | Always | Verify | Fresh target FSM export | verify_lru_registration_package | Child hierarchy requires both exact unchanged parents and preserved empty function file | Refresh export and include both parents | Shape, parent, zero-row child, fingerprint receipt |
| lrur_parents | Parent entity and LRU | Yes | Always | Lookup | Fusion legal-entity and LRU LOVs | verify_lru_registration_parents | Two natural keys own every child row | Supply exact entity and LRU under it | LegalEntityIdentifier and LegalReportingUnitName |
| lrur_jurisdiction | Compatible jurisdiction | Yes | Always | Lookup | Fusion legal-jurisdiction LOV | resolve_lru_registration_jurisdiction | Jurisdiction drives identifying state and LRU label | Supply one exact jurisdiction name | Name, IdentifyingFlag, label, context |
| lrur_address | Registered legal address | Yes | Always | Verify | Fresh legal-address export | resolve_lru_registration_address_exact | Registration requires one exact location natural key | Supply one exact active address | FormattedAddress |
| lrur_existing | Existing or colliding registration | Yes | Before CREATE | Verify | Complete target LRU-registration export | find_lru_registration_conflict | Enforce exact LRU definition plus sibling-LRU jurisdiction/number scope | Resolve existing match or collision | Existing definition or candidacy |
| lrur_authority | Issuing authority | No | Supported authority-free scope | Satisfied | Explicit scope exclusion |  | Current path requires null authority values | Remove authority input | Authority carriers null |
| lrur_function | Registration function | No | Supported function-free scope | Satisfied | Explicit scope exclusion plus optional enabled-code receipt | resolve_lru_enabled_function_code | Enabled code does not prove jurisdiction permission or authority/site pair | Remove function input and preserve zero rows | Zero function rows |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Explicitly excluded branch is absent or exact evidence exists | Continue |
| Lookup | Documented read-only Fusion lookup is required | Read-only only |
| Verify | Export, hierarchy, natural-key, or collision evidence must be checked | Local verification only |
| Blocked | Parent ownership, identity, evidence, eligibility, uniqueness, or supported scope is missing | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LRUR.CHECK_DEPENDENCIES | decision | 30 | resolve_dependency | ready->LRUR.APPLY_DEFAULTS;blocked->LRUR.HANDLE_ERROR | LRUR.RESOLVE_REFERENCES | stop | After reference resolution |
