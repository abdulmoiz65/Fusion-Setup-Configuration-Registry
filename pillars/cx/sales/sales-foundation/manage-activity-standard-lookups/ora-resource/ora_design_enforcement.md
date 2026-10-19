# Activity Standard Lookup Design Enforcement

Apply these gates before a guided UI plan, explicit setup-data import handoff,
or Apps Common Standard Lookup code handoff. An endpoint being available does
not override the lookup configuration level, predefined-data restrictions, or
Activity-specific behavior.

## Oracle Documentation Sources

| Source | Used For |
|---|---|
| https://docs.oracle.com/en/cloud/saas/sales/oasal/overview-of-lookup-types.html | User, Extensible, and System operation matrix |
| https://docs.oracle.com/en/cloud/saas/applications-common/26c/facia/overview-of-lookups.html | Code conventions, predefined data, translations, effective dates, enablement, deletion, and session refresh |
| https://docs.oracle.com/en/cloud/saas/sales/oasal/considerations-when-setting-up-call-reports.html | Activity Objective and Outcome behavior and no-tag restriction |
| https://docs.oracle.com/en/cloud/saas/sales/oasal/enable-default-task-status.html | Lowest status display sequence becomes the default task status |
| https://docs.oracle.com/en/cloud/saas/sales/oasal/change-calendar-colors.html | ZMM_ACTIVITY_TYPE is the only Activity lookup type that supports tags |
| https://docs.oracle.com/en/cloud/saas/sales/fasqa/how-do-i-configure-default-activity-search-in-accounts.html | Activity-search order and protected supplied values |
| https://docs.oracle.com/en/cloud/saas/sales/oasal/about-activity-type-and-subtype.html | Activity Type function membership and tag requirement |
| https://docs.oracle.com/en/cloud/saas/sales/faaps/op-activitytypelookupslov-get.html | Function-specific Activity Type verification |

## Configuration-Level Operation Matrix

| Requested Change | User Level U | Extensible Level E | System Level S |
|---|---|---|---|
| Insert a new lookup code | Allowed | Allowed | Blocked |
| Change Meaning | Allowed | Allowed | Allowed |
| Change EnabledFlag, StartDateActive, or EndDateActive | Allowed | Allowed only for non-predefined data | Blocked |
| Delete a lookup code | Allowed | Allowed only for non-predefined data | Blocked |
| Change Tag | Allowed only when the Activity lookup type supports tags | Blocked | Blocked |

Treat `LastUpdatedBy=SEED_DATA_FROM_APPLICATION` as positive predefined-data
evidence, but do not treat another updater as proof that the row was never
predefined. For an Extensible parent, confirm the live task control before a
restricted date, enablement, or delete change when predefined status remains
uncertain. When the live task page provides stricter editability than this
matrix, the stricter live control wins.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm task boundary | Verify that the existing parent type belongs to Manage Activity Standard Lookups. |
| 2 | Confirm exact current state | Read the parent and exact child code before choosing Create or a maintenance operation. |
| 3 | Apply editability | Enforce the configuration-level matrix and predefined-data restrictions for every changed field. |
| 4 | Apply Activity-specific rules | Enforce tag support, status-default impact, Activity-search order, and supplied-value restrictions. |
| 5 | Enforce Activity Type functions | For ZMM_ACTIVITY_TYPE Create, require exact function selection, enablement, effective start, and the canonical derived Tag. |
| 6 | Confirm downstream impact | Review consumers before deactivation or deletion and prefer reversible end-dating when historical interpretation matters. This preference is an FSCR safety recommendation. |
| 7 | Bind approval | Bind an Apps Common write to the exact environment, current-state fingerprint, method, endpoint, and body or delete effect; bind an explicit import to the exact ZIP SHA-256, row delta, task code, environment, and verification plan. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Any create or maintenance request | Error | resolve_activity_standard_lookup_type | The parent exists in Standard Lookups but no current evidence places it in Manage Activity Standard Lookups | Use one of the publicly documented Activity types or provide current task-page or task-export evidence | Yes, by correcting or verifying the task scope |
| Operation is Create | Error | find_activity_standard_lookup_code | The exact code already exists, the parent is System level, or Meaning is missing | Review the existing row or submit a distinct stable code under a User or Extensible parent | Yes |
| Operation is Create and LookupType is ZMM_ACTIVITY_TYPE | Error | derive_activity_type_function_tag | ActivityFunctionCodes is blank, contains an unsupported or duplicate value, EnabledFlag or StartDateActive is missing, or Tag differs from the canonical function-derived value | Supply the exact intended functions, enablement, and start date; derive Tag without selecting a function on the requester's behalf | Yes |
| Operation is Update | Error | find_activity_standard_lookup_code | The request attempts to change LookupCode or includes a field disallowed by the configuration matrix | Keep LookupCode immutable and limit PATCH to permitted fields | Yes |
| Operation is Deactivate | Error | find_activity_standard_lookup_code | The parent is System level or the row is predefined data under an Extensible parent | Preserve the protected row; change Meaning only if that is the authorized business need | Yes when the matrix permits it |
| Operation is Delete | Error | find_activity_standard_lookup_code | The matrix disallows deletion or downstream and historical impact has not been reviewed | Prefer disablement or end-dating when history must remain interpretable; delete only after explicit impact acceptance | Yes when Oracle and policy permit it |
| Tag is supplied for a new Activity Type | Error | derive_activity_type_function_tag | LookupType is not ZMM_ACTIVITY_TYPE or Tag differs from the exact canonical function-derived value | Use the derived colon-wrapped function Tag only on a new ZMM_ACTIVITY_TYPE code | Yes |
| A calendar-color Tag update is requested | Error | find_activity_standard_lookup_code | Current evidence doesn't prove a representation that preserves existing function membership while storing the requested HTML color | Use guided UI or provide reviewed current-environment evidence for the combined representation; do not overwrite the function Tag | Yes |
| LookupType is ORA_ZMM_ACTIVITY_OBJECTIVE or ZMM_ACTIVITY_OUTCOME | Error |  | Tag is supplied | Remove Tag; Oracle documents that these types do not support tags | Yes |
| LookupType is ZMM_ACTIVITY_STATUS_CD and DisplaySequence changes | Error | list_activity_standard_lookup_codes | The full active sibling order was not read or the requester has not accepted the resulting default task status | Show the current and proposed lowest sequence and obtain explicit impact acceptance | Yes |
| LookupType is ORA_ZMM_ACTIVITY_FILTER_TYPE | Error | list_activity_standard_lookup_codes | The request adds, deletes, or end-dates a value, or changes sequence without accepting the resulting default Activity search | Limit the change to documented display-sequence behavior for the fixed supplied list and approve the proposed order | Yes |
| Operation is Translate | Error |  | Language is not enabled, TranslatedMeaning is blank, or a direct translation write is requested without a documented executor contract | Use the lookup translation UI or a current approved setup-data package | Yes |
| Create, Update, Deactivate, or Delete is selected for live execution | Error | find_activity_standard_lookup_code | The exact current state, canonical link, target environment, immutable Apps Common preview, or matching explicit approval is missing | Re-read the target and rebuild the preview; never reuse stale approval | Yes |
| Operation is Import | Error | verify_activity_standard_lookup_csv_package | The ZIP is not a completed current task package, the ZMM_ACTIVITY_TYPE parent or metadata-derived headers changed, the candidate row has system audit values, the row delta is not unique, or exact package approval is missing | Build a separate ZIP from the completed export, add only the reviewed row with blank system fields, validate it, and route it through core.data-loader | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_activity_standard_lookup_type | Always | LookupType, CustomizationLevel, ParentItemLink, TaskScopeEvidence | ora_reference_lookups.md |
| find_activity_standard_lookup_code | A LookupCode is supplied | LookupCode, current fields, LastUpdatedBy, CodeItemLink | ora_reference_lookups.md |
| list_activity_standard_lookup_codes | An order-sensitive DisplaySequence is created or changed | CurrentLookupOrder, CurrentDefaultCode, ProposedLookupOrder, ProposedDefaultCode | ora_reference_lookups.md |
| derive_activity_type_function_tag | ZMM_ACTIVITY_TYPE is created | ActivityFunctionCodes, Tag | ora_reference_lookups.md |
| verify_activity_standard_lookup_csv_package | Operation is Import | PackageTaskCode, PackageProcessStatus, ParentRow, ChildHeaders, CandidateRow, PackageSha256 | ora_reference_lookups.md |
| verify_activity_type_by_function | Post-create verification for ZMM_ACTIVITY_TYPE | VerifiedActivityFunctionCodes, VerifiedLookupCode, VerifiedMeaning, VerifiedEnabledFlag, VerifiedStartDateActive, VerifiedTag | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ACTIVITY_STD.DESIGN | decision | 7 | design_enforcement | allowed->ACTIVITY_STD.EXECUTION_GATE;policy_block->ACTIVITY_STD.BLOCKED;invalid_evidence->ACTIVITY_STD.FAILED | ACTIVITY_STD.DEFAULTS | stop | Always |
