# Career Sites Regression Suite

Use this suite after a Career Sites registration or skill change, before calling the changed behavior ready. It is intentionally Markdown-driven: use the existing `core/data-loader` and read-only Fusion routes, not a task-specific script or direct REST write. When the user says to run regression, the agent executes the suite rather than merely presenting this checklist.

## Inputs and result

Require a fresh portal registration JSON, starter DAT metadata, and matching attribute-details workbook retrieved for this regression run, plus the proposed source/archive when applicable and a non-production target environment. Do not accept an earlier project artifact as registration evidence. Persist one redacted result under the active project's Career Sites `current/regression/` directory. Record each case as `PASS`, `FAIL`, or `BLOCKED`, with the archive hash, request ID when submitted, and read-back evidence. Never include credentials or full sensitive payloads.

Do not submit a test archive without the normal immutable-archive approval. A failed test is not authority to retry the same archive or change Fusion data outside the declared operation.

## Execution protocol

1. Ask once for the non-production target environment and a unique test-code prefix, unless both are already explicit in the current task. Ask only for the requested test cases' needed inputs: site name/code when creating, selected default and additional languages, or existing site code and requested change when operating on a created test site.
2. Run Gate A and Gate B automatically. Report `BLOCKED` and stop if either gate fails.
3. Run Gate D validation cases automatically when their evidence can be produced locally or by read-only lookup. Never submit a deliberately malformed or invalid source to Fusion merely to test rejection.
4. For each Gate C mutation, prepare and structurally validate exactly one archive. Present its exact target, operation, source summary, hash, and expected read-back. Request approval for that one archive; do not request or accept blanket approval for future cases.
5. After approval, submit through `core/data-loader` once. Record the initiation/request ID and stop that submission turn. On the user's next instruction to continue or check regression status, retrieve final status through the core workflow, run read-back verification, persist the case result, and advance to the next selected case.
6. Reuse a successfully verified test site only where the matrix says so. Never rerun a failed or partial archive; create a fresh archive and obtain new approval if a recoverable correction is needed.

The agent may run Gate A, Gate B, and Gate D without approval because they are read-only or local validation. Every actual Data Loader load remains individually approved.

## Gate A — static registration and DAT shape

Run this gate for every registration change; it has no Fusion side effect.

1. Fetch and parse the current registration, starter DAT, and attribute-details schema through the core Data Loader resolver. Require the main parent `recruitingCESites` and registered `cookieConsent`, `languages`, `filters`, and `settings` children. Each child must reference the current parent business-object ID. Do not use a saved project artifact from an earlier run.
2. Require parent String `SiteNumber` / `SITE_NUMBER` as the surrogate and `SiteCode` as its only alternate resolver. Parent `SiteNumber` stays in the DAT, blank on create, and excluded from the REST body. Do not require cleared custom URLs to be visible to the core resolver.
3. Require Cookie Consent `CookieId` / `COOKIE_ID`, `ParentId=SiteNumber`, empty `foreignKeys`, the `SiteCode → CookieId` Object User Key, and `CookieId,SiteId,SiteNumber,SiteCode` excluded from its REST body. Do not require custom child URLs to be visible to the core resolver.
4. Require Languages `SiteLanguage` / `SITE_LANGUAGE`, `ParentId=SiteNumber`, empty `foreignKeys`, no child object user key, `MandatoryOnCreate=SiteLanguage`, and `SiteId,SiteCode,SiteNumber` excluded from its REST body. Reject a composite child surrogate or a `SiteId` foreign-key set.
5. Require Filters `ObjectCtxId` / `OBJECT_CXT_ID`, `ParentId=SiteNumber`, empty `foreignKeys`, no child object user key, `MandatoryOnCreate=DimensionTypeCode`, and `SiteNumber,SiteCode` excluded from its REST body while `ObjectCtxId` remains mapped. `ObjectId` may be absent from the generated header; reject an `ObjectId` foreign-key set or custom POST/PATCH URL dependency.
6. Require Settings `SettingKey` / `SETTING_KEY`, `ParentId=SiteNumber`, empty `foreignKeys` and child object user keys, `MandatoryOnCreate=SettingKey`, and `SettingId,SiteNumber,SiteCode` excluded from its REST body while `SettingKey` and `SettingValue` remain mapped. Reject a `SiteId`/`SiteNumber` foreign-key set or custom POST/PATCH URL dependency.
7. Require the starter DAT metadata sections `recruitingCESites`, `languages`, `cookieConsent`, `filters`, `settings`, and `talentCommunitySignUp`. The `languages` header must contain `SiteId`, `SiteLanguage`, `SiteCode`, `SiteNumber`, and `RestAction`; the `filters` header must contain `ObjectCtxId`, `DimensionTypeCode`, `SiteCode`, `SiteNumber`, and `RestAction`; the Settings header must contain `SettingKey`, `SettingValue`, `SiteCode`, `SiteNumber`, and `RestAction`; the Talent Community header must contain `Id`, `SiteId`, `ShowAtSearchResultsFlag`, `ShowWhenNoSearchResultsFoundFlag`, `SiteCode`, `SiteNumber`, and `RestAction`, with no Talent Community `MandatoryOnCreate` business fields. When the parent starter header is skeletal, require the matching parent attribute-details worksheet to contain the six published parent create fields; do not classify this as a registration failure.
8. For every prepared source, remove `SourceRef*` fields; require the schema-complete parent header to contain `SiteName`, `SiteCode`, `DefaultLang`, `SequenceNumber`, `StatusCode`, and `TemplateNumber`; require each action row to start `MERGE|<section>|`; and require its value count to equal that section's sanitized metadata attribute count. Reopen the final DAT member and repeat this count after splitting each line on `|`, preserving trailing blanks. Require that each row was built from one field-name-to-value map by iterating its sanitized header exactly once; reject any row with an appended delimiter or post-serialization value. For a combined create, every `languages`, `cookieConsent`, or `filters` row whose header contains `SiteCode` must hold the exact parent Site Code in that mapped field; parent and child `SiteNumber` remain blank.

Stop at Gate A on any mismatch. Do not run a live test against a stale template or infer missing child columns.

## Gate B — read-only preflight

Run before every create or existing-site test.

- Resolve the exact site code: it must be unused for create and uniquely present for existing-site operations.
- Resolve every requested language from the installed-language LOV and require `ActivationStatus=ACTIVE`.
- Resolve every requested Filter through its corresponding current Site Editor LOV. Require the final Job Location/Organization ID or Job Category/Job Function/Recruiting Type code to be returned by that lookup; require Job Category `ActiveStatus=A`; and stop for zero or ambiguous display-name matches. For Job Function and Recruiting Type, retain a redacted receipt of the exact `finder`, `onlyData`, `limit`, `Ora-Irc-Language`, `Accept-Language`, response status, and count. An empty body without that receipt fails Gate B as a request defect.
- For a create, require a selected default language and ensure the ordered initial-language set contains it exactly once.
- Resolve the next sequence through the existing core-owned paginated lookup.
- For existing sites, retain opaque String `SiteNumber`, current default language, status, `EventsEnabledFlag`, Language collection, and Cookie Consent collection.
- For a Settings discovery/update case, use the declared read-only global-capability step. Verify `IRC_ELASTIC_SEARCH_ENABLED` produces the same ZIP/distance visibility behavior as the Site Editor. Global Events/AI flags are environment-capability context only; use parent `EventsEnabledFlag` for the site Events state.

## Gate C — approved functional matrix

Use unique non-production codes. Run the cases in this order because later cases reuse verified sites.

| ID | Operation | Test input | Expected read-back |
| --- | --- | --- | --- |
| C1 | Combined create, one language | Default `US`; languages `US` | Source maps the exact parent Site Code into every child `SiteCode` column, leaves generated IDs and `SiteNumber` blank, then produces one inactive minimal site, languages `[US]`, one Cookie Consent child, one default Talent Community child, and an Editor/Language page that loads. |
| C2 | Combined create, non-US default | Default `KO`; languages `KO` | One inactive minimal site, languages `[KO]`, one Cookie Consent child, and one default Talent Community child. No `US` row is invented. |
| C3 | Combined create, multiple languages | Default `US`; languages `US, KO` | One inactive minimal site, exactly `US` and `KO` once each, one Cookie Consent child, and one default Talent Community child. |
| C4 | Add language | Add `KO` to C1 | Child-only Languages POST; parent and Cookie Consent unchanged; languages become `[US, KO]`. |
| C5 | Change default | Change C4 from `US` to `KO` | Parent-only PATCH; languages remain `[US, KO]`; Cookie Consent unchanged. |
| C6 | Activate / inactivate | C4 or C5 site | Parent-only `StatusCode` PATCH each direction; no child changes. |
| C7 | Site Editor Copy Link | Existing active or inactive site, the same target-environment `restBaseUrl` used by login/create/Data Loader, selected/default enabled language, and `SiteNumber` | Derive `{restBaseUrl}/hcmUI`, then return `{uiBaseUrl}/CandidateExperience/{LanguageTag}/sites/{SiteNumber}`. Verify the configured port is retained when present, language precedes `sites`, `SiteNumber` is used, and no `CandExpSecured` route is returned. Do not request or select a separate environment while the active environment's `restBaseUrl` is configured. For an inactive site, state that the link works after activation; for an active site, state that the public link is available. |
| C8 | Cookie Consent named-field PATCH | Existing site with one child; one or more explicitly named child field/value pairs | Only the named child fields change; parent and language collection remain unchanged. The immutable preview lists each field's current and proposed value. |
| C9 | Existing-site Job Location Filter POST | Existing site; one value confirmed by the live Geography LOV | Child-only Filters POST adds exactly the resolved `ORA_LOCATION` filter; parent, Languages, and Cookie Consent are unchanged. |
| C10 | Combined create with Job Location Filter | Default `US`; one value confirmed by the live Geography LOV | One inactive minimal site with its required Languages/Cookie Consent children and exactly one approved resolved `ORA_LOCATION` Filter. |
| C11 | Show available Settings | Existing site with Settings collection | Friendly groups, current persisted/default state, valid choices, dependencies, and global feature availability are returned; no archive. |
| C12 | Update Settings | Existing site; set a valid catalog option | Child-only Settings POST/PATCH reflects each requested string value; parent and other children remain unchanged. |
| C13 | Settings global capability display | Existing site; current global-capability response | ZIP/distance are hidden or unavailable when Elastic Search is false; Events/AI availability matches global flags; no archive. |
| C14 | Combined create default Talent Community Sign-Up | One unused demo Site Code; default `US` | Combined archive contains one empty Talent Community POST row; resulting site contains exactly one child with both visibility flags `false`. |
| C15 | Update Talent Community Sign-Up | C14 site; one or more writable field changes | Child-only PATCH contains the exact read-back singleton `Id` as the Data Loader surrogate-routing field, changes exactly the approved fields, creates no duplicate child, and leaves unrelated data unchanged. |
| C16 | Talent Community global capability | Existing site; fresh `GET /hcmRestApi/CandidateExperience/globalSettings` response with `ORA_IRC_TC_OPTIN_ENABLED=Y` | Talent Community controls and archive preparation are available; the global value is not sent in the child payload. |
| C17 | Effective default discovery | A normal combined-create site with no Settings overrides and no Filters | Discovery reports Classic Search as the editor default, empty Filters as All/no restriction, the returned Cookie Consent and Talent Community values as Fusion-initialized defaults, and the persisted default/enabled Languages. It must not describe any of those effective states as “none configured.” |
| C18 | Site Events state versus global capability | Existing site with `EventsEnabledFlag=false`; global Events capability `Y` | Report Events as disabled for that site and available in the environment; do not infer the site state from the global flag. |
| C19 | Site Events state when globally unavailable | Existing site with `EventsEnabledFlag=true`; global Events capability `N` | Report Events as configured for that site but unavailable in Site Editor because the environment capability is disabled. |
| C20 | Site Events state when the global lookup fails | Existing site with readable `EventsEnabledFlag` and unavailable global lookup | Report the site Events state and state that environment capability could not be determined; do not fail the read-only discovery. |

Each successful load requires its own immutable preview and approval. Capture the source section list, structural-validation result, final Data Loader status, and read-back result.

## Gate D — no-side-effect negative matrix

These cases must stop before archive approval/upload and leave no Fusion change:

| ID | Input | Required blocker |
| --- | --- | --- |
| D1 | Existing Site Code on create | Duplicate-code blocker. |
| D2 | Inactive or unknown initial language | Invalid language blocker. |
| D3 | Duplicate initial language, such as `US,US` | Duplicate-language blocker. |
| D4 | Initial language set omits DefaultLang | Default-language membership blocker. |
| D5 | Add a language already enabled on the site | Idempotency/duplicate-language blocker. |
| D6 | Set default language to one not enabled on the site | Membership blocker. |
| D7 | Activate or inactivate an already-current status | Idempotent no-op; no archive. |
| D8 | Cookie PATCH that violates UI dependencies | Validation blocker; for example enabled Decline without its label. |
| D9 | Malformed source row, including an appended trailing blank after `RestAction` | Structural blocker for wrong section discriminator or unequal header/value count. |
| D10 | Settings or another unreviewed child in create | Scope blocker; no archive. The required empty Talent Community default child is allowed. |
| D11 | Main Languages registration selects `SiteNumber,SiteLanguage` as one child surrogate | Registration blocker; no archive. |
| D12 | Main Cookie Consent registration configures `SiteId` as a foreign key or a nonempty Cookie business field is requested in combined create | Registration/scope blocker; no archive. |
| D13 | Cookie PATCH has no existing child, resolves an ambiguous/mismatched `CookieId`, or violates a UI dependency | Target/validation blocker; no archive. |
| D14 | Default-language target is inactive/not site-enabled, or requested status is already current | Membership blocker or idempotent no-op; no archive. |
| D15 | Filter with unknown type, no matching value, more than one type-specific value, or a duplicate normalized type/value pair | Filter-validation blocker or idempotent duplicate; no archive. |
| D16 | Filters registration selects `ObjectId` as a foreign key or omits `ObjectCtxId` from REST mapping | Registration blocker; no archive. |
| D17 | Raw/unknown Settings key, invalid boolean/order token, mode-incompatible choice, or Settings in initial create | Settings validation/scope blocker; no archive. |
| D18 | Settings registration uses `SettingId` instead of `SettingKey` as surrogate, configures a parent foreign key, or lacks String `SiteNumber` | Registration blocker; no archive. |
| D19 | Talent Community registration uses `SiteId` as a foreign key, lacks the `Id` resource surrogate or String `SiteNumber`, or exposes routing fields in the REST payload | Registration blocker; no archive. |
| D20 | Talent Community combined-create row contains a business value, existing-site operation uses POST, finds zero/multiple child rows, or requests a translation update | Validation/scope blocker; no archive. |
| D21 | Talent Community global capability is disabled, absent, or cannot be read | Capability blocker; no archive. |
| D22 | A Filter row places a resolved value in a nonmapped type-specific column, for example `ORA_CAMPUS` in `OrganizationId` instead of `RecruitingTypeCode` | Structural/mapping blocker; no archive. |
| D23 | Talent Community PATCH has a blank, absent, or read-back-mismatched `Id` | Key-resolution blocker; no archive. |
| D24 | Talent Community visibility PATCH collapses one or more blank fields before `ShowAtSearchResultsFlag` | Structural blocker: rebuild the row by iterating the sanitized header and require exactly one value cell per header cell. |
| D25 | Cookie Consent request such as “custom labels: Hello” without named target fields | Ambiguity blocker; request explicit field/value pairs and produce no archive. One supplied value must never populate multiple fields. |

## Exit rule

Report the changed capability ready only when Gate A, its relevant Gate C case, and all applicable Gate D cases pass. A registration/skill change that affects create, Languages routing, or Cookie Consent routing reruns C1, C3, C4, C8, D3, D4, D5, D8, D9, and D25 at minimum. A Filters registration/skill change also reruns C9, C10, D15, D16, and D22. A Settings registration/skill change also reruns C11, C12, C13, D17, and D18. A Talent Community registration/skill change also reruns C14, C15, C16, D19, D20, D21, D23, and D24. Add a separate matrix only when a later child is migrated to the main contract. Keep the prior successful registration JSON and test result as the rollback baseline; do not overwrite it.
