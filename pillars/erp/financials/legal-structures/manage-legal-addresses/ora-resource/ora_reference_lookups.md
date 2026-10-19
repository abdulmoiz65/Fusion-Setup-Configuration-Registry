# Manage Legal Addresses Reference Lookups

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| find_existing_legal_address | Before CREATE and whenever another Legal Structures task selects an address | Fresh same-target, same-release, scope-complete XLE_LE_LEGAL_ADDRESS.csv; Country and complete canonical component tuple or LeFormattedAddress | Require one exact normalized active internal row with InternalFlag Y and StatusFlag A; export is the only approved CREATE-value-resolution exception and yields natural keys only | Existing FormattedAddress or LeFormattedAddress natural-key receipt; collision evidence for a new OrigSystemReference | Zero is a create candidate only after complete-scope proof; many blocks; never copy physical IDs, audit fields, or another row's source reference |
| record_address_validation_status | After layout validation and again after re-export | User-entered components, resolved style, FormattedAddress, ValidatedFlag, GeometryStatusCode | Record the supplied tuple and resulting status without a dependent-geography match or canonicality claim | Disclosure showing ValidatedFlag N and GeometryStatusCode DIRTY are accepted for this scope | Missing mandatory layout data blocks; N/DIRTY does not block |
| verify_address_package_baseline | Before package preview | Fresh target ASM_SETUP_CSV_METADATA.xml, XLE_LE_LEGAL_ADDRESS.csv header and scope receipt | Require exact current metadata hierarchy, header spelling/order, empty child preservation, target identity, release, task-scoped successful-status evidence, and evidence fingerprint | Shape and collision-check receipt | Stale, partial, required-object failure or warning, wrong-target, or ambiguous evidence blocks |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_address_territory | Country is supplied | Country name or two-letter code | /fscmRestApi/resources/11.13.18.05/territoriesLOV | TerritoryCode, TerritoryShortName, EnabledFlag, ObsoleteFlag | One exact code or case-insensitive exact short-name match with EnabledFlag Y and ObsoleteFlag N | Country as TerritoryCode and country display receipt | Zero or many blocks |
| resolve_address_style_layout | Territory resolves | Exact TerritoryCode | /crmRestApi/resources/11.13.18.05/addressStyleFormats/{CountryCode} and child AddressStyleFormatLayout | CountryCode, CountryName, StyleFormatCode, StyleFormatName, AttributeName, AttributeLabel, GeographyType, GeographyLevel, MandatoryFlag, UppercaseFlag, LineNumber, Position | Require one country style and its complete layout; every MandatoryFlag true attribute must be supplied | AddressStyle from StyleFormatCode and the exact conditional-required component set | Missing style, zero layout rows, incomplete pagination, or ambiguous style blocks |
| resolve_address_timezone | TimezoneCode is supplied | Exact TimezoneCode | /fscmRestApi/resources/11.13.18.05/timezonesLOV | TimezoneCode, Name, EnabledFlag, LongName, ShortName, Offset | One exact code with EnabledFlag Y | TimezoneCode | Zero, many, or disabled blocks only the optional time-zone branch |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Free-text LOV input | Normalize only outer whitespace, use exact code or Unicode-normalized case-insensitive exact display matching, follow all pages, and require exactly one active eligible row |
| Lookup receipt | Retain resolver, target environment, release, as-of instant, normalized inputs, method/path, requested fields, pre/post eligibility counts, natural keys, receipt-only IDs, effective/status evidence, derived values, and evidence fingerprint |
| Physical ID returned | Keep it in the receipt only; no physical ID enters CREATE |
| REST or export failure | Classify the actual auth, transport, Fusion API, catalog, or evidence failure; never reinterpret failure as zero matches |
| Broader export container | A task-level export must complete successfully. A broader functional-area or offering export may have overall status Completed with errors only when its archive is available, the exact process log identifies every failed object, every object/member required by this task completed successfully with zero failed, warning, or partial rows, every failure is provably outside this task, and target, release, freshness, fingerprint, hierarchy, and headers are verified. Record and disclose the scoped exception; any required-object failure, warning, partial result, missing counter, or indeterminate status blocks. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LA.RESOLVE_REFERENCES | step | 20 | reference_lookup | resolved->LA.CHECK_DEPENDENCIES;blocked->LA.HANDLE_ERROR;failure->LA.HANDLE_ERROR | LA.VALIDATE_INPUT | stop | Resolve every applicable local and live reference |
