# Supported coverage and remaining capabilities

This is an assisted, conditionally executable FSM package. It provides local
domain checks and delegates export, full Task Hook validation, immutable
approval, import and independent readback to existing shared/core workflows.
The local helpers neither connect to Fusion nor approve or submit changes.

Package readiness applies to this declared scope. It is not certification of
full UI parity, current pod inheritance, every object/classification, or a live
write. Runtime refusal for an unsupported operation or unavailable current
evidence is a valid outcome; never report it as business success.

## Current scope

| Intent | Available behavior | Required runtime evidence |
|---|---|---|
| Read / export | Resolve named current identities or export the selected task | Same-target complete identity coverage where required; native detail gaps remain visible |
| PROJECT create | Resolve allowed classification; materialize current controls or explicitly disclosed standard configuration | Current identity, dates, exact template, control basis and all normal task/import gates |
| Other addable objects | Prepare only the fields and inherited values supported by the field matrix | Current inherited weight where required and a verified native creation-field route; otherwise stop |
| Ordinary update / end-date / action Allow | Preserve identity and all unrequested values; validate object/classification editability | Current baseline, relevant use-state, actual controls and exact field/child diff |
| Lifecycle append | Prepare the complete old-plus-new target set without removing or reinterpreting rows | Verified current mode/set, same-object U identities or exact S bridges, normal native package checks |
| Workflow change | Prepare supported flag/outcome edits while preserving fixed or protected fields | Actual outcome codes and baseline; requests that require unverified clearing remain refused |

## Tracked capability follow-ups

| ID | Capability outside this release | Why it stays guarded | Evidence needed to enable it |
|---|---|---|---|
| PSTATUS.FOLLOWUP.RENAME | Rename an existing status | Native object/name is an alternate key; a new name alone can identify a different record | Supported old/new identity mapping; controlled rename proving the same stored identity, with no duplicate and correct translations/children |
| PSTATUS.FOLLOWUP.CLEAR | Clear stored scalar or workflow outcome values | Blank/null import semantics are not established | Exact channel clear representation; controlled readback proving cleared fields and preservation of unrelated values |
| PSTATUS.FOLLOWUP.LIFECYCLE | Remove/replace targets or change the type of existing child rows | CSV row omission is not a verified removal/rekeying operation | Supported mutation contract and complete post-write target/mode equality; do not substitute a smaller CSV |
| PSTATUS.FOLLOWUP.SBRIDGE | Every classification-mode target | Some classification codes lack the exact native name/code bridge | Verified task-native representation for each missing bridge; never substitute a custom or prefixed status |
| PSTATUS.FOLLOWUP.CURRENT | Exact current inherited controls, progress weight and use-state on every target | Standard configuration and identity reads do not establish those current values | Supported complete same-target read contract and provenance; retain strict evidence gates until supplied |
| PSTATUS.FOLLOWUP.CERTIFICATION | Full release-specific source closure and expanded live regression certification | Local tests validate local behavior; prior executions do not certify a changed version | Complete relevant source/dependency evidence and approved exact artifacts, one submission and independent readback for each newly enabled scope |

Delete is excluded from the execution scope. These follow-ups do not authorize
core changes, new external calls, UI execution, raw database access, or new
import semantics. A future capability change requires fresh task evidence,
resource authoring, tests and review. Until then the request must stop at its
named guard.

## Local verification

Run both task-local test modules through `python3 -m unittest discover -s
<task-folder>/tests -v`, then compile the registry, validate its plan without an
override, and run the Skill Merge Auditor. Test coverage includes early refusal,
implicit rename/clear detection, complete append sets, removal/type-switch
holds, explicit false values, identity coverage, control defaults and separate
input-versus-evidence diagnostics. These checks are not live Fusion tests.

One prepared happy-path prompt is: "Prepare a new Active project status named
EXAMPLE_STATUS, effective 15 October 2026, with no outgoing transitions." Resolve
absence in the selected sandbox before using a concrete unique name. The
expected preview has Initial=N, Workflow=N, next type=N, blank To Date and
explicit control rows with their basis disclosed. Preparation is not creation;
submission still needs the normal immutable-artifact approval.
