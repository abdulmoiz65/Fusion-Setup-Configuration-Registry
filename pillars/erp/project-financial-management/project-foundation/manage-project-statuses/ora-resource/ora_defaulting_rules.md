# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| StartingStatusFlag (Initial Status) | N | Create, omitted | No |  |
| EnableBpFlag (Enable Workflow) | N | Create, omitted | No |  |
| NextAllowableStatusFlag | A (All) | Create, omitted | No |  |
| PredefinedFlag | N | New custom status only; not consultant configurable | Yes; reject a request to create seeded data |  |
| StartDateActive (From Date) | No default | Create | No; require explicit date |  |
| EndDateActive (To Date) | Blank | Create, omitted | No |  |
| Omitted scalar or child group | Carry forward baseline in the proposed diff | Update | No | find_project_status |
| PredefinedFlag, generated identity and audit fields | Preserve source values | Update | Yes; reject consultant attempts to overwrite protected values | find_project_status |
| PROJECT controls policy | prefer-current-else-standard; exact-inheritance when explicitly requested | Create PROJECT status only | No; preserve explicit exact-inheritance requirement | resolve_status_controls |
| Project action controls | Copy exact current classification's action codes, sort order and EnabledFlag when available; otherwise use the seven standard source rows under prefer-current-else-standard; CopyToUserStatusFlag=N | Create PROJECT status | No; explicit permitted Allow changes affect AllowOverridesFlag instead | resolve_status_controls |
| Project control AllowOverridesFlag (UI Allow) | N for DRAFT/CLOSED; Y otherwise | Create PROJECT status | No; honor an explicit permitted Allow choice; CLOSED remains protected | resolve_status_controls |
| ProjectStatusWeight | Copy selected progress classification's status weight | Create PROGRESS status | No; require verified inherited value | resolve_progress_weight |
| Workflow outcomes | No implicit accepted/rejected status | EnableBpFlag=Y except the submitted milestone exception | No | resolve_status_graph |

Defaults are create defaults, not update resets. Read and export operations do not apply defaults or materialize missing fields as current values. Materialize normalized create/update values in the immutable preview. The UI copies control rows and progress weight through its creation flow; do not assume FSM import invokes that flow. Standard-source controls are chosen configuration with unverified current inheritance, not a successful inheritance lookup. Under exact-inheritance, missing controls still block. Missing progress weight and missing current update values remain blockers under either policy.

## Conditional Changes

| Situation | What Happens |
|---|---|
| All selected | Transitions may go to any status; no explicit lifecycle rows are needed |
| None selected | No outgoing transitions; no explicit lifecycle rows are needed |
| Status selected | Resolve exact same-object status identities and materialize U-mode native child rows; setting only the parent flag is incomplete |
| Status Classification selected | Resolve parent-object classification codes and their exact native bridges; do not select arbitrary custom statuses in those classifications |
| Next Allowable Status Type changed with existing children | UI warns; confirmation removes existing lifecycle rows, rejection restores the previous type. A CSV change requiring removals remains blocked until that loader operation is verified |
| Workflow explicitly disabled in the enhanced editor | The UI listener resets accepted/rejected selectors, except the submitted milestone. Do not infer CSV blank/null clearing semantics; a requested persisted clear needs a verified route |
| Initial selected | Workflow control is disabled; do not set the opposite stored flag automatically |
| Workflow selected | Initial control is disabled; outcomes become required where editable |
| Workflow omitted on update | Preserve the existing flag and outcomes; disabling a field visually is not an update request |
| Accepted/rejected targets supplied by name | Resolve actual same-object status codes; no default or string-concatenation rule creates a workflow code |
| Existing legacy lifecycle value or read-only SOV workflow | Preserve exact stored values when omitted; do not apply create A/N/N defaults during update |
| All action Allow flags explicitly No | Materialize N for every existing permitted action; do not treat false as a missing value or change EnabledFlag |
| CR_DTL custom status created | Do not copy Project's seven actions; the Project control-copy method does not run for this object |
| Progress status created | Inherit its weight; do not assign a universal numeric default from one export row |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PSTATUS.APPLY_DEFAULTS | step | 4 | apply_default | applied->PSTATUS.RESOLVE_GRAPH;failure->PSTATUS.RETURN_ISSUES | PSTATUS.FIND_STATUS | stop | After object/classification and baseline resolution; resolve PROJECT create controls using the selected current-or-standard policy with basis disclosure, apply other create defaults or preserve updates; read/export performs no defaulting |
