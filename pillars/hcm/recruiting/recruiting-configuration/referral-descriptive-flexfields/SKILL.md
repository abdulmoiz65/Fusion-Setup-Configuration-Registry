---
skill_id: "hcm.recruiting.recruiting-configuration.referral-descriptive-flexfields"
name: "Referral Descriptive Flexfields Setup Task Guidance"
description: "Provides task-specific setup guidance for Referral Descriptive Flexfields under the Recruiting Configuration functional area."
layer: "pillar"
pillar: "HCM"
offering: "Recruiting"
functional_area: "Recruiting Configuration"
functional_area_code: "ORA_RECRUITING_CONFIGURATION"
task_code: "ORA_IRC_REFERRAL_DESCRIPTIVE_FLEXFIELD"
task_name: "Referral Descriptive Flexfields"
parent_skill_id: "hcm.recruiting.recruiting-configuration"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "hybrid"
owner_team: "HCM recruiting pillar team"
version: "0.4.5"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "interactive_segment_input"
  - "task_csv_export_artifact"
  - "retrieved_context_segments"
  - "final_fsm_archive"
  - "immutable_submission_preview"
  - "data_load_execution_result"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
persists_project_state: true
token_usage_tracking:
  enabled: true
  granularity: "per_skill_run"
  artifact_type: "token_usage_record"
  default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
  estimation_method: "chars/4 estimate unless exact tokenizer or API accounting is available"
  required_fields:
    - "activity_start_time"
    - "skill_id"
    - "task"
    - "trigger"
    - "artifacts_written"
    - "files_read"
    - "estimated_input_tokens"
    - "estimated_output_tokens"
    - "estimated_total_tokens"
    - "estimation_method"
    - "notes"
state_updates:
  - "setup_task_sequence"
  - "configuration_blueprints"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-configuration/referral-descriptive-flexfields/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-configuration/referral-descriptive-flexfields/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "May create and download a read-only Referral Descriptive Flexfields task CSV export through shared.setup-export.task-level-export."
  - "May route an explicitly approved immutable FSM CSV/ZIP to core.data-loader after the Referral package contract is validated."
required_privileges:
  - "Fusion privileges appropriate to export Referral Descriptive Flexfields setup data."
  - "Fusion privileges appropriate to upload and import a validated Referral Descriptive Flexfields FSM package."
---

# Referral Descriptive Flexfields Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Referral Descriptive Flexfields` under `Recruiting Configuration`.

## Setup Task Skill Contract

- task_code: `ORA_IRC_REFERRAL_DESCRIPTIVE_FLEXFIELD`
- task_name: `Referral Descriptive Flexfields`
- parent_skill_id: `hcm.recruiting.recruiting-configuration`
- pillar: `HCM`
- offering: `Recruiting`
- functional_area: `Recruiting Configuration`
- functional_area_code: `ORA_RECRUITING_CONFIGURATION`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Referral Descriptive Flexfields` under `Recruiting Configuration`.

## Basic Test Cases

Supported operations are `Inspect`, `PlanCreate`, `PlanUpdate`, `PlanDisable`, and `Verify`; copy/duplicate is handled as `PlanCreate`. Search enablement, filters/facets, search indexing, and Search Views configuration are outside this skill. Return `UNSUPPORTED` for a search-operation request without running search lookups or changes.

Review the [contract test cases](tests/referral-descriptive-flexfields-contract-tests.md) when validating a change to this skill or its task-local rules. These checks do not authorize a Fusion mutation.

## Current-Definition Export Route

Use `shared.setup-export.task-level-export` for every standalone retrieval and every copy, update, or disable request. For copy/update/disable collect the Segment Name first, then attempt a fresh export even when a prior validated package exists. For a new create, use the latest validated matching exact-task package or export fresh when none exists. Global create, copy, update, and disable may use the qualified fallback when the fresh export is unavailable or empty; follow the Global fallback for segment changes below.

For every standalone retrieval, start a fresh exact-task export and show supported segments grouped by verified scope. For copy, update, and disable, follow the fresh-export intake above; an older matching export may supply an explicitly unverified fallback proposal only after the fresh attempt fails or is empty. For a new create, reuse only the latest validated matching exact-task package or export when unavailable. Preserve all task-specific scope and package-validation guards below.

Treat a Fusion pod URL only as environment identity for routed workflow steps; never navigate to, inspect, debug, probe, or derive segment information from the URL itself. Do not use browser developer tools, guessed or discovered REST endpoints, direct DFF API calls, or direct REST reads or mutations as a fallback.

### Historical Global Package Contract and Fallback

A historical populated Referral DFF export reviewed on 2026-09-23 establishes a package contract for **Global segment changes**. Its SHA-256 is `4973ec635a6ecb8092dde7e80ee28e4ae7afb1c4672cb555092055d84eb0a32d`. The package is explicitly old and is structural evidence, not a current-definition baseline. Never use its segment rows, occupied columns, sequences, value-set assignments, audit identities, timestamps, submitter, process ID, or environment provenance as current target-environment facts.

Document the segment configuration fields here; obtain the complete archive structure from the validated current exact-task export, or from the checksum-pinned historical archive for a qualified Global create, copy, update, or disable. Do not reconstruct the member list or CSV headers from a hardcoded list or memory.

- Require exactly one parent row for `IRC_RF_REFERRALS_DFF` / application `821` in `FND_APP_DESCRIPTIVE_FLEXFIELD.csv` and retain `ASM_SETUP_CSV_METADATA.xml`.
- Place Global rows only in `ORA_FND_APP_DESCRIPTIVE_FLEXFIELD_GLOBAL_SEGMENT.csv`, with `ContextCode` `Global Data Elements`.
- Supply the complete exported configuration fields, including `SegmentCode`, `SegmentIdentifier`, `ColumnName`, `Name`, `Prompt`, `ShortPrompt`, `SequenceNumber`, `EnabledFlag`, `DisplayType`, `RequiredFlag`, `ReadOnlyFlag`, `BIEnabledFlag`, and a compatible `ValueSetCode`. Preserve or explicitly validate every remaining exported column.
- Preserve the exact source archive's complete member set and member order, CSV headers and column order, encoding, parent/hidden context-selector transport rows, and metadata; apply the operation-specific row transformation in the [Referral Global archive contract](ora-resource/ora_referral_global_segment_archive_contract.md).
- Verify archive integrity, every CSV row's field count, exact task/DFF/application identity, and the requested delta. The historical checksum verifies structural evidence only; it does not establish current target configuration.

For create, copy, update, or disable in `Global` scope, attempt the selected-environment exact-task export first. If that export fails, times out, or succeeds with headers but no usable root/segment rows, the workflow may continue through this contract fallback only when all of the following are true:

1. The operation is Global create, copy, update, or disable; Inspect/list, verify, and `EMPLOYEE_REFERRAL` work remain outside this structural fallback.
2. The requester explicitly confirms the complete suggested design: name, code, API name, data type, table column, value set, prompt, display type, Short Prompt, positive Sequence Number, and the optional-fields checkpoint. When current-definition data is unavailable, present the fallback choices in the `Unavailable current-definition proposal` below before asking for confirmation.
3. The preview clearly states that current duplicate, column-occupancy, sequence-occupancy, and target value-set existence checks were unavailable. The requester must confirm the selected column, sequence, and displayed value-set code/name with that limitation visible; do not describe them as verified or unused.
4. The final archive uses the verified archive-derived member structure and exact headers, retains only the required parent and transport structure, excludes every historical custom segment row, and includes only the confirmed operation-specific Global row. Historical audit and process-provenance values must not be treated as requested segment values or current-state evidence.
5. The archive passes exact identity, member, header, row-placement, required-field, encoding, metadata-presence, delta-only, and checksum validation before the normal immutable Data Loader preview and standalone approval.

This fallback does not make an old package authoritative. If the exact contract package is unavailable or its checksum or structure differs, return `ARTIFACT_PREPARATION` rather than reconstructing it from memory. A later successful populated export supersedes the fallback for current-state analysis.

After the requester confirms the complete fallback design, follow the [Referral Global archive contract](ora-resource/ora_referral_global_segment_archive_contract.md). It defines the immutable delta, verified baseline checksum and archive-derived member order: retain only the Referral parent and hidden context-selector transport rows, clear their audit fields, make every unrelated CSV header-only, add exactly one confirmed Global segment row, preserve the metadata contract, and never overwrite an existing archive. A contract-validation failure is `ARTIFACT_PREPARATION`; do not reproduce or repair the archive manually.

### Unavailable Current-Definition Proposal

When a selected-environment export fails, times out, produces no usable rows, or otherwise cannot provide a validated current definition for a Global create, copy, update, or disable, do not end intake with a generic baseline-unavailable message. Instead, show a single clearly labeled `UNVERIFIED` proposal and ask the requester to select or revise it:

- Use the name-based design rules below for the supported fallback route; never propose `Character`, `TEXT_BOX`, or `ATTRIBUTE_CHAR1` for every name. Propose sequence `10` only as an unverified starting suggestion when sequence evidence is unavailable.
- Retrieve existing compatible target-environment value sets and show their displayed code, description, validation type, data type, and maximum length for selection. Do not propose or create a new value set.
- If no compatible existing value set can be retrieved, stop with a reference-data blocker; do not substitute an invented code or a new value set.
- Ask the requester to accept or revise the proposed column and sequence and to select one retrieved existing value set. The fallback column and sequence remain suggestions only and do not establish target-environment availability.

## Global Fallback for Segment Changes

For Global create, copy, update, and disable, an unavailable, failed, timed-out, missing, or empty fresh export leads to a suggested fallback proposal, not an automatic stop. Attempt the routed export first; an older package is never described as freshly exported or verified current state. Use the pinned task-specific archive for structure and, where available, an older matching same-environment export for historical source/target values. Preserve its capture time and provenance. A successful populated export that contradicts the proposed target takes precedence over historical evidence.

Show `Field`, `Historical or supplied value`, `Suggested value`, and `Evidence / assumption` in a clear table, labeled **UNVERIFIED — current configuration could not be retrieved**. Retain the Segment Name already supplied. Mark missing source/target facts `Needs confirmation`; suggest design values where the supported contract allows them, but never invent an existing segment code, API name, column assignment, or value-set identity from its name.

| Operation | Fallback proposal and confirmation |
| --- | --- |
| Create | Apply the name-based design and existing compatible value-set suggestions; confirm column and sequence with occupancy checks marked unverified. |
| Copy | Show the historical or requester-supplied source record, confirm its identity/type, and propose the copy suffixes plus new compatible column and sequence. Confirm required values first, then optional defaults. |
| Update | Show the historical or requester-supplied target record and requested changes. Explicitly confirm the exact target keys and every unchanged configuration value required by the transport; do not replace preserved values with create defaults. If the change is unspecified, ask which displayed field to change. |
| Disable | Show the historical or requester-supplied target record with Enabled → No. Confirm the exact target keys and the complete preserved configuration; do not infer current enabled status or reset any other property. |

After required confirmation, show optional fields: defaults for create/copy, confirmed preserved values for update/disable (Enabled remains No for disable). Continue to immutable archive preparation once confirmed. If there is no historical source/target record, still show the proposal first and ask only for unresolved identity or preservation values; a segment name alone is insufficient to construct an existing-record update. Never label user-confirmed historical values as independently verified. Disclose unverified existence, duplicate, storage, sequence, and current-property checks in the final preview.

The pinned contract supplies archive structure, not target existence or current values. Prepare exactly one operation-specific Global row: a new row for create/copy, the confirmed target row plus only the requested delta for update, or the confirmed target row with EnabledFlag N for disable. Exclude unrelated historical rows and historical audit/provenance fields. Preserve confirmed keys, column, sequence, and all unchanged configuration for update/disable. Validate the existing-row import/key semantics against the declared transport contract before submission; do not silently turn update/disable into creation. If necessary identity, preserved values, compatible value set, or the structural contract remain unavailable after the proposal, report that specific remaining gap. Context-sensitive work and standalone list/verify do not use this Global fallback.

Retain the normal checksum-bound Data Loader preview, submission approval, monitoring, and ProcessLog review. Fallback design confirmation is not submission approval.

## Name-Based New-Segment Suggestions

For every new segment, including a qualified Global fallback, use the supplied name and any stated meaning to propose the data type, compatible display control, storage-column family, and existing value-set choices together. A name is a suggestion signal, not a confirmed business decision. Preserve an explicitly supplied type or confirmed copy-source type; never override it merely because of the name. Explain the inferred meaning briefly and ask the requester to confirm or revise the complete proposal.

| Meaning suggested by name | Suggested data type | Display suggestion | Storage suggestion |
| --- | --- | --- | --- |
| Text, description, comments, or a person's/name label; e.g. Referral Comments | Character | `TEXT_BOX` when supported and appropriate | Compatible `ATTRIBUTE_CHAR<n>`; fallback candidate `ATTRIBUTE_CHAR1` |
| A quantity, amount, count, or numeric score; e.g. Referral Amount or Referral Score | Number | A supported numeric-compatible control (`TEXT_BOX` if compatible) | Compatible `ATTRIBUTE_NUMBER<n>`; fallback candidate `ATTRIBUTE_NUMBER1` |
| A calendar date; e.g. Referral Date or Expiration Date | Date | A supported date-compatible control; do not guess its transport code | Compatible `ATTRIBUTE_DATE<n>`; fallback candidate `ATTRIBUTE_DATE1` only when that family is supported |
| A date and time; e.g. Referral Timestamp | Date Time | A supported date-and-time-compatible control; do not guess its transport code | Compatible timestamp/date-time storage verified for the target; do not invent a column |

Treat numbers used as identifiers (phone numbers, postal codes, account/reference numbers) as potentially Character because leading zeros, formatting, or letters may matter. Do not force Number from the word “Number” alone. If a name such as “Referral Value” or “Identification Number” is ambiguous, show a provisional type and its assumption in the proposal, and clarify only if compatibility or intent remains unresolved. Offer Character versus Number or Date versus Date Time as appropriate.

With current evidence, select an unused column compatible with the confirmed type and existing value set. In fallback mode, label the inferred design and column occupancy `UNVERIFIED`; a suffix `1` is a candidate, not evidence of availability. Validate the column family and display mapping against the supported target/transport contract before building the archive. If the supported column or display code cannot be established, stop with the exact compatibility gap rather than reverting to Character or `TEXT_BOX`. Retrieve compatible existing value sets for the proposed type, require selection, and never create or invent one.

## Referral Segment Retrieval Guard

When the user asks to retrieve or list current segments, or asks to copy or duplicate a segment without identifying the source, read the routed task CSV export and return both of these supported groups:

1. Global segments.
2. Context-sensitive segments from the exact seeded context whose code is `EMPLOYEE_REFERRAL` and whose displayed name is `Employee Referral`.

- Match both the context code and displayed context name before reading segment rows.
- Do not treat `Agency Referral` as an alias for `EMPLOYEE_REFERRAL`.
- Retain Global segments, but exclude `Agency Referral` segments and segments from every other context.
- If the exact Employee Referral code and displayed name cannot both be verified, return Global segments separately and report the Employee Referral portion as `MISSING` or `AMBIGUOUS`; never substitute another context.

## Segment List Presentation

For every explicit list, retrieve-all, inspect, or unnamed-copy source response, show a compact table for every returned segment in the screenshot-style layout. Do not reduce a segment list to only name and code unless the requester explicitly asks for a compact summary.

If the fresh exact-task export is header-only or lacks the required Referral DFF root row, treat the condition as an internal unavailable-current-definition state. For a list, retrieve-all, or inspect request, respond simply: `No Referral DFF segments are currently configured.` Do not mention headers, missing root rows, internal statuses, or export mechanics. Do not use such an export as a current-definition baseline for a change; preserve the existing qualified Global-create fallback and all other change-operation safeguards.

Use exactly these columns in this order: `Seq.`, `Name`, `Code`, `API Name`, `Column`, `Type`, `Value Set`, and `Required`. Render the `Seq.` value from `SequenceNumber`, render `Required` as `Yes` or `No`, and show `—` only when a supported value is blank or unavailable. Group rows under a clear `Referral DFF — IRC_RF_REFERRALS_DFF` heading; when context-sensitive rows are present, show a separate heading with the exact verified context name. Do not add audit fields, internal identifiers, credentials, tokens, or unsupported context rows unless the requester explicitly asks for more detail.

## Missing-Input Collection for Segment Changes

For create, copy, update, and disable, ask only `What is the Segment Name?` at initial intake if it is missing. For create this is the new name; for copy it is the source name; for update or disable it is the existing target name. Retain every supplied value and do not repeat answered questions. Do not ask a setup questionnaire for type, scope, value set, required behavior, or administrative fields.

For every copy, update, or disable request, after collecting the name, run a fresh exact-task export through `shared.setup-export.task-level-export`, even if a validated older package exists. Validate environment, task, DFF, application, and context identity before resolving the exact source/target. If multiple segments share the name, show their scopes/codes and ask for one selection. If the fresh export is unavailable, fails, times out, or contains no usable rows, continue with the Global fallback proposal below. If a valid populated export explicitly lacks the named segment, report that absence and clarify the target; do not replace contradictory current evidence with historical rows. Reuse this request's fresh validated export through proposal and archive preparation, rather than exporting at each confirmation.

### Required Values Proposal

After the name and applicable evidence are available, show a Markdown table with `Field`, `Suggested value`, and `Basis` columns. Populate actual supported values; do not show unresolved placeholders as a ready-to-confirm design. Include all UI-required fields and transport-required fields together: Segment Name, Code, API Name, Data Type, Table Column, Value Set, Prompt, Display Type, Short Prompt, and Sequence Number. Show scope/context and environment above the table. Propose Global scope for a new segment when none is supplied, explicitly as a suggestion requiring confirmation; preserve the verified source/target scope for other operations.

- **Create:** derive code, API name, prompt, and short prompt from the name; infer a compatible type/display from the name-based rules. Suggest an available compatible column, the next unused positive sequence in increments of 10, and one retrieved compatible existing value set with its code/name and rationale. Confirming the table selects that value set; do not require a separate selection question. Label any qualified new-Global fallback choices and unavailable checks as `UNVERIFIED` under the existing fallback contract.
- **Copy:** show `Field`, `Current source value`, `Suggested value`, and `Basis`. Suggest `_Copy` for the new name, code, and prompt, and `Copy` without an underscore for API Name. Preserve the source type and compatible value set, but propose a distinct unused column and sequence. Validate uniqueness and field lengths. The requester need not invent a new name before seeing the proposal.
- **Update:** show `Field`, `Current value`, `Suggested value`, and `Basis` from the fresh export. Apply changes already requested and mark other values `Keep current`. If no intended change was supplied, show the current values first and ask which displayed field/value to change; never invent a business change or submit a no-op update.
- **Disable:** show the exact target name, code, scope, and `Enabled: current value → No`; mark all other properties `Keep current`. If already disabled, report that no change is needed. Preserve all optional settings; do not reset them to create defaults.

Ask once to confirm or revise the required-values proposal. Include Short Prompt and Sequence Number in this confirmation, not in later individual questions. Present a defensible suggestion for an ambiguous name with its assumption; ask a targeted clarification only if compatibility cannot be established or a business decision remains unresolved after the proposal. Never invent an existing value set, occupied-column status, or unsupported transport code.

### Optional Edit Segment Fields

Only after the required-values proposal is confirmed, show one Markdown table with `Field`, `UI default`, and `Proposed value` columns for create/copy. For update add `Current value` and preserve it unless the requester explicitly changes it. Use these defaults for new/copied segments unless a supplied value overrides them:

| Field | UI default |
| --- | --- |
| Description | Blank |
| Enabled | Yes |
| Range Type | None |
| Required | No |
| Default Type | None |
| Definition Help Text | Blank |
| Instruction Help Text | Blank |
| Display Size | Blank (UI default) |
| Display Height | Blank (UI default) |
| Read-only | No |

Ask once: `Use these optional values, or would you like to change any?` After confirmation, proceed to validation, archive preparation, and the existing immutable Data Loader submission preview. Do not repeat completed design questions. For disable, show preserved optional values after the required proposal is confirmed, then proceed after optional confirmation; do not invite unrelated changes or apply Enabled Yes. Design confirmation does not replace the final archive submission approval.

### Supported Segment and Value Set Options

Use only these Create Segment `Data Type` choices shown by the supported UI:

- `Character`
- `Number`
- `Date`
- `Date Time`

Always retrieve and present existing compatible target-environment value sets for selection. Use the requester's selected displayed value-set code or name; do not create a new value set in this workflow.

Require the segment data type, value-set data type, table column, and display type to be compatible. If no compatible existing value set is available for the selected data type, stop and ask the requester to select a different supported design; never invent an internal identifier or create a value set.

While collecting inputs, do not display `MISSING`, task-node IDs, action types, internal execution paths, registry state, or commentary such as “no CSV export or Fusion change occurred.” Do not dump the complete missing-field checklist unless the user explicitly asks for it. Keep internal workflow state in the run record only.

Do not invent, infer, or silently default a missing business decision. Do not ask the user to guess Oracle-managed identifiers such as an `ATTRIBUTE_*` storage column, an internal value-set identifier, or a generated deployment artifact. Resolve those through the approved CSV current-state and lookup workflow when available. Never create a value set in this workflow. The sole exception is the explicitly labeled new-Global fallback proposal, which offers a name-based, type-compatible column candidate and sequence `10` for the requester to accept or revise, never as verified target-environment facts.

## Interactive Prompts for New Segments

Follow the staged intake above: Segment Name only, complete required-values table and confirmation, then optional-values table and confirmation, then archive preparation. When prompt controls are available offer `Use suggested values` and `Revise values`; do not offer optional settings before required design confirmation. Supplied values remain visible in the proposal and are never silently replaced.

## Final Segment Change Submission Workflow

After every required and applicable optional input for `PlanCreate`, `PlanUpdate`, or `PlanDisable` is confirmed, complete this sequence, pausing only at the explicit submission-approval gate:

1. Build the final FSM CSV/ZIP from the confirmed inputs, analysed current-definition package, and an established package contract, preserving every authoritative property outside an update's requested delta. For the qualified Global change fallback, use the verified historical structural contract and confirmed delta instead of treating historical rows as current state. Validate task identity, filenames, CSV headers, UI-required values, transport-required `ShortPrompt` and `SequenceNumber`, encoding, metadata presence, archive structure, compatibility, and exact delta. Validate uniqueness and occupancy from current evidence when available; in fallback mode, label those checks `UNVERIFIED` in the preview and require the requester's explicit confirmation. If the applicable package contract, required current property, or deterministic archive construction is unavailable, return an artifact-preparation blocker and stop; never invent or reconstruct missing state.
2. Freeze the validated archive bytes, calculate its SHA-256 checksum, and route that exact archive to `core.data-loader`. Show the complete immutable Data Loader preview, including the target environment, operation, segment identity, requested values, archive filename, and checksum.
3. Stop before the first upload POST and ask exactly: `Do you want to proceed with submitting the reviewed archive?` Only a standalone affirmative reply to the latest unchanged preview authorizes submission. Any change to the inputs, archive, validation, target environment, or checksum invalidates approval and requires a new preview.
4. After valid approval, let `core.data-loader` revalidate the same checksum, upload the immutable archive to UCM, initiate the FSM import once, and complete its standard monitoring cycle. Do not ask for a second task-level approval; the Data Loader approval workflow is authoritative.
5. `core.data-loader` must poll every 15 seconds until Fusion reaches a terminal state or 300 seconds elapse. Never report upload or initiation acceptance as the final result.
6. On terminal status, require `core.data-loader` to download and read the FSM ProcessLog and reconcile it with the status endpoints. Report only that the segment operation completed successfully, with the ProcessLog link, or that it completed with errors, with a concise summary of every actionable error and the ProcessLog link.
7. Never retry the upload or initiation automatically. On monitoring timeout or unavailable terminal evidence, report the request ID, last status, elapsed wait, and one safe status-check action without resubmitting the archive.

Never treat successful upload or initiation as the final result. The final user-facing response must state whether the import succeeded or failed after completion monitoring and Process Log review.

This completion requirement applies whenever the requester has asked to wait, monitor, verify completion, or post the final result; retain that request through archive approval and initiation. It takes precedence over a generic initiation-only handoff.

## Preflight and Error Handling

Before archive construction or submission, preflight the exact task/DFF/application identity, scope, selected environment, applicable current-definition or historical-contract route, complete confirmed design, package members and headers, metadata presence, checksum, Run Book state, privileges, and approval status. In historical-contract fallback mode, also verify the exact contract fingerprint and show every unavailable current-state check as `UNVERIFIED`.

Classify export, contract, archive, authorization, submission, monitoring, and ProcessLog failures using the task-local error-handling resource. Stop without automatic retry or route substitution. Persist sanitized diagnostics under the selected project workspace when available. Redact secrets, tokens, authorization headers, token-cache contents, historical submitter/environment provenance, and sensitive runtime or referral data from user-facing output and reusable skill files.

## Segment Copy or Duplicate Requests

Treat a request to copy or duplicate a segment as `PlanCreate` using one existing segment as the source; it never overwrites the source segment.

1. Ask only for the source Segment Name when missing. Then start a fresh exact-task export, resolve the exact supported source, and show the copy proposal. List supported sources only if requested or needed to resolve an ambiguous name.
2. If the requester already identifies the source segment, retain its name first, then start and validate a fresh exact-task export before presenting suggestions. Suggest `_Copy` for the new segment name, segment code, and prompt where present. Suggest the source API Name followed by `Copy` with no separator because Oracle `SegmentIdentifier` doesn't allow underscores. For example, `Referral Source` becomes `Referral Source_Copy`, `REFERRAL_SOURCE` becomes `REFERRAL_SOURCE_Copy`, and API Name `referralSource` becomes `referralSourceCopy`.
3. Validate the API Name as the FSM `SegmentIdentifier` before building an archive: it must be 1–30 characters, begin with an English letter, contain only English letters or digits after that first letter, and not be a reserved word. Reject spaces, underscores, hyphens, and every other punctuation character. Validate the segment code separately against its own field contract, including its 30-character maximum; underscores remain permitted in the segment code.
4. Ask the requester to accept or revise the suggested values. If the source lacks a name, code, API name, or prompt, if a suggested value is too long, grammatically invalid, reserved, conflicting, or declined, propose a valid shortened candidate and require confirmation. Do not silently truncate, alter, or reuse an identifier.
5. Validate that every proposed identifier is valid and unique for its target field using the analysed current-definition package. Then proceed through the normal build, preview, and approval workflow.

## Segment Deletion Requests

Deletion of a Referral DFF segment is not supported. When a user asks to delete any segment, clearly state: **"Delete is not supported, but this Referral DFF workflow supports disabling a segment—not deleting it outright."**

Offer `PlanDisable` as the supported alternative. Continue only if the user confirms that disabling the exact identified segment meets their intent; then follow the normal preview, validation, and approval workflow using a fresh exact-task export for this disable request, reusing it through proposal and archive preparation. For an unavailable or empty fresh export, use the qualified Global fallback for disable.

## Setup Task Metadata

- Task name: `Referral Descriptive Flexfields`
- Task code: `ORA_IRC_REFERRAL_DESCRIPTIVE_FLEXFIELD`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task. Use the Current-Definition Export Route above: copy, update, and disable always need a fresh export attempt for the request; Global create, copy, update, and disable can qualify for the structural fallback.

Use this task metadata when invoking those skills:

- Offering: `Recruiting`
- Functional area / Setup Object: `Recruiting Configuration`
- Setup task name: `Referral Descriptive Flexfields`
- Setup task code: `ORA_IRC_REFERRAL_DESCRIPTIVE_FLEXFIELD`




## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `interactive_segment_input`
- `task_csv_export_artifact`
- `retrieved_context_segments`
- `final_fsm_archive`
- `immutable_submission_preview`
- `data_load_execution_result`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `hcm.recruiting.recruiting-configuration` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
