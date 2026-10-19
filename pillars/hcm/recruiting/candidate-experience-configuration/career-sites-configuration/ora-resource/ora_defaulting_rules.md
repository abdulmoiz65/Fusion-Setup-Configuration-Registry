# Defaulting Rules — Effective Site Behavior

| Field | Default / rule |
| --- | --- |
| `DefaultLang` | Default `US`; validate against the active language LOV. |
| `languages.SiteLanguage` | One row per selected unique active initial language. The set must include `DefaultLang` exactly once; never hard-code `US`. |
| `TemplateNumber` | `minimal` |
| `StatusCode` | `ORA_INACTIVE` |
| `SequenceNumber` | Approved resolver result plus one. |
| Parent `SiteId`, `SiteNumber` | Fusion-generated; blank in the combined parent row. |
| Combined-child `SiteCode` | Exact requested parent Site Code whenever the live child header contains `SiteCode`; used only for Data Loader routing and excluded from the REST payload. |
| Cookie Consent `CookieId`, `SiteId`, `SiteNumber` | Fusion-generated/routing values; blank in the combined default row. |
| Cookie Consent `RestAction` | `POST` in the combined default row. |
| Talent Community `Id`, `SiteId`, `SiteNumber`, `Language` | Fusion-generated/routing values; blank in the combined default row. |
| Talent Community `RestAction` | `POST` in the combined default row. |

The required Language children initialize the site-language collection with the selected set, including the default language. The empty Cookie Consent and Talent Community child POST rows initialize their default records; they must not populate user-facing values.

For a Cookie Consent PATCH, use the resolved `CookieId`, exact `SiteCode`, and `RestAction=PATCH`; leave `SiteId` and `SiteNumber` blank. There are no default business-field values: use only explicitly requested values validated against the current child template.

## Effective-state reporting

For every read-only discovery or question about current configuration, distinguish the persisted record from the behavior that the Site Editor applies. Do not answer **none configured** when one of the following effective states is known.

| Supported feature | No persisted value/row means | Required user-facing result |
| --- | --- | --- |
| Parent status | New-site default is `ORA_INACTIVE`; an existing parent always has a persisted `StatusCode`. | For a new preview, say **Inactive (creation default)**. For an existing site, report its persisted Active/Inactive status. |
| Default language and Languages | A combined create always materializes one or more Language rows, including the parent `DefaultLang`. | Report the persisted enabled-language set and identify the persisted default language. If a returned parent has no matching Language row, report **Data inconsistency**, not an assumed default. |
| Cookie Consent | A normal combined create materializes exactly one Fusion-default child. | Read the returned child and report its actual effective flags/text as **Fusion-initialized default** until the site has an explicit PATCH. A missing or multiple child collection is **Data inconsistency**, not “no consent configured.” |
| Standard Filters | An empty collection is the UI's **All** selection for each supported filter category. | Say **No restriction — All locations, organizations, job categories, job functions, and recruiting types**. For a populated type, report its persisted selected values; do not infer an unrequested type-specific restriction. |
| Settings | The Site Editor applies source-backed defaults to an absent key. | Report the effective friendly value and append **Using editor default; no persisted override**. Do not expose the raw key unless requested. |
| Talent Community Sign-Up | A normal combined create materializes one child with both visibility flags `false`. | Report **Hidden at search results** and **Hidden when no results are found** as **Fusion-initialized defaults** until a PATCH changes either flag. A missing or multiple child collection is **Data inconsistency**. |

An undocumented or environment-derived fallback must not be invented. When the UI source does not establish an effective value, say **No persisted override; effective default requires source confirmation**, rather than treating the value as disabled or unconfigured.

## Settings defaults required in discovery

Settings discovery must merge the returned `settings` collection over the documented Site Editor defaults before presenting any friendly result. The default itself is an effective value; the absence of a `SettingKey` is only its provenance.

| Friendly option | When the key is absent | Required presentation |
| --- | --- | --- |
| Search experience (`SEARCH_TYPE`) | The Site Editor initializes and falls back to `classic`. | **Search experience: Classic Search (Using editor default; no persisted override)** |
| Smart location search type (`SMART_SEARCH_LOCATION_TYPE`) | When Smart Search is effective, the Site Editor default is `centralised`. | **Location search type: Fixed Location Search (Using editor default; no persisted override)** |
| Classic facets | Use the source-backed Classic facet defaults: Locations, Categories, Titles, and Posting Dates on; Work Locations, Workplace Types, and Organizations off; use the default facet order. | Present each friendly facet state as an effective default when its key is absent. |
| Smart Search controls | When Smart Search is effective, use the Site Editor's controlled Smart Search default catalog for missing keys. | Present the friendly effective value and default provenance; omit Smart-only sections when Classic Search is effective. |

The Search experience fallback is source-confirmed in the Site Editor's `SEARCH_SETTINGS_TYPE.CLASSIC` initialization and load fallback. The Classic facet defaults and Smart Search fallback catalog are likewise client-controlled. Keep this table aligned when the front-end defaults change.
