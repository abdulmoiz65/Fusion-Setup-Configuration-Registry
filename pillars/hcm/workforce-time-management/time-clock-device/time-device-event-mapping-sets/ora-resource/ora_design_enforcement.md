# Time Device Event Mapping Set Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate inputs | Require Name and at least one Event Mapping. |
| 2 | Search and prevent silent duplicates | Retrieve every page and evaluate every supplied parent and supported child attribute; complete the required candidate selection or create duplicate decision. |
| 3 | Validate parent-child relationship | Apply the documented create-time local correlation or verify the persisted update relationship. |
| 4 | Resolve Event Mappings | Verify every selected Event Mapping before any summary is formed. |
| 5 | Apply defaults | Apply only documented defaults and preserve the absence of a default. |
| 6 | Generate Complete Summary | Always generate exactly one business-only summary from verified structured values. |
| 7 | Disclose validated archive | Immediately after the Complete Summary and Defaults Applied, render a direct Markdown link to the exact validated ZIP archive when one was generated. Keep this artifact link outside the business-only summary. |
| 8 | Gate provider approval | Display the Complete Summary and Defaults Applied, then the validated archive link and approval request, without changing provider execution or approval ownership. |
| 9 | Gate execution handoff | Keep technical values internally; use the selected task's approved execution route and approval gates. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A Mapping Set is created or updated | Error | resolve_time_device_mappings | A selected Event Mapping is not verified | Resolve every selected Event Mapping before preparing the summary | Yes |
| A Mapping Set update is prepared | Error | resolve_existing_time_device_mapping_set | The parent or requested existing child relationship is not verified | Read the selected Mapping Set and use only returned relationship data | Yes |
| A Mapping Set search, update, or create duplicate check is prepared | Error | search_time_device_mapping_sets_by_criteria | The search did not retrieve every page, did not evaluate every supplied parent and supported child attribute, did not use the documented Name comparison, or did not complete the required selection or use-existing/create-new decision | Complete the paginated criteria search and required candidate decision before preparing changes | Yes |
| A user-facing result is prepared | Error | | An identifier, code, key, opaque link, request detail, fingerprint, technical field, API detail, resolver name, rule name, internal status, technical file name, or raw Boolean would be shown | Show only verified business labels and business display values | Yes |
| A request is ready for provider-owned approval | Error | | Complete Summary or Defaults Applied is absent or was not displayed immediately before approval; contains blank, null, unused, metadata-only, technical, identifier, code, key, opaque link, request detail, fingerprint, diagnostic, warning, or technical note; omits a verified user selection or actually applied user-facing default; or renders an empty child section | Generate and display the exact business-only summary format below immediately before requesting provider-owned approval, without changing provider execution or approval ownership | Yes |
| A validated ZIP archive is prepared for approval | Error | | The approval response omits a direct Markdown link to the exact validated archive, or the link is placed inside the business-only summary | Render the complete business-only summary first, then show the validated archive link and the approval request directly below it | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| search_time_device_mapping_sets_by_criteria | A criteria search, update selection, or create duplicate check | Matching business values, all matching candidates, selected complete record when applicable, and duplicate-choice state | ora_reference_lookups.md |
| resolve_time_device_mappings | Every selected Event Mapping | Verified MappingId and Event Mapping display name | ora_reference_lookups.md |
| resolve_existing_time_device_mapping_set | A Mapping Set update or existing child relationship change | Verified parent and child relationship values | ora_reference_lookups.md |

## Required Complete Summary Format

Generate exactly this business-only structure after validation, lookup resolution,
and defaulting or preservation. Add a populated child section only when it has
business values; do not render empty child sections.

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

The summary must include every verified user-provided business value and every
actually applied user-facing default. Do not add warnings, diagnostics, or
technical notes. Display identifiers as resolved business display names, codes
as verified business meanings, and Booleans as Selected or Not selected,
Enabled or Disabled, or Yes or No. Display internal statuses using a verified
business-friendly status such as Draft or Submitted. Keep technical values
internally for validation and provider execution.

## Approval Artifact Disclosure

When an immutable ZIP archive has passed all validation and is awaiting
approval, render the required Complete Summary and Defaults Applied exactly as
shown above. Immediately beneath that summary, render a direct Markdown link to
the exact validated ZIP archive, followed by the approval request. The archive
link is a deliverable, not a business setting: do not place it in either
business-only table, omit it because the summary is constrained, or substitute
an unlinked file path. Do not disclose archive fingerprints, internal paths,
payload fields, or identifiers alongside the link.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TDEMSET_ENFORCE_SUMMARY | step | 7 | design_enforcement | passed->TDEMSET_PROVIDER_APPROVAL;blocked->TDEMSET_SUMMARY_BLOCKED | TDEMSET_APPLY_DEFAULTS | stop | Validation, criteria search, lookup resolution, defaulting or preservation, and Complete Summary generation have completed |
