# Manage Legal Entity Registrations Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Target registration package | Bind current ASM, registration/function headers, exact unchanged parent row, and zero-row function child |
| 2 | Parent legal entity | Resolve one exact effective parent and its natural identifier |
| 3 | Jurisdiction and legal address | Resolve one active compatible jurisdiction and one exact active internal address |
| 4 | Existing registration | Check exact parent/jurisdiction/number and compare complete definition and identifying state |
| 5 | Authority/function scope | Require null authority values and zero function candidate rows; enabled code lookup does not reopen scope |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| ler_package | Current registration package shape | Yes | Always | Verify | Fresh target FSM export | verify_entity_registration_package | Child import requires exact current parent hierarchy and preserved empty function file | Refresh export and include the unchanged parent row | Shape, parent, zero-row child, fingerprint receipt |
| ler_parent | Parent legal entity | Yes | Always | Lookup | Fusion legal-entity LOV | verify_registration_parent_entity | The entity identifier owns the child | Supply one exact effective parent | LegalEntityIdentifier |
| ler_jurisdiction | Compatible jurisdiction | Yes | Always | Lookup | Fusion legal-jurisdiction LOV | resolve_entity_registration_jurisdiction | Jurisdiction drives identifying state and labels | Supply one exact jurisdiction name | Name, IdentifyingFlag, label, context |
| ler_address | Registered legal address | Yes | Always | Verify | Fresh legal-address export | resolve_entity_registration_address | RegistrationEO requires location semantics | Supply one exact active address natural key | FormattedAddress |
| ler_existing | Existing registration | Yes | Before CREATE | Verify | Complete target registration export | find_entity_registration_conflict | Prevent duplicate or contradictory child rows | Resolve an existing match or conflict | Existing definition or create candidacy |
| ler_authority | Issuing authority | No | Supported authority-free scope | Satisfied | Explicit scope exclusion |  | Current path requires null authority values | Remove any authority input | PartyName and IssuingFormattedAddress null |
| ler_function | Registration function | No | Supported function-free scope | Satisfied | Explicit scope exclusion plus optional enabled-code receipt | resolve_enabled_registration_function_code | Enabled code does not prove jurisdiction permission or authority/site pair | Remove function input and preserve zero child rows | Zero function rows |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Explicitly excluded branch is absent or exact evidence already exists | Continue |
| Lookup | Documented read-only Fusion lookup is required | Read-only only |
| Verify | Export, package hierarchy, or natural-key evidence must be checked | Local verification only |
| Blocked | Required identity, evidence, eligibility, uniqueness, or supported scope is missing | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LER.CHECK_DEPENDENCIES | decision | 30 | resolve_dependency | ready->LER.APPLY_DEFAULTS;blocked->LER.HANDLE_ERROR | LER.RESOLVE_REFERENCES | stop | After reference resolution |
