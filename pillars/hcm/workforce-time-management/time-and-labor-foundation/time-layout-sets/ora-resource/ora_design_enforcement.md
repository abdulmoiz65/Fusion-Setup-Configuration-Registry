# Time Layout Sets Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate selections | Confirm consumer and lookup dependencies. |
| 2 | Search and prevent silent duplicates | For search, update, and delete, require candidates to meet every supplied condition. For create, search Name first and then supplied non-Name conditions only when no name candidate exists; obtain the user's use-existing or create-new choice before continuing. |
| 3 | Validate layout | Enforce field, total, and Web Clock rules. |
| 4 | Generate Complete Summary | Always generate exactly one business-only Complete Summary from verified structured fields after validation, lookup resolution, and defaulting or preservation. |
| 5 | Gate provider approval | Transition from the completed Complete Summary to the provider-owned approval process without changing provider execution or approval ownership. |
| 6 | Gate side effects | Require preview and current approval before import. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Project Team Membership selected | Error |  | Project Costing is absent | Select Project Costing first | Yes |
| A default-eligible value is absent from the prepared Data Loader source or final archive | Error |  | An applicable documented default was not materialized before preview | Apply the documented default and regenerate the immutable archive | Yes |
| Create requested | Error | resolve_default_time_card_layout_totals | Generated default time-card layout totals are absent from the prepared source or final archive | Generate the default totals and regenerate the immutable archive | Yes |
| Create requested with Time Consumer Sets | Error | resolve_default_time_card_fields | The generated default Time Card Fields are absent, are not linked to the new Time Entry Layout, or were generated for a different consumer selection | Retrieve the fields for the selected consumers and regenerate the immutable archive | Yes |
| Create through Data Loader | Error |  | A Time Layout Set, Time Entry Layout, Web Clock Layout, or Web Clock Button local correlation is missing, nonnumeric, reused across levels, or is not repeated in its documented child reference | Allocate unique numeric-only local correlations and repeat each only in its documented descendants | Yes |
| Create through Data Loader | Error |  | Code, LayoutCode, ButtonSetId, ButtonId, or TimeCardFieldTemplateId is used as a structural parent-child relationship key, or a loader-local correlation is treated as a persisted Fusion identifier | Use only the documented local correlation fields for a create; retain codes and lookup-selection IDs as business values and use persisted Fusion IDs only for updates or deletes | Yes |
| Web Clock Layout is configured | Error |  | A Web Clock Layout does not repeat its parent TimeLayoutSetId, a Web Clock Button does not repeat its parent WebClockLayoutId, or a Button Time Card Field does not repeat its parent WebClockButtonId | Correct each direct parent-reference ID before preview | Yes |
| Web Clock Layout is configured | Error |  | Button or Button Time Card Field DisplaySequence is missing, nonpositive, duplicated within its direct parent, or nondeterministic | Assign a positive sequence in deterministic row order within the direct parent | Yes |
| Time card fields configured | Error |  | More than three List View fields | Keep three or fewer | Yes |
| A criteria search or create duplicate check is prepared | Error | search_time_layout_sets_by_criteria | The collection was not fully paginated, every supplied business attribute including supported child attributes was not evaluated, or a candidate found by the required create sequence was not presented for a choice | Complete the paginated criteria search and present the required candidates or use-existing/create-new choice | Yes |
| Update or delete requested | Error | search_time_layout_sets_by_criteria | A candidate meeting every supplied condition was not selected completely, the persisted numeric TimeLayoutSetId, WebClockLayoutId, WebClockButtonId, or leaf TimeCardFieldInstanceId is unavailable, or a supplied value is a code, lookup-selection ID, random value, or Data Loader correlation | Resolve and use only Fusion-returned persisted numeric IDs for the selected target records | Yes |
| Update or delete requested | Error | search_time_layout_sets_by_criteria | A create-only local correlation is reused for an update or delete | Use the create correlation contract only for new records; use Fusion-returned persisted numeric IDs for updates and deletes | Yes |
| Update requested for any child section | Error | search_time_layout_sets_by_criteria | The final archive omits a `PATCH` context row for any ancestor in the changed child's live hierarchy | Add every ancestor `PATCH` row in root-to-child order and regenerate the immutable archive | Yes |
| A validated request is ready for provider-owned approval | Error | | Complete Summary is absent; contains a blank, metadata-only, technical, identifier, code, key, opaque link, request detail, fingerprint, diagnostic, or warning; omits a verified user selection or actually applied default; or uses a technical label where a verified business label is available | Generate the exact business-only summary format below, then transition to the provider-owned approval process without changing provider execution or approval ownership | Yes |
| Import requested | Error |  | Preview, identity, validation, or approval incomplete | Complete required workflow first | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_default_time_card_layout_totals | New layout has no supplied totals rows | Generated timeTotalsHoursCategories rows | ora_reference_lookups.md |
| resolve_default_time_card_fields | Create requested with Time Consumer Sets | Generated timeCardFields rows with returned TimeCardFieldTemplateId, Name, Label, Description, and row-order DisplaySequence | ora_reference_lookups.md |
| search_time_layout_sets_by_criteria | Search, update, delete, or create duplicate check | Matching business values, selected aggregate snapshot, persisted IDs, and duplicate-choice state | ora_reference_lookups.md |

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
actually applied default. Display identifiers as resolved business display
names, codes as verified business meanings, and booleans as Selected or Not
selected, Enabled or Disabled, or Yes or No. Display internal statuses using a
verified business-friendly status such as Draft or Submitted. Keep technical
values internally for validation and provider execution.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TLS.ENFORCE_DESIGN | step | 50 | design_enforcement | compliant->TLS.PROVIDER_APPROVAL;blocked->TLS.HANDLE_ERROR | TLS.APPLY_DEFAULTS | stop | Validation, lookup resolution, defaults, preservation, and Complete Summary generation have completed |
