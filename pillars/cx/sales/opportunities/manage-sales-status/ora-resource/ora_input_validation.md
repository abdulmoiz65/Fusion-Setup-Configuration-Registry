# Manage Sales Status Input Validation

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

Use these task-scoped rules for Manage Sales Status under the Opportunities
functional area. The source basis is Oracle's
[Create and Change Sales Statuses](https://docs.oracle.com/en/cloud/saas/sales/fasqa/how-do-i-create-and-modify-sales-statuses.html)
guidance plus a fresh same-target task export for exact status identity, current
values, CSV members, and headers.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
| --- | --- | --- | --- | --- | --- |
| Sales status | Status Code, Status, Active, Status Category | Block package preparation | Provide a unique nonblank code and display value plus one predefined category | Creating a sales status |  |
| Immutable package readiness | Exact target/release/task identity, completed `MOO_MANAGE_SALES_STATUS` export receipt, exact `TaskName`, ASM identity, exact member/header receipt, reviewed `OPTY_STATUS` row delta and state lock, unrelated-content receipt, final `PackagePath`, reopened `PackageSha256`, and validation result; require persisted `TaskContextPath` plus positive `TaskSequence`, resolved to the exact skill path, `TaskCode`, `TaskName`, offering, and functional area | Block Core Data Loader handoff | Export the exact task again, rebuild only the reviewed delta, reopen and hash the final ZIP, validate persisted Data Loader task context, and never hand-author or synthesize task context | Every Core Data Loader handoff | verify_sales_status_package_readiness |

## Field Validation

| Check | What Happens | Applies When | Resolver |
| --- | --- | --- | --- |
| Status Code and Status are unique and nonblank | Accept for package design | Creating a sales status |  |
| Status Category is one of the four predefined categories | Accept for package design | Creating or changing a sales status |  |
| Target, release, export completion, or exact task code/name is missing or inconsistent, or a persisted project context has a blank task-context path or nonpositive sequence | Reject handoff and refresh the exact task export or selected project context; missing or inconsistent task context blocks handoff; never hand-author or synthesize task context | Every Core Data Loader handoff | verify_sales_status_package_readiness |
| ASM identity, member inventory, CSV header spelling or order, row counts, reviewed delta, state lock, or unrelated-content receipt differs from the fresh baseline | Reject the complete package; do not repair metadata, normalize headers, or submit a valid subset | Every Core Data Loader handoff | verify_sales_status_package_readiness |
| Reopening `PackagePath` does not reproduce `PackageSha256`, or the path/hash refers to evidence for another package | Invalidate readiness and rebuild and revalidate the immutable package | Every Core Data Loader handoff | verify_sales_status_package_readiness |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OPP.SALES_STATUS.VALIDATE | step | 1 | validate_input | valid->OPP.SALES_STATUS.DESIGN;missing->OPP.SALES_STATUS.RETURN_MISSING | none | stop | Every sales-status setup request |
