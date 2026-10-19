# CAP terminal results and write refusal

A completed read/proposal branch is not a Data Loader validation. Never translate its ALL_GOOD terminal into passed write rules. Shared approval/uploader negative tests retain this boundary.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CAP-BATCH-READY | terminal | 380 | terminal | none | CAP-BATCH-DESIGN | stop | Retain unapproved batch preview; later exact consent before shared REST POST, then part verification and independent readback; no Data Loader approval reuse |
| CAP-I-DONE | terminal | 290 | terminal | none | CAP-I-READ | stop | Return sanitized root observation and child count completeness/limits; no job/access or write readiness inference |
| CAP-P-DONE | terminal | 50 | terminal | none | CAP-P-DESIGN | stop | Return draft/revision, source attribution, unknowns, next step and reply example; no external effects |
| CAP-R-DONE | terminal | 140 | terminal | none | CAP-R-GET | stop | Return complete accessible read result; no write eligibility |
| CAP-R-PARTIAL | terminal | 150 | terminal | none | CAP-R-GET | stop | Return partial/failed list with no total and safe next action; never claim completion |
| CAP-WRITE-BLOCK | step | 200 | execution_gate | unavailable->CAP-WRITE-UNAVAILABLE | CAP-SELECT | stop | Raw cap_workflow mutation requests stop; create/update use separate preparation and approved submission contracts; lifecycle and child writes unavailable |
| CAP-WRITE-UNAVAILABLE | terminal | 210 | terminal | none | CAP-WRITE-BLOCK | stop | UNSUPPORTED; report missing operation contract and shared safety requirements, zero side effects |
| CAP-CHECK-DONE | terminal | 195 | terminal | none | CAP-CHECK-LOADER | stop | Return assessed_writes_blocked with advertised metadata, unknown privileges/defaults and per-operation blockers; never approval-ready |
| CAP-CREATE-ARTIFACT | step | 240 | execution_gate | passed->CAP-CREATE-READY | CAP-CREATE-EVIDENCE | stop | Validate exact shared-prepared archive with cap_create_validation and bind inputs/evidence/source/task/target/Run Book; evaluate Task Hook resource results before building unapproved preview; no uploader execution |
| CAP-CREATE-READY | terminal | 250 | terminal | none | CAP-CREATE-ARTIFACT | stop | Await exact-load approval only after all evidence and artifact checks pass; write_eligible false; no upload, automatic approval or submission |
| CAP-UPDATE-ARTIFACT | step | 330 | execution_gate | passed->CAP-UPDATE-READY | CAP-UPDATE-DESIGN | stop | Validate one PATCH row and final shared ZIP; bind baseline/input/identity/evidence/target/Run Book and evaluate Task Hook results; no upload |
| CAP-UPDATE-READY | terminal | 340 | terminal | none | CAP-UPDATE-ARTIFACT | stop | Await exact-load approval with write eligibility false; later submission verifies frozen shared approval and refuses repeat attempts |

## Error Rules

| Failure Class | Situation | What Happens | Next Action |
|---|---|---|---|
| input_validation | Invalid selectors/proposal/file rows or incomplete intent | Stop before network, preserve missing facts without invented values | Request the exact missing/corrected field |
| catalog_mismatch | Stale/incomplete compiled graph or describe mismatch | Stop; no readiness override or alternate client | Resolve source/metadata mismatch and correct the task source and registry, then rerun the local plan |
| auth/authz | Shared login or GET rejected | Sanitize failure; never interpret denial as absence or write privilege | Use supported shared login/read-access recovery, no blind retry |
| transport/environment | Wrong target, forbidden redirect or failed shared request | Stop under shared configured-host policy; discard raw credential-bearing errors | Confirm configured target and authorized route |
| process_timeout | Metadata/page/auth exceeds budget | Terminate bounded shared-client subprocess; report partial list or failed exact query | Resume through a new bounded read; no complete/absence claim |
| approval_blocker | Missing create evidence, altered preview/artifact, missing exact approval or unsupported mutation | Raw cap_workflow refuses; only exact-approved cap_create_submission or cap_update_submission may call shared uploader | Complete preparation and approve its retained preview; no read promotion, alternate client or permission probe |
| artifact_persistence | Proposal/record write fails | Do not report saved; keep verified partial state | Explain what remains unsaved; do not silently overwrite history |

The separate approved submission continuation never re-executes this preparation
graph after approval. It checks frozen preview/ZIP/context integrity, retains a
durable target-plus-ZIP attempt marker before shared upload, and never retries an
uncertain result. A receipt failure after accepted initiation must report submitted
with known returned identifiers, not blocked/no effects. Retain recovery envelopes
on failure; retire internal envelopes only after accepted initiation and a verified
receipt. Shared explicit-rejection recovery remains owned by core, not this pillar.
