# Manage Actions Design Enforcement

## Purpose

Defines the mandatory Action and association design gates evaluated before
preview or routing. It does not perform lookups, apply defaults, or create
missing setup.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm object and identity | Require a supported object shape and one exact Action or create-availability result |
| 2 | Resolve supplied references | Resolve Country, Action Type, Action Reason, assignment status, and role values exactly |
| 3 | Validate association | Confirm the correct usage row, parents, role, and registered mapping shape |
| 4 | Confirm mutation control | Require current source, preview, approval, and the declared Data Loader route |
| 5 | Decide readiness | Continue only when no applicable blocking rule remains |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| REGISTERED_OBJECT | Every request | Blocking |  | Actions does not support the requested operation, field, source shape, parent chain, or association row | Use only the registered supported operation and shape | No |
| IDENTITY | Read, copy, edit, delete, association work, or create uniqueness check | Blocking | find_manage_actions | The Action identity, Action Code, association, or create result is missing, ambiguous, or duplicated | Supply one exact target or unique Action Code | Lookup fix |
| CONFIGURED_REFERENCE | A configured Action value is supplied | Blocking | resolve_action_common_lookup | Action Type, Action Reason, assignment status, or another configured value is missing, disabled, ineffective, ambiguous, or incompatible | Resolve one compatible stored value | Lookup fix |
| COUNTRY | Country is supplied or required | Blocking | resolve_action_country | Country is missing or ambiguous | Resolve one canonical country code | Lookup fix |
| ASSOCIATION_DATE | An association date changes | Blocking | find_manage_actions | The change targets a global Action Reason row instead of the matching action-reason usage row | Target the exact current usage row | Lookup fix |
| ROLE_MAPPING | An action-reason role mapping is requested | Blocking | resolve_action_role | The parents, Action Type, active role, or registered mapping shape is missing or inconsistent | Resolve the exact parents and active role, then use the registered mapping shape | Lookup fix |
| SOURCE | A mutation is prepared | Blocking |  | XLSX source, key provenance, validation result, or immutable preview is missing or stale | Rebuild and validate the smallest current XLSX source | Source rebuild |
| PREVIEW_CONTENT | A mutation preview is prepared | Blocking |  | The preview omits the environment alias, operation, exact target, requested delta, preserved rows, resolved reference labels, XLSX source fingerprint, immutable Data Loader preview, or post-load reconciliation plan | Rebuild the complete immutable preview | Re-preview |
| SENSITIVE_OUTPUT | A preview or user-facing result is produced | Blocking |  | Credentials, runtime links, raw payloads, or transient IDs are exposed | Regenerate the output with sensitive and transient values removed | Re-preview |
| APPROVAL | A mutation is ready for submission | Blocking |  | Approval is absent, stale, bound to different target, source, metadata, preview, or reconciliation evidence, or any displayed or source value changed after approval | Obtain approval for the exact immutable preview | Re-preview |
| ROUTE | Create, edit, or delete | Blocking |  | Fusion REST, FSM import, CSV omission, or an unapproved retry is proposed | Use only the declared Core Data Loader route | No |

| ACTION_REUSE_IMPACT | Create or edit | Warning |  | An existing Action is not considered, required Action Reasons are absent, or downstream impact is unreviewed | Reuse a suitable Action, create Reasons first, and review payroll, reporting, and integrations | Input fix |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_manage_actions | Target, association, date-row, copy-source, or create-uniqueness evaluation | Exact Action identity, current usage rows, effective context, and match cardinality | ora_reference_lookups.md |
| resolve_action_common_lookup | A configured Action value is supplied | One enabled effective compatible stored value | ora_reference_lookups.md |
| resolve_action_country | Country is supplied or required | One canonical country code | ora_reference_lookups.md |
| resolve_action_role | An action-reason role mapping is requested | One active exact RoleCode and RoleName | ora_reference_lookups.md |

## Enforcement Outcomes

| Outcome | When Used | Next Action |
|---|---|---|
| passed | Every applicable blocking rule is satisfied | Continue to the declared routing node |
| not_required | No design rule applies to the requested operation | Continue without changing the request |
| blocked | An applicable blocker remains or required evidence is unavailable | Stop and require the declared correction |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ACT.ENFORCE | decision | 6 | design_enforcement | passed->ACT.ROUTE;not_required->ACT.ROUTE;blocked->ACT.ERROR | ACT.DEFAULTS | stop | After validation, dependencies, lookups, and defaulting are complete |
