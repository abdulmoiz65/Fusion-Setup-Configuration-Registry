# Personal Payment Method Preferences Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_payment_method_preferences | A mutation is classified, existing preferences are displayed, or LDGs eligible for preference creation are requested | Intent; optional LegislativeDataGroupName | /hcmRestApi/resources/latest/paymentMethodOptions?finder=findByLegislativeDataGroupName;Intent=SEARCH or CREATE,LegislativeDataGroupName=<encoded LDG name> | Every preference response field returned by the live service, including optional attributes and supplied action-contract attributes | For a mutation, resolve the LDG then use SEARCH: no preference sets operation to CREATE; exactly one preference sets operation to MERGE unless deletion was requested, in which case it sets DELETE. CREATE is only for creation eligibility. URL-encode LDG name when used. | Available preference records or eligible LDG records; for MERGE, the complete latest returned preference state, including optional attributes | Stop for an ambiguous result or deletion with no preference. For MERGE, do not infer a missing field, use stale cached data, or omit an optional returned attribute. |
| find_ldg_by_exact_name | LegislativeDataGroupName is supplied | LegislativeDataGroupName | /hcmRestApi/resources/latest/legislativeDataGroupsLOV | LegislativeDataGroupId, LegislationCode, LDG display name | Match exactly one valid record by the supplied LDG name | LegislativeDataGroupId, LegislationCode | Stop on no match or multiple matches and request a more precise LDG name |
| find_organization_payment_methods_by_ldg | Available or noneditable OPMs must be resolved or displayed | LegislativeDataGroupId | /hcmRestApi/resources/latest/organizationPaymentMethods?finder=findByFilterCriteria;LegislativeDataGroupId=<LDG_ID> | Organization payment method ID and name | Use the resolved LDG ID; do not query without LDG context | Organization payment method IDs and names | Stop on no match or multiple matches for a user-supplied OPM name; do not choose one |
| find_yes_no_lookup | A yes-or-no preference is supplied or displayed | LookupType YES_NO | /fscmRestApi/resources/latest/commonLookupsLOV?finder=LookupTypeFinder;LookupType=YES_NO | LookupCode, Meaning | Match Y to its returned Yes meaning and N to its returned No meaning; otherwise match the requested meaning or code to exactly one returned YES_NO entry | LookupCode for create and update payloads; Meaning for presentation | Stop on no match or multiple matches; do not substitute a code |
| describe_payment_method_options | Attribute metadata is requested | None | /hcmRestApi/resources/latest/paymentMethodOptions/describe | Every attribute and its server-provided name, display name, type, required status, read-only or updateable status, business-key indicator, LOV or reference details, allowed values, maximum length, precision, scale, default, nullability, create/update/search applicability, source resource, and relationships | Retain only values explicitly returned by describe | Attribute metadata rows for every returned field | Do not infer omitted metadata; report Not specified by describe response for an omitted field property |

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| resolve_payment_amount_type | Payment Amount Types is supplied or displayed | Developer-supplied Payment Amount Type Array: A = Amount, P = Percentage, B = Both | Match exactly one supplied code or meaning | PaymentAmountTypes code and user-facing meaning | Stop and request Amount, Percentage, Both, or a valid code; do not infer another value |

## Attribute Presentation Mapping

| User-Facing Label | REST Attribute | Reference Resolver | Display Rule |
|---|---|---|---|
| Available Payment Methods | OrgPaymentMethodsAvailableToWorker | find_organization_payment_methods_by_ldg | When fetched through REST, split pipe-separated IDs, trim whitespace, reject empty values, resolve each ID in order, remove duplicate IDs while preserving first-occurrence order unless the REST contract requires duplicates, retain the pipe-separated REST value for presentation, and display every resolved OPM name. |
| Noneditable Payment Methods | OrgPaymentMethodsRestrictedForEdit | find_organization_payment_methods_by_ldg | When fetched through REST, split pipe-separated IDs, trim whitespace, reject empty values, resolve each ID in order, remove duplicate IDs while preserving first-occurrence order unless the REST contract requires duplicates, retain the pipe-separated REST value for presentation, and display every resolved OPM name. |
| Maximum Personal Payment Methods | PaymentMethodsMaximumNumber | | Display the returned value without replacing it with a REST attribute name. |
| Payment Amount Types | PaymentAmountTypes | resolve_payment_amount_type | Retain A, P, or B internally and display Amount, Percentage, or Both. |
| Exclude from 100% Validation | ValidationExclusionFlag | find_yes_no_lookup | Retain the lookup code internally and display the resolved YES_NO meaning. |
| Legislative Data Group | LegislativeDataGroupId | find_ldg_by_exact_name | Use a denormalized LDG display value in the response when present; otherwise resolve it. |

## Describe Attribute Metadata

| Level | Attribute | REST Field | Data Type | Required | Reference/LOV | Validation | Source |
|---|---|---|---|---|---|---|---|
| Payment Method Preferences | Not available until a describe response is supplied | Not specified by describe response | Not specified by describe response | Not specified by describe response | Not specified by describe response | Not specified by describe response | paymentMethodOptions |

When a describe response is available, replace this placeholder with one row per returned attribute. Preserve each returned property exactly; use Not specified by describe response only for a property absent from that response.

## Custom Action Attribute Contract

The following is the developer-supplied custom-action contract. It specifies known attributes that must be represented in a MERGE payload; it does not infer server data types, requiredness, or updateability, which remain describe-controlled. In addition, MERGE must carry every optional attribute returned by the current preference lookup.

| Attribute | User-Facing Label | MERGE Construction Rule | Metadata Source |
|---|---|---|---|
| LegislativeDataGroupId | Legislative Data Group | Include the latest existing identity; it is immutable for MERGE. | Developer-supplied custom-action contract |
| PaymentMethodsMaximumNumber | Maximum Personal Payment Methods | Include the validated changed value, or the latest existing value when unchanged. | Developer-supplied custom-action contract |
| ValidationExclusionFlag | Exclude from 100% Validation | Include the validated changed value, or the latest existing value when unchanged. | Developer-supplied custom-action contract |
| PaymentAmountTypes | Payment Amount Types | Include the validated changed value, or the latest existing value when unchanged. | Developer-supplied custom-action contract |
| OrgPaymentMethodsAvailableToWorker | Available Payment Methods | For a REST custom action, include the validated pipe-separated changed value, or the latest pipe-separated REST value when unchanged. DAT conversion is governed separately below. | Developer-supplied custom-action contract and developer-supplied DAT delimiter instruction |
| OrgPaymentMethodsRestrictedForEdit | Noneditable Payment Methods | For a REST custom action, include the validated pipe-separated changed value, or the latest pipe-separated REST value when unchanged. DAT conversion is governed separately below. | Developer-supplied custom-action contract and developer-supplied DAT delimiter instruction |

## DELETE attributesMap Contract

| DAT Section | Required Structural Fields | Required Business Attribute | Other Business Attributes | Construction Rule | Source |
|---|---|---|---|---|---|
| attributesMap | PreferencesKey set to the resolved LegislativeDataGroupId; RestAction set to POST | LegislativeDataGroupId set to the resolved ID | Leave blank | Always emit one populated attributesMap DELETE row. LegislativeDataGroupId is sufficient for the delete business payload; do not populate payment-method controls or OPM attributes. RestAction is POST regardless of operation. | Developer-supplied DELETE payload guidance and custom-action RestAction instruction |

## DAT OPM Attribute Formatting

| Attribute | Applies When | Required DAT Value | Example | REST Handling |
|---|---|---|---|---|
| OrgPaymentMethodsAvailableToWorker | User-provided input is converted into DAT content | Join validated OPM IDs with a comma. Do not use a pipe in DAT content. | 300100023362296,300100023362299 | Fetch and parse the REST attribute as pipe-separated; retain pipe-separated formatting when presenting the REST value. |
| OrgPaymentMethodsRestrictedForEdit | User-provided input is converted into DAT content | Join validated OPM IDs with a comma. Do not use a pipe in DAT content. | 300100023362296,300100023362299 | Fetch and parse the REST attribute as pipe-separated; retain pipe-separated formatting when presenting the REST value. |

## Search Presentation

| Output Mode | Fields to Display | Presentation Rule |
|---|---|---|
| Default search result | Legislative Data Group; Maximum Personal Payment Methods; Payment Amount Types; Exclude from 100% Validation | Display names and resolved meanings; do not show raw IDs or lookup codes. |
| Complete details | Default search fields; Available Payment Methods; Noneditable Payment Methods | Resolve and display OPM names in their preserved order. |
| Technical details explicitly requested | LDG ID; Organization Payment Method IDs; raw lookup codes | Add technical values alongside, not instead of, user-facing names and meanings. |

## Preference Hierarchy Presentation

Use this wire diagram when the user asks to show or explain complete Payment Method Preference details:

```text
Payment Method Preference: <LEGISLATIVE_DATA_GROUP_NAME>
├── Available Payment Methods
│   ├── <OPM_NAME_1>
│   └── <OPM_NAME_2>
├── Noneditable Payment Methods
│   └── <OPM_NAME_3>
└── Preference Controls
    ├── Maximum Personal Payment Methods: <NUMBER>
    ├── Payment Amount Types: <AMOUNT | PERCENTAGE | BOTH>
    └── Exclude from 100% Validation: <YES | NO>
```

| Presentation Condition | Required Behavior |
|---|---|
| Diagram preparation | Resolve the LDG name, every available and noneditable OPM ID, Payment Amount Types, and Validation Exclusion Flag before presenting the diagram. |
| Denormalized response values | Use a returned name, display value, description, or meaning directly; do not perform a duplicate REST lookup. |
| Technical details requested | Add an OPM ID below its resolved name and include the LDG ID and raw lookup codes alongside their user-facing values. |
| Unresolved OPM reference | Show ID: <OPM_ID> followed by Name: Unresolved. Never display the ID as though it were a resolved name. |
| Other unresolved reference | Retain the supplied ID or code internally, show Unresolved to the user, and state which resolver did not return one match. |

## Request-Scoped REST Efficiency

| Rule | Required Behavior |
|---|---|
| LDG resolution | Cache and reuse a resolved LDG identity for the full user request. |
| OPM retrieval | Retrieve OPMs once for a resolved LDG, then reuse the result for Available Payment Methods, Noneditable Payment Methods, validation, and diagram presentation. |
| Lookup retrieval | Reuse each resolved YES_NO and Payment Amount Type value within the same user request. |
| Denormalized values | Prefer a source response name or meaning over an additional lookup. |
| Static values | Do not repeatedly retrieve static lookup values in one request. |
| Multi-value ordering | Preserve the original order of multi-value attributes through resolution and presentation. |

## Resource Coverage

| Requested Capability | Resource Package Coverage |
|---|---|
| Functional overview and task scope | Existing generated task SKILL.md and the functional, validation, and design resources. |
| REST resources, finder, custom action, references, and LOVs | ora_reference_lookups.md and ora_dependency_readiness.md. |
| Attribute labels, user-facing display, hierarchy, and error behavior | ora_reference_lookups.md and ora_error_handling.md. |
| Validation, duplicate prevention, create, update, or delete preconditions, and full-state MERGE construction | ora_input_validation.md, ora_dependency_readiness.md, and ora_design_enforcement.md. |
| Describe attribute metadata | Describe contract is present; per-attribute rows require the actual describe response. |
| Payload templates, REST-execution resource, standalone samples, and test files | Not supported by fusionapps-resource-authoring current-strict scope; do not create them here. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| An identifier is already supplied | Retain it only after the applicable documented validation succeeds; do not replace it with a guessed display value. |
| A name resolves exactly once | Use the resolved ID or code internally and the returned user-facing name or meaning in presentation. |
| A name value is supplied for any mapped attribute | Derive its ID or code through the applicable documented reference lookup; do not ask the user to provide an ID or code. |
| A response already includes a name, display value, description, or meaning | Use that denormalized human-readable value and do not make an additional REST call. |
| A pipe-separated OPM value is fetched from REST and contains an unresolved ID | Preserve its position and ID, retain pipe-separated presentation, mark it Unresolved, and return a validation error for a create or update request. |
| A pipe-separated OPM value is fetched from REST and contains an empty value | Reject the field and identify the empty position; do not silently remove it. |
| A pipe-separated OPM value is fetched from REST and contains duplicate IDs | Keep the first occurrence and remove later duplicates while preserving order, unless a future REST contract explicitly requires duplicates. |
| User-provided OPM input is converted into DAT content | Convert the validated ordered IDs to one comma-separated value for OrgPaymentMethodsAvailableToWorker and OrgPaymentMethodsRestrictedForEdit only. Do not convert REST response values or their presentation to commas. |
| A name has no match or many matches | Stop and request a more precise value; never select a candidate automatically. |
| A mutation is prepared | Resolve the LDG and run Intent SEARCH. Never ask for operation: use CREATE when no preference exists, MERGE when exactly one exists, and DELETE only when deletion was requested and exactly one exists. Intent CREATE can be used as an additional eligibility check. |
| A custom-action payload or DAT row is prepared | Set RestAction to POST for CREATE, MERGE, and DELETE. Keep the SEARCH-derived operation separate from RestAction. |
| operation is MERGE | Build the payload or DAT row from the complete just-read preference state. Include every returned attribute, including optional attributes, and all supplied action-contract attributes; overlay only user-supplied validated values. Do not submit a modified-fields-only or stale-state payload. |
| A preference hierarchy is requested | Resolve only values without a denormalized human-readable value, reuse request-scoped results, and mark every unresolved reference clearly in the wire diagram. |
| Describe metadata is requested but unavailable | Do not claim field types, required status, lengths, updateability, defaults, or relationships; request the describe response. |
| CRUD details are requested | Use resolved IDs and codes in the developer-supplied custom action only. For MERGE, use the complete latest action-contract state described here; the resource package does not generate standalone payload templates or execute mutations. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PPMP.LOOKUP_PREFERENCES | step | 3 | reference_lookup | create->PPMP.APPLY_DEFAULTS;merge->PPMP.APPLY_DEFAULTS;delete->PPMP.APPLY_DEFAULTS;not_found_for_delete->RETURN_ISSUES;ambiguous->RETURN_ISSUES | PPMP.RESOLVE_DEPENDENCIES | stop | A mutation requires automatic operation selection or a preference search is requested |
| PPMP.LOOKUP_LDG | decision | 4 | reference_lookup | opm_required->PPMP.LOOKUP_OPMS;resolved->PPMP.APPLY_DEFAULTS;not_found->RETURN_ISSUES;ambiguous->RETURN_ISSUES | PPMP.RESOLVE_DEPENDENCIES | stop | An LDG name is supplied or OPMs are needed |
| PPMP.LOOKUP_OPMS | step | 5 | reference_lookup | resolved->PPMP.APPLY_DEFAULTS;not_found->RETURN_ISSUES;ambiguous->RETURN_ISSUES | PPMP.LOOKUP_LDG | stop | OPM choices are supplied or displayed |
| PPMP.LOOKUP_YES_NO | step | 6 | reference_lookup | resolved->PPMP.APPLY_DEFAULTS;not_found->RETURN_ISSUES;ambiguous->RETURN_ISSUES | PPMP.RESOLVE_DEPENDENCIES | stop | A yes-or-no preference is supplied or displayed |

## Sources

- Oracle Fusion Cloud HCM REST API, Get legislative data groups list of values: https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-legislativedatagroupslov-legislativedatagroupid-get.html
- Oracle Fusion Cloud HCM REST API, Get all common lookups: https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-commonlookupslov-get.html
- Developer-supplied endpoint and finder details for Payment Method Preferences and Organization Payment Methods.

## Data Creation and Import Execution Policy

The documented REST routes, finder details, and custom-action material in this file are retained for reference only. They are not an execution route for creating, importing, or loading Personal Payment Method Preferences.

| Requested Outcome | Required Execution Route | Business Object | Prohibited Route |
|---|---|---|---|
| Create data | core.data-loader preparation, preview, approval, and load workflow | paymentMethodOptions | Direct CRUD endpoint or custom action |
| Import data | core.data-loader preparation, preview, approval, and load workflow | paymentMethodOptions | Direct CRUD endpoint or custom action |
| Load data | core.data-loader preparation, preview, approval, and load workflow | paymentMethodOptions | Direct CRUD endpoint or custom action |

## Execution Policy Source

- Developer instruction: retain documented instructions for reference; perform actual data create, import, and load through the documented business object.
