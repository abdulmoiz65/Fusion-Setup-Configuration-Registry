# Design Enforcement

## Source

- Oracle readiness: Streamline the Import and Export of Messaging Setup Data, 26C, https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/sccv26c/26C-sccv-wn-f46531.htm
- Oracle readiness: Redwood: Simplify Configuration and Processing for B2B Messaging, 25C, https://docs.oracle.com/en/cloud/saas/readiness/scm/25c/sccv25c/25C-sccv-wn-f39141.htm

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm simplified feature state | Do not proceed unless the feature is enabled on the selected host |
| 2 | Confirm migration scope | Include the service-provider task when migrating all Collaboration Messaging configuration objects |
| 3 | Confirm supported simplified setup | Do not use unsupported documents, predefined providers, or override message definitions where the enabled release documents those limitations |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Migrating all Collaboration Messaging configuration data through a configuration package | Blocking | | Manage Collaboration Messaging Service Providers is not included with this task | Add both documented tasks to the implementation project | Yes |
| Simplified B2B Messaging is enabled | Blocking | resolve_simplified_feature_state | Feature state cannot be verified | Provide approved feature-state evidence | Yes |
| A release documents simplified-setup limitations | Blocking | | Requested document, provider, or override-message design conflicts with the documented limitation | Adjust scope or obtain a release-qualified design decision | Conditional |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_simplified_feature_state | Before simplified configuration is accessed | Feature enabled state | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CMKSC.ENFORCE_DESIGN | decision | 40 | design_enforcement | passed->CMKSC.GATE_EXECUTION;blocked->CMKSC.RETURN_ISSUES | CMKSC.RESOLVE_FEATURE_STATE | stop | Always |
