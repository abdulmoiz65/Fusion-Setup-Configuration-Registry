# Manage Legal Reporting Unit Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Parent and country gate | Resolve one effective parent and one exact active country receipt |
| 2 | Jurisdiction and conditional-child gate | Null jurisdiction produces no registration child; explicit jurisdiction requires unambiguous selection and complete number/address data |
| 3 | Collision and main-history gate | Prevent duplicate LRU and overlapping main intervals |
| 4 | Supported-scope and package gate | Reject non-country geography, authority, functions, partial children, missing unchanged parent row, or unproven target hierarchy; this graph validates final-package readiness, while the selected task SKILL.md local FSM workflow constructs the archive; resource rules do not construct, approve, upload, or import it |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every CREATE | Error | verify_lru_parent_entity | Parent is absent, inactive, ineffective, ambiguous, or mismatched | Resolve one effective parent | Yes |
| Every CREATE | Error | resolve_lru_country_geography | Country receipt is zero/many/inactive or any code/name/type/use/element/transient carrier differs | Rebuild all carriers from one receipt | Yes |
| Explicit jurisdiction is supplied | Error | resolve_lru_jurisdiction | Jurisdiction has no effective candidate, remains ambiguous, or has a duplicate importer-equivalent name | Correct input or ask which candidate; accept either identifying flag and do not add a geography-association gate | Yes |
| Jurisdiction is omitted or blank | Error |  | A jurisdiction was defaulted, a registration lookup was required, or a new registration child was emitted | Keep jurisdiction null and skip the registration branch | Yes |
| Before CREATE | Error | find_lru_conflict | Same-name LRU exists under parent or result is ambiguous | Reuse or choose a distinct approved name | Yes |
| Registration child applies | Error | resolve_lru_registration_address | Number/address is missing, address is incompatible, or authority is present | Complete supported child and remove unsupported data | Yes |
| Function input or new row exists | Error | resolve_lru_enabled_function_code | Any function input is present or function CSV contains a new candidate row | Remove function input; preserve existing unrelated rows | Yes |
| Main flag is Y | Error | verify_lru_main_history | History scope is incomplete, dates invalid, or interval overlaps | Expand export scope or correct dates | Yes |
| Any non-country request | Error |  | GeographyType is STATE, COUNTY, CITY, POSTAL_CODE, or other non-country | Report current country-only scope; do not silently replace the selected territory with its country or omit its code to bypass validation | No in current scope |
| Package preview | Error | verify_lru_package_baseline | Exact unchanged parent, hierarchy, header, empty child, or fingerprint evidence is absent | Refresh the target export and rerun the selected task SKILL.md local FSM package-preparation workflow | Yes |

## Resolved Scope Decisions

| ID | Status | Enforced Contract | Future Expansion Gate |
|---|---|---|---|
| LS-TBD-007 | Resolved for supported scope | Any registration child is authority-free; authority/site carriers are null and supplied authority blocks | Exact active eligible XLE authority plus active identifying authority-site/address resolver |
| LS-TBD-008 | Resolved for supported scope | Function child has zero new candidate rows and supplied function blocks; existing unrelated rows are preserved | Jurisdiction function permission resolver plus LS-TBD-007 authority/site contract |
| LS-TBD-010 | Resolved for country-only scope | Fixed COUNTRY/MASTER_REF tuple from territoriesLOV and addressGeographies; no GeographyId lookup prerequisite; country code and its transient must be populated | Controlled import with both code fields blank for a non-country geography whose actual code exists, using its complete resolved name/type/use/hierarchy, followed by re-export verifying the intended geography and no unrelated changes |

addressGeographies supports non-country lookup, including hierarchy levels2-5. The current country-only boundary reflects unvalidated blank-code import behavior, not a limitation of the endpoint's GeographyType filter. A naturally code-less postal geography does not prove that omitting an existing state code is safe. Do not generalize the earlier partial-STATE failure to a complete-hierarchy candidate. Before expanding scope, test that candidate through the normal Data Loader workflow and compare the re-exported normal/transient fields and hierarchy with the intended geography; record failure or ambiguity without enabling the branch. The test must not depend on unrelated pre-existing LRUs.

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| verify_lru_parent_entity | Every CREATE | Exact effective parent identifier and receipt-only identity | ora_reference_lookups.md |
| resolve_lru_country_geography | Every CREATE | Fixed persistent/transient country tuple; identifier-row ID only for receipt | ora_reference_lookups.md |
| resolve_lru_jurisdiction | Explicit jurisdiction is supplied | Selected effective Name, registration code, and import-name uniqueness evidence | ora_reference_lookups.md |
| find_lru_conflict | Before CREATE | Parent-scoped existing definition or create-candidacy receipt | ora_reference_lookups.md |
| resolve_lru_registration_address | Registration child applies | Exact compatible FormattedAddress natural key | ora_reference_lookups.md |
| verify_lru_main_history | Main flag Y | Complete sibling/history receipt and validated interval | ora_reference_lookups.md |
| verify_lru_package_baseline | Every preview | Parent and current package evidence | ora_reference_lookups.md |
| resolve_lru_enabled_function_code | Function input is supplied for scope assessment | Enabled code/meaning receipt that does not authorize CREATE | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LRU.ENFORCE_DESIGN | decision | 50 | design_enforcement | passed->LRU.PACKAGE_PREVIEW_GATE;blocked->LRU.HANDLE_ERROR | LRU.APPLY_DEFAULTS | stop | Before final-package readiness validation |
