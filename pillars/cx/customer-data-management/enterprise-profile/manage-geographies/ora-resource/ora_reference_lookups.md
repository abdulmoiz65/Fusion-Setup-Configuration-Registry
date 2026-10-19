# Reference Lookups

## Execution phase boundary

`full_import` uses only the native `core.data-loader` CX Import handoff in
[REST execution](ora_rest_execution.md#native-data-loader-cx-import). Its stage
mapping CSV replaces direct mapping lookup/create and MappingNumber requirements.
Its retained preflight envelope replaces direct UCM/import-activity payloads.
Return the loader's required preview/result fields, check status only on explicit
request, and use a fresh approved hierarchy load after confirmed structure success.
REST mapping lookup/create, reuse/drift rules, and mapping IDs below apply only
to `mapping_only`. Loqate ESS behavior remains under its own execution contract.

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| country_code_resolver | Country intake passes basic validation | country | https://docs.oracle.com/en/cloud/saas/customer-data-management/faicd/list-of-available-countries-with-loqate-geography-reference-data.html | Country Name, Country Code | Trim and compare case-insensitively against exactly one documented name or code | country_name, country_code | Stop before Fusion execution and show supported or close values |
| loqate_enabled_profile_resolver | Country is supported | ORA_HZ_ENABLE_DAAS_LOQATE | /fscmRestApi/resources/11.13.18.05/profileOptions/ORA_HZ_ENABLE_DAAS_LOQATE/child/siteProfileOptionValues | ProfileOptionValue | Trim, uppercase, and compare with Y | loqate_profile_value, loqate_profile_matches | Stop as fusion_api_error for multiple results; for missing or mismatched value prepare a confirmation-gated change |
| daas_endpoint_profile_resolver | Country is supported | ORA_HZ_DAAS_GEO_ENDPOINT | /fscmRestApi/resources/11.13.18.05/profileOptions/ORA_HZ_DAAS_GEO_ENDPOINT/child/siteProfileOptionValues | ProfileOptionValue | Require exactly one `SITE` record containing at least one non-whitespace character after trimming; do not compare with a fixed URL | daas_geo_endpoint_value, daas_geo_endpoint_present | Stop as fusion_api_error for multiple results; for missing or blank value ask the user to configure it in Fusion and stop before import |
| user_country_resolver | geography_source is user_provided | country name and optional two-letter code | Explicit user code or an implementation-approved local ISO country catalog | Country name, Country Code | Require one exact ISO alpha-2 code, uppercase it, and do not call Fusion geography/product-catalog APIs for structure preflight | country_name, country_code | Stop as input_validation when the local country/code cannot be resolved exactly; do not substitute a different country |
| geography_type_resolver | User data contains structure levels | GeographyType | User-supplied structure | Canonical import code | Trim, uppercase, and replace internal spaces or hyphens with underscores; show the normalized values in the preview and let Import Management validate them | validated_geography_types | Stop as input_validation only for blank, duplicate, or malformed local values; target rejection is reported from the import activity |
| cx_object_metadata_resolver | Before full_import approval only | Exact stage mapping IMPORT OBJECT | Native Data Loader objectMetadata lookup | UcmAccount | Require one nonblank account; helper normalizes slash segments to dollar syntax and retains it without a later lookup | ucm_document_account, ucm_account_source=live_object_metadata | Stop on missing/ambiguous account; no overrides or fallback; return required loader disclosure |
| import_mapping_definition_resolver | Before every mapping preview | requested_scope | `references/import-mapping-definitions.json` | Name, Description, ObjectCode, ImportMappingColumns | Select structure, hierarchy, or both exactly; validate stable names, expected object codes, unique ordered identity column pairs, and name length; compute a canonical SHA-256 fingerprint | mapping_name, mapping_object_code, mapping_columns, mapping_fingerprint | Stop as catalog_or_metadata_mismatch; never infer or accept a runtime override |
| data_loader_import_authorization | Before Loqate or mapping_only mutations; full_import uses the native approved preflight envelope | selected Fusion environment and immutable artifact | `core.data-loader.task-hook` preview, approval, and archive-verification workflow | taskValidationEnvelope, archiveSha256, preview reference | Require standalone approval of the latest preview and exact artifact SHA-256 verification before the adapter is invoked | data_loader_authorized, data_loader_preview_reference, task_validation_envelope, archive_sha256 | Stop as approval_blocker and preserve the preview; never accept a caller override or implement task-local transport |
| import_mapping_resolver | Before the business preview for GET; after approval only for a missing-definition POST | stable mapping name and object code | Data Loader-validated REST core service GET on `/crmRestApi/resources/11.13.18.05/importMappings` plus mapping-column GET/expand, all with framework version 9 | MappingNumber, Name, ObjectCode, ImportMappingColumns | Reuse exactly one result only when every pair matches; canonicalize into task order; plan one create only when zero results exist | mapping_number, mapping_outcome | Stop on duplicates or drift; keep mapping details internal and reconcile an uncertain POST only by this exact read |

## Supported Country Values

| Country Name | Country Code |
|---|---|
| Andorra | AD |
| Angola | AO |
| Argentina | AR |
| Australia | AU |
| Austria | AT |
| Belgium | BE |
| Bolivia | BO |
| Bosnia and Herzegovina | BA |
| Brazil | BR |
| Bulgaria | BG |
| Canada | CA |
| Cayman Islands | KY |
| Chile | CL |
| China | CN |
| Croatia | HR |
| Cuba | CU |
| Cyprus | CY |
| Czech Republic | CZ |
| Denmark | DK |
| Dominican Republic | DO |
| Ecuador | EC |
| Estonia | EE |
| Finland | FI |
| France | FR |
| Germany | DE |
| Great Britain | GB |
| Greece | GR |
| Guadalupe | GP |
| Guam | GU |
| Guernsey | GG |
| Hungary | HU |
| Iceland | IS |
| India | IN |
| Indonesia | ID |
| Ireland | IE |
| Isles of Man | IM |
| Israel | IL |
| Italy | IT |
| Jamaica | JM |
| Japan | JP |
| Jordan | JO |
| Kenya | KE |
| Latvia | LV |
| Liechtenstein | LI |
| Lithuania | LT |
| Luxembourg | LU |
| Malaysia | MY |
| Malta | MT |
| Martinique | MQ |
| Mexico | MX |
| Netherlands | NL |
| New Zealand | NZ |
| Norway | NO |
| Oman | OM |
| Peru | PE |
| Poland | PL |
| Portugal | PT |
| Puerto Rico | PR |
| Qatar | QA |
| Reunion Island | RE |
| Romania | RO |
| Russia | RU |
| San Marino | SM |
| Singapore | SG |
| Slovakia | SK |
| Slovenia | SI |
| South Africa | ZA |
| South Korea | KR |
| Spain | ES |
| Sri Lanka | LK |
| Swaziland | SZ |
| Sweden | SE |
| Switzerland | CH |
| Taiwan | TW |
| Thailand | TH |
| Tunisia | TN |
| Turkey | TR |
| United Arab Emirates | AE |
| United States | US |
| Uruguay | UY |
| Vatican City | VA |
| Vietnam | VN |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Country name or code matches exactly one row | Return the documented name and uppercase two-letter code |
| User supplies a common alias not present in the table | Do not infer; show close documented values and ask for one |
| Authentication is required before a lookup | Start the configured Fusion authentication flow automatically; do not ask the user for authentication permission |
| A profile lookup returns a 401 or 403 for a cache-managed token | Let the shared core client refresh automatically once without asking permission; if rejected again, report and stop as auth or authorization failure |
| A country or profile lookup cannot be fetched | Tell the user which lookup failed, the affected environment when applicable, a safe error summary, and the recommended retry, authentication, access, or connectivity action |
| ORA_HZ_ENABLE_DAAS_LOQATE returns zero rows or a value other than Y | Show `ORA_HZ_ENABLE_DAAS_LOQATE`, its safe current state, and proposed `Y` in the one business preview, ask whether the user wants Loqate as the source for geography data, and explain that choosing it requires enabling the profile option |
| ORA_HZ_DAAS_GEO_ENDPOINT returns zero rows or a null, empty, or whitespace-only value | Ask the user to configure its site-level value in Fusion and stop before import; re-read it when the user resumes; preserve every existing nonblank value exactly |
| A site-level profile lookup returns multiple rows | Stop as fusion_api_error and disclose the result count without exposing values or tokens |
| A profile value is created or updated after approval | Re-read both profiles, verify their exact expected values, and report the change before ESS submission |
| ORA_HZ_ENABLE_DAAS_LOQATE is Y and ORA_HZ_DAAS_GEO_ENDPOINT is nonblank | Report both as validated, perform no write, ask no profile-change question, and continue |
| User-provided source is selected | Resolve the country and normalize geography types locally without reading Loqate profiles or calling a Fusion geography/product-catalog preflight API |
| mapping_only is selected | Skip country and geography-type resolution; resolve the selected task-owned mapping definitions and applicable Data Loader authorization only |
| Stable import mapping lookup finds one exact definition | Reuse and persist its MappingNumber; do not issue a mapping POST |
| Stable import mapping lookup finds no definition | Record the planned create internally; after the single approval, verify the artifact and create once through the Data Loader-authorized REST core service without another prompt |
| Stable import mapping lookup finds duplicates or drift | Stop; never select an arbitrary result, mutate it, or create another similarly named mapping |
| User-provided upload stage is selected | Resolve and adapter-validate the destination before the business preview and again before upload; do not render it, ask the user, or use a fallback |
| Target rejects a country code or geography type during import | Preserve the activity diagnostic and stop without retry, delete, replacement, or a geography/product-catalog preflight call; the required object-metadata UCM lookup remains read-only and unrelated to semantic validation |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GEO.COUNTRY | decision | 5 | evaluate_result | supported->GEO.DEFAULTS;unsupported->GEO.BLOCKED;failure->GEO.FAILED | GEO.SOURCE | stop | Resolve one Oracle-supported country code for the Loqate branch |
| GEO.PROFILES | step | 7 | reference_lookup | success->GEO.READINESS;failure->GEO.FAILED | GEO.DEFAULTS | stop | Read both configured site-level geography profile values through core.fusion-api.apps-common on the Loqate branch |
| GEO.PROFILE.VERIFY | decision | 14 | evaluate_result | verified->GEO.EXECUTE;blocked->GEO.BLOCKED;failure->GEO.FAILED | GEO.PROFILE.UPDATE | stop | Re-read both profiles and require their exact expected values, then continue without another confirmation |
