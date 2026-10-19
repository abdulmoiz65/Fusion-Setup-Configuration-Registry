# Career Sites Main Registration Contract

## Scope

Use this as the main Career Sites registration contract for parent creation, Languages, default Cookie Consent, standard Filters, Settings, Talent Community Sign-Up, Cookie Consent PATCH, add Language, default-language change, and status updates. It does not infer support for another unreviewed child.

Keep the current registration export and current skill behavior as rollback. Do not modify Data Loader framework scripts.

| Main operation | Allowed scope |
| --- | --- |
| Create Career Site | One parent POST, one or more `languages` POST rows including `DefaultLang` exactly once, and exactly one empty `cookieConsent` POST row. |
| Add standard Filters | One or more `filters` POST rows in the create archive or a persisted-parent child-only archive. |
| Discover or update Settings | Read-only discovery or persisted-parent `settings` POST/PATCH rows only. |
| Default or update Talent Community Sign-Up | One empty `talentCommunitySignUp` POST row in normal create; persisted-parent singleton PATCH only afterward. |
| Add Language | One persisted-parent `languages` POST row only. |
| Update Cookie Consent | One persisted-parent `cookieConsent` PATCH row only. |
| Change default language | One parent-only `DefaultLang` PATCH. |
| Activate / inactivate | One parent-only `StatusCode` PATCH. |

Language PATCH/DELETE, Filter PATCH/DELETE, DFF Filters, Talent Community translations, Pages, Widgets, and every other unreviewed child remain blocked.

## Required fresh parent contract

Resolve the registration, starter DAT, and attribute-details workbook afresh through the core Data Loader metadata resolver immediately before preflight and again immediately before archive generation. Require all of the following:

| Contract item | Required value |
| --- | --- |
| Parent surrogate attribute | `SiteNumber` |
| Parent surrogate database column | `SITE_NUMBER` |
| `SiteNumber` data type | String |
| Parent alternate user key | `SiteCode` only |
| `SiteCode` resolver | Returns `SITE_NUMBER AS SiteNumber` from `IRC_CX_SITES_B` for `SITE_TYPE = 'EXT'` |
| Mandatory create fields | `SiteName,SiteCode,DefaultLang,SequenceNumber,StatusCode,TemplateNumber` |

The core metadata resolver does not expose registration `PostUrl`, `PatchUrl`, or `ExcludeInPayload` override values. Do not block the main workflow because those unobservable values are absent from the resolver response. The portal-generated registration export is the configuration evidence for cleared URL overrides and payload exclusions; the core Data Loader validation remains authoritative for the resulting archive and payload shape.

Reject the main workflow if `SiteId` remains selected as a surrogate, if `SiteNumber` is Number-typed, or if a self-mapping `SiteNumber` user-key set exists. Generic workbook `Required`/`Mandatory` flags for generated `SiteId` or `SiteNumber` do not make them caller inputs: both remain blank on the parent POST row.

## Languages child contract

Require fresh registration, starter DAT, and matching attribute-details evidence for both parent and `languages` immediately before preflight and again before archive generation.

| Contract item | Required value |
| --- | --- |
| Child table | `IRC_CX_SITE_LANGS` |
| Child surrogate attribute / column | `SiteLanguage` / `SITE_LANGUAGE` |
| Child REST parent identity | `ParentId=SiteNumber`, with `SiteNumber` String-typed |
| Parent alternate key | `SiteCode` resolving `SITE_NUMBER AS SiteNumber` from external `IRC_CX_SITES_B` for `SITE_TYPE='EXT'` |
| Child object user keys | None for POST-only Languages support |
| Mandatory on create | `SiteLanguage` |
| Exclude in REST payload | `SiteId,SiteNumber,SiteCode` |

`SiteNumber,SiteLanguage` is the effective hierarchical REST identity, not a comma-separated child surrogate selection. The child surrogate is `SiteLanguage` only; the parent supplies `SiteNumber` through the hierarchy. `foreignKeys` must be empty: configuring `SiteId` as a Data Loader foreign key makes same-load creation fail because the parent has not yet been persisted when the lookup runs. `SiteId` remains a blank technical column in the generated source and is supplied by Fusion's nested REST association. Require the sanitized Language header to contain `SiteId`, `SiteLanguage`, `SiteCode`, `SiteNumber`, and `RestAction`. Do not require custom child Post/Patch URL overrides when the main registration intentionally clears them.

## Source and approval rules

For parent-only mode, create exactly one `recruitingCESites` POST row and include no child rows. For the combined Languages mode, also include one `languages` POST row for each selected unique active Language. A starter DAT containing only `SiteNumber`, `SiteId`, `RestAction`, and `SiteCode` is a routing skeleton, not a complete source schema. Build the schema-complete parent header from the fresh attribute-details workbook, retain the six required business fields, remove all `SourceRef*` columns, populate `RestAction=POST`, and leave both `SiteId` and `SiteNumber` blank.

For a combined Language row, populate only `SiteLanguage`, the exact requested parent `SiteCode`, and `RestAction=POST`; leave `SiteId` and `SiteNumber` blank. For persisted-parent add-language, resolve the exact parent by Site Code, reject an already-enabled or inactive Language, then create one child-only Language row from the fresh sanitized header. Populate `SiteLanguage`, `SiteCode`, and `RestAction=POST`; use the current header's physical/routing fields only as required by this contract and keep them out of the REST body. Never include a parent data row in this operation.

Build the row from the sanitized header field map, then require equal `METADATA` and `MERGE` cell counts before immutable preview. Route approval, upload, and verification through `core/data-loader`; do not use a direct REST write.

## Filters child contract

Require fresh registration, starter DAT, matching attribute-details evidence, and fresh type-specific LOV resolution for every requested Filter immediately before preflight and again before archive generation. Apply the five controlled type/value mappings and validation rules in [ora_filters.md](ora_filters.md).

| Contract item | Required value |
| --- | --- |
| Child table | `IRC_AVAIL_CONTEXT` |
| Child surrogate attribute / column | `ObjectCtxId` / `OBJECT_CXT_ID` |
| Child REST parent identity | `ParentId=SiteNumber`, with `SiteNumber` String-typed |
| Parent alternate key | `SiteCode` resolving `SITE_NUMBER AS SiteNumber` from external `IRC_CX_SITES_B` for `SITE_TYPE='EXT'` |
| Child foreign keys and child object user keys | Empty for POST-only standard Filters support |
| Mandatory on create | `DimensionTypeCode` |
| Exclude in REST payload | `SiteNumber,SiteCode` and internal nonbusiness fields; retain `ObjectCtxId` in the REST mapping. `ObjectId` may be absent from the generated header. |

`ObjectCtxId` is blank on POST and generated by Fusion. `ObjectId` is the physical parent relationship but is supplied by the nested REST association; it can be absent from the generated DAT header. If a future live header exposes it, leave it blank and exclude it from the REST payload. Do not configure an `ObjectId` foreign-key lookup: it would require the parent database row before a same-load parent exists. Do not require custom child URL overrides when the main registration clears them.

For each approved Filter, construct one row from the fresh sanitized `filters` header. Populate the exact parent `SiteCode`, `DimensionTypeCode`, its one matching type-specific field, and `RestAction=POST`; leave `ObjectCtxId`, `SiteNumber`, every other type-specific field, and unrequested business field blank. If the live header includes `ObjectId`, leave it blank. Combined creation includes the Filters section only when requested. A persisted-parent add uses only top-level and Filters metadata plus its Filter rows, never a parent, Language, or Cookie Consent data row. Verify every approved normalized type/value pair after final success and require parent, Languages, and Cookie Consent to remain unchanged for persisted-parent additions.

## Settings child contract

Settings are persisted-parent only. Require fresh registration, starter DAT, matching attribute-details evidence, the friendly Settings catalog, and the declared read-only global-capability response immediately before discovery or archive generation. Never include `settings` in an initial or combined create archive.

| Contract item | Required value |
| --- | --- |
| Child table | `IRC_CX_SITE_SETTINGS` |
| Child surrogate attribute / column | `SettingKey` / `SETTING_KEY` |
| Child REST parent identity | `ParentId=SiteNumber`, with `SiteNumber` String-typed |
| Parent alternate key | `SiteCode` resolving `SITE_NUMBER AS SiteNumber` from external `IRC_CX_SITES_B` for `SITE_TYPE='EXT'` |
| Child foreign keys and child object user keys | Empty; the hierarchical resource identity is `SiteNumber,SettingKey` |
| Mandatory on create | `SettingKey` |
| Exclude in REST payload | `SettingId,SiteNumber,SiteCode`; retain `SettingKey` and `SettingValue` |
| POST / PATCH URL overrides | Blank; do not depend on custom URLs |

`SettingKey` is the selected child resource key. This lets the skill identify and update a setting by its friendly catalog mapping without requiring the caller to know a generated `SettingId`. If a live header includes `SettingId`, leave it blank; Fusion generates and maintains it. Do not configure a `SiteId` or `SiteNumber` foreign-key lookup because parent association is inherited through `ParentId=SiteNumber`.

For each approved Settings change, generate one child-only row from the fresh sanitized header. Populate `SettingKey`, the normalized string `SettingValue`, exact `SiteCode`, and `RestAction=POST` for an absent key or `PATCH` for an existing key. Leave `SettingId` and `SiteNumber` blank when present. Include only top-level and `settings` metadata, never a parent, Language, Cookie Consent, or Filters data row. Apply UI/global-capability validation before preview and verify only the requested Settings after final success.

## Talent Community Sign-Up child contract

Talent Community Sign-Up is a required default child in the normal combined create. Require fresh registration, starter DAT, and matching attribute-details evidence before archive generation. The normal combined source includes exactly one empty `talentCommunitySignUp` POST row. For an existing-site update, require a read-back of the expanded singleton collection immediately before archive generation.

| Contract item | Required value |
| --- | --- |
| Child table | `IRC_CX_TC_SIGNUP_B` |
| Child surrogate attribute / column | `Id` / `SITE_ID` |
| Child REST parent identity | `ParentId=SiteNumber`, with `SiteNumber` String-typed |
| Parent alternate key | `SiteCode` resolving `SITE_NUMBER AS SiteNumber` from external `IRC_CX_SITES_B` for `SITE_TYPE='EXT'` |
| Child foreign keys and child object user keys | Empty; the singleton hierarchy supplies its physical `SiteId` association. PATCH supplies the read-back `Id` directly. |
| Mandatory on create | None — Fusion supplies default `false` flags for the empty combined row |
| Exclude in REST payload | `Id,SiteId,SiteNumber,SiteCode,Language,ObjectStatus,ObjectVersionNumber` and audit fields when exposed |
| POST / PATCH URL overrides | Blank; do not depend on custom URLs |

The REST item identifier `Id` is the inherited parent `SiteNumber`, although the persistence table uses `SITE_ID`; it is not a caller-supplied physical ID. Do not configure `SiteId` as a foreign key or an Object User Key. For a persisted-parent PATCH, place the exact `Id` returned by the singleton read-back in the DAT routing field. It remains excluded from the REST body, but Data Loader requires it to resolve the child surrogate when no child Object User Key is configured.

For normal creation, add one row with `SiteCode` and `RestAction=POST`; leave `Id`, `SiteId`, `SiteNumber`, `Language`, both flags, all text fields, and `ObjectStatus` blank. Fusion then creates the default singleton with both visibility flags `false`. For exactly one existing child, create one `PATCH` row with that child’s exact read-back `Id`, only requested writable fields, `SiteCode`, and `RestAction=PATCH`; leave `SiteId`, `SiteNumber`, `Language`, and all unrequested business fields blank. A missing or blank returned `Id`, a missing child after a historical/partial create, a multi-row collection, a duplicate POST, translations, deletion, or a requested translation language different from the site default is a blocker. Verify the exact requested values after final success while the parent and all unrelated child collections remain unchanged.

## Cookie Consent child contract

Use this contract for every normal create. Require fresh registration, starter DAT, and matching attribute-details evidence for `cookieConsent` immediately before preflight and again before archive generation.

| Contract item | Required value |
| --- | --- |
| Child table | `IRC_CX_COOKIES_B` |
| Child surrogate attribute / column | `CookieId` / `COOKIE_ID` |
| Child REST parent identity | `ParentId=SiteNumber`, with `SiteNumber` String-typed |
| Foreign keys | Empty; do not configure `SiteId` as a Data Loader foreign key for same-load creation. |
| Child object user keys | None for default-child POST-only support. |
| Mandatory on create | None |
| Exclude in REST payload | `CookieId,SiteId,SiteNumber,SiteCode` |

`SiteNumber,CookieId` is the effective hierarchical REST identity, not a composite child surrogate selection. `CookieId` remains blank on POST and is generated by Fusion. Require the sanitized Cookie Consent header to contain `CookieId`, `SiteId`, `SiteCode`, `SiteNumber`, and `RestAction`. Do not require custom child Post/Patch URL overrides when the main registration intentionally clears them.

## Cookie Consent PATCH

Use this contract for every Cookie Consent update. Add this Object User Key to the Cookie Consent registration; it is for existing-child selection only and must not be used by default-child POST:

```json
{
  "UserKeySet": 0,
  "UserKeyAttributes": "SiteCode",
  "UserKeyQuery": "SELECT c.COOKIE_ID AS CookieId FROM IRC_CX_COOKIES_B c JOIN IRC_CX_SITES_B s ON s.SITE_ID = c.SITE_ID WHERE s.SITE_CODE = :SiteCode AND s.SITE_TYPE = 'EXT'"
}
```

Before preparation, resolve one exact parent by Site Code, retain its opaque String `SiteNumber`, and require exactly one Cookie Consent row. Resolve `CookieId` with the Object User Key and cross-check it against the read-only child response. Stop for zero/multiple parents or children, a lookup mismatch, missing `CookieId`, an unrequested technical field, or a field absent from the fresh template.

Apply the requested fields to the read-back child state, then apply the Cookie Consent UI-state rules in [ora_input_validation.md](ora_input_validation.md#cookie-consent-ui-state-rules). Construct a child-only source from the fresh sanitized header. Set `CookieId` to the resolved value, `SiteCode` to the exact requested code, `RestAction=PATCH`, and only requested business fields to their validated target values. Leave `SiteId`, `SiteNumber`, and unrequested business fields blank. Each requested text value must have one named target field; collective input such as “custom labels: Hello” is ambiguous and must stop for clarification, never populate every text field with `Hello`. Do not configure a `SiteId` foreign key or send technical routing fields in the REST body. After a final successful load, read the same child back and verify every approved field.

## Parent PATCH

Use this contract for default-language changes and activation/inactivation. The parent registration already supplies the required `SiteCode → SiteNumber` Object User Key and excludes `SiteId` and `SiteNumber` from the REST payload; do not add custom parent URL overrides or another user key.

Resolve one exact existing parent by Site Code and retain its current `DefaultLang`, `StatusCode`, nonblank String `SiteNumber`, and enabled Languages collection. For a default-language change, require the requested language to be active and already present exactly once in the enabled site Languages collection. For a status change, return an idempotent no-op if the requested status is already current. Stop on an unresolved/ambiguous parent, missing generated `SiteNumber`, unavailable parent business field, or requested child behavior.

Construct a parent-only source from the fresh sanitized parent header. Populate `SiteCode`, `RestAction=PATCH`, and exactly one business field: requested `DefaultLang`, `StatusCode=ORA_ACTIVE`, or `StatusCode=ORA_INACTIVE`. Leave `SiteId` and `SiteNumber` blank, remove all `SourceRef*` columns, and add no child metadata or row. Verify the row cell count before preview. After approval and final success, read the parent back and verify only the requested `DefaultLang` or `StatusCode`; the Languages and Cookie Consent collections must remain unchanged.

## Verification and stop condition

After a successful load, read the exact site by `SiteCode`. Require a nonblank String `SiteNumber` and the approved parent values. For a Languages operation, also require the selected Language collection equals the approved set exactly (or includes the requested added Language exactly once for persisted-parent POST) and that `DefaultLang` remains present. Record the generated `SiteNumber` only as verification evidence. Stop there: do not attempt Filters, Settings, or another unreviewed child.
