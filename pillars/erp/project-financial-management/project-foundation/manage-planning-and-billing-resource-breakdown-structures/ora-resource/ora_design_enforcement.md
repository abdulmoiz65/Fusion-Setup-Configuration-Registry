# Design Enforcement

The only supported mutation prepared by this rule set is a new custom PLANNING RBS. Business-policy checks do not authorize a write; the selected runbook and Core Data Loader still own the final package, approval and submission.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Protect observed create scope | Reject existing names, maintenance operations and untested resource combinations |
| 2 | Obtain CSV context and proven conversions | Resolve Project Unit context by supplied name plus PRJ_PROJECT_UNIT and conditional Organization context without prevalidating business eligibility; retain the observed format map and applicable Set, Job and Person conversions |
| 3 | Reproduce UI-equivalent defaults | Require explicit Resource Class format, root and four default class elements in FSM input |
| 4 | Preserve tested hierarchy | Include the Job parent only for the tested Job: Expenditure Category combination; show actual Alias values |
| 5 | Validate consolidated package | Require all requested rows in one immutable seven-member task ZIP and checksum before loader preview |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every create | Blocker | find_new_rbs_identity | Same Name already appears in target export, or export is incomplete | Choose a new name or obtain a complete current-target export | Yes |
| Every create | Blocker | resolve_rbs_project_unit_context | Project Unit CSV classification or effective context cannot be populated from one Name plus PRJ_PROJECT_UNIT result | Use the confirmed field mapping; do not copy values from an unrelated RBS or reject the name as ineligible before Fusion import | Yes |
| Extra format or resource selected | Blocker | resolve_rbs_hierarchy | Path is not one of the observed formats, or an untested actual descendant row is requested | Obtain new UI and FSM evidence before extending this profile | Yes |
| Job component selected | Blocker | resolve_rbs_job | Job Set absent, Job label ambiguous or JobCode unresolved | Resolve set first, then one job in that set | Yes |
| Named Person component selected | Blocker | resolve_rbs_person | Display Name and fallback List Name do not yield one PersonNumber, or that PersonNumber lacks one consistent date/enterprise context in the complete target export | Clarify the worker identity or provide an authoritative person effective-date source | Yes |
| Organization component selected | Blocker | resolve_rbs_organization | No unique Organization exists under the first matching precedence class, or Organization/enterprise context cannot be populated | Apply PA_EXPENDITURE_ORG, PA_PROJECT_ORG, DEPARTMENT, FUN_BUSINESS_UNIT precedence and copy the confirmed fields; leave business eligibility to Fusion import | Yes |
| Organization, Expenditure Type or Expenditure Category actual row | Blocker |  | Resource Class or Spread Curve omitted; the tested UI preselected neither | Ask the customer to select both; only the tested pairs have observed serialization | Yes |
| Job: Expenditure Category actual row | Blocker | resolve_rbs_hierarchy | Job format or generated Job parent absent, or Job/category value missing | Include the tested parent-child shape and both required values | Yes |
| Every prepared package | Blocker | verify_rbs_task_export | Resource Class format or five defaults absent; root Alias stale; missing member; invalid checksum; partial batch | Regenerate the complete package and preview every requested structure | Yes |
| Outside observed profile | Blocker |  | Update, end-date, delete, billing maintenance or an untested descendant resource row entered through this route | Use a separately evidenced and authored workflow | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_new_rbs_identity | Every create | Exact current-target existence count | ora_reference_lookups.md |
| resolve_rbs_project_unit_context | Every create | One Name plus PRJ_PROJECT_UNIT result; OrgName and copied classification/effective import context; no Status or RBS From Date eligibility check | ora_reference_lookups.md |
| resolve_rbs_hierarchy | Any extra format or resource | Observed format ID and proven parent relationship | ora_reference_lookups.md |
| resolve_rbs_job | Job resource component | One JobCode in the selected set | ora_reference_lookups.md |
| resolve_rbs_person | Named Person resource component | One PersonNumber and WorkEmail plus one consistent matching export context for person dates and enterprise Name6/date pair 7 | ora_reference_lookups.md |
| resolve_rbs_organization | Organization resource component | One precedence-selected name/classification/date row plus unique target-export enterprise Name4/date pair 5; no OrganizationId or FSCR eligibility decision | ora_reference_lookups.md |
| verify_rbs_task_export | Every prepared package | Task identity, seven members and checksum | ora_reference_lookups.md |

## Package Gate

| Check | Block Preview When | Required Evidence |
|---|---|---|
| Customer minimum | Any Name, Project Unit or From Date missing | Row-level validated input |
| Complete task package | Any of the six task CSV members or ASM_SETUP_CSV_METADATA.xml missing, wrong header or mixed target | Seven flat members from one current-target task contract |
| UI-equivalent default | Resource Class format, root or any of four class elements missing for a new RBS | Explicit format and element rows per RBS |
| Requested extras | Selected format missing, or a format-only choice creates an unrequested specific resource | Format and element diff for each new RBS |
| Tested child parent closure | Job: Expenditure Category is missing the Job format or generated Job parent | Job code and category child under one Job parent |
| Resource references | Required SetCode, JobCode, PersonNumber, Project Unit context or Organization context is unavailable or malformed | Canonical code/number and copied CSV context as applicable; Fusion import decides Project Unit and Organization name eligibility |
| Root identity | Root Alias is a cloned fixture name instead of the requested RBS Name | Root Alias equals new Name |
| Bulk consolidation | Any invalid row is silently omitted, or more than one ZIP/import is planned for one batch | All rows accounted for in one immutable ZIP and one loader submission |
| Immutable handoff | Final artifact differs from preview or lacks SHA-256 | Exact ZIP path, SHA-256, row counts and selected target for loader preflight |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RBS.ENFORCE_DESIGN | decision | 12 | design_enforcement | pass->RBS.EXECUTION_GATE;blocked->RBS.RETURN_REFUSAL;failure->RBS.RETURN_ISSUES | RBS.RESOLVE_DEPENDENCIES | stop | Observed create profile and complete package gate before Data Loader preview |
