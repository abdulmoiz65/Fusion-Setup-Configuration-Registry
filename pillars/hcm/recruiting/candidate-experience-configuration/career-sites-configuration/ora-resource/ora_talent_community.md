# Talent Community Sign-Up — Persisted-Parent Setup

## Scope

Talent Community Sign-Up is a one-per-site child. The normal combined Career Site create always includes one empty `talentCommunitySignUp` `POST` row, matching the Site Editor's nested `talentCommunitySignUp:[{}]` payload. Fusion then materializes the default singleton. Later work supports only its default-language child `PATCH` when that one row exists. Do not expose initial Talent Community business fields during Career Site creation.

Do not support translation updates, deletion, or a multi-language Title/Description/Button Label flow. Fusion exposes translations at a separate child endpoint, but translation row materialization is unproven.

## User-facing wording

For an existing-site update, the optional `Title`, `Description`, and `ButtonLabel` apply only to the site's resolved current default-language record. In user-facing questions, describe this as, for example: “Optional: update the Talent Community title, description, or button label for this site's default language (`US` — American English).” Substitute the actual resolved default language and display name for each site. Do not call the attribute a “US-language title,” and do not imply that US is required when the site's default language is another locale.

## REST and persistence evidence

The physical table is `IRC_CX_TC_SIGNUP_B`; its `SITE_ID` is both primary key and parent foreign key. Fusion supplies that physical association from the hierarchical parent resource. The child item identifier `Id` is read-only and equals the parent generated String `SiteNumber`, not `SiteId`.

```text
POST  /recruitingCESites/{SiteNumber}/child/talentCommunitySignUp
PATCH /recruitingCESites/{SiteNumber}/child/talentCommunitySignUp/{SiteNumber}
```

The writable default-language REST fields are:

| Field | Required for POST | Type |
| --- | --- | --- |
| `ShowAtSearchResultsFlag` | No for nested default create; yes for standalone recovery POST | Boolean |
| `ShowWhenNoSearchResultsFoundFlag` | No for nested default create; yes for standalone recovery POST | Boolean |
| `Title` | No | Text |
| `Description` | No | Text |
| `ButtonLabel` | No | Text |

`SiteId`, `Id`, `Language`, `ObjectStatus`, object version, and audit fields are system-managed or read-only. `ObjectStatus` defaults to `ORA_ACTIVE`.

## Registration contract

Configure the `talentCommunitySignUp` child in the same main SiteNumber hierarchy used by the supported children:

| Contract item | Required value |
| --- | --- |
| Child table | `IRC_CX_TC_SIGNUP_B` |
| Child surrogate attribute / column | `Id` / `SITE_ID` |
| Child REST parent identity | `ParentId=SiteNumber`, with `SiteNumber` String-typed |
| Parent alternate key | `SiteCode` resolving `SITE_NUMBER AS SiteNumber` from external `IRC_CX_SITES_B` for `SITE_TYPE='EXT'` |
| Child foreign keys and child object user keys | Empty; association is inherited through `ParentId=SiteNumber` |
| Mandatory on create | None — the normal combined row is empty and Fusion supplies `false` defaults |
| Exclude in REST payload | `Id,SiteId,SiteNumber,SiteCode,Language,ObjectStatus,ObjectVersionNumber` and audit fields when exposed |
| POST / PATCH URL overrides | Blank; use the hierarchical resource identity |

`Id` is the REST item identifier even though the physical table stores `SITE_ID`; it is the SiteNumber value that the item URL requires. Do not create a `SiteId` foreign-key set or send `SiteId` in the body. Do not add an Object User Key. For PATCH, Data Loader must receive the exact singleton `Id` from the fresh read-back as its surrogate-routing value; `ExcludeInPayload` keeps that value out of the REST body.

## Preconditions and archive rules

For a normal create, include one empty `talentCommunitySignUp` POST row with the parent, Languages, and Cookie Consent rows. Populate only `SiteCode` and `RestAction=POST` from the fresh header; leave `Id`, `SiteId`, `SiteNumber`, `Language`, both flags, and all text fields blank. Verify one returned child with both flags `false`.

For a later update, resolve exactly one parent by Site Code and retain its generated String `SiteNumber`, current default language, enabled languages, and expanded `talentCommunitySignUp` collection.

For a later update, read `GET /hcmRestApi/CandidateExperience/globalSettings` through the declared read-only capability route first. This exact Candidate Experience path is required; do not construct a `resources/latest/globalSettings` request. `ORA_IRC_TC_OPTIN_ENABLED` must be enabled (`Y` or Boolean `true`), matching the Site Editor's global Talent Community availability. It is not a child payload field and must never be written by this skill. `ORA_IRC_TC_ACTIVE_ATTRIBUTES` is returned as informational context because it controls the global candidate attributes for Talent Community; it does not alter this site's Sign-Up payload or block a valid site-level operation. If the opt-in capability is disabled, absent, or unavailable, report Talent Community as unavailable and do not generate an update archive. The normal combined empty-child initialization records this global state but is not blocked by it.

- If the collection is empty after a historical or partial create, stop and diagnose; do not add a second nonstandard initialization path automatically.
- If it contains exactly one row, prepare one `PATCH`.
- If it contains more than one row, stop as a one-to-one data inconsistency.
- Reject a requested translation language that differs from the current default language.

Build the child-only update source from the fresh sanitized `talentCommunitySignUp` header. Populate the exact singleton read-back `Id`, `SiteCode`, only requested writable fields, and `RestAction=PATCH`. Leave `SiteId`, `SiteNumber`, `Language`, `ObjectStatus`, and all unrequested fields blank. Reparse the final row against its header and require the populated `Id` to equal the read-back child `Id`; stop before preview if it is blank or differs. Include only the top-level and `talentCommunitySignUp` metadata; never include a parent, Languages, Cookie Consent, Filters, or Settings row.

For a visibility-only PATCH, do not hand-count pipe separators. Build the row from the sanitized header names. For example, when the live header is `ButtonLabel|SiteId|Description|Title|Language|ShowAtSearchResultsFlag|ShowWhenNoSearchResultsFoundFlag|Id|SiteNumber|SiteCode|RestAction`, the field map for enabling both choices is `ButtonLabel=""`, `SiteId=""`, `Description=""`, `Title=""`, `Language=""`, `ShowAtSearchResultsFlag="true"`, `ShowWhenNoSearchResultsFoundFlag="true"`, `Id=<read-back Id>`, `SiteNumber=""`, `SiteCode=<exact Site Code>`, and `RestAction="PATCH"`. Iterate those eleven header names once to serialize the values. The five leading blank business cells, including `Language`, must remain five distinct cells; they must not be collapsed into a shorter pipe sequence.

Use the common field-map serialization rule: one value per sanitized header cell and an equal metadata/merge cell count before preview. After approved successful load, reread the singleton child and verify only the approved fields; verify the parent, Languages, Cookie Consent, Filters, and Settings remain unchanged.
