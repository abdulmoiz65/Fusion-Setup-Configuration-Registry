# Candidate Selection Process Reasons Input Validation

## Purpose

Defines the task input, field, translation, status, and package-shape checks that must pass before exact identity resolution or result verification.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | create_reason, update_reason, change_reason_status, create_group, update_group, change_group_status, maintain_translation, associate_reason, verify_result | Block | Provide one explicit supported operation | Every request |  |
| Current task baseline | Approved task-wide export containing ASM metadata and the five CSP CSV members | Block authoring and reconciliation | Export ORA_IRC_MANAGE_CSP_REASONS for the intended target and validate it | Every authoring or verification request | verify_csp_export_package |
| Reason create | ReasonCode, ReasonName, ReasonStatusCode | Block | Provide all required reason values | create_reason | resolve_existing_reason |
| Existing reason change | Exact ReasonCode and at least one supported non-code change or desired status | Block | Provide the exact persisted code and requested delta | update_reason or change_reason_status | resolve_existing_reason |
| Reason group create | ReasonGroupCode, ReasonGroupName, ReasonGroupStatusCode; optional ReasonGroupComments | Block | Provide all required group values | create_group | resolve_existing_reason_group |
| Existing group change | Exact ReasonGroupCode and at least one supported non-code change or desired status | Block | Provide the exact persisted code and requested delta | update_group or change_group_status | resolve_existing_reason_group |
| Translation | Exact parent code, Language, export-evidenced SourceLang, and translated name; translated group comments optional | Block | Provide explicit target-evidenced language values and approved text; copy SourceLang from the current export | maintain_translation | resolve_translation_context |
| Reason-to-group association | Exact ReasonCode and ReasonGroupCode | Block | Provide one exact pair | associate_reason | resolve_existing_association |
| Result evidence | Post-import task-wide export or sanitized ProcessLog | Block verification | Supply current result evidence for the intended target | verify_result | verify_csp_export_package |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A create ReasonCode is exactly present in the current export | Intent mismatch | Reclassify as update or already-satisfied replay only after confirming intent | resolve_existing_reason |
| A create ReasonGroupCode is exactly present in the current export | Intent mismatch | Reclassify as update or already-satisfied replay only after confirming intent | resolve_existing_reason_group |
| An update ReasonCode is absent or only a case-insensitive lookalike exists | Missing or ambiguous | Stop and request the exact persisted code; never normalize case | resolve_existing_reason |
| An update ReasonGroupCode is absent or only a case-insensitive lookalike exists | Missing or ambiguous | Stop and request the exact persisted code; never normalize case | resolve_existing_reason_group |
| A translation parent or Language is not evidenced in the target baseline, or SourceLang differs from the current exported row | Missing or inconsistent | Stop and obtain exact target evidence; never derive or change SourceLang through CSV | resolve_translation_context |
| A new association reason is absent or not Active | Invalid | Stop; activate an approved exact reason first or select another Active reason | resolve_existing_reason |
| A new association group is absent | Missing | Stop and provide an exact existing group | resolve_existing_reason_group |
| An exact association already exists | Already satisfied | Preserve one association row; do not create a duplicate | resolve_existing_association |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| ReasonCode shape | Require a nonblank case-preserved value of at most 30 characters; reject duplicate codes within the proposed package | A reason is defined or referenced |  |
| ReasonName shape | Require a nonblank value of at most 512 characters; duplicate names are allowed | A reason or reason translation is authored |  |
| ReasonStatusCode | Accept only ORA_DRAFT, ORA_ACTIVE, or ORA_INACTIVE and only a supported lifecycle transition | A reason is created or its status changes |  |
| ReasonGroupCode shape | Require a nonblank case-preserved value of at most 30 characters; reject duplicate codes within the proposed package | A group is defined or referenced |  |
| ReasonGroupName shape | Require a nonblank value of at most 512 characters; duplicate names are allowed | A group or group translation is authored |  |
| ReasonGroupComments shape | Allow omission; when supplied, require at most 1000 characters | A group or group translation is authored |  |
| ReasonGroupStatusCode | Accept only ORA_DRAFT, ORA_ACTIVE, or ORA_INACTIVE and only a supported lifecycle transition | A group is created or its status changes |  |
| Language and SourceLang | Require an installed target Language and values of at most 4 characters. Use Language to target the translated row. Preserve SourceLang exactly as evidenced for that row in the current target export because the FSM migration view marks SourceLang non-updateable. For a new reason or group, use the target base/source language evidenced by the current export; the verified US-base target produced SourceLang US for its installed-language rows. Never derive SourceLang from translation authorship or import language assumptions from another environment | A translation is authored | resolve_translation_context |
| Reason translation parent | Require the exact case-sensitive base ReasonCode in the package or approved target baseline | A reason translation is authored | resolve_existing_reason |
| Reason-group translation parent | Require the exact case-sensitive base ReasonGroupCode in the package or approved target baseline | A reason-group translation is authored | resolve_existing_reason_group |
| CSV member inventory | Require ASM_SETUP_CSV_METADATA.xml plus ORA_IRC_CSP_REASON.csv, ORA_IRC_CSP_REASON_TRANSLATION.csv, ORA_IRC_CSP_REASON_GROUP.csv, ORA_IRC_CSP_REASON_GROUP_TRANSLATION.csv, and ORA_IRC_CSP_REASON_USAGE.csv | A package is validated | verify_csp_export_package |
| CSV header and order | Preserve exact exported filenames, headers, metadata, and reason then group then usage order; translations remain nested under base records | A package is validated | verify_csp_export_package |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CSPRSN.VALIDATE_INPUTS | decision | 10 | validate_input | valid->CSPRSN.CLASSIFY_REQUEST;missing->CSPRSN.HANDLE_ISSUES;invalid->CSPRSN.HANDLE_ISSUES;unsupported->CSPRSN.HANDLE_ISSUES | none | stop | Every Candidate Selection Process Reasons request |
| CSPRSN.CLASSIFY_REQUEST | decision | 20 | evaluate_result | authoring->CSPRSN.RESOLVE_REFERENCES;verification->CSPRSN.VERIFY_RESULT;unsupported->CSPRSN.HANDLE_ISSUES | CSPRSN.VALIDATE_INPUTS | stop | Classify the validated request as authoring, verification, or unsupported |
