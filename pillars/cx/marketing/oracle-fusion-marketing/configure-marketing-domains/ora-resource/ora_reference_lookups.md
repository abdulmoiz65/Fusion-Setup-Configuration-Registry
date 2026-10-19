# Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| list_marketing_domains | A Marketing domain list, inspection, or update is requested | Configured target environment, optional domainToUpdate, $limit=100, and $offset=0 | /api/boss/data/objects/ora/cxMarketingCommonShared/configuration/v1/domains | primaryDomain, activeFlag, emailDomainFlag, micrositeDomainFlag, emailDomainPreference, micrositeDomainPreference, senderName, senderEmail, replyToName, replyToEmail, bounceBackEmail | Start with $limit=100 and $offset=0; fetch every page. Without domainToUpdate, present the completed list. With domainToUpdate, select exactly one record whose primaryDomain exactly equals it. | Completed domain list, or selected primaryDomain and selected record | Without domainToUpdate: ask the required exact selection prompt and stop. No exact match: show available values and stop. Many exact matches: stop; duplicate resolution is not documented. |
| read_selected_marketing_domain | An exact domainToUpdate value was selected from the completed domain list | Configured target environment, domainToUpdate, $limit=100, and $offset=0 | /api/boss/data/objects/ora/cxMarketingCommonShared/configuration/v1/domains | primaryDomain, activeFlag, emailDomainFlag, micrositeDomainFlag, emailDomainPreference, micrositeDomainPreference, senderName, senderEmail, replyToName, replyToEmail, bounceBackEmail | Re-run every page, then select exactly one response record whose primaryDomain exactly equals domainToUpdate | Unredacted Section, Field, Current Value table: Domain (Primary Domain, DNS Status); Domain Settings (every enabled preference); Default Headers (all five header fields) | No exact match: stop and return to the domain list without requesting changes. Many exact matches: stop; duplicate resolution is not documented. |
| read_back_marketing_domain | Data Loader accepts the approved update | Configured target environment, domainToUpdate, $limit=100, and $offset=0 | /api/boss/data/objects/ora/cxMarketingCommonShared/configuration/v1/domains | primaryDomain, activeFlag, emailDomainFlag, micrositeDomainFlag, emailDomainPreference, micrositeDomainPreference, senderName, senderEmail, replyToName, replyToEmail, bounceBackEmail | Re-run every page, then select exactly one response record whose primaryDomain exactly equals domainToUpdate | Unredacted Section, Field, Current Value table using the selected-record layout | No exact match or many matches: stop and disclose the failure. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DOMAINS.LIST_SELECT | step | 3 | reference_lookup | listed->DOMAINS.AWAITING_SELECTION;selected->DOMAINS.SHOW_SELECTED;no_match->RETURN_ISSUES;many_match->RETURN_ISSUES | DOMAINS.ACCESS | stop | A completed Marketing domain list is requested, with or without domainToUpdate |
| DOMAINS.SHOW_SELECTED | step | 5 | reference_lookup | shown->DOMAINS.COLLECT_CHANGES;no_match->RETURN_ISSUES;many_match->RETURN_ISSUES | DOMAINS.LIST_SELECT | stop | domainToUpdate exactly matches one primaryDomain from the completed domain list |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| BOSS client and OAuth | Route /api/boss calls through core.fusion-api.rest-api-client and its BOSS client with boss_scope. Use the configured shared OAuth flow and token cache; never construct or disclose an Authorization header. |
| Pagination | Start with $limit=100 and $offset=0; increase $offset by the returned-page size until no records remain before presenting the domain list or selecting a primaryDomain. |
| List completion | After every successful completed list without domainToUpdate, ask exactly: Which primaryDomain would you like to inspect or update? Please provide one value exactly as shown. End at DOMAINS.AWAITING_SELECTION; do not collect changes, build a preview, or make another BOSS operation. |
| Selected-record and read-back presentation | Render the approved response fields unredacted in a Section, Field, Current Value table. Domain contains Primary Domain and DNS Status; Domain Settings contains every enabled preference; Default Headers contains all five header fields. Never display record IDs, self links, ETags, or If-Match values, and do not persist displayed values in project artifacts. |
| Read-only scope | These reference lookups are source-backed BOSS read-only operations after target, identity, privilege, and input preflight. |
