# Enterprise Shifts Design Enforcement

## Source Basis

- Enterprise Shifts Rest Describe, Confluence page 21451526148, version 3
- Enterprise Shifts Test Technical Design Document for FSCIR, Confluence page 21452837175, version 4
- User-Facing Value Resolution Policy, user-provided authoring source, received 11 August 2026
- Enterprise Shifts UI does not provide shift deletion, user confirmation, 11 August 2026
- Enterprise Shifts naming, category recommendation, time, reuse, and approval policy, developer-provided, received 18 August 2026
- Enterprise Shift name, field-value precedence, and default-origin display rules, user-provided, received 19 August 2026
- Explicit Enterprise Shift Name policy, user-provided, received 24 September 2026
- Automatic final Data Loader completion and read-back verification, user-provided, received 19 August 2026
- Always poll Enterprise Shifts loads automatically after approval, user-provided, received 20 August 2026
- Full task-rule review before generated-sample interpretation, user-provided, received 21 August 2026
- Enterprise Shifts business-only Complete Summary and provider-owned approval boundary, user-provided, received 10 September 2026
- Terminal Enterprise Shifts result must use a business-only summary after success or error, user-provided, received 10 September 2026

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Rule-set review gate | Before interpreting a generated sample, read this selected task's complete input validation, dependency readiness, reference lookup, defaulting, design enforcement, error handling, and compiled rule-registry guidance. Treat samples as schema evidence only; they do not override a task rule, documented default, dependency, lookup result, or error-handling requirement. |
| 2 | Identity gate | Target, task, and one shift identity or create-candidacy receipt are exact |
| 3 | Naming, input, and category gate | Attempt name construction before lookup from all documented valid inputs, preserve an explicit Shift Name, and otherwise require Shift Name directly. Required create or update values validate; an optional supplied category resolves to one lookup code or a missing category receives a recommendation only |
| 4 | Duration and time gate | Positive duration, nearest-minute time representation, and same-day or next-day state are consistent. Reconcile End Time minus Start Time, using the declared end day, to Work Duration plus Unpaid Break Duration before preview. |
| 4a | Time-arithmetic test gate | When same-day or overnight patterns are in scope, test the applicable start time, end time, work duration, unpaid-break duration, and total elapsed duration arithmetic before reporting the configuration ready |
| 5 | Reuse and mutation-safety gate | Display and classify every retrieved candidate. Reuse only an exact configuration-and-behavior match; mark nonmatching or ambiguous candidates for specialist review. The approved operation is immutable: create can create only, and update can update only its explicitly selected target. |
| 6 | Complete Summary gate | Generate the business-only Complete Summary from verified structured fields after validation, lookup resolution, and defaulting. The summary must be complete and sanitized before the provider-owned approval process begins. |
| 7 | Handoff and final-completion gate | After the Complete Summary, a separate provider-owned runbook owns the immutable preview, explicit user approval before creation or update, one write attempt, automatic terminal-status monitoring, and read-back verification. The terminal result is always task-owned: successful completion returns the business-only Complete Summary and Defaults Applied sections from saved values; an unsuccessful terminal result returns a business-only result and one safe next action. An update preview identifies the target Shift and displays current values, proposed values, and an attribute-by-attribute change summary. |
| 8 | Value-resolution gate | Every value intended for a user-facing response is classified and every internal value is resolved privately from a verified source |
| 9 | Response-sanitization gate | The response contains only verified business labels, names, meanings, descriptions, and intentionally displayed business codes |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A generated sample is available | Error |  | The sample is interpreted for a required field, default, identifier, activation setting, naming decision, dependency, lookup, behavior, or error response before all governing skill and task-rule files are read | First read the parent WFM Common SKILL.md, the selected Enterprise Shifts SKILL.md, complete input validation, dependency readiness, reference lookup, defaulting, design enforcement, error handling, compiled rule-registry, and required task-node execution guide. Use the sample only to confirm schema or field availability; resolve all business decisions from the governing rules and verified current state. Block preview and execution until this review is complete. | Yes |
| Every create | Error | find_enterprise_shift_by_exact_name | Exact-name candidate discovery is incomplete, ambiguous, or would show an existing shift whose configuration values or intended scheduling behavior do not all match | Resolve all candidates; show an existing shift only for an exact full match, otherwise retain create candidacy or require an explicit update target | Yes |
| Candidate review | Error | find_enterprise_shift_by_exact_name | A retrieved candidate is not displayed and classified as an exact reusable match, a nonmatching candidate requiring specialist review, or an ambiguous candidate requiring specialist review | Display each candidate's configuration-and-behavior comparison and require specialist review for every nonmatching or ambiguous result before approval | Yes |
| Creating or renaming a shift without an explicit Shift Name | Error |  | The derived Shift Name is absent after documented name construction, does not include the required start time, end time, and unpaid-break duration, is not recognizable for its population or purpose, or contains DEV, TEST, UAT, or PROD | Attempt a recognizable construction using supplied start time, end time, unpaid-break duration, Population or Purpose, and only a supplied nonregular Shift Type. Preserve an explicit user-provided Shift Name without applying derived-name restrictions. When construction fails, ask directly for Shift Name; do not request missing naming inputs. | Yes |
| ShiftCategory is omitted | Info |  | No category code is supplied | Recommend a category name from the shift time and description; do not block, default, or submit a category code | Yes |
| ShiftCategory is supplied | Error | resolve_shift_category_code | Category is a display meaning, invalid code, disabled code, zero match, or many matches | Use the exact enabled LookupCode returned by Workforce Scheduling – Common – Manage Common Lookups for ORA_HTS_ENT_SHIFTS_CATEGORY | Yes |
| Time or duration is supplied | Error |  | Work duration is not positive, values conflict, End Time minus Start Time does not equal Work Duration plus Unpaid Break Duration using the declared same-day or next-day end day, time was not rounded to the nearest minute when seconds were supplied, exact time serialization is unverified, or same-day and next-day values disagree | Correct the conflicting business values, declare the end day for overnight shifts, reconcile the total elapsed duration across midnight when applicable, and confirm the target time contract | Yes |
| Same-day or overnight patterns are in scope | Error |  | The applicable same-day or overnight time arithmetic has not been tested before readiness is reported | Test each in-scope pattern using start time, end time, work duration, unpaid-break duration, total elapsed duration, and declared end day; retain the validation result | Yes |
| Create or update | Error |  | Audit fields are supplied or both time and offset representations are sent without a proven contract | Remove read-only and conflicting representations | Yes |
| Update | Error | find_enterprise_shift_by_id | The current item was not reread, no sparse difference exists, or the requested identity is ambiguous | Reread one item and submit only source-backed changed writable fields through the separate runbook | Yes |
| Update preview | Error | find_enterprise_shift_by_id | The preview does not identify the explicit target Shift, show its current and proposed Shift Name, Shift Category, Work Duration, Unpaid Break Duration, Start Time, and End Time, or provide an attribute-by-attribute change summary | Block approval until the complete current-versus-proposed comparison and change summary are presented | Yes |
| Approved create or update | Error |  | The approved operation is absent, a create request would update an existing Shift, an update request would create a new Shift, or an update target differs from the explicitly selected approved Shift | Bind the approved operation and, for an update, the exact selected target to the immutable preview. Submit only the approved create or update operation; any change requires a new preview and approval. | Yes |
| Complete Summary | Error |  | The summary is absent, is generated before validation, lookup resolution, and defaulting complete, omits a user-provided business value or an actually applied default, includes blank, null, unused, metadata-only, diagnostic, warning, or technical content, or does not use the required sections and columns | Generate the Complete Summary only from verified structured fields. Include every user-provided business value in `## Complete Summary`; include every actually applied default only in `## Defaults Applied`; omit blank, null, unused, and metadata-only values. Add a populated child section only when it has values, using business labels only. Do not transition to provider-owned approval until this summary is complete. | Yes |
| Terminal result | Error |  | A terminal Enterprise Shifts success or error ends with only a generic Data Loader status table, or a successful result omits the saved business configuration | After every terminal outcome, return the task-owned business summary. A success uses the Complete Summary and Defaults Applied sections from verified saved values. An error, timeout, partial result, uncertainty, or verification mismatch uses business language, includes the Shift Name and known completed and failed counts when available, and gives one safe next action. | Yes |
| Upsert | Error |  | Match key and duplicate behavior are TBD | Do not use upsert until controlled non-production testing proves the match contract | No |
| Delete | Error |  | The Enterprise Shifts UI does not provide a delete action | Treat deletion as unsupported and do not offer or route it | No |
| Advanced-search action | Error |  | The action is placed in ADF batch or filters and sort shapes are invented | Invoke it separately and omit undocumented object shapes | Yes |
| Any creation or update | Error |  | Exact preview, current user approval, writable executor, or verification route is absent | Complete the external runbook handoff and obtain explicit approval before creation or update | Yes |
| An approved asynchronous request is accepted | Error | verify_final_shift_load | Final success is reported from acceptance alone, terminal status is not monitored automatically, the final result is not read back, or the persisted shift differs from approved supported values | Wait for a documented terminal status, then verify the persisted Enterprise Shift against approved required values, supplied optional values, and applicable defaults before reporting final success | Yes |
| Any creation or update | Error |  | A required field has no explicit, current-conversation, selected-configuration, or documented-default value, an optional field is requested, or an unsupported inferred value would be used | Resolve fields in the documented precedence order. Request all unresolved required fields together; do not request optional fields or infer unsupported values | Yes |
| Proposed or final Enterprise Shift details | Error |  | A documented default is unlabeled, or a user-provided value is labeled Default | Label only system-populated documented defaults as Default | Yes |
| Any user-facing response | Error |  | A lookup value, enumeration, record key, REST key, internal object or attribute name, service alias, endpoint identifier, finder value, bind value, or other implementation-only value would be exposed | Resolve the value privately and present only its verified business label, name, meaning, or description | Yes |
| A user supplied an internal value | Error |  | Confirmation, explanation, or recommendation repeats the raw value | Accept the value only as private processing input, verify its business meaning, and use only that meaning in the response | Yes |
| Both an internal value and display label were supplied | Error |  | The pair was not verified as one selection, or a conflict message would disclose the internal value | Verify the pair; when inconsistent, report inconsistent selection information using business language only | Yes |
| An internal value cannot be resolved | Error |  | The response guesses a label, exposes the raw value, or recommends an action based on it | Mark the selection unresolved or incomplete and request the displayed label or relevant lookup information | No |
| A field or attribute is mentioned to the user | Error |  | An internal field name is used when a verified user-facing label exists | Use the verified label; otherwise describe the field by business purpose without exposing the internal name | Yes |
| A code is proposed for display | Error |  | The UI does not explicitly present it as a meaningful business field, or it is only a lookup, enumeration, database, or implementation identifier | Omit it unless UI evidence confirms an intentionally displayed business code under a user-facing label | Yes |
| A technical URL is shown | Error |  | The URL contains a real record or implementation identifier | Replace the value with a descriptive placeholder such as `{RECORD_IDENTIFIER}` | Yes |
| Final response construction | Error |  | A recommendation uses unresolved or implementation-only values, an internal code-to-label mapping is exposed, or the response requires implementation knowledge | Resolve first, reason second, and present only the business meaning | Yes |

## Complete Summary Contract

Generate this business-only response after validation, lookup resolution, and defaulting, and immediately before the provider-owned approval process. Generate it for every valid request. Do not include warnings, diagnostics, technical notes, or any content outside the populated sections below.

```md
## Complete Summary
| Business Setting | Selected Value |
|---|---|
| <business label> | <verified business display value> |

## Defaults Applied
| Business Setting | Default Applied |
|---|---|
| <business label> | <verified default display value> |
```

Use verified business labels and verified display values only. Translate identifiers to their resolved business display name, codes to their verified business meaning, boolean values to Selected or Not selected, Enabled or Disabled, or Yes or No as applicable, and internal statuses to a business-friendly status such as Draft or Submitted.

Never display identifiers, keys, opaque links, request references, fingerprints, REST or API terms, payload or DAT details, database names, resolver names, rule IDs, task-node names, internal statuses, technical file names, raw boolean values, or an internal code when a verified business label is available. Keep those values internal for validation and provider execution.

## Terminal Result Contract

After the final status is known, the Enterprise Shifts task owns the user-facing result. Do not end with a generic Data Loader status table.

- On success, generate `## Complete Summary` and `## Defaults Applied` from the verified saved configuration, using the same business-only rules as the approval summary.
- On an error, timeout, partial result, uncertainty, or verification mismatch, show only the Shift Name, a business-friendly outcome, known completed and failed counts when available, and one safe next action.
- Do not expose technical diagnostics, request references, identifiers, raw status values, or internal names in either terminal result.

## User-Facing Resolution Source Order

| Priority | Verified Source | Required Use |
|---|---|---|
| 1 | Display label supplied with the selected value | Use after confirming that it represents the selected value |
| 2 | Name, Meaning, DisplayName, Label, or Description attribute | Use the verified display attribute, not its internal key |
| 3 | Active list of values or selection provider | Resolve against the active selectable result |
| 4 | Configured value and display attributes | Use the configured display attribute after verifying the mapping |
| 5 | Verified lookup-service result | Resolve privately and retain only sanitized evidence for the response |
| 6 | Verified REST response display attribute | Use a documented display attribute from the selected record |
| 7 | Verified metadata definition | Use the documented user-facing label or meaning |
| 8 | Verified static value-to-label mapping | Use only a checked and current mapping |
| 9 | Checked-in application source | Use only when higher-priority sources are unavailable and the mapping is explicit |

Do not derive a label by removing prefixes, replacing underscores, changing
capitalization, expanding abbreviations, or comparing similar internal values.

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_enterprise_shift_by_exact_name | Before create | Existing item or create-candidacy receipt | ora_reference_lookups.md |
| find_enterprise_shift_by_id | Before update | Current shift identity and comparison values | ora_reference_lookups.md |
| resolve_shift_category_code | ShiftCategory is supplied | Exact LookupCode and receipt-only Meaning | ora_reference_lookups.md |
| verify_final_shift_load | An approved asynchronous Enterprise Shift request is accepted | Terminal status, verified Enterprise Shift details, default-origin indicators, and approved-value comparison result | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ES.ENFORCE_DESIGN | decision | 50 | design_enforcement | passed->ES.EXECUTION_GATE;blocked->ES.HANDLE_ERROR | ES.CHECK_DEPENDENCIES | stop | Before interpreting a generated sample for a business decision, any mutation handoff, or any all-good result; generate the Complete Summary before provider-owned approval |
