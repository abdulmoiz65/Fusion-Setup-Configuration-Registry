# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Prove the route | A fresh same-task export must establish the FSM CSV route and package shape. |
| 2 | Constrain the change | For an update, include the selected parent and its complete desired child collection. Preserve existing child rows exactly as exported unless the approved change modifies or removes them, and exclude other sets. |
| 3 | Validate the package | Validate the exact FSM ZIP against the fresh export and task-specific field rules. |
| 4 | Generate Complete Business Summary | Generate the Complete Business Summary and Defaults Applied only from verified structured business values after validation, lookup resolution, and defaulting. |
| 5 | Complete import preflight | Complete Core Data Loader validation, persist the immutable preflight artifact, and complete Task Hook validation for the exact ZIP. |
| 6 | Disclose the validated ZIP | Immediately beneath those tables, display one direct link to the exact validated ZIP. |
| 7 | Gate provider approval | Request one approval immediately before upload and import, after every validation gate passes. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Before package preparation | Blocker |  | No fresh same-task export or FSM route evidence | Stop and obtain a validated fresh export | Yes |
| Before Core Data Loader handoff | Blocker | resolve_questionnaire_lov | A supplied Questionnaire cannot be validated by one normalized exact match against export-confirmed authoritative LOV values | Obtain the authoritative LOV contract; do not infer a value or source | Yes |
| Before Core Data Loader handoff | Blocker | resolve_time_category_lov | A supplied Time Category does not resolve to exactly one returned TcatName from timeCategoriesLOV | Resolve the supplied value through the documented lookup; do not infer an ID or select a partial match | Yes |
| Before Core Data Loader handoff | Blocker |  | Name is blank; a populated attestation row has a missing or nonnumeric Processing Sequence; an Initiating Event is outside IN, OUT, Save, Submit, or Resubmit; or Display Level is blank or outside Day, Detail, or Time Card | Correct the attestation data before handing the ZIP to Core Data Loader | Yes |
| Before Core Data Loader handoff | Blocker |  | Metadata XML casing, task-scoped CSV, keys, or row scope is invalid | Rebuild only from the validated export | Yes |
| Before Core Data Loader handoff | Blocker |  | An update ZIP contains a parent or child row for another Time Attestation Set, omits an existing child row without an approved removal, or changes an existing child row outside the approved change | Rebuild the ZIP with the selected parent and complete reconciled child collection | Yes |
| Before Core Data Loader handoff | Blocker |  | The Complete Business Summary is absent, contains an unverified, blank, null, unused, metadata-only, or technical value, or omits a supplied business value or applied default | Regenerate the summary from verified structured values using business labels and display values only | Yes |
| Before Core Data Loader handoff | Blocker |  | The exact validated ZIP link is not displayed immediately after the Complete Business Summary and Defaults Applied | Display the direct validated ZIP link after the two tables, then hand the same ZIP to Core Data Loader | Yes |
| Any operation | Blocker |  | Proposed direct REST mutation, HCM Data Loader conversion, or unrelated exported-value change | Use only the declared FSM ZIP flow | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_questionnaire_lov | A Questionnaire is supplied in an attestation row | Questionnaire allowed value | ora_reference_lookups.md |
| resolve_time_category_lov | A Time Category is supplied in an attestation row | Time Category allowed value | ora_reference_lookups.md |

## Required Complete Business Summary Format

Generate the following business-only disclosure only after validation, lookup resolution, and defaulting. Include every verified business value provided by the user and every default actually applied. Omit blank, null, unused, and metadata-only values. Show populated child records only when they have values, and use business labels and verified display values only. Never show identifiers, codes, keys, internal identifiers, opaque links, request IDs, fingerprints, technical fields, REST fields, API paths, methods, payload fields, DAT columns, directives, discriminators, database columns, resolver names, rule IDs, task-node names, internal statuses, raw Boolean values, warnings, diagnostics, or technical notes.

```md
## Complete Business Summary
| Business Setting | Selected Value |
|---|---|
| <business label> | <verified business display value> |

## Defaults Applied
| Business Setting | Default Applied |
|---|---|
| <business label> | <verified default display value> |
```

## Validated ZIP Disclosure

Immediately beneath those tables, show a direct link to the exact validated ZIP. Display identifiers as resolved business display names, codes as verified business meanings, Boolean values as Selected or Not selected, Enabled or Disabled, or Yes or No, and internal statuses as verified business-friendly values such as Draft or Submitted. Keep technical values internally for validation and provider execution. Then hand that same ZIP to Core Data Loader, which owns the immutable preview, the single approval, and submission.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TAS_ENFORCE_FIELDS | step | 40 | design_enforcement | satisfied->TAS_CORE_DATA_LOADER_HANDOFF;blocked->RETURN_ISSUES | TAS_VALIDATE_LOVS | stop | Validation, lookup resolution, defaulting, task-specific package enforcement, Complete Business Summary, Defaults Applied, and validated ZIP disclosure have completed |
