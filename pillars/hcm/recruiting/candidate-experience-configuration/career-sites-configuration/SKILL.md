---
skill_id: "hcm.recruiting.candidate-experience-configuration.career-sites-configuration"
name: "Career Sites Configuration Setup Task Guidance"
description: "Create an Oracle Fusion Career Site with Languages, default Cookie Consent, and optional standard Filters, or perform governed Language, Filter, Settings, Talent Community, Cookie Consent, default-language, and status updates through Data Loader workflows."
layer: "pillar"
pillar: "HCM"
offering: "Recruiting"
functional_area: "Candidate Experience Configuration"
functional_area_code: "ORA_CANDIDATE_EXPERIENCE_CONFIGURATION"
task_code: "ORA_IRC_CONFIGURE_CAREER_SITE"
task_name: "Career Sites Configuration"
parent_skill_id: "hcm.recruiting.candidate-experience-configuration"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "recruitingCESites"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM recruiting and candidate experience pillar team"
version: "0.26.13"
inputs: ["implementation_objective", "project_context", "setup_task_scope", "setup_data_artifacts"]
outputs: ["setup_task_plan", "setup_data_routing", "validation_checkpoints", "post_load_verification_result", "regression_result", "skill_run_record", "token_usage_record"]
depends_on: ["shared.setup-export.task-level-export", "shared.validation.setup-data-validator", "shared.validation.reference-data-validator", "core.data-loader"]
uses_core: ["core.project-mgmt.artifact-version-manager", "core.project-mgmt.artifact-registry-manager", "core.project-mgmt.project-state-manager", "core.fusion-api.rest-api-client"]
persists_project_state: true
token_usage_tracking:
  enabled: true
  granularity: "per_skill_run"
  artifact_type: "token_usage_record"
  default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
  estimation_method: "chars/4 estimate unless exact tokenizer or API accounting is available"
state_updates: ["setup_task_sequence", "configuration_blueprints", "validation_results", "token_usage_records"]
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/candidate-experience-configuration/career-sites-configuration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/candidate-experience-configuration/career-sites-configuration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
applicability:
  industries: ["All"]
  countries: ["All"]
  fusion_releases: ["Current Oracle Fusion Cloud release"]
side_effects: []
required_privileges: []
---

# Career Sites Configuration — Parent, Languages, Cookie Consent, Filters, Settings, and Talent Community

## Scope

The default workflow uses the proven REST-identifier contract: it creates one inactive minimal Career Site, one or more `languages` children that include its `DefaultLang`, one empty `cookieConsent` child, and one empty `talentCommunitySignUp` child in one combined Data Loader archive. The parent REST identity is generated String `SiteNumber`; child ownership is inherited through `ParentId=SiteNumber`; child `foreignKeys` are empty. A site with a `DefaultLang` but no matching `languages` row leaves the Site Editor unable to load its Languages page. Both parent and child generated identifiers, including `SiteNumber`, remain blank in the combined source.

This is the single supported workflow. Users do not select a version, experiment, or alternate create mode. If a combined load partially succeeds, record that result and stop; never resubmit the archive or substitute an unverified alternate flow. Every unreviewed child remains unavailable until it has compatible registration and regression evidence.

An explicit Cookie Consent PATCH may modify one or more existing Cookie Consent business attributes in one child-only archive against an existing site; it never creates, modifies, or resubmits the parent. This skill also supports site-configuration discovery (summary, enabled languages, effective Filter state, Cookie Consent state, Settings, and Talent Community state), adding one site language, changing the default language, activating or inactivating a site, and producing the verified Site Editor **Copy Link** route, adding standard Job Location, Organization, Job Category, Job Function, and Recruiting Type Filters during creation or later, friendly persisted-parent Settings discovery and updates, and Talent Community Sign-Up updates. Settings are never included in initial creation; Talent Community Sign-Up is included only as its empty default child. Pages, Widgets, Talent Community translations, Filter PATCH/DELETE, DFF Filters, Settings deletion/key rename, and every other child remain deferred.

For every read-only discovery or "what is configured" request, return the **effective Site Editor behavior**, not merely the presence or absence of a persisted row. Label each result as **Persisted**, **Using editor default**, **Fusion-initialized default**, **No restriction**, or **Data inconsistency**, following [defaulting rules](ora-resource/ora_defaulting_rules.md). Never describe an absent setting or child as simply "none configured" when the Site Editor has a known effective default.

When a user asks for functional guidance, an explanation of a Career Sites capability, or a source to read further, use the curated [Oracle public documentation reference](ora-resource/ora_oracle_public_documentation.md). Give the concise answer first, then link the closest official topic. Public documentation is user guidance only: it must not replace the current live Data Loader registration, live LOVs, global-capability result, or verified Site Editor behavior when constructing or validating an archive.

## Routing and boundaries

1. Begin with `router/implementation-router/SKILL.md`.
2. Route archive generation, validation, approval, submission, monitoring, and failure diagnosis through `core/data-loader/SKILL.md`.
3. Use [ora_reference_lookups.md](ora-resource/ora_reference_lookups.md) through `core.fusion-api.rest-api-client` for read-only preflight and verification. Never mutate Career Sites through REST.
4. Do not create task-specific scripts or modify Data Loader core code.
5. Apply the [main registration contract](ora-resource/ora_main_registration_contract.md). Do not require unexposed registration overrides from the core resolver; use the portal export as evidence for cleared overrides and payload exclusions. Do not infer compatibility for an unreviewed child from the supported parent, Languages, Cookie Consent, Filters, Settings, and Talent Community flows.

When changing `ora-resource/ora_rule_registry.json`, every node `source.file` must name an existing `ora_*.md` resource. Before handoff, parse the registry and run the Data Loader Task Hook `data-load` route against the selected task context; do not rely only on local JSON syntax validation.

Read [ora_input_validation.md](ora-resource/ora_input_validation.md), [ora_dependency_readiness.md](ora-resource/ora_dependency_readiness.md), and [the main registration contract](ora-resource/ora_main_registration_contract.md) before preparing an archive. For an initial or existing-site Filter request, also read [ora_filters.md](ora-resource/ora_filters.md). For Settings discovery or change, also read [ora_settings.md](ora-resource/ora_settings.md). For Talent Community Sign-Up initialization or update, also read [ora_talent_community.md](ora-resource/ora_talent_community.md).

Before handing off a registration or skill enhancement, run [ora_regression_suite.md](ora-resource/ora_regression_suite.md). When the user asks to run regression, execute that suite: perform its static and read-only gates, prepare each selected test through the existing Data Loader workflow, request the case-specific inputs and immutable-archive approval, submit only after approval, and record its result. It never bypasses approval or directly calls a Fusion write endpoint.

## Reuse boundaries

Reuse `core.fusion-api.rest-api-client` for every Career Sites and Candidate Experience read, including the live HCM LOVs. Reuse `core/data-loader` for every archive validation, approval, submission, status check, and error diagnosis. The existing `shared.validation.reference-data-validator` dependency provides cross-pillar validation structure, while this skill retains the Candidate Experience-specific endpoint, header, active-status, and identifier rules in [ora_reference_lookups.md](ora-resource/ora_reference_lookups.md).

Do **not** route Candidate Experience LOVs through `core.fusion-api.apps-common.lookups`: that skill is for Application Common Features lookup resources under `/fscmRestApi`; Career Site Languages, Job Families, Job Functions, Recruiting Types, Locations, and Organizations use the separately documented `/hcmRestApi` endpoints. A future feature may reuse it only after its live endpoint is confirmed to be an Application Common lookup.

## Offline contract tests

Run the offline Career Sites contract suite whenever this skill or an `ora-resource` contract changes:

```bash
python3 -m unittest discover -s pillars/hcm/recruiting/candidate-experience-configuration/career-sites-configuration/tests -v
```

The suite validates the local contract only: skill identity, registry graph/source integrity, supported read-only modes, critical combined-create invariants, documentation references, and Site Editor Copy Link behavior. It never authenticates to Fusion or creates a Data Loader archive. Keep live registration, LOV, and task-hook validation as separate gates.

## Conversation contract

For creation, collect Site Name, Site Code, optional active Default Language (default `US`), optional additional initial language codes, and optional standard Filter type/value pairs. The final language set must contain the exact Default Language once; reject empty or duplicate codes and validate every selected language is active. Resolve every Filter against its fresh live LOV, rejecting an unknown, inactive, ambiguous, or duplicate selection. Derive the sequence and use `TemplateNumber=minimal` and `StatusCode=ORA_INACTIVE`. Do not ask for IDs, `SiteNumber`, Cookie Consent text, Talent Community text, or child settings. The combined archive always contains the parent, Languages, one empty default Cookie Consent child, and one empty default Talent Community child, and contains Filters only when requested. Reject Settings and any other unreviewed child before archive generation.

For a Cookie Consent update, collect the existing Site Code and one or more live-template Cookie Consent business attribute/value pairs. Each supplied value must name exactly one target field; do not interpret collective wording such as “custom labels”, “all labels”, or “cookie text” as a value to fan out across fields. Ask the user to identify each intended field when the target is ambiguous. Do not accept or request `CookieId`, `SiteId`, `SiteNumber`, `RestAction`, audit fields, or any excluded routing field as user inputs. Stop if the request has no business-field change, duplicates a field, or names a field absent from the current child template. Use the REST-identifier PATCH contract by default.

For a Cookie Consent PATCH, confirm one exact persisted parent, one existing Cookie Consent child, and the child Object User Key described in the [main registration contract](ora-resource/ora_main_registration_contract.md#cookie-consent-patch). Apply the Cookie Consent UI-state rules before archive generation. Do not accept Cookie Consent creation, parent fields, Languages, Filters, Settings, Talent Community, or arbitrary technical fields in this operation.

For default-language changes, collect an exact active Language already enabled on the site. For activation/inactivation, accept no business input beyond the Site Code. Use the [parent PATCH contract](ora-resource/ora_main_registration_contract.md#parent-patch). Reject an already-current status, a default Language absent from the site collection, or any requested child operation.

For Languages, default-language changes, activation, inactivation, Site Editor Copy Link, or read-only site discovery, collect the existing Site Code and only the requested business input: an exact language code for add/default-language change, or an optional enabled site language for a link. Treat an unqualified request for a "site link", "URL", "Copy Link", or "open site" as **Site Editor Copy Link**. Follow [ora_parent_operations.md](ora-resource/ora_parent_operations.md). Use the same selected target environment already used for login, site creation, or Data Loader operations; derive its standard `restBaseUrl` as `{restBaseUrl}/hcmUI` and never select, infer, or request a separate environment while that context is available. The returned URL must use `/CandidateExperience/{LanguageTag}/sites/{SiteNumber}`; a `/CandExpSecured/` result is invalid. Return the same Copy Link while a site is inactive, but explicitly state that it works only after activation. For an existing-site Filter add, collect the exact Site Code and one or more Filter type/value pairs, then resolve each through the current live LOV as specified in [ora_filters.md](ora-resource/ora_filters.md). For Settings, first present the friendly catalog and current values from [ora_settings.md](ora-resource/ora_settings.md), using Site Editor labels and grouped layout; collect named option/value pairs rather than raw keys. For Talent Community Sign-Up, collect the existing Site Code, both visibility choices, and optional `Title`, `Description`, and `ButtonLabel` for the site's current default language. Refer to the language using its resolved display name and code, for example, `US — American English`; never call an attribute a "US-language title" or imply that US is required for every site. Follow [ora_talent_community.md](ora-resource/ora_talent_community.md), require current global `ORA_IRC_TC_OPTIN_ENABLED` to be enabled, and retain the exact read-back singleton `Id` for the PATCH routing field. Listing languages, the Site Editor Copy Link, summary, effective Filters, Cookie Consent, Talent Community state, and Settings discovery are read-only results; each add/default/status/Filter/Settings/Talent Community change is a separate archive and approval, never a parent resubmission or Cookie Consent archive.

## Site state and tenant capability scope

For any question phrased as “for this site” or “on this site,” resolve the exact `recruitingCESites` parent first and answer from the site-scoped owner of the requested value: a parent attribute, its corresponding expanded child, or the `settings` child. Do not use `globalSettings` as evidence of a site's configured state. Use `globalSettings` only as a tenant-level capability gate for a supported action or to explain why Site Editor makes an otherwise site-scoped control unavailable. A failed or unavailable global lookup must not prevent a read-only site-state answer. For an Events question, read `EventsEnabledFlag` from the resolved parent; report `ORA_IRC_GLOBAL_EVENTS_ENABLED` only as separate environment capability context. Before preparing an Events mutation, require both the published updateable parent `EventsEnabledFlag` contract and the enabled global Events gate; otherwise stop without an archive.

## Preflight

Use the [main registration contract](ora-resource/ora_main_registration_contract.md). Do not require unexposed registration overrides from the core resolver. The standard create requires only the parent, Languages, and Cookie Consent contracts stated in that resource; do not infer another child capability.

1. Confirm the Site Code has no exact existing match.
2. Confirm every supplied/default initial language is active, unique, and includes the Default Language.
3. Resolve the next sequence with the published read-only collection request.
4. Immediately before every preflight and every archive generation, resolve a fresh `recruitingCESites` registration, starter DAT, and attribute-details schema through the existing `core/data-loader` metadata resolver, passing the exact case-sensitive discriminator. Do not implement a task-local or ad hoc REST lookup for `dataLoaderBusinessObjects`: the core resolver owns the finder selection, pagination, registered-object detail, live-template retrieval, and attribute-details retrieval. Treat the exact resolved discriminator, starter DAT, and matching live attribute-details schema together as the registration evidence. Never use a prior project artifact, downloaded workbook, previous DAT, or prior registration JSON as live input; persist each fresh response only as audit evidence for that run.
5. Require parent `recruitingCESites` and children `languages`, `cookieConsent`, `talentCommunitySignUp`, and `filters` under the [main registration contract](ora-resource/ora_main_registration_contract.md). Require `settings` only for a Settings discovery or update; Settings is not a creation prerequisite. Reject unrelated children.
6. Require parent `MandatoryOnCreate=SiteName,SiteCode,DefaultLang,SequenceNumber,StatusCode,TemplateNumber` and matching selectable attributes in the live parent attribute-details schema. Require parent `SiteNumber` in the source header, blank in the parent create row, and excluded from the REST payload. A starter DAT containing only `SiteId`, `SiteNumber`, `RestAction`, and `SiteCode` is a routing skeleton, not evidence that the other selected parent attributes are unavailable. Build the schema-complete parent source header from the live attribute-details schema; retain the starter DAT only for its registered sections and technical columns. Evaluate required parent-create inputs from this explicit `MandatoryOnCreate` list only. Never block the combined archive because generic live attribute metadata lists `SiteId`, `SiteNumber`, or `RestAction` as mandatory: `SiteId` and `SiteNumber` are generated, while the workflow supplies `RestAction=POST`.
7. Keep every generated/routing field out of its REST body. In a same-load source, leave generated parent IDs and `SiteNumber` blank. When a child header contains `SiteCode`, always populate it with the exact requested parent Site Code.
8. For a Filter request, resolve every requested type/value through the corresponding live Site Editor LOV defined in [ora_filters.md](ora-resource/ora_filters.md), normalize it to the returned ID/code, and stop on an unavailable, inactive, or ambiguous choice. Require the Filters child contract in the [main registration contract](ora-resource/ora_main_registration_contract.md#filters-child-contract): `ObjectCtxId` remains the selected surrogate, `SiteNumber` is the String parent identity, Fusion supplies the physical `ObjectId` association, and child foreign keys are empty. For Settings discovery or change, read global capability only through the declared read-only route, then require the [Settings child contract](ora-resource/ora_main_registration_contract.md#settings-child-contract), including `SettingKey` as the child surrogate, String `SiteNumber` parent identity, and empty child foreign keys. For Talent Community, read the global `ORA_IRC_TC_OPTIN_ENABLED` capability through that same declared read-only route and stop unless it is enabled, then require the [Talent Community child contract](ora-resource/ora_main_registration_contract.md#talent-community-sign-up-child-contract), including its `Id` resource surrogate, String `SiteNumber` parent identity, and empty child foreign keys.

## Source construction invariant

For **every** parent, child, and PATCH source row, first create its complete sanitized header list, then create exactly one value list by looking up each header name in the row's field-value map, using `""` only when that header has no value. Serialize that one list once as `MERGE|<section>|` followed by the joined values. Do not append a delimiter, a blank value, `RestAction`, or any routing value after serialization; those values belong in the field-value map before the list is created.

Immediately before immutable preview, reopen the exact DAT member that will be archived and split each `METADATA` and `MERGE` line on `|`. Require `len(mergeCells) == len(metadataCells)` for its same section, including trailing blank cells. This count check is independent of—and must precede—live-schema validation. A mismatch is a local structural failure: make no ZIP preview or Fusion submission. Keep the per-row header-to-value mapping as validation evidence. Do not hand-edit a DAT after this verification; a changed member must be reconstructed and rechecked from its field map.

Do not manufacture, predict, transform, or copy a `SiteNumber`: Fusion generates it only when the parent POST is processed. Validate the complete combined source structurally, including exact `METADATA|<section>|` and `MERGE|<section>|` prefixes for every included section, before generating an immutable preview or using the normal approval gate.

## Main archives

Use this section for the main workflow. Generate a source containing sanitized `recruitingCESites`, `languages`, `cookieConsent`, and `talentCommunitySignUp` metadata, one parent POST row, one Language POST row for every selected unique active Language, one empty Cookie Consent POST row, and one empty Talent Community POST row. Include the `filters` metadata and one Filter POST row per approved Filter only when Filters were requested. Include `DefaultLang` exactly once. For every Language row, leave `SiteId` and `SiteNumber` blank, populate `SiteCode` with the exact requested parent Site Code, set `SiteLanguage`, and set `RestAction=POST` where present.

For add-language, generate only the required top-level and `languages` metadata plus one Language POST row; do not include a parent row. Resolve the persisted parent by Site Code and reject a duplicate or inactive language before preparing the archive. Use the same field-map and equal-cell-count invariant as the default archive. Each archive receives its own immutable preview, Data Loader approval, final-status check, and read-back verification under the [main registration contract](ora-resource/ora_main_registration_contract.md).

Add one sanitized `cookieConsent` metadata section and exactly one Cookie Consent POST row to the main combined source. Leave `CookieId`, `SiteId`, and `SiteNumber` blank; populate `SiteCode` with the exact requested parent code and set `RestAction=POST`. Leave every Cookie Consent business field blank so Fusion supplies its default state. Do not send routing values or a Cookie Consent business value in the REST body. The post-load verifier must require exactly one default Cookie Consent row as well as the approved Language set.

Add one sanitized `talentCommunitySignUp` metadata section and exactly one Talent Community POST row to the main combined source. Leave `Id`, `SiteId`, `SiteNumber`, `Language`, and every Talent Community business field blank; populate `SiteCode` with the exact requested parent code and set `RestAction=POST`. This reproduces the Site Editor's `talentCommunitySignUp:[{}]` create payload and lets Fusion materialize the default singleton. Do not send routing values or Talent Community business values in the REST body. The post-load verifier must require exactly one default Talent Community row with both visibility flags `false`.

For each approved Filter, add the sanitized `filters` metadata section and one `filters` POST row from the [Filters child contract](ora-resource/ora_main_registration_contract.md#filters-child-contract). Populate `SiteCode`, `DimensionTypeCode`, the one matching normalized type-specific value, and `RestAction=POST`; leave `ObjectCtxId`, `SiteNumber`, every nonmatching type-specific field, and unrequested business field blank. Reparse the serialized row by its exact live header and require the resolved value in its designated column: `GeographyId`, `OrganizationId`, `JobFamilyId`, `JobFunctionCode`, or `RecruitingTypeCode`, respectively. If a future header includes `ObjectId`, leave it blank. For a persisted-parent Filter add, include only top-level and Filters metadata plus the requested Filter rows. Do not include a parent, Language, or Cookie Consent data row. Apply the same field-map serialization and equal-cell-count check, then verify the exact normalized additions while parent, Languages, and Cookie Consent remain unchanged.

For Cookie Consent PATCH, use the [Cookie Consent PATCH contract](ora-resource/ora_main_registration_contract.md#cookie-consent-patch). Include no parent or other child data row. Populate the resolved `CookieId`, the requested validated Cookie Consent business fields, `SiteCode`, and `RestAction=PATCH`; leave `SiteId` and `SiteNumber` blank. Build the row strictly from the fresh sanitized header and verify equal header/value cell counts before preview. The immutable preview must list the effective requested changes and retained UI dependencies; approval is required before the one Data Loader submission.

For parent PATCH, use the [parent PATCH contract](ora-resource/ora_main_registration_contract.md#parent-patch). Include only the sanitized parent section and one `recruitingCESites` PATCH row. Populate `SiteCode`, `RestAction=PATCH`, and exactly one business field: `DefaultLang`, `StatusCode=ORA_ACTIVE`, or `StatusCode=ORA_INACTIVE`. Leave `SiteId` and `SiteNumber` blank, include no child section or row, and verify only the approved parent change after submission.

After a successful combined load, resolve the parent by exact `SiteCode` and verify its language collection contains every approved language exactly once, including `DefaultLang`, exactly one Cookie Consent row, exactly one default Talent Community row with both visibility flags `false`, and every approved normalized Filter type/value pair. If the parent succeeds but any requested child fails, record the partial success and do not retry the combined archive.

## Cookie Consent PATCH

Resolve one exact persisted parent by Site Code and one Cookie Consent child through the published Object User Key. Apply the requested fields to the read-back state, validate the effective UI state, and create a child-only PATCH archive. Populate the resolved `CookieId`, requested business values, exact `SiteCode`, and `RestAction=PATCH`; leave `SiteId` and `SiteNumber` blank. Remove every `SourceRef*` field and construct the row from its sanitized live header map. Verify every approved field after final success; do not retry a failed PATCH without a new approved archive and a known recoverable cause.

## Existing-site language, status, and link operations

Use [ora_parent_operations.md](ora-resource/ora_parent_operations.md) for the operation-specific registration gates, source shape, approval, and verification. These operations must not change the combined-create defaults or Cookie Consent values. Do not infer that a parent PATCH or `languages` child POST is available from the web-client route alone: the current published Data Loader registration and template must expose the needed operation before an archive can be prepared.

## Final verification

After a final successful combined load, verify the approved parent values, every approved language child exactly once including the default language, exactly one Cookie Consent row, every approved Filter, and that the Career Site editor opens. After a PATCH or existing-site child POST, verify every approved child field and retain the parent unchanged. Do not retry an import without a new approved archive and a known recoverable cause.

## Phase exit criterion

The default combined parent-plus-Language-plus-Cookie-Consent-plus-Talent-Community path, standard Filter create/add, Cookie Consent PATCH, add Language, default-language change, activation, inactivation, Settings discovery/update, and Talent Community Sign-Up update are supported. Add no additional child capability without a separate migration, registration review, and regression evidence.
