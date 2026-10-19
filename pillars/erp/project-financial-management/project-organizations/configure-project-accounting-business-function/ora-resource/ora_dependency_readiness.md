# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Scope and enabled BU | Exact target and one active Project Accounting BU |
| 2 | Applicable financial context | Ledger, legal entity, currency, and accounting calendar ready only for implementation-row creation or a financial-dependent group change |
| 3 | Current baseline/features | Fresh task export and target opt-ins resolved |
| 4 | Changed-group references | Hierarchy, calendar, costing, relationships, and cross-charge dependencies pass |
| 5 | Package and approval | Exact package, immutable preview/checksum, explicit approval |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| BUFUNC.SCOPE | Task scope/target | Yes | Every request | Verify | Catalog/project context | verify_bu_function_scope | Prevent cross-target writes | Supply target | Scope |
| BUFUNC.ENTITY | Active BU or Project Unit identity | Yes | Business-unit identity for every write and Project Units in the requested relationship delta | Lookup | Financials Business Units LOV for BU; fresh Project Unit relationship evidence for Project Units | resolve_active_project_accounting_entity | Prevent wrong BU or relationship identity; defer start-organization roles to their dedicated REST dependencies | Provide one active entity in the selected role | Exact returned name and entity receipt |
| BUFUNC.BU | Enabled Project Accounting BU | Yes | Every write | Lookup | Target BU evidence | find_project_accounting_business_unit | Task configures an existing enabled BU | Enable function separately first | BU |
| BUFUNC.FINANCIAL | Financial context | Conditional | Implementation-row creation or calendar/period, costing/conversion, or cross-charge change | Lookup | Target financial evidence | resolve_bu_financial_context | Drives periods, currency, costing/conversion, and cross-charge; unrelated relationship additions preserve it | Complete ledger/legal-entity setup only when this dependency applies | Context |
| BUFUNC.PERIODS | Period/calendar readiness | Conditional | Existing-row calendar/period change | Lookup | Calendar and generated-period state | resolve_project_calendar | Calendar changes require periods not yet copied; common accounting/project periods do not require copied periods | Resolve calendar and periods before changing an existing row | Calendar/period values |
| BUFUNC.BASELINE | Current options/features | Yes | Update/import | Lookup | Fresh export/feature status | find_current_bu_options | Preserves omissions and runtime branch | Export immediately before preview | Baseline |
| BUFUNC.OPTIONS | Costing references | Conditional | Costing fields change | Lookup | Source-specific lookup results | resolve_costing_references | Prevent invalid costing values | Resolve each applicable value | Resolved values |
| BUFUNC.HIERARCHIES | Hierarchy references | Conditional | Hierarchy group changes | Lookup | Per-role fndTrees technical-code receipts and FndTreeVersionVO exact unique ACTIVE version receipts with effective-date bounds and current configuration date, plus the two dedicated projectOrganizationsLOV role receipts; independent membership proof not required when the available PABF export does not expose hierarchy membership | resolve_project_org_hierarchies | Require exact tree resolution and exact unique version-name match under its returned code, ACTIVE status and effectiveness on the current configuration date, preserving organization active-state and classification gates; defer validation of unproven membership to Fusion FSM import when the available PABF export does not expose hierarchy membership; proven membership mismatches still block | Resolve the selected hierarchy and carry the missing-membership-evidence warning without blocking this dependency when the available PABF export does not expose hierarchy membership | REST-sourced hierarchy technical codes, validated version names/status/effective dates/configuration date, organization values and membership warning |
| BUFUNC.RELATIONSHIPS | Project Unit relationships | Conditional | Relationship group changes | Lookup | Current relationships and Project Unit evidence; usage evidence for removals | resolve_project_unit_relationships | Validate the requested relationship delta | Resolve additions and check removability for removals | Add/remove/keep sets |
| BUFUNC.CROSS_CHARGE | Cross-charge references | Conditional | Cross-charge group changes | Lookup | Target cross-charge reference evidence | resolve_cross_charge_references | Enforce cross-charge prerequisites | Resolve applicable references | Cross-charge values |
| BUFUNC.PACKAGE | FSM package | Yes | Import preview | Verify | Template and generated package | verify_bu_function_package | Exact loader contract required | Preserve headers/checksum | Package |
| BUFUNC.PROJECT_START_ORG | ProjStartOrgName role readiness | Conditional | Project hierarchy supplied for creation/change | Lookup | Fully paginated target projectOrganizationsLOV receipt and target validation effective date | resolve_project_start_organization | One eligible OrganizationId must have active effective PROJECTS; rows for both roles do not imply multiple identities | Resolve the exact supplied name and required role before ZIP generation | Exact ProjStartOrgName, identity, effective dates, active status, required role and source receipt |
| BUFUNC.EXPENDITURE_START_ORG | ExpStartOrgName role readiness | Conditional | Expenditure hierarchy supplied for creation/change | Lookup | Fully paginated target projectOrganizationsLOV receipt and target validation effective date | resolve_expenditure_start_organization | One eligible OrganizationId must have active effective EXPENDITURES; rows for both roles do not imply multiple identities | Resolve the exact supplied name and required role before ZIP generation | Exact ExpStartOrgName, identity, effective dates, active status, required role and source receipt |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | All applicable dependencies ready | Yes |
| Missing runtime artifact | Target export, feature, reference, or template absent | No; collect it |
| Unsupported route | Enterprise BU/function mutation or direct composite REST write | No; route separately or use FSM |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BUFUNC.RESOLVE_DEPENDENCIES | step | 14 | resolve_dependency | ready->BUFUNC.ENFORCE_DESIGN;missing->BUFUNC.RETURN_ISSUES;conflict->BUFUNC.RETURN_REFUSAL | BUFUNC.ROUTE_OPERATION | stop | Before validation or import preview completes |

## Refined Operational Readiness

- **BP-004 — Operational control:** Define a daily close reconciliation covering GL period, accounting period, project accounting period, transaction-source status, cost-distribution status, revenue status, and invoice status, with exceptions and owners.
- **BP-005 — Blocking control:** When a different project calendar is approved, require selection of the project accounting calendar before project accounting periods are copied and require a separate period-maintenance plan.
- **BP-006 — Blocking control:** Validate coherence for the option groups explicitly created or changed across Project Setup, Expenditures, Costing, Project Units, and Cross-Charge Options. Preserve unchanged groups from the fresh task baseline; do not turn an unrelated group or evidence source into a gate for a relationship-only addition. For a project-unit association change, validate the enabled Project Accounting business unit, exact project unit, authorization, current relationship set, and requested delta.
- **BP-008 — Operational control:** After organization-classification or hierarchy changes, hand off to `PJF_SUBMIT_PROCESS_TO_DENORMALIZE_ORGANIZATION_HIERARCHY` and require its independently verified completion before organization readiness is claimed.
