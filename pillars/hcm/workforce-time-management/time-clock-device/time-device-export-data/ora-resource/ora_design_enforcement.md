# Time Device Export Data Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate inputs | Validate required business values and normalize Start Date when supplied. |
| 2 | Search and prevent silent duplicates | Retrieve every page and evaluate every supplied parent and supported child attribute; complete the required candidate selection or create duplicate decision. |
| 3 | Apply defaults | Apply only documented defaults and preserve the absence of a default. |
| 4 | Generate Complete Summary | Always generate exactly one business-only summary from verified structured values. |
| 5 | Disclose validated archive | Immediately after the Complete Summary and Defaults Applied, show a direct Markdown link to the exact validated ZIP archive. Keep this artifact link outside the business-only summary. |
| 6 | Gate provider approval | Display the Complete Summary and Defaults Applied, then the direct validated ZIP link, then the approval request without changing provider execution or approval ownership. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A Time Device Export Data search, update, or create duplicate check is prepared | Error | search_time_device_export_data_by_criteria | The search did not retrieve every page, did not evaluate every supplied parent and supported child attribute, did not use the documented comparison, or did not complete the required selection or use-existing/create-new decision | Complete the paginated criteria search and required candidate decision before preparing changes | Yes |
| A user-facing result is prepared | Error | | An identifier, code, key, opaque link, request detail, fingerprint, technical field, API detail, resolver name, rule name, internal status, technical file name, or raw Boolean would be shown | Show only verified business labels and business display values | Yes |
| A request is ready for provider-owned approval | Error | | Complete Summary or Defaults Applied is absent or was not displayed immediately before approval; contains blank, null, unused, metadata-only, technical, identifier, code, key, opaque link, request detail, fingerprint, diagnostic, warning, or technical note; omits a verified user selection or actually applied user-facing default; or renders an empty child section | Generate and display the exact business-only summary format below immediately before requesting provider-owned approval, without changing provider execution or approval ownership | Yes |
| A validated ZIP archive is prepared for approval | Error | | The approval response omits a direct Markdown link to the exact validated archive, places it before the business-only summary, after the approval request, or inside either business-only table | Render the business-only summary first, then a direct link to the exact validated ZIP archive, then the approval request | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| search_time_device_export_data_by_criteria | A criteria search, update selection, or create duplicate check | Matching business values, all matching candidates, selected complete record when applicable, and duplicate-choice state | ora_reference_lookups.md |

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
as verified business meanings, and checkboxes as Selected or Not selected when
a verified business label is available. Display internal statuses using a
verified business-friendly status such as Draft or Submitted. Keep technical
values internally for validation and provider execution.

## Approval Artifact Disclosure

When a validated ZIP archive is awaiting approval, render the required Complete
Summary and Defaults Applied first. Immediately beneath the summary, render a
direct Markdown link to the exact validated ZIP archive. Place the approval
request immediately beneath that link. The archive link is a deliverable, not a
business setting: do not place it in either business-only table or disclose
archive fingerprints, internal paths, payload fields, or identifiers alongside
the link.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TDEDEXPORT_ENFORCE_SUMMARY | step | 4 | design_enforcement | passed->TDEDEXPORT_PROVIDER_APPROVAL;blocked->TDEDEXPORT_SUMMARY_BLOCKED | TDEDEXPORT_APPLY_DEFAULTS | stop | Validation, criteria search, lookup resolution, defaulting or preservation, and Complete Summary generation have completed |
