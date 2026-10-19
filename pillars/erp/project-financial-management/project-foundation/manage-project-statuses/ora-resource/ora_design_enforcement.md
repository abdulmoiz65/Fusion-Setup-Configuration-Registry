# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Protect identity and capabilities | Resolve object/name across classifications; distinguish create permission, field editability and lifecycle permission |
| 2 | Enforce dates and Initial eligibility | Validate range, protect the seeded Active status and apply use warnings; do not impose one Initial status per object |
| 3 | Validate lifecycle | Match type and children, same-object targets, confirmed edge changes and disclosed cycles |
| 4 | Validate workflow and controls | Apply classification-specific workflow exceptions; preserve fixed outcomes and inherited control restrictions |
| 5 | Protect package and approval | Native two-pass contract, exact diff, immutable checksum and approved route |

Evaluate only the evidence supplied. Missing downstream workflow mappings can be deferred to Fusion service validation with disclosure. Missing required identity, defaults unresolved under the selected policy, package or clear/delete semantics blocks affected changes. Standard-source PROJECT create controls are explicit configuration, not deferred or passed current-inheritance checks. Deferred checks are never passed checks.

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Operation scope | Blocker | check_project_status_operation_scope | Local scope result is unsupported, invalid or still needs a required baseline | Return the exact reason before preparing an import; scope eligibility still requires all following task checks | No |
| Create | Blocker | find_project_status | Name already exists under the same StatusType, even in another classification; or absence cannot be established from scoped evidence | Choose a unique name and obtain identity coverage | Yes |
| Create or field update | Blocker | resolve_status_capabilities | Pair cannot be resolved; creation is disallowed; or a requested field is read-only for that object/classification/status | Preserve protected fields and describe allowed edits | No |
| System-owned fields or predefined classification | Blocker | find_project_status | Attempt to change predefined flag, generated identity or audit fields, or reclassify a predefined status | Preserve target-owned values | No |
| Existing lifecycle update | Blocker | resolve_status_capabilities | Object lacks lifecycle capability; do not use creation permission as this gate | Update only a supported existing lifecycle | No |
| Date range | Blocker |  | EndDateActive precedes StartDateActive | Supply a valid range | Yes |
| End-date | Blocker | find_project_status | Request targets the seeded Active project status | Preserve its end date; do not confuse it with all custom Active-classification statuses | No |
| Initial flag | Blocker | resolve_status_capabilities | Object disallows Initial, or Initial=Y and EnableBpFlag=Y are requested together | Clarify mutually exclusive behavior | Yes |
| Initial or end-date change on an in-use status | Warning | resolve_status_graph | None solely from use; UI warns about affected projects/templates | Disclose affected use and obtain acknowledgement in the exact preview | No |
| Lifecycle shape | Blocker | resolve_status_graph | S/U has no target; U target or workflow outcome belongs to another object; S classification is not valid for the parent object; A/N contradicts explicit children | Validate business target scope separately from S transport bridge; materialize all required child rows with exact parent columns | Yes |
| S-mode native bridge | Blocker | resolve_status_graph | No unique current status identity has ProjectStatusCode equal to the requested parent-object classification code | Report that exact classification as unencodable through this CSV route; never substitute a custom or prefixed seeded status code | No |
| Lifecycle append or replace | Blocker | resolve_status_graph | A replacement, S/U reinterpretation, type switch or empty target set requires removal/rekeying of existing children without verified import semantics | Preserve old rows for a genuine append; compare the complete post-write target set. Do not drop old rows and call the result replacement | No |
| Ordinary lifecycle cycle | Warning | resolve_status_graph | None solely from a cycle; reopening can return to an earlier status | Explain the cycle and confirm intended lifecycle | No |
| Workflow | Blocker | resolve_status_capabilities | Enable or outcome change is outside the full field matrix; editable enabled workflow lacks both outcomes; requested stored clear has no verified loader semantics | Preserve read-only SOV fields and the exact MS_SUBMITTED exception; no capability-only override | Yes |
| Workflow target identity | Blocker | resolve_status_graph | A target name/code is unresolved, ambiguous, wrong-object, guessed from classification, or belongs to a new status whose actual code is not available | Resolve current code/name identity through the declared lookup; stage new target creation before a separately approved workflow update | Yes |
| Workflow recursion | Blocker | resolve_status_graph | Available evidence proves self-triggering or an unbounded approval loop | Correct outcomes; classify as an FSCR execution safeguard, not a general ban on lifecycle cycles | Yes |
| Controls | Blocker | resolve_status_controls | Unsupported/missing action row, PROJECT/CLOSED Allow change, incomplete requested all-action set, or EnabledFlag used as the Allow switch | Resolve action labels to object-scoped ActionCode. Apply every explicit Y/N to AllowOverridesFlag; preserve EnabledFlag, copy, sort and control dates. Repairs need verified original values and exact approval | Yes |
| PROJECT create control basis | Blocker | resolve_status_controls | Exact-inheritance lacks current source controls; standard source is used for an existing update or another object; inconsistent current control evidence is replaced with defaults; or standard basis/warning is omitted from the immutable preview | Prefer current exact classification rows. Only a missing source parent permits the standard create mode. Preserve policy and basis in the blueprint outside native CSV columns; approval covers the exact disclosed values | Yes |
| Progress creation | Blocker | resolve_progress_weight | Inherited classification weight unavailable | Supply verified inherited weight | No |
| Native identity rename, delete, child removal or persisted clearing | Blocker | verify_project_status_package | Selected loader has no verified operation/presence semantics | Prepare guidance only; do not silently turn an update into a create | No |
| Import | Blocker | verify_project_status_package | Native structure, field mapping, checksum or Data Loader approval is invalid | Rebuild and approve the exact artifact | Yes |
| Independent completion check | Blocker | verify_project_status_package | Status only initiated; current readback lacks a requested child, has a different complete target/control set, or has wrong workflow codes despite successful import | Compare against the original normalized business request, not just the generated payload. Report failed verification and reconcile before correction; no automatic resubmission | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| check_project_status_operation_scope | Input and current baseline resolved | Scope result, explicit change shape and complete lifecycle set comparison | ora_reference_lookups.md |
| find_project_status | Create/update | Identity, seed coverage and existing values | ora_reference_lookups.md |
| resolve_status_capabilities | Every change | Allowed creation, fields and lifecycle | ora_reference_lookups.md |
| resolve_status_graph | Behavior/end-date | Targets, date/use findings and warnings | ora_reference_lookups.md |
| resolve_status_controls | Project creation or control change | Current or standard create rows, policy, basis, inheritance verification and editable Allow flags; current baseline required for updates | ora_reference_lookups.md |
| resolve_progress_weight | Progress creation | Classification's inherited weight | ora_reference_lookups.md |
| verify_project_status_package | Import | Native field/presence contract and checksum | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PSTATUS.ENFORCE_DESIGN | decision | 8 | design_enforcement | pass->PSTATUS.EXECUTION_GATE;blocked->PSTATUS.RETURN_REFUSAL;failure->PSTATUS.RETURN_ISSUES | PSTATUS.RESOLVE_DEPENDENCIES | stop | Before import approval; warnings and deferred checks stay visible |
