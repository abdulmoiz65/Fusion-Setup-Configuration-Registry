# Time Consumer Sets Design Enforcement

## Source Basis

- Time Consumer Sets authoring pack: 01-functional-specification.md, 03-authoring-guardrails.md, 05-crud-lifecycle-behavior.md, and 06-rest-describe-evidence.md.
- Developer-provided business-only Complete Summary requirements, 2026-09-09.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm environment release support | Retrieve environment_version_details through shared.baseline-assessment.topology-manager.environment-info. Before 27A, inform the user that Time Consumer Sets is not available through this skill and stop. |
| 2 | Confirm REST capability | For 27A and later, or unavailable release details, require one exact usable current timeConsumerSets Data Loader registration and metadata set. |
| 3 | Validate selected consumers | Require at least one selected consumer and a Time Category for each selected consumer. |
| 4 | Search and prevent silent duplicates | For search and update, return candidates that meet every supplied condition. Before preparing or submitting a create, check exact Name first and then partial Name. Only when neither matches, compare every applicable user-supplied parent and configuration parameter against existing records and retrieve complete candidate details as needed. If an equivalent record is found, present it and wait for the user's use-existing or create-new choice before creating anything. |
| 5 | Enforce supported routing | Require one documented Absence Approval Routing value. |
| 6 | Preserve child identity boundaries | Use ConfigurationId only from a verified existing child record; do not infer a nested create/update contract. |
| 7 | Generate Complete Summary | Always generate exactly one business-only Complete Summary from verified structured fields after validation, lookup resolution, and defaulting or preservation. Keep ApprovalWorkflowForWorkersFlag internal and omit Worker approval. |
| 8 | Gate provider approval | Display the completed business-only Complete Summary and Defaults Applied, then request the provider-owned approval process without changing provider execution or approval ownership. |
| 9 | Gate execution handoff | Do not present a direct REST write as authored by these resources; use the selected task's approved execution route and approval gates. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A Time Consumer Sets request is prepared | Error | resolve_environment_release_support | The target release is before 27A | Inform the user that Time Consumer Sets is not available through this skill for environments before release 27A and stop before validation, lookup, sample generation, approval, or execution | No |
| The release is 27A or later, or release details are unavailable | Error | resolve_time_consumer_sets_rest_capability | One exact usable current timeConsumerSets registration and metadata set was not confirmed | Stop; do not select an FSM fallback, reuse historical metadata, or use a direct REST route | No |
| A consumer is selected | Error | resolve_time_category | The selected consumer has no verified TimeCategoryId | Resolve one supported Time Category before preview | Yes |
| A criteria search or create duplicate check is prepared | Error | search_time_consumer_sets_by_criteria | The search did not retrieve every page, did not apply every supplied condition, did not compare all applicable user-supplied parent and configuration parameters after both name checks had no match, or did not present an equivalent record for a create choice | Complete the paginated search, retrieve candidate details as needed, and present the required candidates or use-existing/create-new choice | Yes |
| An existing Consumer Set is updated | Error | search_time_consumer_sets_by_criteria | The current Consumer Set was not selected from candidates meeting every supplied condition and read completely before an update is shaped | Use the verified current record as the preservation source and add only the requested consumer | Yes |
| A new Consumer Set or explicit routing change is prepared | Error |  | The routing code is missing or outside the two documented static values | Select Absence approval rules or Time approval rules | Yes |
| A child update or delete is prepared | Error | resolve_existing_configuration | ConfigurationId was not returned by a verified current detail read | Resolve the selected child before preparing a separately authorized child operation | Yes |
| A nested parent payload is prepared | Error |  | UI nesting is treated as proof of a REST nested-write contract | Use only the approved execution route; retain nested-write semantics as a source gap until verified | Yes |
| A user-facing result is prepared | Error |  | A sample ID, opaque key, internal consumer code, or endpoint identifier would be shown as business guidance | Show only the verified business label or a descriptive placeholder | Yes |
| A validated request is ready for provider-owned approval | Error |  | Complete Summary or Defaults Applied is absent or was not displayed immediately before the approval request; contains a blank, metadata-only, technical, identifier, code, key, opaque link, request detail, fingerprint, diagnostic, warning, Worker approval, or ApprovalWorkflowForWorkersFlag; omits a verified user selection or actually applied user-facing default; or uses a technical label where a verified business label is available | Generate and display the exact business-only summary format below immediately before requesting provider-owned approval, without changing provider execution or approval ownership | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_environment_release_support | Every Time Consumer Sets request | environment_version_details and a release comparison to 27A | shared.baseline-assessment.topology-manager.environment-info |
| resolve_time_consumer_sets_rest_capability | The release is 27A or later, or release details are unavailable | Confirmed current registration and metadata evidence for timeConsumerSets | ora_reference_lookups.md |
| resolve_time_category | Every selected consumer needs a Time Category | TimeCategoryId and verified Time Category name | ora_reference_lookups.md |
| search_time_consumer_sets_by_criteria | A criteria search, create duplicate check, or existing Consumer Set update | Matching business values, required complete record, private update identity, and duplicate-choice state | ora_reference_lookups.md |
| resolve_existing_configuration | A separately authorized existing child configuration is changed or deleted | ConfigurationId and current child values | ora_reference_lookups.md |

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
actually applied user-facing default. Retain ApprovalWorkflowForWorkersFlag as
false internally for execution, but never display it as Worker approval.
Display identifiers as resolved business display
names, codes as verified business meanings, and booleans as Selected or Not
selected, Enabled or Disabled, or Yes or No. Display internal statuses using a
verified business-friendly status such as Draft or Submitted. Keep technical
values internally for validation and provider execution.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TCS.ENFORCE_DESIGN | step | 50 | design_enforcement | passed->TCS.PROVIDER_APPROVAL;blocked->TCS.HANDLE_ERROR | TCS.APPLY_DEFAULTS | stop | Validation, lookup resolution, defaults, preservation, and Complete Summary generation have completed after release support and REST capability confirmation |
