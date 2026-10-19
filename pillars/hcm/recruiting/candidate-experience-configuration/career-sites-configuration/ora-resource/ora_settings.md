# Site Settings — Friendly Discovery and Persisted-Parent Updates

## User-facing contract

Users do not provide a `SettingKey`. For “show available settings for `<site>`”, resolve the exact site and its `settings` collection, then return the Site Editor's friendly groups, labels, current values, valid choices, and applicable dependencies. Do not collapse multiple controls into “all enabled” or expose internal enum values. For an update, accept one or more friendly option/value pairs, normalize them to the controlled keys, and show the mapping in the immutable preview.

Settings are supported only after the parent exists. Never include a `settings` row in a create or combined-create archive. Do not support delete, key rename, arbitrary keys, AI/chatbot controls, or global-setting writes in this phase.

All boolean values are serialized as lowercase strings: `"true"` or `"false"`.

## Global capability read

Before Settings discovery or update, perform the workflow-declared **read-only** `GET /hcmRestApi/CandidateExperience/globalSettings` through `core.fusion-api.rest-api-client`. This is a Candidate Experience endpoint, not a `resources/latest` endpoint; do not shorten it to `/globalSettings` when constructing the request. It is not a Data Loader operation and it never changes an environment value. Retain only the following capability results in the redacted run record:

| Global value | Site Editor behavior | Skill behavior |
| --- | --- | --- |
| `IRC_ELASTIC_SEARCH_ENABLED` | ZIP-code search is hidden; distance calculation is disabled when false. | Hide ZIP-code search and show Distance Calculation as unavailable; do not prepare a change to either. |
| `ORA_IRC_GLOBAL_EVENTS_ENABLED` | Events controls are unavailable when false. | Report this only as the environment capability. For “is Events enabled for this site?”, read the parent `EventsEnabledFlag`; never infer that site value from this global flag. Events remains outside this Settings child scope. |
| `IRC_CE_GENAI_SITE_ENABLED` | AI Assistant controls are unavailable when false. | Show AI Assistant as unavailable in the feature-availability summary; AI remains outside this Settings child scope. |

Do not use a global value to block an unrelated local setting. If the capability read cannot be completed, allow discovery and ordinary Settings updates but label the three gated feature areas **Global capability unavailable** and block only a requested change that requires the missing capability.

## Supported catalog

| Group | Friendly option | Controlled key | Allowed value |
| --- | --- | --- | --- |
| Search Settings | Search experience | `SEARCH_TYPE` | **Classic Search** (`classic`) or **Smart Search** (`smart`) |
| Classic search | Show locations / work locations / workplace types / categories / titles / organizations / posting dates facet | `LOCATIONS_FACET_ENABLED`, `WORK_LOCATIONS_FACET_ENABLED`, `WORKPLACE_TYPES_FACET_ENABLED`, `CATEGORIES_FACET_ENABLED`, `TITLES_FACET_ENABLED`, `ORGANIZATIONS_FACET_ENABLED`, or `POSTING_DATES_FACET_ENABLED` | `true` or `false` |
| Classic search | Facet display order | `FACET_ORDER` | Comma-separated unique tokens from `locationsFacet,workLocationsFacet,workplaceTypesFacet,titlesFacet,categoriesFacet,organizationsFacet,postingDatesFacet` |
| Location Search | Search locations | `LOCATION_SEARCH_MODE` | **All locations** (`all`) or **Posting locations** (`recruiting`) |
| Classic search | Enable ZIP, geolocation, or distance search | `ZIPCODE_SEARCH_ENABLED`, `GEOLOCATION_SEARCH_ENABLED`, `DISTANCE_CALCULATION_ENABLED` | `true` or `false` |
| Classic search | Show maps | `MAPS_ENABLED` | `true` or `false` |
| Classic search | Enable on-site / hybrid / remote workplace type | `WORKPLACE_TYPE_ONSITE_ENABLED`, `WORKPLACE_TYPE_HYBRID_ENABLED`, `WORKPLACE_TYPE_REMOTE_ENABLED` | `true` or `false` |
| Smart Search — Location | Location search type | `SMART_SEARCH_LOCATION_TYPE` | **Fixed Location Search** (`centralised`) or **Proximity Search** (`retail`) |
| Smart search | Smart location, work location, workplace-type, category, title, organization, posting-date, map, distance, and workplace-type controls | respective documented `SMART_SEARCH_*` key | `true` or `false` |
| Smart search | Smart primary / retail / secondary facet order | `SMART_SEARCH_PRIMARY_FACET_ORDER`, `SMART_SEARCH_RETAIL_FACET_ORDER`, `SMART_SEARCH_SECONDARY_FACET_ORDER` | Comma-separated unique tokens from the matching family in the client configuration. |
| Smart search | Suggested-panel visibility, text, animation, and animation URL | `SMART_SEARCH_SUGGESTED_PANEL_ENABLED`, `SMART_SEARCH_SUGGESTED_PANEL_MESSAGE`, `SMART_SEARCH_ANIMATION_SUGGESTED_PANEL_ENABLED`, `SMART_SEARCH_CUSTOM_ANIMATION_URL` | boolean for visibility/animation; nonblank text or URL where selected. |

The documented Smart boolean keys are `SMART_SEARCH_RETAIL_LOCATION_FACET_ENABLED`, `SMART_SEARCH_LOCATION_LEVEL1_FACET_ENABLED`, `SMART_SEARCH_LOCATION_LEVEL2_FACET_ENABLED`, `SMART_SEARCH_LOCATION_LEVEL3_FACET_ENABLED`, `SMART_SEARCH_LOCATIONS_FACET_ENABLED`, `SMART_SEARCH_WORK_LOCATIONS_FACET_ENABLED`, `SMART_SEARCH_WORKPLACE_TYPES_FACET_ENABLED`, `SMART_SEARCH_MAPS_ENABLED`, `SMART_SEARCH_DISTANCE_CALCULATION_ENABLED`, `SMART_SEARCH_WORKPLACE_TYPE_ONSITE_ENABLED`, `SMART_SEARCH_WORKPLACE_TYPE_HYBRID_ENABLED`, `SMART_SEARCH_WORKPLACE_TYPE_REMOTE_ENABLED`, `SMART_SEARCH_CATEGORIES_FACET_ENABLED`, `SMART_SEARCH_TITLES_FACET_ENABLED`, `SMART_SEARCH_ORGANIZATIONS_FACET_ENABLED`, and `SMART_SEARCH_POSTING_DATES_FACET_ENABLED`.

## Required discovery presentation

Use the following UI-aligned result shape. Omit a section that is inapplicable to the selected search experience; do not print underlying key names or values. Resolve every absent persisted key to its source-backed effective Site Editor default before presentation, then mark it **Using editor default; no persisted override**. Do not respond that a setting is “not configured” without its effective behavior.

```text
Search Settings
- Search experience: Classic Search (Using editor default; no persisted override)

Facets
- Locations facet: On
- Work locations facet: Off
- Workplace types facet: Off
- Job categories: On
- Job titles: On
- Organizations: Off
- Posting dates: Off

Environment capabilities
- Events: Available
- AI Assistant: Available
```

For Classic Search, present separate **Facets**, **Location Search**, **Maps**, **Distance Calculation**, and **Workplace Tag Display** sections. Use **All locations** and **Posting locations** for its location-search choices. When `IRC_ELASTIC_SEARCH_ENABLED` is false, label ZIP-code search and distance calculation as **Unavailable in this environment** rather than presenting them as changeable controls.

End every Settings discovery result with a concise **Environment capabilities** section: Events and AI Assistant show **Available** or **Unavailable in this environment** from their global gates. This is not a report of a site's configured state. For a site-specific Events question, resolve `EventsEnabledFlag` from the parent and optionally report the environment capability separately. Events and AI Assistant remain informational until their separate supported workflows are implemented.

## Validation and archive rules

1. Read the exact persisted parent and `settings` collection before any change. Use its opaque String `SiteNumber` for routing.
2. Reject an option outside this catalog, duplicate requested keys, an invalid boolean, unknown/repeated facet token, a mode-incompatible smart/classic option, or a missing required text/URL value. Preserve all unrequested settings.
3. Use PATCH when the requested key exists on the site; use POST only when it is absent. A unique setting is scoped to the hierarchical identity `(SiteNumber, SettingKey)`.
4. Fetch the current registration/template through the core Data Loader resolver immediately before source generation. Require `SettingKey`, `SettingValue`, `SiteNumber`, `SiteCode`, and `RestAction` in the live template. `SettingId` may be present as a generated technical field, but it is not needed for PATCH selection.
5. Generate a child-only archive. The row contains the exact `SettingKey`, the normalized string `SettingValue`, `SiteCode`, and `RestAction=POST` or `PATCH`; leave `SettingId` and `SiteNumber` blank when present. Do not include a parent, Languages, Cookie Consent, or Filters data row.
6. `SettingId`, `SiteNumber`, and `SiteCode` are technical/routing-only and excluded from the REST body. The REST body contains only `SettingKey` and `SettingValue`.
7. Build and re-open the final DAT using the standard header-to-value cardinality invariant before preview. After the separately approved load succeeds, read back the specific setting and every requested value; verify the parent and unrelated children are unchanged.

The UI shows defaults for unset keys. Discovery must present the effective friendly value and label an absent key as **Using editor default; no persisted override**, never as a persisted value or simply “not configured.” In particular, a missing `SEARCH_TYPE` means **Classic Search**, not an indeterminate choice between Classic and Smart Search.
