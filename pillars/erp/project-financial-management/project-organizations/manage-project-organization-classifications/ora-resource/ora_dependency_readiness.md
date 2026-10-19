# Dependency Readiness

**Omitted classification input means preserve existing state.**

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Existing identity/state | Complete governed REST identity and independent PTO/PEO existence before additions/defaults |
| 2 | Existing update identity only | Legacy single request: existing PTO with supplied permissions; bulk: also require update_existing_pto_permissions=true; no permission-value export |
| 3 | Owner/schema/mappings | Verify original update keys and metadata; persist keys only for new components |
| 4 | Submission | Immutable delta, approval, one core HDL initiation and registered acceptance binding; return In Progress without monitoring |
| 5 | Requested status/verification | A later explicit request resumes saved bindings; requested readback follows terminal success only; preserve partial results and separate maintenance handoff |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| PORGCLASS.IDENTITY | Existing organization/classifications | Yes | Every request | Lookup | Complete governed REST baseline | find_existing_project_organization | Prevent duplicates; omission depends on real state | Resolve one exact effective organization and all target classifications | identity and baseline |
| PORGCLASS.PTO_UPDATE | Original information-row identity | Conditional | REST-confirmed existing PTO with supplied permissions in a legacy single request; bulk additionally requires update_existing_pto_permissions=true on that entry | Lookup | Already registered original exported identity binding; no permission values | resolve_existing_pto_update_identity | HDL updates must address the actual row | Missing key blocks only an explicit existing update; bulk without opt-in bypasses this dependency; do not export to obtain flags | ExistingPtoInformation |
| PORGCLASS.OWNER | Valid source owner | Conditional | Mutation | Verify | Common lookup code; original owner for updates | verify_classification_source_owner | Preserve source identity | Create only confirmed missing new-component owner with approval | SourceOwner |
| PORGCLASS.SCHEMA | Target Organization metadata | Conditional | Mutation | Verify | Core metadata | verify_classification_schema | Valid headers/references | Validate changed segments and identity | HdlSchema |
| PORGCLASS.MAPPING | Parent link/new keys | Conditional | Mutation | Verify | Original update identity and new-component ledger | verify_classification_mapping | Never allocate new existing-row keys | Bind only requested new components to REST provenance | mapping/reference |
| PORGCLASS.ARCHIVE | Exact delta | Conditional | Submission | Verify | Generated request-derived DAT | verify_classification_archive | Protect scope/approval | Review exact payload/checksum | checksum |

No task export or current permission values are required for additions. Existing omitted permissions/PEO are preserved; total omission exits before mutation prerequisites. Parent creation and ESS remain separate.

For bulk processing, complete all organization baselines in the same validation run before preparation. Resolve owner/schema/parent references and original update identity independently for each active organization. Persist new component mappings with validation_run_id, baseline_collected_at and baseline_as_of_date plus existing organization/target/delta bindings. Supply one complete shared PersistedMappings ledger; proposal-only mappings never authorize generation. No-op entries require no owner/schema/mapping, artifact or approval. Each nonempty PEO/PTO ZIP independently requires Core Data Loader preflight, Task Hook preview, immutable approval and acceptance ID persistence; return In Progress without status reads. On a later explicit request, validate each saved project/target/task/role/request/archive binding before core status checks and requested terminal-success readback. Never allocate keys for a pure update or replay an accepted ZIP.

## Task Nodes
| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PORGCLASS.RESOLVE_DEPENDENCIES | step | 11 | resolve_dependency | ready->PORGCLASS.ENFORCE_DESIGN;failure->PORGCLASS.RETURN_ISSUES | PORGCLASS.VERIFY_SCHEMA | stop | Resolve original update identity and per-organization parent/schema/owner; complete shared ledger with fresh current-run bindings only for additions; skip no-op entries; never allocate keys for a pure update |
