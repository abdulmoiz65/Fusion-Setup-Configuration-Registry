# Manage Legal Reporting Unit Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Parent legal entity | Resolve one exact effective parent per LRU input; retain each distinct numeric LegalEntityId for export and its LegalEntityIdentifier for CSV linkage |
| 2 | Target LRU package | Acquire the selected parent set using the ordered scoped payload in ../SKILL.md: TaskCode, SetupTaskCSVExportCriteria, SetupTaskCSVExportProcess. Use XLE_ENTITY_PROFILE / LEGAL_ENTITY_ID and a distinct AttributeSet per parent ID. Verify exact scope IDs and root identifiers, then bind current ASM, unchanged parent rows, LRU/registration headers, and existing function rows |
| 3 | Country geography | Resolve one enabled territory and one active COUNTRY/MASTER_REF receipt; derive every carrier from it |
| 4 | Optional jurisdiction and address | Skip both when jurisdiction is null. Otherwise resolve the explicitly supplied jurisdiction and one scoped exported address; require the registration number |
| 5 | Existing LRU and main history | Check parent-scoped name collision and complete main intervals when Y |
| 6 | Supported package scope | Emit no registration child for null jurisdiction, or one complete authority-free child for explicit jurisdiction; emit no new function rows and preserve existing rows |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| lru_package | Current LRU package shape | Yes | Always, after parent resolution | Acquire and verify | Fresh exact-parent-set target FSM export through shared.setup-export.task-level-export | verify_lru_package_baseline | Parent hierarchy and geography carriers depend on current contract | Use the criteria-first payload in ../SKILL.md and include each exact unchanged parent row; do not substitute a successful broad export | Ordered request/hash, ProcessId, exact scope-ID and parent-identifier sets, shape, child inventory, fingerprint receipt |
| lru_parent | Parent legal entity | Yes | Before scoped export, for each LRU input | Lookup | Fusion legal-entity LOV | verify_lru_parent_entity | Numeric ID scopes the export; parent identifier links every CSV child | Supply one exact effective parent per LRU; group only explicitly selected parents into a combined export | LegalEntityId for export criteria; LegalEntityIdentifier for CSV linkage |
| lru_country | Country geography | Yes | Always | Lookup | Fusion territoriesLOV and addressGeographies | resolve_lru_country_geography | Migration requires the coherent fixed country tuple; no GeographyId lookup prerequisite | Supply country name or code | Persistent/transient country carriers; identifier-row ID is receipt-only |
| lru_jurisdiction | Explicit LRU jurisdiction | Conditional | Jurisdiction is supplied | Lookup | Fusion legalJurisdictionsLOV | resolve_lru_jurisdiction | Registration is an optional explicit branch | Supply a jurisdiction only when a registration is intended; choose among ambiguous candidates | Exact Name, registration type code, and selection receipt; association to LRU geography is not checked |
| lru_address | Registration address | Conditional | Registration child applies | Verify | Fresh legal-address export | resolve_lru_registration_address | Child requires one exact location natural key | Supply exact address | FormattedAddress |
| lru_existing | Existing LRU | Yes | Before CREATE | Lookup | Fusion LRU LOV | find_lru_conflict | Prevent parent-scoped duplicate | Resolve match or choose new name | Existing definition or candidacy |
| lru_main | Main-LRU history | Conditional | MainEstablishmentFlag is Y | Verify | Complete target LRU history export | verify_lru_main_history | Main periods must not overlap | Expand scope until all sibling/history rows are proven | Validated main dates |
| lru_function | Registration function | No | Supported function-free scope | Satisfied | Explicit scope exclusion plus optional enabled-code receipt | resolve_lru_enabled_function_code | Enabled code does not prove jurisdiction permission or authority/site pair | Remove function input; preserve unrelated baseline rows | Zero new function rows |

A starter environment need not contain any existing LRU or registration examples. The parent LE must exist and be present in the fresh scoped export. Its identity and a suitable exported parent address may be reused; its jurisdiction and geography must not be copied as defaults for the new LRU. An empty legal-address set blocks only an explicit registration branch requiring an address.

For a combined export, verify every requested parent and no unexpected entity roots; partition child checks by `XLE_ENTITY_PROFILE.LegalEntityIdentifier`. Multiple parent criteria are alternative scope selections, not permission to select the first parent or reuse one parent's main history for another. Reference address coverage may be broader than the root scope and must be checked independently.

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Exact evidence already exists | Continue |
| Lookup | Documented read-only Fusion lookup is required | Read-only only |
| Acquire and verify | Parent IDs, exact ordered payload, target, catalog and approval requirements are satisfied | Create one scoped export through the selected shared export workflow, then poll/download that ProcessId and verify its actual scope; no setup import |
| Verify | Export, package, address, or main-history evidence must be checked | Local verification only |
| Blocked | Identity, country scope, eligibility, uniqueness, complete child, or history is missing | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LRU.CHECK_DEPENDENCIES | decision | 30 | resolve_dependency | ready->LRU.APPLY_DEFAULTS;blocked->LRU.HANDLE_ERROR | LRU.RESOLVE_REFERENCES | stop | After reference resolution |
