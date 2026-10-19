# Activity Standard Lookup Defaulting Rules

Apply only REST-contract or task-intrinsic defaults. Never invent a parent type,
lookup code, meaning, description, date, sequence, tag, translation, or
deactivation method.

## Oracle Documentation Sources

| Source | Used For |
|---|---|
| https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/op-http-servername-fscmrestapi-resources-11.13.18.05-standardlookups-lookuptype-child-lookupcodes-get.html | EnabledFlag default and lookup-code fields |
| https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-standard-lookups.html | Standard lookup create and update behavior |
| https://docs.oracle.com/en/cloud/saas/applications-common/26c/facia/overview-of-lookups.html | Effective-date and enablement semantics |
| https://docs.oracle.com/en/cloud/saas/sales/oasal/about-activity-type-and-subtype.html | Activity Type function codes and tag requirement |

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| EnabledFlag | Y | Operation is Create and EnabledFlag is omitted | No |  |
| UpsertMode | false | Every Apps Common Create | No |  |
| AutomaticMutationRetry | disabled | Every POST, PATCH, or DELETE | No |  |
| VerificationMethod | Exact GET of the returned CodeItemLink or the exact LookupType and LookupCode path | Every Apps Common mutation | No | find_activity_standard_lookup_code |
| Tag | Canonical leading-and-trailing-colon string derived from exactly the supplied ActivityFunctionCodes in APPOINTMENT, TASK, CALLREPORT order | Operation is Create and LookupType is ZMM_ACTIVITY_TYPE | No | derive_activity_type_function_tag |
| Description | No automatic default | Create, Update, or Translate | No |  |
| StartDateActive | No automatic default | Create or Update | No |  |
| EndDateActive | No automatic default | Create, Update, or Deactivate | No |  |
| DisplaySequence | No automatic default | Create or Update | No |  |
| Tag | No automatic default | Create or Update when LookupType is not ZMM_ACTIVITY_TYPE | No |  |
| Meaning | No automatic default | Create, Update, or Translate | No |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ACTIVITY_STD.DEFAULTS | step | 6 | apply_default | defaults_applied->ACTIVITY_STD.DESIGN;no_default_needed->ACTIVITY_STD.DESIGN;invalid_default_context->ACTIVITY_STD.BLOCKED | ACTIVITY_STD.LOOKUP_ORDER | stop | Always |
