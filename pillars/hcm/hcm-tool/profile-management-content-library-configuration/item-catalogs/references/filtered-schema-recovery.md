# Filtered Item Catalog schema recovery

Read this when a reusable same-task template is missing, or a separately
requested export encounters an unrelated catalog's `RatingModelId` /
`HRC-1035539` failure. This is an optional, separately approved data-export
investigation, not a pre-import requirement or automatic fallback. Preserve the
[skip-pre-import policy](optional-export-policy.md), data-handling restrictions,
and all package/provider/Core Data Loader approval boundaries.

## Select the supported export

Route through `shared.setup-export.task-level-export` and its shared FSM CSV
engine, with Core authentication and the parent operation-scoped preflight.
Use a **data export**, not `--template-only`: the existing template/spec export
route does not accept selection criteria. A metadata-only ZIP missing the CSV
members is not a usable template, even if a completion flag is true.

For the explicitly selected **Licenses and Certifications** catalog, the tested
criteria are below. Pass this JSON array through the owning helper's
`--export-criteria-file`; it supplies the task/process wrapper. Both attributes
belong to `Set1` (AND), with no wildcard. These are product-source fields and a
seeded content-type identity, not a guessed target catalog ID.

```json
[
  {
    "TaskCode": "ORA_MANAGE_PROFILE_ITEM_CATALOG",
    "BusinessObjectCode": "ORA_TALENT_PROFILE_ITEM_CATALOG",
    "AttributeSet": "Set1",
    "AttributeName": "ContentTypeId",
    "AttributeValue": "103"
  },
  {
    "TaskCode": "ORA_MANAGE_PROFILE_ITEM_CATALOG",
    "BusinessObjectCode": "ORA_TALENT_PROFILE_ITEM_CATALOG",
    "AttributeSet": "Set1",
    "AttributeName": "ValueSetName",
    "AttributeValue": "Licenses and Certifications"
  }
]
```

Do not apply this selector to another context/catalog or silently replace a
user-supplied name. Other selectors require source-backed field and identity
resolution. `ContextName` is transient in the catalog export VO; do not substitute
it as a SQL selection attribute. Unknown attributes may be ignored by the
provider, so accepted submission alone does not prove filtering worked.

Present the exact target, complete request and hash for approval after preflight.
Submit once. Do not retry the POST, broaden to an unfiltered export, repair the
database, or change Rating Models under that approval. Filtering is scope
selection, never a bypass of data-handling rules or complete-evidence gates.

## Resolve the existing process, not a new export

Delegate polling and downloads to the owning shared export engine; retain its
process ID and a bounded 300-second polling ceiling. `ProcessCompletedFlag=true`
and a zero-row result collection are not success evidence. This combination was
observed even though the direct result resource reported `COMPLETED`.

Within the status workflow, use the engine's `result_resource(scope, process_id)`
for a status-only GET of the **same** process when its collection is empty. Bind
the returned ProcessId to the accepted ID. Use its `download_result` for
ProcessLog and FileContent. This is an existing-resource read, not a submission
retry or a separate pillar transport implementation.

Require a terminal StatusCode: `COMPLETED_ERRORS` is failure regardless of CLI
exit status, completion flag, or partial ZIP. Review warnings for
`COMPLETED_WARNINGS`; do not claim clean success from that code alone. Unknown
status, missing direct result, or exhausted polling remains incomplete; report
the target alias, task, ID, last status, elapsed wait and a status-only next step.
Retain the log when available. Do not infer success from download availability.

## Validate schema and actual scope

Use `shared.validation.setup-data-validator` with the parent's local
`scripts/profile_content_library_fsm_evidence.py`, `--purpose schema`, and the
actual source/target aliases. **Do not set `--unfiltered-task-export`.** Require
safe ZIP members, same-task XML metadata, and exact observed CSV headers:

- `ASM_SETUP_CSV_METADATA.xml`
- `ORA_TALENT_PROFILE_ITEM_CATALOG.csv`
- `ORA_TALENT_CATALOG_CONTENT_ITEM.csv`
- `ORA_TALENT_CATALOG_CONTENT_ITEM_RDESC.csv`

For the selector above, require exactly one parent with the exact requested
`ValueSetName` and `ContextName=CERTIFICATION`. Check every child context and
exported parent-key link; reject unrelated/COMPETENCY rows or ambiguous parents.
Report actual row counts, including rating descriptions. Empty/header-only output
does not establish a resolved parent. Numeric `ContentTypeId` CSV cells can be
blank even when that filter succeeds: verify the exported portable context/name
and parent-child keys, disclose the missing numeric readback, and do not fill
generated IDs or modify headers to pass validation.

Keep schema eligibility separate from import eligibility. A validated filtered
archive can be reviewed as a format source under `kind: reviewed-template`,
subject to the package data-handling contract; it is not a full current-state
baseline, global duplicate-absence proof, complete readback, or provider
promotion evidence. Known observed collisions remain blockers. Never submit
the full export or retain its business rows in a reusable template; the approved
builder preserves validated metadata and constructs CSVs from approved rows.
This does not authorize copying customer-bearing exports into the project,
redacting them to bypass a handling gate, or package construction without its
separate approval. Missing data-handling authority remains a blocker.

## Evidence and limits

A controlled 2026-09-25 run completed with the exact selector above. Local checks
confirmed the four expected members and headers, one certification parent,
58 linked certification children, zero rating-description rows and no competency
rows. The retrieved log contained no `RatingModelId` / `HRC-1035539` error.
Those counts describe that observation, not required counts for future targets.
It verifies this scoped export, not repair of the excluded competency data or
acceptance of a later import. Target/process IDs, hashes and raw artifacts belong
in the owning run's sanitized evidence, not reusable skill source.

Source basis: `ItemCatalogMigrationAMImpl.java` applies the
`ORA_TALENT_PROFILE_ITEM_CATALOG` criteria by AttributeSet;
`ContentTypeValueSetVO.xml` defines persistent `ContentTypeId` and `ValueSetName`
and the ContentItem child accessor; `HrtProfileConstants.java` identifies
CERTIFICATION as content type 103; `HcmViewObjectImpl.java` applies criteria
before child traversal. The inspected 26.10 source index is provenance, not a
target-release gate or proof that every target has the same data. The
[Oracle data-export API](https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/op-fscmrestapi-resources-11.13.18.05-setuptaskcsvexports-post.html)
documents `SetupTaskCSVExportCriteria` and grouped attribute-value pairs.
