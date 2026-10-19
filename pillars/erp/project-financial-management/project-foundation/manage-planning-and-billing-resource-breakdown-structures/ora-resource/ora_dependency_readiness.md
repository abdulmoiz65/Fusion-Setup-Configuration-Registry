# Dependency Readiness

This create-only profile does not create related reference data. The observed FSM fields for nonlabor resources, expenditure types and categories are names; a separate live directory requirement for each was not proven by the successful import. Project Unit, Job, Named Person and Organization mappings are confirmed from supplied responses and the complete current target export. A Named Person is supported only when its resolved PersonNumber already has one consistent effective-date and enterprise context in that export. Fusion import owns business-eligibility checks for copied context.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Target and task baseline | Identify the exact environment/task and obtain a complete same-target seven-member CSV export |
| 2 | New-name and project-unit context | Check the new RBS Name in the export; obtain Project Unit CSV context without deciding Project Unit eligibility |
| 3 | Observed formats and references | Use only the tested format map; resolve Job Set, Job and person codes when needed, and obtain Organization CSV context for an actual row |
| 4 | Tested tree | Add the explicit Resource Class defaults and the proven Job parent for a Job: Expenditure Category row |
| 5 | Consolidated package | Validate all rows, complete CSV members, immutable ZIP and checksum before Data Loader preview |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| RBS.BASELINE | Complete target task export | Yes | Every create batch | Verify | Shared task-level export | verify_rbs_task_export | Prevent mixed or partial package and support duplicate check | Export the full task from the selected target | Task, target, member shape, header baseline |
| RBS.IDENTITY | New planning RBS name | Yes | Every create row | Verify | Complete current target task export | find_new_rbs_identity | Do not overwrite a matching Name; exact product uniqueness scope was not tested | Give a new Name | No matching Name in the current export |
| RBS.PROJECT_UNIT | Project Unit import context | Yes | Every create row | Lookup | Current-target organizations read by exact Name plus PRJ_PROJECT_UNIT; items[].Name, ClassificationCode, EffectiveStartDate and EffectiveEndDate | resolve_rbs_project_unit_context | The tested CSV carried OrgName plus classification and dates; the read supplies fields, not an FSCR eligibility verdict | Give the Project Unit name; resolve and copy its confirmed context before preparing the proven CSV shape | OrgName <- Name; ClassificationCode <- ClassificationCode; OrgEffectiveStartDate/OrgEffectiveEndDate <- EffectiveStartDate/EffectiveEndDate |
| RBS.FORMAT | Observed selected format | Conditional | Extra format or resource selected | Verify | Tested UI/FSM format map, rechecked in the selected target | resolve_rbs_hierarchy | An exported numeric ID alone does not establish an untested descendant path | Give one of the observed format paths | Selected format ID and tested parent relationship |
| RBS.SET | Job Set | Conditional | Job Set supplied or Job component selected | Lookup | Current-target set collection | resolve_rbs_set | UI set name differs from imported SetCode | Give the set name | SetName, SetCode |
| RBS.JOB | Job | Conditional | Actual Job component selected | Lookup | Current-target Job LOV read by exact SetName plus JobName | resolve_rbs_job | Job display label differs from JobCode | Give the displayed Job value and Job Set | JobCode <- JobCode; SetCode <- SetCode |
| RBS.PERSON | Named Person | Conditional | Actual Named Person row | Lookup | Current-target publicWorkers identity read plus consistent matching PersonNumber context in the complete current task export | resolve_rbs_person | Tested FSM element takes PersonNumber, email, person dates and target-enterprise context | Give Display Name; the same value is tried as List Name only after zero Display Name matches; the person must already have context in the target export | Alias, PersonNumber, WorkEmail, EffectiveStartDate/EffectiveEndDate, Name6 and enterprise date pair 7 |
| RBS.ORGANIZATION | Organization import context | Conditional | Actual Organization row | Lookup | Current-target organizations read using PA_EXPENDITURE_ORG, PA_PROJECT_ORG, DEPARTMENT, FUN_BUSINESS_UNIT precedence plus unique enterprise context in the current task export | resolve_rbs_organization | Tested element uses Name5, ClassificationCode1, Organization date pair 4, Name4 and enterprise date pair 5; no OrganizationId | Give the organization name | Alias/Name5, selected ClassificationCode1, Organization dates 4 and target-enterprise Name4/dates 5 |
| RBS.HIERARCHY | Observed format and element hierarchy | Yes | Every create row | Verify | Tested format map and proposed tree | resolve_rbs_hierarchy | The only proven generated resource parent is Job for Job: Expenditure Category | Preview the explicit class tree and any tested Job parent | Tested format IDs and element paths |
| RBS.PACKAGE | Complete immutable FSM package | Yes | Before Data Loader handoff | Verify | Prepared seven-member ZIP and source task contract | verify_rbs_task_export | Generic ZIP classification alone does not validate RBS rows | Review exact package, count and checksum | Seven members, row counts, SHA-256 |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Complete task baseline, unique references, verified paths and package evidence | Yes; only the selected workflow can continue |
| Missing source | A resolved Named Person has no matching complete target-export context | No; request an authoritative person effective-date source before supporting that person |
| Missing value | A customer-required value or row component is absent | No; ask for the named value |
| Ambiguous reference | Zero or multiple matches, incomplete pagination or conflicting returned codes | No; do not guess |
| Unsafe package | Explicit class tree absent, tested parent chain invalid, changed artifact or partial batch | No; correct and re-preview |
| Unsupported | Update, end-date, billing maintenance, delete or direct setup REST requested through this create route | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RBS.RESOLVE_DEPENDENCIES | step | 11 | resolve_dependency | ready->RBS.ENFORCE_DESIGN;missing->RBS.RETURN_ISSUES;conflict->RBS.RETURN_REFUSAL | RBS.RESOLVE_HIERARCHY | stop | Observed create-batch dependencies must be satisfied before preview |
