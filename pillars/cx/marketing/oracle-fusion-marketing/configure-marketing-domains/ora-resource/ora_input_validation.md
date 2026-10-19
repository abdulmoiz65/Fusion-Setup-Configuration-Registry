# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Domain selection | domainToUpdate exactly matches one primaryDomain from the completed Domains GET | Display the list and ask exactly: Which primaryDomain would you like to inspect or update? Please provide one value exactly as shown. | Do not collect changes, build a preview, or make another BOSS operation until the user supplies one exact displayed value | A domain is selected for inspection or update | list_marketing_domains |
| Proposed update | One or more supported changed fields | Display the selected record, then request supported changes before preview | The complete selected-domain record must be shown before change input is collected | A selected domain record has been displayed | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Supported fields | Allow only enabled emailDomainPreference and micrositeDomainPreference plus senderName, senderEmail, replyToName, replyToEmail, and bounceBackEmail | Proposed changes are supplied | |
| Nonblank values | Reject blank or empty submitted fields | Proposed changes are supplied | |
| Preference values | Accept only lowercase default, alternate, or null, case-sensitively | An enabled preference field is supplied | |
| Preference applicability | Reject a preference field when its corresponding domain-type flag is false | A preference field is supplied | |
| Email local part | Permit senderEmail and bounceBackEmail changes only before @; preserve the selected domain suffix | An editable email field is supplied | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DOMAINS.VALIDATE | step | 1 | validate_input | valid->DOMAINS.ACCESS;invalid->RETURN_ISSUES | none | stop | A Marketing domain list, inspection, or update is requested |
| DOMAINS.COLLECT_CHANGES | step | 6 | validate_input | changes_valid->DOMAINS.PREVIEW;awaiting_changes->DOMAINS.AWAITING_CHANGES;invalid->RETURN_ISSUES | DOMAINS.SHOW_SELECTED | stop | The complete selected-domain record has been displayed |
