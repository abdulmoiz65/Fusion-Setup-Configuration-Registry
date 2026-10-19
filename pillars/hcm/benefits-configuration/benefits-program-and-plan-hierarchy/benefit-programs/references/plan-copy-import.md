# Benefits Plan Configuration REST Import

This skill imports an existing native Benefits plan package. It does not build,
extract, rewrite, or repackage the ZIP.
The catalog task is named Benefit Programs, but this route accepts only plan
packages (`ComponentObjType=PLN`). Reject packages with program setup rows.

The Benefits-owned adapter is
`pillars/hcm/benefits-configuration/benefits-common/scripts/benefits_plan_copy.py plan`. Select exactly one
`--template {401k,commuter}` or custom `--zip`; there is no implicit template
on this adapter. It selects the maintained Benefits wrapper, whose
plan-task check rejects another task's context or approval before execution.
Always use this Benefits-only entry point for plan requests under this skill's
standing routing exception. Do not ask for route permission again, require a
core route declaration, or modify core files. Retain all validation, active
Run Book, immutable preview and exact submission-approval checks; this is not
auto-approval. Use the same adapter and selection after the user approves the
preview. Direct local `validate` and
`report` operations do not import data and remain available on the pillar wrapper.

## Plan source intake

For generic plan-creation requests, offer the 401(k) template, Commuter
Benefits template, and a custom native Plan Copy ZIP. Follow
`../SKILL.md#plan-source-intake-and-workflow`: accept a current-request ZIP
upload or explicit local path directly; if custom is selected without a file,
ask for the upload or full path before preparing the package. Never limit
the intake to templates or substitute a template for a custom package.
Use `--zip "<end-user-plan.zip>"` instead of `--template` for preview and
approved execution, retaining the unchanged archive and all validation and
approval checks.

## REST sequence

Before creating the preview, ensure the selected active Run Book contains the
catalog-resolved Benefit Programs task using
`../SKILL.md#ensure-the-benefit-programs-task`. A context containing only
Eligibility Profiles is a recoverable prerequisite: use the declared core
Run Book merge workflow, refresh generated project artifacts after confirmed
success, and continue with the same selected package. Never substitute the
Eligibility Profiles task, hand-write a context, or bypass import approval.

1. Validate the ZIP and the reviewed OpenAPI contract locally.
2. Build an immutable approval preview containing the target, effective date,
   metadata, ZIP SHA-256, OpenAPI SHA-256, and package inventory. No Fusion
   write occurs during preview.
3. After a later standalone `approve`, re-read the same ZIP and OpenAPI files
   and verify that their hashes still match the preview.
4. `POST /hcmRestApi/resources/latest/benefitPlanCopyParameters` with
   `ComponentObjType=PLN` and `RequestSource=FDOS`.
5. `PUT` the ZIP bytes to the new row's `enclosure/PackageContent` endpoint.
6. `POST` the `generateMappings` action. For `RequestSource=FDOS`, this is the
   combined mapping/import request; do not call `submitImport`.
7. Poll the returned ESS request, require zero unresolved mapping rows, then
   verify that the Plan Copy parent reaches `ImportPlDesign=12`. Code `10` is
   an application failure even when ESS reports success.
8. Download
   `benefitPlanCopyParameters/{plCopyId}/enclosure/RequestLogs` as
   `application/octet-stream`. This enclosure exposes the consolidated import
   log stored in `BEN_PL_COPY_PARAMS.PARAM_ATTRIBUTE_BLOB2` after import; the
   parent REST JSON does not provide an inline `Log` field. Any recognized
   error in that log makes the import a failure, regardless of ESS or parent
   status. A successful import requires a non-empty log with no recognized
   errors in addition to ESS success and `ImportPlDesign=12`.
9. Parse the post-import `RequestLogs` Plan Copy Report and save its object
   inventory and log hash. Present the summary defined in
   `../SKILL.md#required-user-facing-after-import-summary` directly in the final
   response: business plan name, approved target/date, process status, and an
   inline `Object` / `Count` table using only import-log counts and their total.
   Do not display ZIP comparisons or verification statuses. A report link is
   supporting evidence, not a substitute for the table. Never infer counts
   from the ZIP or rerun an import just to produce its summary.

## Logs after an import error

When a Plan Copy ID has been retained, fetch
`benefitPlanCopyParameters/{plCopyId}/enclosure/RequestLogs` with a read-only
GET and `Accept: application/octet-stream` after an import, mapping, or ESS
error. Use the same target and authentication as the approved import. This
is the same consolidated log route used after success; a failed parent does
not prevent reading it, and empty `child/logs` is not evidence that it is absent.

Report sanitized seeded errors, including `JBO-BEN:::BEN_*` messages, alongside
the original failure and preserve internal recovery IDs. If the log is empty
or cannot be retrieved, state that specific limitation and retain the original
failure. Do not replace it with a log-download error or switch to database
diagnostics solely because child logs are empty. When creation failed before
an ID was returned, retain that failure without guessing an ID or issuing
another POST. Never rerun an import to obtain a log. Keep raw logs outside the
project; persist only their hash, parsed inventory, and sanitized error details.

All requests send REST framework version 9. Live POST and PUT calls are not
automatically retried. Preserve the Plan Copy and ESS request IDs after a
partial failure; do not submit a replacement package without a new preview and
approval.

Keep those IDs and the raw ESS state in internal recovery evidence only.
User-facing progress and completion output contains the approved Plan Copy
name and a `SUCCESS` or `ERROR` status derived from `MappingRequestStatus`.
Do not display the Plan Copy ID, ESS request ID, or ESS status. When status is
`ERROR`, include the sanitized error details extracted from `RequestLogs`.

Keep server-issued IDs and the exact approved metadata `Name` in internal
recovery state. Conversational previews, progress and completion identify the
plan by its business name from `planNames`, not the internal import or export
name. Do not show repository or FDOS branding to end users. Machine events and immutable
approval artifacts retain their original values; do not rewrite them for display.

## Greenfield template packages

Select `--template 401k` for `Greenfield 401k Plan.zip` (renamed archive;
the embedded export log still uses its original `_PLN.log` name), or
`--template commuter` for `Greenfield Commuter Benefits Plan.zip`.
Each template has its own log-derived date, inventory and preview filename.
Use the exact emitted preview path and same selection during approved import;
approval for one package never authorizes the other.

The `child/logs` collection is supplemental diagnostic data. It is not a
substitute for checking the consolidated `RequestLogs` enclosure.

`RequestLogs` may contain an empty Plan Copy Report even when the import
process reports success. In that case, state: "The import log did not report
object counts." Do not substitute ZIP counts. For a populated table, show only
the setup-object names and counts present in the import log, including explicit
zeros, and exclude mapping rows. Do not add source-only or missing-type rows,
before/after columns, or comparison commentary. Do not use the
`Objects with leading/trailing spaces` warning table as an import inventory.

Build the inventory from the embedded Plan Copy export log and require it to
match the nested XML package before presenting the preview. Retain the complete
inventory in the immutable artifact, but show only these log-derived counts to
the user: Plan, Plan Type, Option, Year Period, Eligibility Profile, Benefit
Group, and Age Factor. Omit zero-count objects from CLI and conversational
previews. This is display-only filtering; preserve the complete inventory in
the immutable approval artifact and retain internal machine evidence without displaying ZIP comparisons.
