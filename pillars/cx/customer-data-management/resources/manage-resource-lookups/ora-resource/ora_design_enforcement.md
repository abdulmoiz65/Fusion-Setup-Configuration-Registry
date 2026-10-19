# Manage Resource Lookups Design Enforcement

## Source Basis

- [Overview of Lookups](https://docs.oracle.com/en/cloud/saas/applications-common/26c/facia/overview-of-lookups.html#Using-Lookups-in-Applications)
- [Overview of Lookup Types](https://docs.oracle.com/en/cloud/saas/sales/oasal/overview-of-lookup-types.html)

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Resolve lookup facts | Resolve accessibility and configuration level before planning a change |
| 2 | Enforce editability | Apply configuration-level restrictions to the requested change |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Creating, updating, or deleting a lookup type or code | Blocker | resolve_lookup_accessibility | Configuration level or predefined-data restrictions do not permit the requested change | Use an allowed change or obtain a supported configuration approach | No |
| Accessing lookup values through REST | Blocker | resolve_lookup_accessibility | REST Access Secured is Secure and the caller lacks the required policy | Obtain an authorized role or change REST access only through approved security administration | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_lookup_accessibility | Every request | Configuration level and REST Access Secured setting | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MRL.ENFORCE_CONFIGURATION | decision | 4 | design_enforcement | compliant->MRL.RETURN_SUCCESS;blocked->MRL.RETURN_ISSUES | MRL.RESOLVE_LOOKUP | stop | Every request |
