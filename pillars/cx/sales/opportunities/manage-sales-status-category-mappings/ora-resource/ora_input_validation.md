# Manage Sales Status Category Mappings Input Validation

## FSM Task Identity Policy

Require exact task code/name, selected task `SKILL.md`, target environment, and
immutable archive SHA-256 throughout review, export, package preparation, and
validation.

- Review, export, and package preparation do not require Data Loader task context.
- Every Core Data Loader mutation handoff requires a persisted project
  `TaskContextPath`, exact `TaskName`, and positive `TaskSequence`.
- The selected context entry must resolve to this task's exact skill path,
  `TaskCode`, `TaskName`, offering, and functional area.

The persisted context may come from a project setup-task plan without creating
an Oracle Run Book. Never hand-author, infer, or synthesize it solely to satisfy
Data Loader.

Use these task-scoped rules for Manage Sales Status Category Mappings under the
Opportunities functional area. The source basis is Oracle's
[Sales Status Category Mapping](https://docs.oracle.com/en/cloud/saas/sales/oesws/salesstatuscategorymapping-d41e66075.html)
contract plus a fresh same-target task export for the exact existing mapping,
CSV members, headers, and current revenue-category flags. The supported
mutation route is an export-derived FSM package; no SOAP operation is an
executable route in this skill.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
| --- | --- | --- | --- | --- | --- |
| Existing status-category mapping update | OpptyStatusCategory, RevnOpen, RevnWon, RevnLost, RevnNosale, and a fresh same-target baseline row | Block package preparation | Provide one opportunity status category, all four proposed revenue flags, and export the current task from the exact target environment | Updating a mapping |  |
| Immutable package readiness | Exact target/release/task identity, completed `MOO_MANAGE_SALES_STATUS_CATEGORY_MAPPINGS` export receipt, exact `TaskName`, ASM identity, exact member/header receipt, reviewed four-flag row delta and state lock, unrelated-content receipt, final `PackagePath`, reopened `PackageSha256`, and validation result; require persisted `TaskContextPath` plus positive `TaskSequence`, resolved to the exact skill path, `TaskCode`, `TaskName`, offering, and functional area | Block Core Data Loader handoff | Export the exact task again, rebuild only the reviewed delta, reopen and hash the final ZIP, validate persisted Data Loader task context, and never hand-author or synthesize task context | Every Core Data Loader handoff | verify_status_category_mapping_package_readiness |

## Field Validation

| Check | What Happens | Applies When | Resolver |
| --- | --- | --- | --- |
| OpptyStatusCategory is blank, more than one baseline row matches it, or no baseline row matches it | Reject package readiness and identify the missing or ambiguous category evidence | Updating a mapping |  |
| Any proposed revenue flag is not Y or N | Reject package readiness and identify the invalid flag | Updating a mapping |  |
| The package changes a field outside the selected mapping's four revenue flags | Reject package readiness; preserve all identifiers, version fields, metadata, and unrelated mappings from the baseline | Updating a mapping |  |
| Target, release, export completion, or exact task code/name is missing or inconsistent, or a persisted project context has a blank task-context path or nonpositive sequence | Reject handoff and refresh the exact task export or selected project context; missing or inconsistent task context blocks handoff; never hand-author or synthesize task context | Every Core Data Loader handoff | verify_status_category_mapping_package_readiness |
| ASM identity, member inventory, CSV header spelling or order, row counts, reviewed delta, state lock, or unrelated-content receipt differs from the fresh baseline | Reject the complete package; do not repair metadata, normalize headers, or submit a valid subset | Every Core Data Loader handoff | verify_status_category_mapping_package_readiness |
| Reopening `PackagePath` does not reproduce `PackageSha256`, or the path/hash refers to evidence for another package | Invalidate readiness and rebuild and revalidate the immutable package | Every Core Data Loader handoff | verify_status_category_mapping_package_readiness |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OPP.STATUS_MAPPING.VALIDATE | step | 1 | validate_input | valid->OPP.STATUS_MAPPING.DESIGN;missing->OPP.STATUS_MAPPING.RETURN_MISSING;invalid->OPP.STATUS_MAPPING.RETURN_FAILED | none | stop | Every status-category mapping update request |
