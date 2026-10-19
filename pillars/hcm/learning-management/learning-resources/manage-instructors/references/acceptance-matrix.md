# Acceptance matrix

Local implementation and offline tests do not certify DL_ENV. No live instructor
creation has been performed by this increment. See the project validation report
for actual command outcomes; this table defines the implementation boundary.

| Case | Local coverage | Target / remaining work |
|---|---|---|
| IN-AT-01 missing person | Reject missing/inferred identity; no recommendation | No live call needed |
| IN-AT-02 exact number/ID/full name | String preservation, literal matching, ambiguity, no match | Verify workersLov metadata and target query semantics |
| Partial names | Bound discovery, explicit version-bound selection even one, fresh exact ID required | Case/accent/minimum-input behavior unverified |
| Independent discovery | Environment/origin and input validation; lookup/duplicate GETs independent of incomplete create graph; no write readiness | Account-scoped live search required; no-match is not global absence |
| IN-AT-02 email and broad files | Explicit refusal rather than guessed contract | Email and optional file-reader coverage deferred |
| IN-AT-03 duplicates | Complete per-person baseline, alias/batch dedup; no uncertain-write replay | Live concurrent duplicate rejection/readback pending |
| IN-AT-04 suppliers | Supplied supplier blocked, not silently omitted | Supplier functionality deliberately excluded |
| IN-AT-05 inactive workers | ACTIVE only; suspended/inactive blocked | FDD/UI conflict unresolved |
| IN-AT-06 Set/DFF | Explicit project Set deferral plus current optional-global DFF metadata supports root-only preflight; unknown/required/defaulted/context-specific values block | Set-enabled and custom-input mappings unsupported; successful load/readback still required |
| IN-AT-06 materials/accounts | No child records in minimal ZIP | Out of scope; broader FDD incomplete |
| IN-AT-07 proposal revision | Fingerprints, exact archive/row binding, stale selection rejection | Live exact approval and partial-load acceptance pending |
| Shared services | Fixed GET CLI, Learning Common rule planner, shared loader/Task Hook boundaries | Complete positive preparation awaits target and configuration evidence |
| Readback | Unique person relation, generated IDs, supplier omission, instructorStatus | Live field/default and scheduling acceptance pending |
| Privacy | Synthetic tests, no response bodies in error messages | Keep real-person state outside project and tracked files |

Regression invariants: no core/router/catalog/sibling edits or imports; no private
HTTP client, direct instructor POST, override flag, automatic polling or replay.
Future live single: nominated eligible person, verified prerequisites, exact load
approval, one submission, separately requested status and unique readback.
Future live batch: only after single acceptance; bounded rows and per-row outcomes,
never infer batch acceptance from a single successful instructor.
