# CAP operation-specific technical readiness

No declared business-skill dependencies. Authentication and compiler are shared technical services; no HCM Filtered Lists. A ready graph includes known refusal branches and never establishes write eligibility.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CAP-I-PREREQ | step | 270 | resolve_dependency | passed->CAP-I-READ | CAP-I-VALIDATE | stop | Source-current compiled graph and exact shared configured target; read-only authorization |
| CAP-R-PREREQ | step | 110 | resolve_dependency | passed->CAP-R-METADATA | CAP-R-VALIDATE | stop | Before authentication or metadata |
| CAP-CHECK-PREREQ | step | 170 | resolve_dependency | passed->CAP-CHECK-ROOT | CAP-CHECK-VALIDATE | stop | Same source-current graph and configured environment/origin checks before read-only contract inspection |
| CAP-CREATE-EVIDENCE | step | 230 | resolve_dependency | passed->CAP-CREATE-ARTIFACT | CAP-CREATE-VALIDATE | stop | Require verified registration/template/writable fields, identity/defaults/dates/contributor-free access, complete duplicate check, pending-processing acceptance and active Run Book; privileges use verified grants or attributed shared-enforcement assessment with no known denial; shared preflight must pass before preview, unproven grants remain a warning |
| CAP-UPDATE-EVIDENCE | step | 310 | resolve_dependency | passed->CAP-UPDATE-DESIGN | CAP-UPDATE-VALIDATE | stop | Current target-bound registration/template/field/key/omission/date evidence, unique complete baseline, rename duplicates, shared privilege assessment and Run Book; GET success is not loader mapping proof |

## Create preparation evidence

The user accepted the existing shared loader transport, not unknown business
contracts or privileges. cap_create_handoff calls the unchanged shared loader
preflight without approval: exact BO/schema/template checks and immutable archive
preparation, then Task Hook data-load and build-data-load-preview. No POST or
approval command is selected. Evidence references must be target-bound and
hash-verified; a hash proves integrity, not the truth of an unverified assertion.
The evaluator must actually establish each fact from supported evidence. Never
use successful GETs, a generated preview, test fixtures or source-only role names
as current effective write grants. Privilege assessment may explicitly retain
unverified write access under the unchanged shared authorization workflow; see
references/create-source-contract.md. Known denials and missing assessments stop.
Only successful shared preflight permits preview, with residual authorization
uncertainty visible. No separate grant certificate or write probe is required.
Shared load_business_object_schema is the supported read-only template/component/
attribute route; allow_aliases=False and allow_attribute_schema_fallback=False.

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| CAP-READ-TARGET | Selected shared GET and confirmed environment | Yes | retrieve/list | Verify | Local shared configuration read through fusion_auth.read_properties; exact environment and restBaseUrl origin match request; unchanged planner ready/planned without override |  | A same-looking host or token is not target confirmation | cap_workflow preflights before launching the declared fusion_rest_client.py; use standard configured-HTTPS/host redirect policy | Confirmed environment/host, readable current graph and supported GET client |
| CAP-READ-ACCESS | Metadata and record access | Yes | retrieve/list | Verify | Current GET describe then actual collection response | describe_cap_root | Authentication failure is not absence and successful GET is not a write grant | Shared authentication handles its one allowed token refresh; report denied access or timeout without fallback | Collection GET, declared field types, selector queryability/finder if exact, observed access outcome |
| CAP-WRITE-UNAVAILABLE | Raw mutation route unavailable | Yes | raw cap_workflow mutations and unsupported lifecycle/child writes | Unavailable | cap_workflow.readiness and references/runtime-contract.md |  | Create/update require separate verified preparation plus exact-approved submission; other operation contracts remain incomplete | Never promote read readiness; use dedicated create preparation then shared approval continuation only when all facts pass | Pillar validation, frozen input/evidence/target binding, privileges, immutable archive approval; no transport override or core changes |
