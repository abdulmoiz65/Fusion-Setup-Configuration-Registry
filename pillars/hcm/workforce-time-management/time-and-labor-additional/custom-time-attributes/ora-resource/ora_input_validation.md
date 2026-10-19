# Custom Time Attributes Input Validation

## Source Basis

- User-provided Generic FSM Baseline for Custom Time Attributes, 5 October 2026.
- User-provided Custom Time Attribute fields and dependent-attribute behavior.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Requested operation and scope | Create or Edit; explicitly identified task-specific change | Block | Obtain the intended operation and approved business scope; this does not approve import submission | Catalog-routed FSM request | |
| Attribute identity | Display Name | Block | Supply Display Name; Name is generated in uppercase | Parent and each dependent attribute | |
| Classification | Without dependent attributes; With dependent attributes | Block | Select one classification | Parent attribute only | |
| Data Type | Text; Number; Date; Time stamp | Block | Select one data type | Parent and each dependent attribute | |
| Default Filtered Data Source for Time Entry | Selected filtered data source | Block | Supply and resolve the source using the documented contract when available | Parent and each dependent attribute | resolve_filtered_data_source |
| Default Unfiltered Data Source for Setup Tasks | Selected unfiltered data source | Block | Supply and resolve the source using the documented contract when available | Parent and each dependent attribute | resolve_unfiltered_data_source |
| Attribute Category | Selected category | Block | Supply and resolve the category using the documented contract when available | Parent attribute only | resolve_attribute_category |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Operation is outside Create or Edit | Stop; the supplied baseline does not authorize other operations | FSM request | |
| Display Name is blank | Reject the attribute | Parent and each dependent attribute | |
| Classification is outside the two supplied choices | Reject the classification | Parent attribute only | |
| Data Type is outside Text, Number, Date, Time stamp | Reject the data type | Parent and each dependent attribute | |
| Description is omitted | Accept; Description is optional | Parent and each dependent attribute | |
| Unit of Measure is omitted | Accept; Unit of Measure is optional | Parent attribute only | |
| Unit of Measure is supplied outside Hours or Units | Reject the value | Parent attribute only | |
| A dependent attribute includes Classification, Unit of Measure, or Attribute Category | Reject these fields for the dependent attribute | Dependent attribute only | |

## Stage Boundary

Missing business rules must be resolved before execution. CSV member names,
keys, relationships, and reconciliation selectors are inspected after the
fresh same-task export. Do not treat the absence of a not-yet-obtained export
as an input-validation failure or invent task-specific behavior from this
generic baseline.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CTA.VALIDATE_INPUT | decision | 10 | validate_input | valid->CTA.RESOLVE_FILTERED_DATA_SOURCE;blocked->CTA.HANDLE_ISSUE | none | stop | A Custom Time Attributes Create or Edit is requested |
