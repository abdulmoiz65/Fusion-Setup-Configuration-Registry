# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Canonical task identity | The requester identifies Job Offer DFF / Job Offers Descriptive Flexfields | Stop as unsupported scope | Resolve `ORA_IRC_MANAGE_JOB_OFFERS_DESCRIPTIVE_FLEXFIELD` and `IRC_OFFERS_DFF` internally | Every request | |
| Explicit operation | Retrieve, Create, Update, Export, Validate, Preview, Import, Deploy, or Verify | Stop and request one operation | Do not convert Create to Update or Update to Create | Every request | |
| Exact DFF target | Global segment code; context code; or context code plus segment code | Stop and request the missing identity | Names, prompts, and descriptions are not business keys | Every filtered read or mutation | resolve_dff_export_model |
| Requested change scope | Exact requested fields and values | Stop as incomplete scope | Preserve every exported value not explicitly requested to change | Every mutation | resolve_dff_export_model |
| Fresh export evidence | Exact target environment, release, export timestamp, and immutable source artifact | Block the executable path | Produce a fresh task-level export before planning a package | Create, Update, Preview, Import, Deploy, or Verify | resolve_dff_export_model |
| Value-set authority | Exact identifier and approved authority contract | Block before preview or import | Supply an approved authoritative value-set source | A segment change specifies a value set or LOV | resolve_value_set_authority |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Create identity | Require zero case-sensitive exact technical-identity matches | Create | resolve_dff_export_model |
| Update identity | Require exactly one case-sensitive exact technical-identity match | Update | resolve_dff_export_model |
| Exported field contract | Validate exported data type, length, enum, requiredness, sequence, storage-column compatibility, display component, default mode, protected state, and translation behavior | Create or Update | resolve_dff_export_model |
| Value-set compatibility | Require a resolved approved value set compatible with the exported segment data type and display component | A value set or LOV is supplied | resolve_value_set_authority |
| Default SQL | Accept only syntax and parameters proven by the export or documentation; documented parameters include PERSON_ID and SUBMISSION_ID where applicable | A default SQL expression is supplied | resolve_dff_export_model |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IRC_OFFER_DFF.VALIDATE_SCOPE | step | 10 | validate_input | valid->IRC_OFFER_DFF.RESOLVE_EXPORT;invalid->IRC_OFFER_DFF.HANDLE_ISSUE | none | stop | Every Job Offer DFF request |

## Tested character-segment input contract

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Constant text value | For existing ValueSetCode 100 Characters require a string of at most 100 characters without control characters; preserve the existing CONSTANT mode | Constant text default update | resolve_dff_export_model |
| SegmentCode | Require a letter followed by up to 79 letters, digits or underscores | New context-sensitive character segment | |
| SegmentIdentifier | Require a letter followed by up to 79 letters or digits; disclose the exact resolved identifier | New context-sensitive character segment | |
| Character column | Require ATTRIBUTE_CHAR1 through ATTRIBUTE_CHAR90 and verified ownership availability | New context-sensitive character segment | resolve_dff_export_model |
| SequenceNumber | Require the supplied nonnegative integer of at most 9 digits; check uniqueness in the selected context | New context-sensitive character segment | resolve_dff_export_model |

These constraints describe the tested character-segment path. Do not extend its
100-character default rule to unrelated value sets or other default modes.
