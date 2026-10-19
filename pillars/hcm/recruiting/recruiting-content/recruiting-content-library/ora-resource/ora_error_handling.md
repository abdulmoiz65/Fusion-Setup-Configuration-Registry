# Recruiting Content Library Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| A required CSV field, identifier, length, language, or date is invalid. | Stop, identify the affected field or row, and correct the task-native artifact through the approved process. |
| DescriptionCode contains leading or trailing whitespace. | Trim it before comparison with existing data or the full export baseline; stop if the normalized code is missing, duplicate, or unmatched. |
| A description is identified only by an alias or display name. | Stop and request the normalized DescriptionCode; do not infer a record from a display name alone. |
| A description version is identified only by an alias or display text. | Stop and request the normalized parent DescriptionCode together with VersionStartDate; do not infer a version from display text alone. |
| The Common Lookups REST API version required by Languages LOV is unavailable. | Stop before the REST call. Resolve {version} to the same REST API version used by Applications Common Lookups; never send {version} literally or request a separate version solely for Languages LOV. |
| A description translation or description-version translation Language or SourceLang has no exact returned LanguageCode match. | Stop; do not infer or substitute a language value. |
| IsFileBased conflicts with the value derived from DescriptionTypeCode. | Derive true only for ORA_OFFER_LETTER_TEMPLATE and ORA_PROV_OFFER_LETTER_TEMPLATE; otherwise derive false. Correct the artifact through the approved process. |
| Availability Context data is supplied for an ineligible DescriptionTypeCode. | Reject or omit it unless DescriptionTypeCode is ORA_HIRING_TEAM_NOTIFICATION, ORA_JA_EMAIL_TEMPLATE, ORA_POSTING_DESCRIPTION, or ORA_PROSPECT_EMAIL_TEMPLATE. |
| Attachment data is supplied for a non-file-based DescriptionTypeCode. | Reject or omit it unless DescriptionTypeCode is ORA_OFFER_LETTER_TEMPLATE or ORA_PROV_OFFER_LETTER_TEMPLATE. |
| Any serialized VersionStartDate does not exactly match yyyy/MM/dd HH:mm:ss[.fffffffff], including a date-only value, hyphenated or ISO timestamp, timezone suffix, malformed fractional seconds, non-zero-padded component, or mismatch between a description-version row and its description-version translation row. | For the permitted yyyy/MM/dd HH:mm user input, append :00 once. A correctly formatted optional .fffffffff suffix remains valid. For an immediate start, explicitly format the current timestamp as yyyy/MM/dd HH:mm:ss before writing either version CSV, retain it as a string, and inspect every VersionStartDate in the final ZIP. Stop and rebuild the artifact on any format or matching failure; do not apply another transformation. |
| A lookup-coded value has no exact active LookupCode match. | Stop; do not infer or substitute a value. |
| A category or description type has no exact active DescriptionTypeCode LookupCode or unique active Meaning match after all active lookup pages are inspected. | Stop and request a valid value; do not infer a code or place Meaning in the import CSV. |
| A Booster-only description type is created or updated by CSV import and the Recruiting Booster feature is disabled or cannot be resolved. | Stop the create or update. Do not block export, infer feature state, or use an unresolved REST API version. |
| The target description is inactive. | Treat it as excluded from the import; do not assume it changed. |
| The existing target version is no longer active. | Treat it as excluded from the import; do not assume it changed. |
| MessageDesignCode has no exact active match, or DesignTypeCode is not ORA_HTML_TEMPLATE_USER. | Stop and correct the message-design reference before an approved import. |
| WabaTemplateName has no exact active match for HCM_RECRUITING and ORA_PROFILE_EMAIL_TEMPLATE. | Stop and correct the WhatsApp-template reference before an approved import. |
| Notification content exceeds 15 MB. | Reduce the content size and optimize images or logos before another approved attempt. |
| A predefined notification is proposed for disabling. | Stop; do not disable it. |
| Required task access is absent or authorization fails. | Stop and route the request to the security owner. |
| A scoped export is requested in the initial skill version. | Stop; use a full task-native export and locate the requested DescriptionCode in the exported baseline. |
| The requested DescriptionCode and its related version and translation rows cannot be located in the full export baseline. | Stop; do not infer a scoped export or prepare an import artifact. |
| A reduced import artifact alters archive structure or non-data files, or omits requested DescriptionCode records with related version and translation records. | Stop; restore archive structure and non-data files unchanged and retain the requested records. A reviewed full export may be re-imported. |
| A CSV member begins with UTF-8 BOM bytes EF BB BF, or ORA_IRC_ORGANIZATION_DESCRIPTION.csv does not begin directly with "DescriptionCode". | Stop before import. Rebuild the affected CSV member as UTF-8 without BOM, preserve the required header exactly, and repeat the raw-byte validation for every CSV member before approval. |
| Import status contains an error or unresolved warning. | Stop completion review; do not retry automatically. |
| A CSV File Package is rejected before Submit as not in CSV format. | Stop and correct the task-native package through the approved task flow; do not submit the rejected package. |
| Export completes with a Description.xml batch-size warning. | Do not use the package as an import baseline until completeness is independently verified. |
| Post-import comparison has failed objects, configuration-only data, or mismatches. | Stop and review the comparison details; correct the source through the approved task flow before re-comparison. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required CSV values or structural constraints fail. | Correct the source artifact and repeat the approved workflow. |
| Input validation | A description or description version is identified only by an alias or display text. | Request the normalized DescriptionCode, and VersionStartDate for a version; do not infer an identifier. |
| Input validation | A lookup-coded value has no exact active LookupCode match. | Correct the value or provide the intended active lookup code. |
| Input validation | A category or description type cannot resolve to one active DescriptionTypeCode LookupCode after all active lookup pages are inspected. | Request a valid value; do not use a Meaning in the import CSV. |
| Dependency | Recruiting Booster is disabled or its feature state cannot be resolved for a Booster-only import create or update. | Stop the create or update; export remains unaffected. |
| Dependency | The Common Lookups REST API version required by Languages LOV is unavailable. | Stop; resolve the same REST API version used by Applications Common Lookups before calling Languages LOV, and do not issue the REST call with {version}. |
| Input validation | A translation Language or SourceLang value has no exact returned LanguageCode match. | Correct the language value; do not infer or substitute a code. |
| Input validation | IsFileBased conflicts with its DescriptionTypeCode, Availability Context is supplied for an ineligible type, or attachment data is supplied for a non-file-based type. | Derive or retain only the category-supported data and correct the selected import artifact before another approved import. |
| Lifecycle | The target description or version is inactive. | Route lifecycle change to its separately approved process. |
| Dependency | MessageDesignCode or WabaTemplateName has no exact active match. | Correct the reference before another approved import. |
| Authorization | The documented privilege is absent or authorization fails. | Route to the security owner. |
| Scope boundary | A scoped export is requested in the initial skill version or the full export baseline cannot locate the target rows. | Use a full task-native export for baseline discovery; do not infer scoped export behavior. |
| Input validation | A reduced import artifact alters archive structure or non-data files, or omits requested DescriptionCode records with related version and translation records. | Restore the archive structure and non-data files unchanged and retain the requested records; a reviewed full export may be re-imported. |
| Artifact validation | A CSV member has an EF BB BF prefix or the organization-description header is not the exact first text in the file. | Rebuild every affected CSV member as UTF-8 without BOM, verify raw leading bytes for every CSV member, and do not import until the validation passes. |
| Artifact validation | Any final ZIP VersionStartDate does not exactly match yyyy/MM/dd HH:mm:ss[.fffffffff], or a description-version translation value differs from its parent description-version value. | Stop before approval or import. Rebuild the archive with an explicitly formatted canonical string in both version CSVs; do not rely on default date/time serialization. |
| Process failed | Import status reports an error or unresolved warning. | Stop before retry and route to the content owner. |
| Input validation | A CSV File Package is rejected before Submit as not in CSV format. | Correct the task-native package before another approved attempt. |
| Process warning | Export reports a Description.xml batch-size warning. | Do not approve the package for import until completeness is independently verified. |
| Process failed | Post-import comparison has failed objects, configuration-only data, or mismatches. | Review comparison details and correct the source before re-comparison. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation failure | The affected field or row and the missing, invalid, or unverified condition. |
| DescriptionTypeCode resolution failure | The supplied category or description type and whether no active match or multiple active Meaning matches across the complete result set prevented resolution. |
| Recruiting Booster feature-resolution failure | The Booster-only DescriptionTypeCode and whether the REST API version was unresolved or EnabledFlag did not indicate Recruiting Booster is enabled. |
| Description or version identity failure | The alias supplied and the missing normalized DescriptionCode or VersionStartDate required to continue. |
| Dependency or authorization failure | The missing capability, access, artifact, approval, or result-review evidence. |
| Languages LOV version-resolution failure | The unavailable Common Lookups REST API version and the requirement to resolve that same version before the call. |
| Import result review | Sanitized errors and warnings and their required disposition. |
| Package acceptance failure | The package rejection and the requirement to correct it before another approved attempt. |
| Warning-completed export | Sanitized warning evidence and the outstanding completeness-verification requirement. |
| Full-export baseline failure | The requested DescriptionCode and its related version and translation rows that could not be located, and the requirement to stop. |
| Reduced import-artifact failure | The altered archive structure/non-data files or omitted requested records and the required correction. |
| CSV encoding failure | The affected CSV member, observed leading bytes, expected UTF-8-without-BOM encoding, and required rebuild before approval. |
| Comparison failure | Sanitized failed-object or discrepancy details and the required correction path. |
| VersionStartDate artifact failure | The expected formatted value, the actual values from both version CSVs, and the requirement to rebuild before approval or import. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A requested lookup is outside the documented active LookupCode contract. | Do not invent an endpoint, query, source, or value. |
| A category or description type is evaluated from only a partial active lookup result. | Do not conclude that there is no match; inspect every page before applying the documented LookupCode or Meaning resolution rule. |
| A category or description type resolves only to a Meaning. | Do not place Meaning in the import CSV; require the documented resolver to return one validated LookupCode. |
| A Booster-only description type is created or updated while Recruiting Booster is disabled or unresolved. | Do not create or update the item; do not block export or infer feature state. |
| The Languages LOV path still contains {version}. | Do not issue the REST request until the variable is resolved to the same REST API version used by Applications Common Lookups. |
| A description or description version is identified only by an alias or display text. | Do not infer the record or version; require the documented identifiers. |
| An import, export, activation, or direct service operation is requested by this resource. | Do not execute it; use the selected routed workflow and its approval gates. |
| An import result is uncertain or failed. | Do not automatically retry or claim that target content changed. |
| A warning-completed export has not been independently verified for completeness. | Do not use its package as an import baseline. |
| A reduced import artifact alters archive structure or non-data files, or omits requested DescriptionCode records with related version and translation records. | Do not import the reduced artifact until corrected. A reviewed full export may be re-imported. |
| Any CSV member has a UTF-8 BOM or the organization-description header has leading bytes before "DescriptionCode". | Do not import the archive or treat DescriptionCode as a recognized alternate key until every CSV member passes the UTF-8-without-BOM raw-byte validation. |
| An immediate VersionStartDate has been formatted for the import CSV. | Do not parse, coerce, or re-serialize it after formatting. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RCL.DONE | terminal | 90 | terminal | none | RCL.DESIGN | stop | All applicable validation, readiness, defaulting, and design checks pass. |
| RCL.BLOCKED | terminal | 99 | terminal | none | none | stop | A validation, readiness, design, authorization, or process failure occurs. |
