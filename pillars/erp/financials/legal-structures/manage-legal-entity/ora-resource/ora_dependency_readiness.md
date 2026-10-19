# Manage Legal Entity Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Target entity-tree export | Bind exact current ASM, six CSV members, headers, hierarchy, parent rows, and both function files; preserve existing function rows unchanged and retain header-only files when already header-only in the baseline |
| 2 | Country and geography | Resolve one enabled non-obsolete territory and one effective primary country result; no country GeographyId prerequisite |
| 3 | Identifying jurisdiction | Resolve the user's jurisdiction input, including an explicit candidate choice when needed, and pass exact-name import uniqueness |
| 4 | Legal address | Resolve one exact active internal natural key or approved earlier package row |
| 5 | Entity existence and optional parent PSU | Prove identifier availability, disclose name conflicts, and resolve a PSU only when applicable |
| 6 | Complete aggregate | Require root plus exactly three explicit children with authority null and zero candidate function rows |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| le_package | Current aggregate package shape | Yes | Always | Verify | Fresh target export | verify_entity_package_baseline | FSM hierarchy and existing-parent rows are package prerequisites | Re-export when evidence is stale or incomplete | Shape, hierarchy, parent, and fingerprint receipt |
| le_country | Country and country geography | Yes | Always | Lookup | Fusion territory and address-geography services | resolve_entity_country_geography | Root and main-LRU carriers must use the resolved territory and primary country values consistently | Supply a country name or code; refine language only if ambiguous | Country carriers and source-specific receipt-only GeographyIdentifierId |
| le_jurisdiction | Identifying jurisdiction | Yes | Always | Lookup | User's jurisdiction input verified by Fusion jurisdiction service | resolve_entity_identifying_jurisdiction | Both identifying children require the selected eligible jurisdiction and an unambiguous import Name; country association is not independently verified by this flow | Supply the intended identifying jurisdiction if missing, or select among eligible matches when asked | Exact jurisdiction Name, identifying semantics, LE/LRU registration type codes, receipt-only JurisdictionId and jurisdiction GeographyId |
| le_address | Legal address | Yes | Always | Verify | Fresh legal-address export or approved earlier row | resolve_entity_legal_address | Root and registrations require one exact location natural key | Select or create the registered address first | LegalAddress and FormattedAddress |
| le_exists | Entity identity availability | Yes | Before CREATE | Lookup | Fusion legal-entity LOV | find_entity_conflict | Prevent duplicate identifier and disclose name collision | Resolve any existing match before CREATE | Availability receipt |
| le_parent_psu | Parent payroll statutory unit | Conditional | Input supplied or supported HCM design requires it | Lookup | Fusion legal-entity LOV plus eligibility evidence | resolve_entity_parent_psu | Parent must be exact, effective, and eligible | Supply one eligible PSU or remove the unsupported branch | ParentPsuLeIdentifier |
| le_functions | Both registration-function branches | No | Supported function-free scope | Satisfied | Explicit scope exclusion plus optional enabled-code receipt | resolve_entity_enabled_function_code | Enabled code does not prove jurisdiction permission or authority/site pair | Remove function input, preserve existing function rows unchanged, and add zero candidate rows | Zero candidate function rows |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Exact evidence already exists | Continue |
| Lookup | Documented read-only Fusion lookup is required | Read-only only |
| Verify | Export, approved prior row, or package hierarchy must be checked | Local verification only |
| Blocked | Required identity, evidence, eligibility, uniqueness, or complete aggregate is missing | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LE.CHECK_DEPENDENCIES | decision | 30 | resolve_dependency | ready->LE.APPLY_DEFAULTS;blocked->LE.HANDLE_ERROR | LE.RESOLVE_REFERENCES | stop | After reference resolution |
