# Dependency Readiness

For a supplied CSV pass-through import, require only the dependencies needed to
route and transport the unchanged bytes:

| Sequence | Dependency | Requirement |
|---|---|---|
| 1 | Target | Resolve one exact environment, session, and upload/import privileges. |
| 2 | Object routing | Resolve the exact Import Management object code without inspecting data columns or rows. |
| 3 | Mode routing | Resolve exactly one job-level `ImportMode`: `CREATE_ONLY`, `CREATE_RECORD`, or `DELETE_RECORD`. Do not infer it from CSV content and do not rely on an implicit default. |
| 4 | Source transport | Retain the ordered nonempty `.csv` sources and compute the immutable group hash from exact filenames and bytes. |
| 5 | Live import metadata | Confirm `ImportSupport=Y` for the exact object and resolve its current UCM account. |
| 6 | Core source review | Run non-mutating Core Data Loader preflight without approval flags and retain its envelope and reviewed ZIP outside `project/`. Its archive digest identifies the ZIP, not the CSV group. |
| 7 | Reconciliation and single approval | Run Core `prepare-import` for the exact ordered CSVs, then `scripts/reconcile_tca_import_preview.py`. After matching bytes/order/target/object/mode/account, use the adapter manifest group digest in Task Hook `finalData.archiveSha256`; retain the Core ZIP digest separately. Obtain one exact-artifact approval and record it with `approve-import`. Do not call the physical-archive verifier for a CSV group. |
| 8 | Mode-aware execution | Invoke `execute-approved-import` with the protected `--approval-id` and exact approved local CSV group, `ImportMode`, UCM account, activity name, activation, and schedule. The Core adapter verifies the envelope, source bytes, order and settings, checks current target metadata, consumes approval once, and uploads verified in-memory bytes without automatic mutation retries; never repeat the upload after an uncertain outcome. |

Do not establish data-derived dependencies for a supplied CSV. Parent records,
lookups, field requirements, hierarchy setup, identity sets, duplicate checks,
or volume policy are not pass-through preflight gates. Job-level `ImportMode`
selection remains mandatory because it controls the activity operation without
inspecting CSV data.
Never request a data-validation waiver.

An explicit supplied `Hierarchy` or `HierarchyNode` delete has no additional
row-derived dependency. Exact-object `ImportSupport=Y`, mode-aware
`DELETE_RECORD` readiness, immutable preview, and destructive approval are the
submission gates; Fusion decides whether the rows are valid.

For CSV generation or an explicit data-validation request, apply the object
dependencies and sequencing in `references/object-profiles.json` before
freezing the generated/validated artifact.
In that optional branch, create a separate manifest entry for every requested parent instance.
For hierarchy generation, require direct target evidence for
the tree structure; if absent, route `ORA_HZ_MANAGE_TREE_STRUCTURES` before
`HZ_MANAGE_HIERARCHY_TYPES`. If either route is unavailable, record the workflow gap and stop.
For a generated or explicitly validated Hierarchy or Hierarchy Member delete,
also require an exact pre-delete target match and current target-specific
evidence that the selected object accepts `DELETE_RECORD`. This evidence gate
is required because the current Oracle object-specific pages document Hierarchy
create/update and Hierarchy Member create/update, but do not explicitly promise
delete support.

For a generated or explicitly validated Additional Identifier delete, require
the exact selected party parent and one exact pre-delete child match for the
supplied `PartyIdentifierId`. Preserve that parent and identifier identity
through approval, execution, and post-import verification.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TCA.DEPENDENCIES | decision | 3 | resolve_dependency | satisfied->TCA.METADATA;blocked->TCA.RETURN_ISSUES | TCA.DEFAULTS | stop | Resolve transport dependencies for supplied CSVs; add object-data dependencies only for generation or explicit validation. |
