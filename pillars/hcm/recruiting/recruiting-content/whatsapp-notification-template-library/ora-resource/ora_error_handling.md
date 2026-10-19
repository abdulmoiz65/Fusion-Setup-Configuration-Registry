# WhatsApp Notification Template Library Error Handling

Return the documented user-facing error and stop the affected request. Never retry a lookup automatically, construct a Data Loader payload, or claim that a Fusion change occurred.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Template name is missing | Enter the template name or template code. |
| Template name has an invalid format | The template name must start with a lowercase letter and can contain only lowercase letters, numbers, and underscores. |
| Template name exceeds 100 characters | The template name must not exceed 100 characters. |
| Template display name is missing or blank | Enter the template display name. |
| Template display name exceeds 3,000 characters | The template display name must not exceed 3,000 characters. |
| Meta WhatsApp template category is missing | Enter the Meta WhatsApp template category. |
| Meta WhatsApp template category has no match | The provided value isn't a valid Meta WhatsApp template category. Select one of the supported categories. Display the Meaning values returned by the LOV. |
| Meta WhatsApp template category has multiple matches | More than one Meta WhatsApp template category matches the provided value. Enter the exact category name. Display the matching Meaning values. |
| Recruiting content category is missing | Enter the Recruiting content category. |
| Recruiting content category has no match | The provided value isn't a valid Recruiting content category. |
| Recruiting content category has multiple matches | More than one Recruiting content category matches the provided value. Enter the exact category name or lookup code. Display the matching Meaning values. |
| Content is missing or blank | Enter the WhatsApp template content. |
| Content exceeds 1,024 characters including token names | The template content must not exceed 1,024 characters, including token names. |
| Content contains no token | The template content must contain at least one valid token in the ${TokenName} format. |
| Content contains more than 15 unique tokens | The template content can contain no more than 15 unique tokens. |
| A token has an invalid format | <token> doesn't use the required ${TokenName} format. |
| Mandatory category-specific token validation finds no exact case-sensitive Name match for a token in the selected-category token LOV, or its casing differs | <token> isn't valid for the selected Recruiting content category. Token names are case-sensitive. |
| Conversation Starter content contains an unsupported token | The WhatsApp Conversation Starter template contains an unsupported token. Use only the supported Conversation Starter tokens. |
| Conversation Starter content omits ${MessageBody} | The WhatsApp Conversation Starter template must contain the ${MessageBody} token. |
| A readable input uses a format other than XLS, XLSX, or CSV | Do not reject it because of the file extension. Safely extract its text, tables, records, or image content, preserve source locators, and normalize it into canonical structured records or one natural-language proposal before validation. |
| An input is inaccessible, encrypted without access, corrupt, empty, executable-only, or has no reliably extractable content | The provided input couldn't be read safely. Provide an accessible, non-executable copy, a clearer source, or paste the relevant content. Do not perform any lookup or Data Loader handoff. |
| Extracted row boundaries, labels, values, or canonical field mappings are ambiguous | Show every affected source locator and proposed normalized value. Ask the user to correct or explicitly confirm the mapping, and stop the complete request before any lookup or Data Loader handoff. |
| Duplicate template-language records occur in a structured request | Duplicate template-language records were found. Keep one record for each template and language and resubmit the complete request. |
| Duplicate translation records use the same template and language | Duplicate translation records were found. Keep one record for each template and language and resubmit the complete request. |
| One normalized structured record is invalid | Reject the complete request and show every invalid source locator, record number, canonical field, supplied value, and correction. |
| A provisional natural-language template name already exists | Do not finalize the collided name. Derive a more specific meaningful candidate from the notification purpose, check the full existing-template result set again, and continue only with a zero-match name. Do not append an arbitrary numeric suffix. |
| No meaningful unique natural-language template name can be derived | Show the collided candidates and ask the user for one distinguishing business concept; do not invent or finalize a name. |
| Automatically classified structured template name matches exactly one existing Fusion template | Classify every row in that name group as a translation, preserve WaTemplateId as templateId, resolve each language, and route the rows through recruitingWhatsappLangTemplates. |
| Automatically classified structured template name has no existing Fusion match and one row language matches the active user session language | Classify the matching row as the base for recruitingWhatsappBaseTemplates and defer all remaining languages in the group for recruitingWhatsappLangTemplates until the base load completes successfully. |
| Active user session language is unavailable, or no resolved LanguageCode or Description in a zero-match template-name group matches it uniquely | A base language template doesn't exist. Do you want me to create it first? Please provide the language to use for the base template. Stop the complete request until the user confirms and supplies the preference. |
| Explicitly base-only existing template has WabaTemplateStatus equal to ORA_DRAFT | Classify the row as an update and preserve the existing template identifier; do not create a duplicate. |
| Explicitly base-only existing template has a blank WabaTemplateStatus or a value other than ORA_DRAFT | The existing template isn't in ORA_DRAFT status and can't be updated by this request. Use a different template name or manage the existing template separately. |
| Explicitly base-only existing-template lookup omits WabaTemplateStatus or returns it blank | Stop the complete request because Draft update eligibility can't be verified; do not infer status or run an update. |
| A confirmed natural-language name exists during the pre-handoff recheck | Invalidate the confirmation, derive and check a more meaningful name, update the display name, rerun the category, token, and Meta content rules, and request confirmation again. |
| Natural-language Meta category does not match the message purpose | Reclassify authentication as Authentication, job promotion, talent-pool outreach, or campaigns as Marketing, and all other expected transactional messages as Utility; then revalidate content. Never disguise Marketing as Utility. |
| Natural-language content fails a Meta content standard | Do not present the proposal for confirmation. Show the failed designated-purpose, consent and sender clarity, copy quality, CTA, token sample, safety, or hiring-decision rule and the specific correction required. |
| Natural-language proposal is not confirmed | Show the proposed template name or code, display name, Meta category, Recruiting category, compliant content, tokens, and realistic nonsensitive sample values; wait for explicit confirmation. Corrections require a new proposal. |
| An automatically classified batch contains selected base and translation rows | Return only the recruitingWhatsappBaseTemplates phase first. Keep recruitingWhatsappLangTemplates rows deferred until the owning workflow verifies every corresponding base request completed successfully. |
| Translation language is missing | Enter the translation language. |
| Translation language has no match | The provided language isn't a supported Fusion language. |
| Translation base template has no match | A base language template doesn't exist. Do you want me to create it first? Please provide the language to use for the base template. |
| Translation base template has multiple matches | More than one template matches the provided value. Enter the exact template name or template code. Display the matching template names and display names. |
| productContext or recruitingSource is supplied as user input | These fields are system-defaulted and are not accepted as user input. Omit them from the request. |
| A writable operation is requested from these resource files | Return validated mappings to the owning setup-task workflow only; do not build or submit a payload and do not call Data Loader. |
| A live lookup is unavailable or unauthorized | Stop the affected branch, preserve sanitized input, classify the lookup readiness failure, and do not substitute local or inferred values. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Missing information | A required creation or translation input, active user session language, or preferred base language is absent | Request only the missing documented value or ask whether to create the missing base first and request the preferred base language |
| Invalid input | Content cannot be read or normalized safely, an extracted mapping is ambiguous, or a supplied value fails a documented length, format, blank, token-count, or token-format rule | Return the exact applicable message and request an accessible source, explicit mapping confirmation, or corrected value |
| Lookup no match | A documented live lookup completes with no exact match | Return the exact no-match message and any display values the requirements direct the workflow to show |
| Lookup ambiguity | A documented live lookup returns more than one match | Return the exact ambiguity message and the matching display values required by the source |
| Lookup readiness failure | A live read-only lookup is unavailable, unauthorized, or lacks a complete source-value contract | Stop the affected branch and repair the documented lookup contract before retry |
| Design-policy rejection | Duplicate template-language rows, unavailable or newly collided natural-language names, structured row-role ambiguity, category-purpose mismatch, Meta content-standard failure, explicitly base-only non-Draft collisions, unconfirmed natural-language proposals, premature translation handoff, incorrect Data Loader business-object routing, or Conversation Starter token rules block the request | Return the documented policy message and require the stated correction or confirmation |
| Authoring readiness gap | Another source contract required by the selected branch is unresolved | Resolve the named contract gap and recompile before planning the affected branch |
| Execution boundary | The request reaches a Data Loader handoff | Return the validated mappings to the owning setup-task workflow; no Fusion change has occurred |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation result | The selected creation or translation branch and each missing or invalid business input without exposing credentials or raw sensitive payloads |
| Input normalization | The source format, safe extraction method, source locator for every canonical value, normalized record boundaries and fields, and every ambiguous or missing mapping requiring correction or confirmation |
| Lookup result | Resolver name, sanitized source value, observed match outcome, documented mapped value, and the applicable exact user guidance |
| Structured row-role classification | For each normalized template-name group, show the Fusion existence result, active session-language match result when required, selected base row or translation rows, and the target business object without exposing unrelated template or session details |
| Natural-language name availability | Every meaningful candidate checked, the case-insensitive collision outcome, and the selected zero-match template name and consistent display name; do not expose unrelated template details |
| Natural-language Meta review | Selected Meta category and purpose, confirmation that intended use is limited to opted-in recipients, sender identity and opt-out handling, each content-standard result, exact category-valid tokens, and realistic nonsensitive token or media samples |
| Authoring blocker | The unresolved canonical field, affected task path, and the developer decision needed to resolve it |
| Successful creation handoff | Validated base-template field mappings, session-language evidence when classification came from a structured file, target business object recruitingWhatsappBaseTemplates, resolved category codes, applied defaults, mandatory category-specific token-validation result, and confirmation that no Data Loader or Fusion operation occurred |
| Successful translation handoff | Resolved templateId, language, target business object recruitingWhatsappLangTemplates, and token-validation category plus validated display name, content, and mandatory category-specific token-validation result; confirm that recruitingCategoryCode is lookup context only and that no Data Loader or Fusion operation occurred |
| Successful mixed-batch handoff | Every selected base row and its session-language match, recruitingWhatsappBaseTemplates as the first-phase business object, every deferred translation row, recruitingWhatsappLangTemplates as the second-phase business object, and the requirement to verify all base Data Loader requests as completed before resuming translations |
| Failure | Failure category, affected business value, sanitized evidence, and one safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Undocumented field, lookup, default, or match behavior | Do not infer Oracle behavior, local authority, category values, token names, field mappings, or fallback values |
| A readable user input uses an unfamiliar or non-tabular format | Do not reject it solely because of its extension, and do not execute macros, scripts, embedded programs, or active content; use only safe extraction and continue only after the content is normalized and validated |
| Input extraction is unavailable, incomplete, or ambiguous | Do not invent text, row boundaries, labels, values, or field mappings, and do not perform lookups or return a Data Loader handoff |
| Translation Recruiting content category is omitted | Do not infer or borrow a category from another request or the base-template identifier; reject the translation with Enter the Recruiting content category, and do not call the token LOV or return a handoff until the category resolves uniquely |
| Content-token request returns no or multiple matches | Do not accept, recase, replace, or silently remove the affected token |
| Any normalized structured record is invalid or duplicated | Do not partially process the request, perform duplicate lookups, or return a Data Loader handoff |
| A natural-language candidate name collides | Do not finalize the name, reuse it because a matched template is Draft, or add an arbitrary numeric suffix; derive and fully recheck a more meaningful candidate |
| A natural-language name collides after confirmation | Do not preserve the stale confirmation or convert the request to an update; rename, revalidate, and obtain confirmation again |
| A natural-language Meta category or content standard fails | Do not disguise Marketing as Utility, show the proposal for confirmation, hand it off, or claim that Meta approval is guaranteed |
| Mixed base and translation rows are present | Do not reject a valid batch solely because it is mixed; stage base rows first and do not release translations before verified base completion |
| Structured rows are automatically classified | Do not use a blank Language as the base indicator, classify an existing-name row as a base or Draft update, select a non-session-language row as the base, or send a base row through recruitingWhatsappLangTemplates or a translation through recruitingWhatsappBaseTemplates |
| Active user session language is unavailable or does not identify one row uniquely | Do not infer a base language, choose the first row, or continue partially; return the documented base-creation prompt and wait for the user's confirmation and language preference |
| WabaTemplateStatus is unavailable or blank for an explicitly base-only request | Do not infer ORA_DRAFT status or update eligibility |
| A lookup fails or is uncertain | Do not retry automatically, change the query, bypass the resolver's documented stop condition, or substitute local data |
| productContext or recruitingSource is supplied | Do not accept or preserve the supplied value; instruct the requester to omit the field so the fixed system default can be applied |
| Data Loader handoff is reached | Do not construct or persist a payload, invoke another skill, call Fusion, or claim creation or translation success |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | Rule Selection |
|---|---|---|---|---|---|---|---|---|
| WATL.GATE.NL_CONFIRMATION | decision | 50 | execution_gate | confirmed->WATL.LOOKUP.EXISTING_BASE_BATCH;corrected->WATL.ERROR.INPUT;declined->RETURN_ISSUES | WATL.ENFORCE.META_CONTENT_STANDARDS | stop | Present the unique, purpose-categorized, standards-compliant natural-language proposal with realistic samples and require explicit confirmation before base-template handoff | all |
| WATL.ERROR.INPUT | step | 240 | error_handler | handled->RETURN_ISSUES | none | stop | Input extraction or normalization is unreadable or ambiguous, a required value, session-language base selection, or user base-language preference is missing, or any supplied or derived field fails validation | all |
| WATL.ERROR.LOOKUP | step | 241 | error_handler | handled->RETURN_ISSUES | none | stop | A required live lookup returns no match, multiple matches, or unavailable | all |
| WATL.ERROR.POLICY | step | 242 | error_handler | handled->RETURN_ISSUES | none | stop | Duplicate, row-role, name-availability, explicitly base-only existing-status, category-purpose, Meta content, confirmation, business-object routing, phase-order, or Conversation Starter policy blocks the request | all |
| WATL.ERROR.AUTHORING | step | 243 | error_handler | handled->RETURN_ISSUES | none | stop | An unresolved source contract prevents safe validation, defaulting, or handoff | all |
| RETURN_ISSUES | terminal | 250 | terminal | none | none | stop | A documented issue, declined proposal, or authoring blocker was disclosed with one safe next action | all |
| WATL.RETURN.CREATE_READY | terminal | 200 | terminal | none | WATL.ENFORCE.BATCH_PHASES | stop | Base create or explicit Draft-update mappings are validated for recruitingWhatsappBaseTemplates handoff; no Data Loader or Fusion operation occurred | all |
| WATL.RETURN.BASE_PHASE_READY | terminal | 201 | terminal | none | WATL.ENFORCE.BATCH_PHASES | stop | Session-language base mappings are ready for recruitingWhatsappBaseTemplates and recruitingWhatsappLangTemplates rows are deferred until verified base Data Loader completion | all |
| WATL.RETURN.TRANSLATION_READY | terminal | 202 | terminal | none | WATL.LOOKUP.TRANSLATION_TOKENS | stop | Translation mappings are validated for recruitingWhatsappLangTemplates handoff after the base exists; no Data Loader or Fusion operation occurred | all |
