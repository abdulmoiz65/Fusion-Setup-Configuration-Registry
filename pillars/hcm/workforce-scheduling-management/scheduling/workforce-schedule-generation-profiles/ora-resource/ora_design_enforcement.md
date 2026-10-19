# Schedule Generation Profile Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Schedule dates | Require StartDate to equal ActiveStartDate. |
| 2 | Coverage intervals | Require combined coverage duration to equal 1,440 minutes. |
| 3 | Conditional fields | Enforce auto-generation, notification, and deviation-field conditions. |
| 4 | Self-scheduling rotation | When rotation is enabled, require both self-scheduling window values and at least one rotation child row. |
| 5 | Deferred capability | Ignore rotation groups and published-open-shift groups until Condition Builder support exists. |
| 6 | Create duplicate check | Before any new-profile create approval, compare the complete resolved and defaulted profile configuration and populated child collections with current profiles. Skip the check for an explicit duplicate operation. |
| 7 | Complete Summary | Generate the required business-only summary from verified structured values after validation, lookup resolution, defaulting, and the create duplicate check, then hand off to the unchanged provider-owned approval process. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Always | Error | | StartDate differs from ActiveStartDate | Use the Active Start Date | Yes |
| Coverage rows are supplied | Error | | Combined coverage is not 1,440 minutes | Adjust interval rows to a full day | Yes |
| MethodTypeCode is supplied | Error | resolve_method_type | AutoGenerateScheduleFlag is not true | Enable auto-generation or remove Method Type | Yes |
| SelfSchedRotationEnabledFlag is true | Error | resolve_rotation_type | SelfScheduledOpens or SelfScheduledEnds is missing or less than 0, or no selfSchedulingRotations child row is supplied | Provide both non-negative self-scheduling window values and at least one rotation row, or disable self-scheduling rotations | Yes |
| Rotation groups or published-open-shift groups are supplied | Warning | | Condition Builder support is not yet adopted | Omit rotationGroups[].ListId and opportunityGroups[].ListId from the current request | Yes |
| A new-profile create operation has an exact existing configuration match | Error | find_identical_schedule_profile_configuration | The user has not explicitly chosen to create a separate profile after being shown the matching profile | Show the matching profile's business identity and ask whether to create a separate profile | Yes |
| A provider-owned approval is about to begin | Error | | The Complete Summary is absent; is not generated from verified structured values; omits a user-provided business value or an actually applied default; includes blank, unused, metadata-only, diagnostic, or technical information; or presents a populated child record without business labels | Regenerate the Complete Summary using the required business-only format, then continue to the unchanged provider-owned approval process | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_method_type | MethodTypeCode is supplied | MethodTypeCode | ora_reference_lookups.md |
| resolve_rotation_type | SelfSchedRotationEnabledFlag is true | SelfSchedRotationType | ora_reference_lookups.md |
| find_identical_schedule_profile_configuration | A new-profile create operation is requested | Complete resolved and defaulted parent and populated child configuration | ora_reference_lookups.md |

## Complete Summary Contract

Always generate the Complete Summary only after validation, lookup resolution, defaulting, any applicable create duplicate check, and design enforcement have succeeded. Build it solely from verified structured values. Keep technical values internally for validation and provider execution.

- Include every user-provided business value and every default that was actually applied.
- Place actually applied defaults only in Defaults Applied.
- Omit blank, null, unused, and metadata-only values. Add a populated child section only when it has values, and use business labels for its records and values.
- Render resolved identifiers as business display names, resolved codes as verified business meanings, Boolean values as Selected or Not selected, Enabled or Disabled, or Yes or No, and statuses as business-friendly values such as Draft or Submitted.
- Never put IDs, codes, keys, internal identifiers, opaque links, request identifiers, fingerprints, REST or API details, import-file details, resolver names, rule identifiers, task-node names, internal statuses, diagnostics, warnings, or technical notes in the summary.

Use this exact user-facing structure and no additional user-facing content:

## Complete Summary

| Business Setting | Selected Value |
|---|---|
| <business label> | <verified business display value> |

## Defaults Applied

| Business Setting | Default Applied |
|---|---|
| <business label> | <verified default display value> |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SGP.DESIGN | step | 18 | design_enforcement | passed->SGP.COMPLETE_SUMMARY;blocked->SGP.ERROR | SGP.CREATE_DUPLICATE_CHECK | stop | Always |
| SGP.COMPLETE_SUMMARY | step | 19 | design_enforcement | generated->SGP.EXECUTION_GATE;blocked->SGP.ERROR | SGP.DESIGN | stop | Generate the Complete Summary from verified structured user values and actually applied defaults before provider-owned approval |
