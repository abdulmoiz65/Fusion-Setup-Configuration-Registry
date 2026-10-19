# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate required mapping values | Confirm Name, supplier, supplier event, and application event are valid |
| 2 | Enforce dependent selections | Clear and refresh dependent values whenever their parent changes |
| 3 | Enforce event-map scope | Use the IN map, OUT map, or both maps according to the selected application event |
| 4 | Enforce parent-child ID correlation | For create, repeat one numeric local MappingId on the parent and every new child row; for update, repeat only the persisted parent MappingId returned by Fusion |
| 5 | Enforce parent operation | Use POST only to create a mapping and PATCH only to edit one verified existing mapping; never use UPDATE for the parent mapping |
| 6 | Enforce child-row consistency | For every retained row, select a time attribute before an optional default value; determine each child REST action only from its own verified lifecycle, never from the parent action |
| 7 | Generate Complete Summary | Always generate exactly one business-only Complete Summary from verified structured fields after validation, lookup resolution, and defaulting |
| 8 | Disclose validated archive | Immediately after the Complete Summary and Defaults Applied, render a direct Markdown link to the exact validated ZIP archive when one was generated. Keep this artifact link outside the business-only summary. |
| 9 | Gate provider approval | Display the completed Complete Summary and Defaults Applied, then the validated archive link and approval request, and transition to the provider-owned approval process without changing provider execution or approval ownership |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Always | Error | | Required mapping LOV values are missing or do not resolve | Select valid values in parent-to-child order | Yes |
| DeviceSupplierCode changes | Error | resolve_supplier_device_events | A supplier event from the prior supplier remains selected | Clear the supplier event and select a new event from the refreshed provider | Yes |
| TimeAttrFieldIdRW changes | Error | resolve_time_attribute_default_values | A default value from the prior time attribute remains selected | Clear the default value and select a new supported value when applicable | Yes |
| Create includes Event Attribute Details | Error | | The parent or any new child has a blank or nonnumeric MappingId, or a child MappingId differs from the parent MappingId | Generate one unique numeric local MappingId and repeat it exactly on the parent and every new child row | Yes |
| Update includes Event Attribute Details | Error | | The parent or any child does not use the persisted MappingId returned by Fusion, or a MappingId was generated, replaced, or inferred | Reload the verified parent and repeat its persisted MappingId on the parent and every child row | Yes |
| A parent mapping is prepared | Error | | The parent action is not POST for creation, is not PATCH for editing a verified existing mapping, or is UPDATE | Use POST only for creation and PATCH only for update or edit of one verified existing mapping | Yes |
| An Event Attribute Detail is prepared | Error | | Its action was copied, derived, or inferred from the parent mapping action | Validate the child action only against its verified child lifecycle | Yes |
| A new Event Attribute Detail is prepared | Error | | MappingDetailId is populated for the new child | Remove MappingDetailId and allow Fusion to assign it | Yes |
| Event Attribute Details are supplied | Error | resolve_time_attributes | A retained child row has no time attribute | Select a time attribute or remove the optional row | Yes |
| A request is ready for provider-owned approval | Error | | Complete Summary or Defaults Applied is absent, is not generated only from verified structured business values after validation, lookup resolution, and defaulting, omits a user-provided business value or actually applied default, includes a blank, null, unused, metadata-only, or technical value, or shows an empty child section | Generate and display the exact business-only summary format below immediately before transitioning to the provider-owned approval process, without changing provider execution or approval ownership | Yes |
| A validated ZIP archive is prepared for approval | Error | | The approval response omits a direct Markdown link to the exact validated archive, or the link is placed inside the business-only summary | Render the complete business-only summary first, then show the validated archive link and the approval request directly below it | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_device_suppliers | Before validation of the selected supplier | LookupCode, Meaning | ora_reference_lookups.md |
| resolve_supplier_device_events | After selecting or changing the supplier | LookupCode, Meaning | ora_reference_lookups.md |
| resolve_application_events | Before deciding the event attribute map scope | LookupCode, Meaning | ora_reference_lookups.md |
| resolve_time_attributes | For every retained child row | TimeAttrributeFieldId, DisplayName | ora_reference_lookups.md |
| resolve_time_attribute_default_values | When a retained child row has an LOV-backed default value | Value and ValueChar | ora_reference_lookups.md |

## Required Complete Summary Format

Generate exactly this business-only structure after validation, lookup resolution,
and defaulting. Add a populated child section only when it has business values;
do not render an empty child section. Do not add warnings, diagnostics, or
technical notes.

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

Include every user-provided business value and every default that was actually
applied. Display identifiers as resolved business display names, codes as
verified business meanings, and Boolean values as Selected or Not selected,
Enabled or Disabled, or Yes or No. Display internal statuses using a
business-friendly status such as Draft or Submitted. Keep all technical values
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
| TDEM.GENERATE_COMPLETE_SUMMARY | step | 65 | design_enforcement | passed->TDEM.PROVIDER_APPROVAL;blocked->TDEM.INPUT_ISSUES | TDEM.LOOKUP_TIME_ATTRIBUTES | stop | Validation, lookup resolution, and defaulting have completed |
