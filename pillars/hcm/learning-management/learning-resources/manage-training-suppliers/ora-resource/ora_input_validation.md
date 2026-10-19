# Manage Training Suppliers Input Validation

## Source Basis

- OLC-116674 FDD, latest approved version; Jira OLC-120235 is traceability only.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Supplier identity | User-provided Name | Block the row before proposal | Ask for the supplier name; never generate or recommend it | Every requested supplier |  |
| Tenant-required configuration | Required flexfield segments and accessible Set when enabled | Block creation | Request only the configured missing values | Tenant configuration makes the value mandatory | validate_required_supplier_configuration |
| Recommended-field decisions | Description and Contact | Block proposal completeness, not supplier creation | Present each field as Recommended (optional) and record a value or explicit Skip; never describe either field as required | Before the versioned proposal |  |
| Optional-field decision | Administrator-only related material | Block proposal completeness, not supplier creation | Present URL or file as Optional and record a value or explicit Skip | Before the versioned proposal |  |
| Execution route choice | REST upload or Data Loader | Block proposal completeness, not supplier creation | Present both routes, recommend REST for one approved create row and Data Loader for multiple rows, and record the user's choice | Before the versioned proposal |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Contact is supplied | Resolve exactly one accessible HCM person or offer correction/removal | Continue with resolved contact or user choice | resolve_contact_person |
| Same-name supplier candidates exist | A name match is not a duplicate decision | Show identifiers and statuses; require use-existing or create-another choice | inspect_existing_training_suppliers |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Name is nonblank and user-provided | Trim accidental outer whitespace only; reject missing or generated names | Every row |  |
| Description intake label | Ask for Description as Recommended (optional), then record a value or explicit Skip; do not group it under Required or block creation when skipped | Every row before proposal |  |
| Description provenance | Accept user text; generate only from supplied context and label it skill-generated | Description is present or drafted |  |
| Contact intake label | Ask for Contact as Recommended (optional), accepting full name, person number, person ID, email, or explicit Skip; do not group it under Required or block creation when skipped | Every row before proposal |  |
| Contact identifier | Accept full name, person number, person ID, or email; never choose among multiple matches | Contact is supplied | resolve_contact_person |
| Set and flexfield intake | Label these Conditional; show the accessible Set and configured segment choices when enabled, identify configured required segments, and state Not applicable when the tenant does not expose them | Every row before proposal | validate_required_supplier_configuration |
| Related material intake | Ask for an administrator-only URL or readable file as Optional and allow explicit Skip | Every row before proposal |  |
| Related material validation | Require a valid URL or readable file; allow removal because the material is optional | Administrator-only material is supplied |  |
| Execution route | Accept only the explicit user choice REST upload or Data Loader; never infer approval from row count | Every proposal |  |
| System-populated values | Explain that status, supplier number, supplier ID, and audit fields are returned after creation; do not ask the customer to enter them | Every row |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TS.VALIDATE_INPUT | step | 1 | validate_input | valid->TS.RESOLVE_REFERENCES;invalid->TS.BLOCKED;failure->TS.FAILED | none | stop | After Name is supplied; Description, Contact, and Related Material each have a value or explicit Skip; conditional Set/flexfields are resolved; and the user selected REST upload or Data Loader, before preparing a training-supplier proposal |
