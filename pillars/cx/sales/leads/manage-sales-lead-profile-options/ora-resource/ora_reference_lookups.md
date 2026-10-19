# Reference Lookups

## Local Lookups

| Resolver | Runs When | Source | Match Rule | Values to Fill | Failure Result |
|---|---|---|---|---|---|
| inventory_profile_options_from_reference_export | After fresh export validation | FND_APP_PROFILE_OPTION.csv, FND_APP_PROFILE_VALUE.csv, ORA_FND_APP_PROFILE_OPTION_LEVEL.csv, and ASM_SETUP_CSV_METADATA.xml | Join by exact ProfileOptionName and ApplicationId; require unique definitions, no orphan values or levels, and one unambiguous level capability row per code and level | Complete exported inventory, configured values by scope, level flags, SQL validation, descriptions, row counts, export hash, environment, release, and timestamp | Return failure for duplicate keys, orphan rows, missing metadata, or changed export evidence |
| resolve_documented_profile_option_identity | Inventory or exact option input | Current Oracle Sales Lead Profile Options page, applicable Oracle Sales feature guidance, and the coverage baseline below | Accept an exact case-sensitive code or one exact unique display-name match; refresh documentation when available | Documented code, display name, source URL, section/feature, documentation retrieval date | Return invalid for fuzzy/ambiguous names; documentation failure does not invalidate an exact exported code |
| reconcile_documented_and_exported_options | After documentation refresh and export attempt | Documented and exported exact codes | Classify each code as documented-and-exported, documented-live-only candidate, export-only, or unavailable after live probing | Reconciliation counts, code lists, export status, and live status | Never infer live absence or mutation ineligibility from export omission; require a supported provenance route for mutation |

## Documented Coverage Baseline

Refresh the current Oracle pages before a run when documentation access is
available. This baseline prevents an export-only inventory from silently
dropping documented options; it is not a substitute for exact live resolution.
The table currently contains 38 exact codes. Calculate the documented candidate
count from these rows plus successfully refreshed additions on every run; never
report a remembered count such as 28 or 39. Documentation refresh may annotate
or expand this baseline, but its failure must not terminate environment-backed
Inventory or Review.

| Section | Profile Option Code |
|---|---|
| Lead Assignment | `MKL_LEAD_ASSIGNMENT_QUAL_RULE` |
| Lead Assignment | `MKL_LEAD_ASSIGNMENT_RANK_RULE` |
| Lead Assignment | `MKL_LEAD_ASSIGNMENT_MATCHING_RULE` |
| Lead Assignment | `MKL_LEAD_ASSIGNMENT_SCORE_RULE` |
| Lead Assignment | `MKL_LEAD_ASSIGNMENT_RULE` |
| Lead Assignment | `MKL_LEAD_DEFAULT_ASGN_MODE` |
| Lead Assignment | `MKL_LEAD_BATCH_ASSIGNMENT` |
| Lead Qualification and Assessment | `MKL_LEAD_ASSESSMENT_TEMPLATE` |
| Lead Qualification and Assessment | `MKL_LEAD_QUALIFICATION_TEMPLATE_PROFILE` |
| Lead Qualification and Assessment | `MOW_MULTIPLE_ASSESSMENTS_ENABLED` |
| Lead Qualification and Assessment | `ORA_ZCA_AI_UPDATE_WHO_THRESHOLD` |
| Lead Update and Attribute Mapping | `MKL_LEAD_PRODUCTS_ENABLED` |
| Lead Update and Attribute Mapping | `MKL_LEAD_OOTB_NOTIFICATION` |
| Lead Update and Attribute Mapping | `ORA_MKL_LEAD_ACT_CON_CREATE` |
| Lead Update and Attribute Mapping | `MKL_DIRECT_LEAD_TO_OPTY_MAPPING_NAME` |
| Lead Update and Attribute Mapping | `MKL_LEAD_TO_ACCOUNT_MAPPING_NAME` |
| Lead Update and Attribute Mapping | `MKL_LEAD_TO_CONTACT_MAPPING_NAME` |
| Lead Update and Attribute Mapping | `MKL_LEAD_TO_DEAL_MAPPING_NAME` |
| Partner Leads and Deal Registrations | `MKL_ADD_PARTNER_CONTACT` |
| Partner Leads and Deal Registrations | `MKL_LEAD_REGISTRATION_APPROVAL_ADMIN_PROFILE` |
| Partner Leads and Deal Registrations | `MKL_DEAL_REG_EXPIRATION_DATE` |
| Partner Leads and Deal Registrations | `MKL_DEAL_DEFAULT_SALES_TEAM_ACCESS_LEVEL` |
| Partner Leads and Deal Registrations | `MKL_DEAL_SEARCH_LAST_UPDATED_RANGE_DEFAULT` |
| Partner Leads and Deal Registrations | `MKL_PARTNER_LEAD_TO_OPTY_MAPPING_NAME` |
| Partner Leads and Deal Registrations | `MKL_DEAL_TO_OPTY_MAPPING_NAME` |
| Partner Leads and Deal Registrations | `MKL_DEAL_RBA_RULESETGROUP` |
| Partner Leads and Deal Registrations | `MKL_DEAL_TBA_RULESETGROUP` |
| Partner Leads and Deal Registrations | `MKL_DEAL_DEFAULT_ASGN_MODE` |
| Partner Leads and Deal Registrations | `MKL_PARTNER_LEAD_QUALIFICATION_TEMPLATE` |
| Partner Leads and Deal Registrations | `MKL_DEAL_SEARCH_EXPIRE_RANGE_DEFAULT` |
| Partner Leads and Deal Registrations | `MKL_DEFAULT_DEAL_REGISTRATION_APPROVER` |
| Partner Leads and Deal Registrations | `MKL_DEAL_USE_DEFAULT_APPROVAL_PROC` |
| Lead Searches | `MKL_LEAD_QUERY_IN_N_DAYS` |
| Lead Searches | `MKL_LEAD_SEARCH_CREATION_RANGE_DEFAULT` |
| Lead Searches | `MKL_LEAD_SEARCH_CREATION_RANGE_RECOMMENDED` |
| Lead Searches | `MKL_LEAD_CDS_ENABLED` |
| Lead Searches | `MKL_SRCH_ADDL_CRITERIA_REQD` |
| Convert Lead to Existing Opportunity (25C feature) | `ORA_MKL_LEAD_CONVERT_TO_EXISTING_OPTY` |

## Live Lookups

| Rule ID | Resolver | Runs When | Source Values | Request Paths | Match Rule | Values to Fill | Failure Result |
|---|---|---|---|---|---|---|---|
| SPO.LOOKUP_PROFILE | resolve_exact_profile_option_and_target_value | Inventory, Review, Set, Remove, or BulkSet after identity and dependency preflight | Documented/exported ProfileOptionCode, ProfileLevel, UserName or ProductApplicationShortName, ExpectedCurrentValue, and proposed display or stored value | GET /fscmRestApi/resources/11.13.18.05/profileOptions/{ProfileOptionName}; GET child/profileOptionLevels; GET child/siteProfileOptionValues; GET child/userProfileOptionValues; GET child/productProfileOptionValues; conditionally GET /fscmRestApi/resources/11.13.18.05/profileUsers/{UserName}; conditionally GET /crmRestApi/resources/11.13.18.05/assessmentTemplatesLOV; conditionally GET /fscmRestApi/resources/11.13.18.05/standardLookups/{LookupType}/child/lookupCodes | Require exact case-sensitive profile code, one exact definition, live level flags, complete paginated Site/User/Product collections, and one exact selected child row or explicit absence; require one exact user/template/dependency when applicable; Inventory probes the documented/exported union; Review and mutation probe the exact selected code and scope key | Environment identity, definition, SqlValidation, three live level rows, configured Site/User/Product rows or explicit absence, exact Site/Product/User item key, UserGuid, AssessTemplateId, stored lookup code and meaning, lookup timestamps, per-code status, source classification, export/live reconciliation, and deterministic Create/Update/Delete selection | Return not_found when the definition or required dependency is absent; return many for ambiguous name/user/template/dependency/lookup matches or duplicate scope rows; return failure for systemic auth, authorization, transport, environment, pagination, or response-shape errors; export omission is never a CRUD failure |

## Lookup Rules

- Read `profileValues` only for optional effective-session verification. Its
  omission of a code is inconclusive because security categories restrict the
  collection.
- For `MKL_LEAD_ASSESSMENT_TEMPLATE` and
  `MKL_LEAD_QUALIFICATION_TEMPLATE_PROFILE`, resolve the user-facing template
  name to the numeric `AssessTemplateId`. Never store the name itself.
- Treat live parent `SqlValidation` as the current validation contract. Parse
  only the lookup type or named dependency needed to call an existing safe
  resolver; never execute the SQL text.
- For lookup-backed profiles, accept an exact active stored code or resolve one
  exact active meaning (for example `Yes`) to its code (for example `Y`). Show
  both in the preview and store only the code.
- For Inventory, probe the documented baseline plus exact export-only codes.
  Use bounded parallel GETs, follow pagination, and report live not_found per
  option without aborting the rest of the inventory. Treat individual 404s as
  per-code unavailable results; reserve the node's `failure` outcome for a
  systemic authentication, authorization, transport, or response-shape failure.
- For every resolved Inventory code, read and paginate
  profileOptionLevels, siteProfileOptionValues, userProfileOptionValues, and
  productProfileOptionValues. Record `not configured` when a child collection
  has zero rows. Do not substitute the FSM value, a delivered default, a Site
  value for User, or an effective-session value for a configured child row.
- For Review, execute the same definition and four child-collection reads for
  the exact selected code. An exact parent definition alone is incomplete.
- For Site, use the literal item key `SITE`. An absent Site item selects Create;
  one exact item selects Update or Delete.
- For Product, require one exact application short name and use it as both the
  create `LevelValue` and item key. Never use an application display name.
- For User, resolve `profileUsers/{UserName}` exactly. Use `UserName` as the
  item key and `UserGuid` only as create-body `LevelValue`. Treat zero User rows
  as explicit absence, not export evidence.
- For mutation, choose the method only from exact live state: absent item plus
  Set selects POST; existing item plus Set selects PATCH; existing item plus
  Remove selects DELETE; absent item plus Remove performs no write.
- Inventory output is complete only when every refreshed documented code and
  every exact export-only code has one result. Include configured Site/User
  values for `documented-live-only` options; never substitute the 15-row FSM
  fixture for that reconciled live inventory.
- When the shared export subskill returns, resume at `SPO.LOOKUP_PROFILE`.
  Record `DocumentedCandidateCount`, `ExportOnlyCandidateCount`,
  `LiveAttemptedCount`, `LiveResolvedCount`, `LiveNotFoundCount`, and
  `LiveErrorCount`; require attempted count to equal the unique candidate-union
  count before routing Inventory to `SPO.DESIGN`.
- Preserve exact lookup codes, rule-set-group codes, Copy Map names, role/user
  identifiers, and numeric IDs returned by authoritative lookups.
- A 401 or 403 is an authentication or privilege failure, not not_found.
- Do not state that the environment is inaccessible unless this resolver or the
  mandatory export route was attempted and produced classified evidence. A
  skipped call, documentation result, or absent browser session is not an
  environment-access failure.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SPO.LOOKUP_PROFILE | step | 3 | reference_lookup | found->SPO.ROUTE;not_found->SPO.ROUTE;many->SPO.RETURN_ISSUES;failure->SPO.RETURN_ISSUES | SPO.DEPENDENCIES | stop | Resolve documented and exported candidates against exact live profile, level, configured-value, user, template, lookup, and other conditional dependency evidence |
| SPO.ROUTE | decision | 4 | evaluate_result | proceed->SPO.DESIGN;blocked->SPO.RETURN_ISSUES | SPO.LOOKUP_PROFILE | stop | Proceed for Inventory only with a result/status and complete configured-value evidence for every candidate, Review only with exact definition and complete child reads, or Set/Remove/BulkSet with deterministic method, exact scope key, current-state lock, and dependency closure; block documentation-only current-value results, ambiguous rows, unsupported scope, or unresolved stored-value dependencies |
