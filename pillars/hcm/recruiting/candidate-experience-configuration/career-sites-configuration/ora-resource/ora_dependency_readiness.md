# Dependency Readiness — Combined Parent, Languages, Cookie Consent, and Optional Filters

## Site state and Global Settings capability checks

Resolve an exact `recruitingCESites` parent before answering any question about a particular site. The site-scoped owner is the source of truth: read a parent attribute from the parent record, a nested capability such as Cookie Consent or Talent Community Sign-Up from its expanded child, and a search preference from the `settings` child. For example, `EventsEnabledFlag` on the parent determines whether Events are configured for that site. Do not infer a site's state from a global capability.

`/hcmRestApi/CandidateExperience/globalSettings` is an environment-wide, read-only capability source, not a `recruitingCESites` child and not a Data Loader registration target. It is a Candidate Experience endpoint rather than a `resources/latest` resource; clients must use this exact path. For every Settings discovery or update, and every Talent Community Sign-Up update, the declared global-capability step may read it through `core.fusion-api.rest-api-client`; it never writes it. Use the results only to mirror Site Editor visibility/disabled behavior and to gate a supported mutation: `IRC_ELASTIC_SEARCH_ENABLED` gates ZIP-code search and distance calculation; `ORA_IRC_GLOBAL_EVENTS_ENABLED` gates Events; `IRC_CE_GENAI_SITE_ENABLED` gates AI Assistant; and `ORA_IRC_TC_OPTIN_ENABLED` gates Talent Community Sign-Up updates. `ORA_IRC_TC_ACTIVE_ATTRIBUTES` describes the global Talent Community candidate attributes, but does not change this site's Sign-Up child payload or validation. A failed global read must not block an ordinary read-only site-state answer or unrelated per-site Settings operations such as facets, maps, or workplace-type preferences; label globally gated controls as unavailable until the capability can be read. Do not prepare a persisted-parent Talent Community update unless `ORA_IRC_TC_OPTIN_ENABLED` is explicitly enabled (`Y` or Boolean `true`). An Events update additionally requires a published updateable parent `EventsEnabledFlag`; a global `Y` alone is not authority to construct a parent PATCH. The normal combined create always carries its empty default Talent Community row; record the global state but do not turn that UI-equivalent default initialization into a separate capability blocker.

| Sequence | Dependency | Evidence |
| ---: | --- | --- |
| 1 | Published parent, Languages, and Cookie Consent registration | Parent and both child sections are present and match the registration contract. When Filters are requested, their child section must also match [ora_filters.md](ora_filters.md). |
| 2 | Exact code availability | No exact persisted SiteCode match. |
| 3 | Default language | One active resolved language. |
| 4 | Sequence allocation | Valid current next sequence. |
| 5 | Combined archive | One parent POST row, one Languages POST row per selected unique active language including `DefaultLang`, one Cookie Consent POST row, and zero or more validated Filters POST rows; generated identifiers and child `SiteNumber` fields blank. |
| 6 | Final verification | Final Data Loader success and read-back of the exact parent with every approved language exactly once, including `DefaultLang`, one Cookie Consent row, and every requested Filter. |

## Combined create

The combined path is the sole supported create workflow. A partial child failure is not authority to resubmit the archive or construct an alternate source; record the partial success and stop.

## Cookie Consent PATCH

| Sequence | Dependency | Evidence |
| ---: | --- | --- |
| 1 | Existing target | One exact parent from Site Code with a nonblank String `SiteNumber`. |
| 2 | Existing child | Expanded parent response and Object User Key each resolve the same single `CookieId`. |
| 3 | PATCH registration | Child PATCH URL and `CookieId` Object User Key are published; routing fields remain excluded from REST. |
| 4 | Patch source | No parent row; one child PATCH row with routing fields and one or more requested business-field changes. |
| 5 | Approval and verification | A new immutable preview is approved; final read-back confirms every requested child field and the unchanged parent. |

## Site Settings

| Sequence | Dependency | Evidence |
| ---: | --- | --- |
| 1 | Existing target | One exact parent from Site Code with nonblank String `SiteNumber` and its current `settings` collection. |
| 2 | Friendly catalog | Each requested user-facing option maps to one controlled key and a valid String value in [ora_settings.md](ora_settings.md). |
| 3 | Current child contract | Published `settings` child exposes `SettingId`, `SettingKey`, `SettingValue`, `SiteNumber`, `SiteCode`, `RestAction`, and POST/PATCH routes. |
| 4 | Operation decision | PATCH an existing key; POST an absent key. No create/combined, delete, rename, arbitrary key, or global-setting operation. |
| 5 | Approval and verification | A child-only immutable archive is approved; read-back confirms requested settings and unchanged parent/unrelated children. |
