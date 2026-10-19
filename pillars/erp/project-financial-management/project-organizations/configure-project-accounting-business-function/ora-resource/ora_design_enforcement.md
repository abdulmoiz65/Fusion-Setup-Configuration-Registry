# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Protect BU identity | Existing enabled Project Accounting BU stays fixed; financial context is resolved only when the changed group depends on it |
| 2 | Preserve omitted groups | Diff only explicitly requested option groups |
| 3 | Resolve retained documented lookups | Resolve only values backed by documented lookup endpoints or standard lookups |
| 4 | Enforce hierarchy/calendar rules | Require REST-resolved trees, uniquely existing version names, active classified start organizations and mutable compatible periods |
| 5 | Protect relationships/cross-charge | Prevent used relationship removal and require all method prerequisites |
| 6 | Respect feature branch | Write only surfaces available on the target |
| 7 | Protect package/approval | Exact FSM package and immutable approved preview |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Business-unit identity for every write and Project Units in the requested relationship delta | Blocker | resolve_active_project_accounting_entity | The entity has zero or multiple active matches or a BU/Project Unit context mismatch | Resolve the BU or Project Unit identity; start organizations use dedicated REST role checks | Yes |
| Every write | Blocker | find_project_accounting_business_unit | The BU is ambiguous or inactive, or Project Accounting is disabled | Correct the identity or enable the function separately | Yes |
| Hierarchy change | Blocker | resolve_project_org_hierarchies | The tree or supplied version is missing or ambiguous, technical codes lack matching fndTrees response provenance, the version is not ACTIVE or is ineffective on the current configuration date, or the start organization is inactive, proven out-of-tree or misclassified | Resolve the display tree name first and require one exact ACTIVE version-name match effective on the current configuration date under the returned tree code; select a correctly classified active organization | Yes |
| Hierarchy start-organization membership | Warning | resolve_project_org_hierarchies | Not blocking: independent proof that the selected start organization belongs to the selected tree/version is missing because the available PABF export does not expose hierarchy membership | Record and disclose the warning with the selected tree/version and start organization; continue when all other gates pass and let Fusion FSM import validate membership. Do not infer membership or require additional proof for this export limitation. Proven membership mismatches still block; preserve approval and post-import verification | No automatic fix |
| Calendar change | Blocker | resolve_project_calendar | Periods are copied or the calendars are incompatible | Preserve the calendar or correct the periods | Yes |
| Retained lookup change | Blocker | resolve_costing_references | A supplied value does not resolve uniquely through its documented lookup source | Correct or clarify the value | Yes |
| Project-unit removal | Blocker | resolve_project_unit_relationships | The relationship is used downstream or is nondeletable | Preserve the association | No |
| Cross-charge change | Blocker | resolve_cross_charge_references | Legal entity, rate, or schedule prerequisites are absent | Complete the prerequisites | Yes |
| Feature-hidden field | Blocker | verify_bu_feature_status | The requested field is unavailable on the target branch | Preserve the runtime value | No |
| Direct REST write | Blocker |  | No composite write contract proven | Use FSM CSV | No |
| Import preview | Blocker | verify_bu_function_package | Package contract/checksum invalid or approval absent | Regenerate and approve | Yes |
| ProjStartOrgName is supplied | Blocker | resolve_project_start_organization | No exact match, multiple active effective OrganizationId values, missing active effective PROJECTS, incomplete response/provenance or REST failure | Resolve one active effective identity and its required role before ZIP generation; never count duplicate same-ID role rows as ambiguity | Yes |
| ExpStartOrgName is supplied | Blocker | resolve_expenditure_start_organization | No exact match, multiple active effective OrganizationId values, missing active effective EXPENDITURES, incomplete response/provenance or REST failure | Resolve one active effective identity and its required role before ZIP generation; never count duplicate same-ID role rows as ambiguity | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_active_project_accounting_entity | Business-unit identity for every write and Project Units in the requested relationship delta | Exact BU/Project Unit name and active-state receipt | ora_reference_lookups.md |
| find_project_accounting_business_unit | Every write | BU identity, active state, and Project Accounting function status | ora_reference_lookups.md |
| resolve_project_org_hierarchies | Hierarchy change | REST-resolved trees, unique ACTIVE/effective versions with date/status receipts, and classified start organizations | ora_reference_lookups.md |
| resolve_project_calendar | Calendar/period change | Compatibility and copied-period state | ora_reference_lookups.md |
| resolve_costing_references | Retained lookup change | Expenditure start day, rate-date types, rate types, accounting calendar, and default asset book | ora_reference_lookups.md |
| resolve_project_unit_relationships | Relationship change | Add/remove/usage evidence | ora_reference_lookups.md |
| resolve_cross_charge_references | Cross-charge change | Methods and prerequisites | ora_reference_lookups.md |
| verify_bu_feature_status | Any feature-conditional field | Current target opt-in and feature availability | ora_reference_lookups.md |
| verify_bu_function_package | Import | Contract/checksum | ora_reference_lookups.md |
| resolve_project_start_organization | ProjStartOrgName supplied for creation/change | Exact name, unique active effective OrganizationId, PROJECTS and complete target REST receipt | ora_reference_lookups.md |
| resolve_expenditure_start_organization | ExpStartOrgName supplied for creation/change | Exact name, unique active effective OrganizationId, EXPENDITURES and complete target REST receipt | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BUFUNC.ENFORCE_DESIGN | decision | 15 | design_enforcement | pass->BUFUNC.NORMALIZE_EXPORT_ONLY_EFFECTIVE_DATES;blocked->BUFUNC.RETURN_REFUSAL;failure->BUFUNC.RETURN_ISSUES | BUFUNC.RESOLVE_DEPENDENCIES | stop | Before final package sanitization and import approval; membership warnings do not block the pass outcome, but all other blocking controls remain mandatory |

## Refined Best-Practice Gate

The registry's design-enforcement node evaluates the controls distributed across this task's standard `ora-resource` files. Record `control_id`, `status` (`pass`, `fail`, `needs_input`, or `not_applicable`), evidence, and any approved exception for every applicable control. A failed Blocking control stops the route before preview; missing Required evidence returns `needs_input`; missing Operational controls prevent an operational-readiness claim.

- **BP-001 — Blocking control:** Use common GL and Project Accounting periods by default. A separate calendar requires a documented reporting or operational need, accountable owner, approval reference, effective date, and review date.
- **BP-003 — Blocking control:** Refuse a same-calendar/separate-status design unless a compelling control reason and ownership for the second close process are documented.
- **BP-007 — Blocking control:** Associate a business unit only with project units it is authorized to process. Shared project-management methods do not justify transaction-processing access.

For a relationship-only addition, BP-006 and BP-007 are satisfied from current evidence for the enabled Project Accounting BU, the exact active Project Unit, its authorization/classification, the existing relationship set, and the additive package delta. Unchanged ledger, legal-entity, currency, calendar, costing, and cross-charge groups are preserved and are not independent evidence gates.
