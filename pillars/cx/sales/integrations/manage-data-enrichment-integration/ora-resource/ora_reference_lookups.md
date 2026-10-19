# Manage Data Enrichment Integration Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| read_daas_smart_data_status | operation=check_status after environment, authentication, and design gates pass | Exact Fusion environment; limit and offset controlled by the shared client | GET /crmRestApi/resources/11.13.18.05/daaSSmartData?fields=AccountSmartDataEnabled,AccountSuggestionAPIEndpoint,AddressSuggestionAPIEndpoint,AccountFields,AddressFields&onlyData=true | count, hasMore, limit, offset, items.AccountSmartDataEnabled, items.AccountSuggestionAPIEndpoint, items.AddressSuggestionAPIEndpoint, items.AccountFields, items.AddressFields | Follow pagination until hasMore=false. Zero records means no Smart Data configuration is visible to the authenticated user. One record is returned as the visible configuration. More than one record is ambiguous and must not be collapsed or selected by guesswork. Preserve AccountSmartDataEnabled exactly as returned. | api_reachable=true; configuration_record_count=count across completed pages; account_smart_data_enabled_raw=AccountSmartDataEnabled; account_suggestion_endpoint_configured=nonblank(AccountSuggestionAPIEndpoint); address_suggestion_endpoint_configured=nonblank(AddressSuggestionAPIEndpoint); configuration_visibility=visible, not_visible, or ambiguous | For zero records, return not_visible with the limitation that absence is not proof of disabled configuration. For more than one record, stop as ambiguous and return only the count plus redacted diagnostics. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| The GET returns exactly one record after pagination completes | Return the raw AccountSmartDataEnabled value, endpoint-present indicators, visible configuration status, API reachability, and limitations. |
| The GET returns no records after pagination completes | Return API reachable and configuration not visible; do not claim disabled, unconfigured, or unauthorized. |
| The GET returns more than one record | Stop as ambiguous; do not select a record or merge values. |
| AccountSmartDataEnabled is blank or uses an undocumented value | Preserve the raw value and report enablement interpretation as unknown. |
| An endpoint field is nonblank | Persist only a present indicator by default; do not persist the URL unless the user explicitly requests it for authorized troubleshooting. |
| Fusion returns 401 or 403 | Allow core.fusion-api.rest-api-client to refresh its gitignored cached token once; after another 401 or 403, stop as auth_or_authz. |
| Fusion returns 404 | Stop as catalog_or_release_mismatch; do not substitute another endpoint version or resource. |
| A caller requests a write method or a getAccount/getAddress action | Return unsupported; this status workflow authorizes only the collection GET. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DEI.READ_SMART_DATA | decision | 4 | reference_lookup | visible->DEI.DONE_VISIBLE;not_visible->DEI.DONE_NOT_VISIBLE;ambiguous->DEI.HANDLE_ERROR;unauthorized->DEI.HANDLE_ERROR;not_found->DEI.HANDLE_ERROR;failed->DEI.HANDLE_ERROR | DEI.DESIGN_GATE | stop | operation=check_status and every prior gate passed. |
