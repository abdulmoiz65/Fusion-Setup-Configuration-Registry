# Manage Action Reasons Design Enforcement

## Purpose

Defines the mandatory Action Reason and usage-association design gates evaluated
before preview or routing. It does not perform lookups, apply defaults, or
create missing setup.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm object and identity | Require a supported object shape and one exact Action Reason or create-availability result |
| 2 | Resolve supplied references | Resolve each configured value, Country, role, and parent Action exactly |
| 3 | Validate association | Require both the Action and Action Reason before authoring an association |
| 4 | Confirm mutation control | Require current source, preview, approval, and the declared Data Loader route |
| 5 | Decide readiness | Continue only when no applicable blocking rule remains |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| REGISTERED_OBJECT | Every request | Blocking |  | ActionReasons does not support the requested operation, field, source shape, or association row | Use only the registered supported operation and shape | No |
| IDENTITY | Read, edit, delete, association work, or create uniqueness check | Blocking | find_manage_action_reasons | The Action Reason identity or Reason Code result is missing, ambiguous, or duplicated for create | Supply one exact target or unique Reason Code | Lookup fix |
| CONFIGURED_REFERENCE | A configured lookup value is supplied | Blocking | resolve_action_reason_common_lookup | The value is missing, disabled, ineffective, ambiguous, or incompatible | Resolve one compatible stored value | Lookup fix |
| COUNTRY | Country is supplied or required | Blocking | resolve_action_reason_country | Country is missing or ambiguous | Resolve one canonical country code | Lookup fix |
| ROLE | A role condition is supplied | Blocking | resolve_action_reason_role | The role is missing, inactive, or ambiguous | Resolve one active exact role | Lookup fix |
| ASSOCIATION | An Action Reason association is requested | Blocking | resolve_action_reason_action | The parent Action or Action Reason is unavailable or ambiguous | Resolve both exact parents before authoring the association | Lookup fix |
| SOURCE | A mutation is prepared | Blocking |  | XLSX source, key provenance, validation result, or immutable preview is missing or stale | Rebuild and validate the smallest current XLSX source | Source rebuild |
| PREVIEW_CONTENT | A mutation preview is prepared | Blocking |  | The preview omits the environment alias, operation, exact target, requested delta, preserved rows, resolved reference labels, XLSX source fingerprint, immutable Data Loader preview, or post-load reconciliation plan | Rebuild the complete immutable preview | Re-preview |
| SENSITIVE_OUTPUT | A preview or user-facing result is produced | Blocking |  | Credentials, runtime links, raw payloads, or transient IDs are exposed | Regenerate the output with sensitive and transient values removed | Re-preview |
| APPROVAL | A mutation is ready for submission | Blocking |  | Approval is absent, stale, bound to different target, source, metadata, preview, or reconciliation evidence, or any displayed or source value changed after approval | Obtain approval for the exact immutable preview | Re-preview |
| ROUTE | Create, edit, or delete | Blocking |  | Fusion REST, FSM import, CSV omission, or an unapproved retry is proposed | Use only the declared Core Data Loader route | No |

| REASON_REUSE_ASSOCIATION | Create or edit | Warning |  | An existing reason is not considered or its Action association is not confirmed | Reuse a suitable reason and associate it with the correct Action | Input fix |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_manage_action_reasons | Target, association, or create-uniqueness evaluation | Exact Action Reason identity, effective context, current values, and cardinality | ora_reference_lookups.md |
| resolve_action_reason_common_lookup | A configured lookup value is supplied | One enabled effective compatible stored value | ora_reference_lookups.md |
| resolve_action_reason_country | Country is supplied or required | One canonical country code | ora_reference_lookups.md |
| resolve_action_reason_role | A role condition is supplied | One active exact RoleCode and RoleName | ora_reference_lookups.md |
| resolve_action_reason_action | An association is requested | One current compatible Action identity | ora_reference_lookups.md |

## Enforcement Outcomes

| Outcome | When Used | Next Action |
|---|---|---|
| passed | Every applicable blocking rule is satisfied | Continue to the declared routing node |
| not_required | No design rule applies to the requested operation | Continue without changing the request |
| blocked | An applicable blocker remains or required evidence is unavailable | Stop and require the declared correction |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AR.ENFORCE | decision | 6 | design_enforcement | passed->AR.ROUTE;not_required->AR.ROUTE;blocked->AR.ERROR | AR.DEFAULTS | stop | After validation, dependencies, lookups, and defaulting are complete |
