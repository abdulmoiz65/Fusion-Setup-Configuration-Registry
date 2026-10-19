# Reference Lookups

## Source

| Source | Location | Used For |
|---|---|---|
| Developer-provided non-Cost Organization LOV REST contract | /fscmRestApi/resources/11.13.18.05/nonCostOrganizationsLOV?q=Name = "&lt;cost organization name&gt;"&amp;limit=1 | Exact existing-organization validation and classification and effective-start-date resolution |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_non_cost_organization_exact | CopyExistingOrgFlag is true | One exact CopyOrganizationName and an optional user-supplied EffectiveStartDate | /fscmRestApi/resources/11.13.18.05/nonCostOrganizationsLOV?q=Name = "&lt;CopyOrganizationName&gt;"&amp;limit=1 | OrganizationId, Name, ClassificationCode, EffectiveStartDate | Preserve case and punctuation. Require one returned item whose Name exactly matches CopyOrganizationName, with hasMore false. Compare any user-supplied EffectiveStartDate with the returned EffectiveStartDate. | OrganizationId as lookup evidence; CopyOrganizationName confirmed from Name; CopyOrgClassificationCode from ClassificationCode; EffectiveStartDate from EffectiveStartDate | Zero matches, more than one match, hasMore true, authentication, authorization, transport, or response-shape failures block the workflow. A differing user-supplied EffectiveStartDate requires approval to use the returned date. Do not select the first or partial result. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Operation scope | This resolver performs only the documented read-only nonCostOrganizationsLOV lookup. It must not create, update, delete, upload, or initiate setup data. |
| Environment identity | Join the documented relative request path to the active, approved Fusion restBaseUrl. Do not supply or override a host. |
| Effective start date | When CopyExistingOrgFlag is true, use the EffectiveStartDate returned by this lookup. Do not retain a user-supplied effective start date. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CCO.RESOLVE_EXISTING_ORGANIZATION | step | 3 | reference_lookup | resolved->CCO.CONFIRM_EFFECTIVE_START_DATE_OVERRIDE;not_applicable->CCO.CONFIRM_EFFECTIVE_START_DATE_OVERRIDE;blocked->CCO.HANDLE_ISSUE;failure->CCO.HANDLE_ISSUE | CCO.NORMALIZE_STATUS | stop | Create a cost organization; resolve only when CopyExistingOrgFlag is true |
