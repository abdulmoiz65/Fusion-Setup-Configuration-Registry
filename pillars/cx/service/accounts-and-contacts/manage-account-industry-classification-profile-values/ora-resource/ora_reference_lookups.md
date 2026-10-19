# Reference Lookups

Use only read-only Apps Common Profile Values reads to verify the effective Industry Classification Category value for the current authenticated user session. Do not infer a configured value from a missing response, use these lookups to write a value, or select an import adapter.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| read_industry_classification_profile_value | View or update requests for MOT_INDUSTRY_CLASS_CATEGORY when it is REST exposed | Exact ProfileOptionName=MOT_INDUSTRY_CLASS_CATEGORY | /fscmRestApi/resources/11.13.18.05/profileValues | ProfileOptionName, ProfileOptionValue | Match the resolved profile value for the current authenticated user session | Effective ProfileOptionValue | Identify a non-REST-exposed option separately; do not infer a configured value from a missing response. Use a fresh task export for persisted profile-value verification. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| The request is import and no profile-value row changes | Do not run a Profile Values lookup solely to inspect unrelated values |
| The request changes the MOT_INDUSTRY_CLASS_CATEGORY row | Use a fresh task export to verify the persisted row; read the effective value only when the option is REST exposed |
| A read returns a privilege or transport failure | Stop before preview; classify the failure and do not substitute a browser or guessed configured value |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AICP.READ_PROFILE_OPTION | step | 2 | reference_lookup | resolved->AICP.DEPENDENCY_READINESS;unresolved->AICP.ERROR | AICP.VALIDATE_CONTEXT | stop | When effective-value verification is requested and MOT_INDUSTRY_CLASS_CATEGORY is REST exposed |
