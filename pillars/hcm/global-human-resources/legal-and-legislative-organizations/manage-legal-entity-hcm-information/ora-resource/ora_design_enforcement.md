# Legal Entity HCM Information Design Enforcement

## Purpose

Enforce the business scope, date-effective safety, branch isolation, and Core Data Loader mutation boundary before a result or loader handoff.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Scope | Confirm the request changes only supported Legal Employer or Payroll Statutory Unit EFF information |
| 2 | Identity and synchronization | Require one exact Legal Entity and a completed current synchronization handoff |
| 3 | Branch isolation | Map every requested context to one applicable branch without merging roots or metadata |
| 4 | Effective design | Validate current boundaries, row existence/cardinality, value sets, and delete eligibility |
| 5 | Loader contract | Resolve the exact selected object templates and operation/action sections |
| 6 | Transport boundary | Permit reads or a Core Data Loader handoff; prohibit direct REST mutation |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| LE-DES-01 | Every request | Blocker | find_legal_entity_exact | Zero or multiple exact matches | Supply one exact Name or identifier | Yes |
| LE-DES-02 | Every Get or mutation | Blocker |  | Current ManageLegalEntity Core Data Loader synchronization has not completed or its outcome is uncertain | Complete or reconcile the synchronization-only loader handoff, then resume | Yes |
| LE-DES-03 | Legal Employer work | Blocker | resolve_legal_entity_hcm_roots | LegalEmployerFlag is not Y or the exact root does not resolve | Stop; do not change the classification in this task | No |
| LE-DES-04 | Payroll Statutory Unit work | Blocker | resolve_legal_entity_hcm_roots | PsuFlag is not Y or the exact root does not resolve | Stop; do not substitute the Legal Employer branch | No |
| LE-DES-05 | Both branches apply | Blocker | resolve_legal_entity_hcm_roots | Shared Basic details conflict or contexts are flattened together | Keep branches independent and stop on conflicting shared facts | Yes |
| LE-DES-06 | Every read | Blocker | resolve_legal_entity_eff_metadata | The applicable root did not resolve exact metadata before context traversal | Resolve the selected root's exact CategoryCode describe before following context links | Yes |
| LE-DES-07 | Dated read | Blocker | resolve_legal_entity_hcm_roots | A user-supplied date is not normalized to YYYY-MM-DD, is not appended to the top-level GET, or child links are reused from another effective date | Re-run the top-level GET with &effectiveDate=<YYYY-MM-DD> and follow only its returned child links | Yes |
| LE-DES-08 | View output | Blocker | resolve_legal_entity_eff_context | Branch details are absent, an EFF Name/context heading is absent, configured segments are not shown with display values, or a zero-row context is hidden, treated as a failure, or has its empty fields enumerated | Show branch details first, then EFF Name and context headings; show configured segments only, or `No configured segments` for a zero-row context | Yes |
| LE-DES-09 | Parent/classification mutation | Blocker |  | Name, Status, LegalEmployerFlag, PsuFlag, or another parent field is requested | Use the owning setup task; this task is EFF-only | No |
| LE-DES-10 | EFF mutation | Blocker | resolve_legal_entity_eff_metadata | Context, attribute, cardinality, updateability, or value-set contract is missing or ambiguous | Refresh exact CategoryCode metadata | Yes |
| LE-DES-11 | Multirow child removal | Blocker | resolve_legal_entity_eff_context | Context is single-row or the selected child is ambiguous | Select one exact row from a confirmed multirow context | Yes |
| LE-DES-12 | Date-effective deletion | Blocker | resolve_legal_entity_hcm_history | Target is historical, future, first/only, complete, or not the greatest eligible current change | Limit the request to the latest eligible change | No |
| LE-DES-13 | Date-effective parent delete | Blocker | resolve_legal_entity_loader_contract | The selected object, synchronized identity, eligible history, or current parent-delete loader contract is incomplete or inconsistent | Re-resolve the current loader contract and selected eligible history before handoff | Yes |
| LE-DES-14 | Date-effective parent delete duplication | Blocker | resolve_legal_entity_loader_contract | The same OrganizationId and selected history start are repeated, or the delete is duplicated in an EFF member | Keep one DeleteOrganizationUnitForDTDelete row per distinct OrganizationId and selected history start | Yes |
| LE-DES-15 | Every supported mutation | Blocker | resolve_legal_entity_loader_contract | Selected object is unregistered or the current template lacks the required operation/action contract | Stop and resolve the loader contract; do not copy another object's layout | Yes |
| LE-DES-16 | Every EFF context mutation | Blocker | resolve_legal_entity_loader_contract | Required context or category controls are absent or do not match current metadata | Re-resolve current loader metadata and the selected context before handoff | Yes |
| LE-DES-17 | Correction | Blocker | resolve_legal_entity_loader_contract | The current loader correction contract does not match the requested date and affected organization's effective boundary | Re-resolve the current loader operation contract before handoff | Yes |
| LE-DES-18 | Date-effective update | Blocker | resolve_legal_entity_loader_contract | The current loader dated-update contract does not match the requested date and affected organization's effective boundary | Re-resolve the current loader operation contract before handoff | Yes |
| LE-DES-19 | Every supported mutation | Blocker |  | A plan uses REST batch, PATCH, PUT, DELETE, splitOrganizationUnitForEFFUpdate, or invokes deleteOrganizationUnitForDTDelete directly | Route the mutation through Core Data Loader; use the registered DeleteOrganizationUnitForDTDelete business object only for eligible parent deletion | Yes |
| LE-DES-20 | Mutation approval | Blocker |  | The plan duplicates approval outside Core Data Loader or reuses stale approval | Use the loader's current immutable preview and approval only | Yes |
| LE-DES-21 | Failed or uncertain mutation | Blocker |  | A plan retries automatically or falls back to REST | Reconcile through safe reads and require a new loader cycle | Yes |
| LE-DES-22 | Every read | Blocker |  | A mutating endpoint or an undeclared client is selected | Use only the declared read-only lookup contract | No |
| LE-DES-23 | Loader handoff | Blocker | resolve_legal_entity_loader_contract | Task guidance attempts to construct the upload artifact instead of handing validated intent and current contract evidence to Core Data Loader | Let Core Data Loader build and validate the immutable source and ZIP | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_legal_entity_exact | Every request | Unique business identity and routing flags | ora_reference_lookups.md |
| resolve_legal_entity_hcm_roots | After synchronization | Applicable roots, boundaries, CategoryCode, and EFF links | ora_reference_lookups.md |
| resolve_legal_entity_eff_metadata | Category, context, mutation, or verification work | Labels, attributes, cardinality, updateability, and value sets | ora_reference_lookups.md |
| resolve_legal_entity_eff_context | Context display, changed-value mapping, row removal, or verification | Current values, existence, and selected row | ora_reference_lookups.md |
| resolve_legal_entity_hcm_history | Date-effective deletion | Eligible latest range and complete history fingerprint | ora_reference_lookups.md |
| resolve_legal_entity_loader_contract | Every mutation or import | Registered objects, exact templates, keys, sections, and operation/action fields | ora_reference_lookups.md |

## Enforcement Outcomes

| Outcome | When Used | Next Action |
|---|---|---|
| passed | Every applicable blocking rule is satisfied | Continue to the declared routing node |
| not_required | No design rule applies to the requested operation | Continue without changing the request |
| blocked | An applicable blocker remains or required evidence is unavailable | Stop and require the declared correction |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LE.DESIGN | decision | 12 | design_enforcement | passed->LE.ROUTE;blocked->LE.BLOCKED;failed->LE.ERROR | LE.DEFAULTS | stop | Defaults and preservation rules are applied and execution design must be enforced |
