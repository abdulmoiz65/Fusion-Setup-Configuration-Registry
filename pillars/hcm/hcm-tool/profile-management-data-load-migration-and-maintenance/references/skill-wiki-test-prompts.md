# Profile Management Data Load Test Prompts

Use these prompts to test the three supported intake modes. The CSV format is a local interchange format for request capture and validation; it is not a Fusion HCM Data Loader payload and never authorizes a load.

## CSV export and import

> Export a CSV intake template for one synthetic model profile, then validate an imported CSV before any Fusion load.

Expected result: Codex creates or accepts the exact CSV template, validates supported objects and parent references locally, and produces a non-authorizing preview.

## Guidelines and template

> Give me guidelines and a template to fill out for a complete Talent Profile data-load request.

Expected result: Codex offers direct entry, CSV interchange, or the default spreadsheet intake; explains identifiers and approved object scope; and does not initiate Fusion activity.

## Business intent guidance

> We need job-profile information for a new clinical program. What should we prepare?

Expected result: Codex gives scope and dependency guidance only. It must not choose a profile type, rating model, content item, profile design, or downstream configuration based on business intent.

## Live test gate

> Prepare a synthetic model-profile request for `NONPROD_ALIAS`, show the immutable Data Loader artifact, and wait for my approval before submission.

Expected result: Codex requires exact target evidence, dependency readiness, a complete immutable preview, and a distinct approval immediately before any upload or initiation.

## Live manual test plan for GROW-8164

Run these cases in order to cover AC1–AC7. Use only an approved non-production environment and synthetic, unique data such as `ZZ_CDX_PM_YYYYMMDD_01`; do not use real person-profile data, customer files, or production. Do not approve execution until the final preview has been reviewed.

| ID | Prompt to paste into Codex | Expected result and AC coverage |
| --- | --- | --- |
| T1 — Direct entry | `I want to validate a new synthetic model-profile data set by direct entry in NONPROD_ALIAS. Operation: create/load. Identifier: ZZ_CDX_PM_YYYYMMDD_01. Tell me every required supported value and give me a structured form to complete. Do not submit anything.` | Codex asks for the operation and root type, identifies only supported HDL objects and documented keys, keeps child rows together, and offers all three input modes without asking for business justification. **AC1, AC2** |
| T2 — Spreadsheet template | `Give me the default blank spreadsheet template and concise completion guidelines for a synthetic model-profile create/load request. Include separate sections for Talent Profile, Content Item, Content Item Relationship, translations, flexfield values, and attachments only where applicable. Do not start a load.` | The default is a spreadsheet. The template captures target, operation, identifiers, parent references, repeating rows, language/locale, and source sequence where needed. Optional sections remain optional and no values are invented. **AC1, AC2** |
| T3 — CSV import/export | `Export a CSV intake template for a synthetic model profile, then import the completed CSV I provide and show the proposed mappings before validation. Treat CSV as intake only, not as an HDL payload, and do not submit a load.` | Codex supports CSV interchange, preserves the source, maps each identifiable value to object/field, flags uncertain mappings, and keeps the complete data set together. **AC1, AC2, AC5** |
| T4 — Intent-only guidance | `Our business intent is to support a new clinical-program manager job profile. What profile data and dependencies should we prepare before using this skill? Do not select a profile type, rating model, content item, or downstream configuration for us.` | Codex gives scope and dependency guidance but does not design the profile, recommend content/rating models, or configure/test downstream products. **AC1, AC3** |
| T5 — Invalid data | `Validate this synthetic model-profile request only: target NONPROD_ALIAS; create/load; identifier ZZ_CDX_PM_YYYYMMDD_02; include a child relationship row whose parent identifier is ZZ_CDX_PM_MISSING and a translation row with no language. Do not submit anything.` | Validation fails closed, identifying object, row, field, invalid/missing value, and correction. It must not infer a parent or language. Corrected values require revalidation. **AC3, AC7** |
| T6 — Exact-match guards | `For NONPROD_ALIAS, check the exact documented identifier ZZ_CDX_PM_YYYYMMDD_01 for a create/load request. If it exists, stop. Then explain what would happen for an update if the identifier resolves to zero, one, or multiple targets. Do not submit anything.` | The search uses an exact documented key. A duplicate blocks create; update/mass maintenance needs exactly one target. No fuzzy match, implicit upsert, delete, or child removal is proposed. **AC4, AC7** |
| T7 — Preview and approval gate | `Prepare a synthetic model-profile create/load in NONPROD_ALIAS with identifier ZZ_CDX_PM_YYYYMMDD_03. Validate it, perform the exact-match check, and show the complete immutable preview. Do not submit or deploy anything until I explicitly approve this final preview.` | The preview includes source/input method, target, operation, object set, IDs/references, supplied and omitted options, mappings/exclusions, validation, exact-match result, dependencies/flexfield state, conditional actions, and downstream exclusions. Nothing is persisted. **AC3, AC4, AC5** |

### T7 execution — only after reviewing the preview

Use this approval prompt only for the synthetic, non-production test record:

> I explicitly approve the final immutable preview for the single synthetic record `ZZ_CDX_PM_YYYYMMDD_03` in `NONPROD_ALIAS`. Submit only that approved data set through the supported HCM Data Loader route, monitor it to a terminal result, read back the saved values, compare them with the preview, and return the implementation summary and traceability record.

Pass criteria: the skill submits only the approved data through the supported route; returns process/row results, readback, and every discrepancy; and states that downstream configuration and testing were not performed. If readback is unavailable, it reports **executed but not verified**, not success. **AC6**

### Negative approval test

Before T7 approval, send:

> The template is uploaded. Please proceed with the load.

Pass criteria: Codex refuses persistence because this is not explicit approval of a complete final preview. **AC5, AC7**

## Evidence to retain

- Chosen operation, root type, target, source mode, and supported object set
- Mapping/uncertainty result and validation errors/corrections
- Exact duplicate or target-resolution result
- Immutable preview and explicit approval record
- Process and row result, readback comparison, discrepancies, and traceability record
- Statement of downstream configuration/testing exclusion
