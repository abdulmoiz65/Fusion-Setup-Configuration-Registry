# Input Validation

These rules cover only a new custom PLANNING resource breakdown structure and the format/resource cases observed in the UI and 16-case FSM import/readback. Other task operations and untested resource combinations are not established by this contract. Customer input uses business labels; the tested FSM representation sometimes uses a different code.

## Customer Input Contract

| Business Attribute | Accepted Customer Value | Mandatory | Applies When | FSM Representation or Outcome |
|---|---|---|---|---|
| Name | New planning RBS name | Yes | Every new structure | Header and version Name; root Alias must equal the new name |
| Project Unit | Project unit name | Yes | Every new structure | Resolve by name plus PRJ_PROJECT_UNIT, then copy items[].Name to header OrgName and the confirmed classification/effective CSV context; Fusion import decides whether the name is valid for this RBS |
| From Date | Effective start date | Yes | Every new structure | Header and version StartDateActive in yyyy/MM/dd form |
| Description | Text | No | Supplied | Header, version and applicable translations |
| Job Set | Set name | Conditional | Required for an actual Job or Job: Expenditure Category row; otherwise optional | Resolve name to version SetCode and Job-element SetCode; selecting the Job format alone does not require it |
| Resource Formats | One or more exact paths in the observed format table below | No | Extra formats requested | Include each selected format and its tested parent; selection alone adds no specific-resource element |
| Planning Resources | A value for each starred combination component of an observed format | No | Actual resource row requested | Include the tested resource element and any proven parent element |
| Resource Name | Alias for the directly saved Job, Expenditure Category or Job: Expenditure Category child; blank is proven only for Named Person | Conditional | Require a nonblank alias for these three tested resource rows; the UI did not mark Job Name mandatory, but blank-Job save/import behavior was not tested | Other formats' custom-alias persistence is not established; preview the actual Alias |
| Resource Class and Spread Curve | Business labels | Conditional | Required for actual Organization, Expenditure Type or Expenditure Category rows | Their UI fields were blank and starred; the observed chosen pairs are in the format table |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Supported operation | Create a new custom PLANNING RBS | Refuse an unsupported operation | Do not reinterpret update, end-date, billing maintenance or delete as create | Every request |  |
| New RBS identity | Name, Project Unit, From Date | Block the affected request | Ask for the missing business value; check the complete same-target task export for an existing Name before creating | Every create row | find_new_rbs_identity |
| Target and task evidence | Target environment, exact setup task, complete current task export, seven-member task CSV contract | Block package preparation | Acquire through the declared shared export workflow; no guessed or partial baseline | Every batch | verify_rbs_task_export |
| Observed format | Exact path from the format table | Block an untested path | Do not infer descendant behavior from an exported ID alone | Each selected format or resource |  |
| Resource components | The starred input in the tested Add row; both Job and Expenditure Category for their child combination | Block the affected row | Ask for the missing component; do not turn an empty Add row into a resource | Each actual planning resource row |  |
| Job resource scope | Job Set name and Job display label | Block the affected row and ask which Job Set to use; do not list or query Jobs without it | Resolve SetName to SetCode, then query the selected Job within that set | Job or Job: Expenditure Category actual row | resolve_rbs_job |
| Named Person identity | Display Name, with List Name fallback | Block zero or multiple matches, or missing/conflicting target-export context for the resolved PersonNumber | Resolve the selected worker to PersonNumber and WorkEmail, then copy one consistent person date/enterprise context from the complete target export | Named Person actual row | resolve_rbs_person |
| Organization import context | Organization name | Block when the first matching precedence class is ambiguous or the tested CSV context cannot be supplied | Apply PA_EXPENDITURE_ORG, PA_PROJECT_ORG, DEPARTMENT, FUN_BUSINESS_UNIT precedence; copy Organization name/classification/date pair 4 and current-export enterprise Name4/date pair 5 | Organization actual row | resolve_rbs_organization |
| Explicit class and curve | Resource Class and Spread Curve labels | Block the affected row | Ask for both; the UI did not preselect either | Organization, Expenditure Type or Expenditure Category actual row |  |
| Complete bulk input | Every new RBS and resource row passes the documented shape/conversion checks before one consolidated ZIP | Block the whole batch | Report row-level preflight issues; Fusion import still determines target eligibility for name fields lacking a documented lookup | Multiple new structures or resource rows |  |

## Format Path Contract

These IDs and rows are **observed test-target evidence**, not universal Fusion constants or a complete taxonomy. Recheck them against the selected target before preparation. An unlisted path is outside this evidence-backed create profile, not a claim that Fusion cannot support it.

| Format Path | Observed ResFormatId | Evidence Level | Resource-Row Requirement |
|---|---|---|---|
| Resource Class | 323 | Minimal UI save and populated FSM readback | UI adds root plus four class elements; FSM needs them explicitly |
| Named Person | 195 | Actual person row imported/read back | Named Person input; UI preselects Labor and Prorated Even; blank Name filled from person |
| Project Nonlabor Resource | 306 | Actual nonlabor row imported/read back | Nonlabor name; UI preselects Equipment and Back Loaded |
| Organization | 205 | Actual organization row imported/read back | Organization name plus explicit class and curve; tested Equipment and Back Loaded |
| Job | 166 | Actual Job row imported/read back | Job Set, Job and nonblank saved alias for this tested profile; UI preselects Labor and Prorated Even |
| Expenditure Type | 80 | Actual type row imported/read back | Type name plus explicit class and curve; tested Labor and Prorated Even |
| Expenditure Category | 35 | Actual category row imported/read back | Category name, nonblank saved alias, and explicit class and curve; tested Labor and Prorated Even |
| Job: Expenditure Category | 170 | Actual child row imported/read back | Job Set, Job, category and nonblank child alias for this tested profile; UI preselects Labor and Prorated Even and generated Job parent |
| Organization: Inventory Item | 231 | Format-only UI save and FSM readback | Include Organization parent format; actual Inventory Item row not tested |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| New planning name | Verify | Stop on a matching Name; the exact duplicate-uniqueness scope was not tested | find_new_rbs_identity |
| Job Set supplied without Job format or resource | Valid optional header value | Resolve SetCode; do not add a Job format or element | resolve_rbs_set |
| Extra observed format selected without planning resource | Valid format-only choice | Emit the selected format and tested parent format, but no specific-resource element |  |
| Job format selected without Job Set or Job resource | Valid format-only choice | Do not require a Job lookup or create a Job element |  |
| Job resource selected | Conditional | Require Job Set before listing or resolving Jobs; then resolve JobCode in that set | resolve_rbs_job |
| Job: Expenditure Category resource selected | Conditional | Require Job Set, Job and category; include Job format and the observed synthesized Job parent |  |
| Organization, Expenditure Type or Expenditure Category resource selected | Conditional | Require explicitly selected Resource Class and Spread Curve |  |
| Multiple rows supplied | Conditional | Validate all rows and identities, then prepare one consolidated package |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Nonblank RBS name and project unit; valid From Date | Reject missing or malformed values; resolve Project Unit context by name plus PRJ_PROJECT_UNIT without inspecting Status or prevalidating its business eligibility | Every create row | resolve_rbs_project_unit_context |
| Existing target name | Block a matching Name; never overwrite or silently convert to update | Every create row | find_new_rbs_identity |
| Date serialization | Normalize to yyyy/MM/dd without changing the calendar date | Every date included in FSM |  |
| Format and element shape | Reject an unobserved resource path or missing Job parent for the tested child; no universal descendant synthesis rule is claimed | Format or resource selected | resolve_rbs_hierarchy |
| Reference representation | Set name is not SetCode; Job display is not JobCode; person uses PersonNumber plus required context; Project Unit and Organization names plus copied context are passed to Fusion without FSCR class/date eligibility checks; Organization uses no OrganizationId; tested nonlabor/type/category fields retain names | Those actual resources supplied |  |
| Alias and element ordering | Root Alias equals requested Name; preview the tested Job parent when applicable and report element ordering | Every package |  |
| Package completeness | Seven flat task members and explicit Resource Class default tree for every created RBS | Every package | verify_rbs_task_export |
| Batch atomicity at preparation | Reject any invalid row before the single combined package is submitted | Multiple rows |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RBS.VALIDATE_INPUT | step | 1 | validate_input | valid->RBS.APPLY_DEFAULTS;invalid->RBS.RETURN_ISSUES | none | stop | Every requested create batch |
| RBS.ROUTE_OPERATION | decision | 3 | evaluate_result | supported->RBS.FIND_RBS;unsupported->RBS.RETURN_REFUSAL;invalid->RBS.RETURN_ISSUES | RBS.APPLY_DEFAULTS | stop | Only the observed new custom planning RBS create profile is supported by these authored rules |
