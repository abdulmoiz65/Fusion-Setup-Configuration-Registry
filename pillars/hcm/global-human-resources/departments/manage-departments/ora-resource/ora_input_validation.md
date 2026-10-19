# Manage Departments Input Validation

## Purpose

Defines required inputs, conditional requirements, field checks, and validation routing for Manage Departments.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | get, create, edit, inactivate, or delete-effective-split | Block | Provide one supported operation | Every request |  |
| Existing department selector | Exact Department name | Block | Provide one exact Department name | get, edit, inactivate, or delete-effective-split | find_manage_departments |
| Create identity | Name | Block | Provide the department name | create |  |
| Department classification | ClassificationCode `DEPARTMENT` | Block | Supply the department classification row | create |  |
| Department classification name | `ClassificationName` `Department` in both the `Organization` and `OrgUnitClassification` rows when the current live loader template exposes that attribute | Block | Populate the exact classification display value on both rows | create |  |
| Effective context | Explicit EffectiveStartDate | Block | Provide one valid date for the logical object | create, edit, or inactivate |  |
| Effective-split deletion range | Exact existing Department, retained EffectiveStartDate, and last deleted EffectiveEndDate | Block | Resolve the complete affected history and provide the inclusive deletion range | delete-effective-split | resolve_department_delete_history |
| Edit changes | At least one explicit supported change | Block | Provide the intended change | edit |  |
| Inactivation context | Status `I` for the department classification | Block | Provide the inactive status | inactivate |  |
| Delete confirmation | Explicit confirmation of the displayed effective-split range | Block loader handoff | Show basic details and request confirmation | delete-effective-split | resolve_department_delete_history |
| Department EFF row | `FLEX:PER_ORGANIZATION_INFORMATION_EFF`, `OrgInformationContext`, and every configured multirow unique-key segment | Block | Complete the EFF row from the current loader contract | An OrgInformation row is supplied |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| An existing target does not resolve to exactly one effective department | Missing | Request one exact OrganizationId, code, or name | find_manage_departments |
| A create name matches an existing division, department, or project organization | Invalid | Stop the duplicate create and request a unique name | find_manage_departments |
| The supplied reference-data set is unresolved or inconsistent | Invalid | Correct the set before source preparation | resolve_department_set |
| The supplied location is unresolved or not effective on the department date | Invalid | Correct the location or create it first | resolve_department_location |
| The supplied action reason is unresolved or ineffective | Invalid | Correct the action reason | resolve_department_action_reason |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Loader Boolean value | For an included attribute declared by current loader metadata as Boolean or Flag, write true or Yes as Y and false or No as N; preserve Y or N; do not add an omitted attribute or change REST read values | A Data Loader mutation includes the attribute |  |
| Internal selectors and source-system keys | Do not request, display, or author an internal selector or source-system key to identify a Department for read, edit, inactivation, or effective-split deletion. Resolve one exact current Department using the supplied name; leave source-system columns blank unless the user explicitly asks to set or change that pair. | Read, edit, inactivate, or delete-effective-split | find_manage_departments |
| Date format | Normalize an unambiguous date to the loader date format; reject an ambiguous or invalid date | A date is supplied |  |
| Classification code | Require `DEPARTMENT`; reject another organization classification | create |  |
| Classification name | When the current live loader template exposes `ClassificationName`, require `Department` in both the `Organization` and `OrgUnitClassification` rows; reject an omitted or inconsistent value | create |  |
| Logical-object effective date | Apply the supplied EffectiveStartDate to the Organization row and every included child row | Every mutation |  |
| Mutation source scope | For create, edit, or inactivate, keep the Organization and OrgUnitClassification rows. Omit OrgInformation unless the user explicitly requests an Organization Information/EFF change. When explicitly requested, use the full generated Organization XLSX and include only the operation-required identity, parent, date, classification, flex/context controls, multirow identity, and modified or required segments from the resolved context; exclude other contexts and optional unchanged segments. Let Core convert the reviewed XLSX internally to DAT/ZIP; do not hand-author the DAT. For delete-effective-split, use the full generated Organization XLSX with only the resolved `OrganizationId`, retained EffectiveStartDate, inclusive EffectiveEndDate, one operation-required `OrgUnitClassification` association, and exactly one `SET PURGE_FUTURE_CHANGES Y` row in `Data Loader Directives`; omit OrgInformation and non-key attributes. | create, edit, inactivate, or delete-effective-split |  |
| Effective alignment | Reject a classification effective start date later than its Organization effective start date | create |  |
| Classification status | Accept only `A` for an active create or `I` for inactivation | Status is supplied |  |
| Inactivation boundary | Inactivate only an unused department classification and give the Organization component the same effective date | inactivate |  |
| Date-effective split deletion | Allow deletion of one or more noninitial future effective splits only with an Organization `MERGE` row, at least one operation-required `OrgUnitClassification` association, and exactly one `SET PURGE_FUTURE_CHANGES Y` directive in the full generated XLSX `Data Loader Directives` sheet. Require the resolved OrganizationId as the loader-supported unique reference, EffectiveStartDate to identify the last record to retain, and EffectiveEndDate to identify the last record to delete. Reject a missing or misplaced directive, missing classification association, unresolved OrganizationId, HDL DELETE, first-row deletion, and an unbounded or misaligned range. | delete-effective-split | resolve_department_delete_history |
| EFF context discriminator | Require `FLEX:PER_ORGANIZATION_INFORMATION_EFF` and `OrgInformationContext` to contain the same deployed context code | An OrgInformation row is supplied |  |
| Multirow EFF identity | Require every flexfield segment marked as a unique key for the context; reject incomplete or duplicate combinations | A multirow OrgInformation context is supplied |  |
| Supported fields | Reject response-only IDs, audit fields, links, and fields absent from the registered Organization loader contract. A resolved OrganizationId is permitted only as the loader-supported unique reference for delete-effective-split. | A mutation value is supplied |  |
| Verification boundary | Do not treat source generation, transport, or load acceptance as business verification | Every mutation |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DEPT.VALIDATE | decision | 1 | validate_input | valid->DEPT.READ;missing->DEPT.ERROR;invalid->DEPT.ERROR;unsupported->DEPT.ERROR | none | stop | Every Manage Departments request |
