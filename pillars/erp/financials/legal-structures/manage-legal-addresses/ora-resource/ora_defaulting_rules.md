# Manage Legal Addresses Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| ActualContentSource | USER_ENTERED | Every supported CREATE | No |  |
| InternalFlag | Y | Every supported legal-location CREATE | No |  |
| StatusFlag | A | New active legal location | No |  |
| ValidatedFlag | N | No approved address-validation result exists | No | record_address_validation_status |
| GeometryStatusCode | DIRTY | No approved geocoding result exists | No | record_address_validation_status |
| SalesTaxInsideCityLimits | 1 | Target metadata permits the observed address-framework default | No | verify_address_package_baseline |
| AddressStyle | Resolved StyleFormatCode | Country style resolves | No | resolve_address_style_layout |
| CreatedByModule | XLE_CREATE_LE | Every CSV CREATE | No |  |
| OrigSystemReference | New nonblank collision-checked FDoS-owned identifier | Every CSV CREATE | No | find_existing_legal_address |
| TimezoneCode | Null | User omits the optional time zone | No |  |
| Optional dates, phonetic fields, DFF and localization segments | Null | Not supplied and no active runtime context requires them | Yes |  |

FormattedAddress and FormattedMultilineAddress are Fusion-generated; leave them blank on CREATE. Author LeFormattedAddress deterministically from the reviewed components when the target migration contract requires it. Leave physical IDs, audit fields, ESS fields, object versions, and login values blank.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LA.APPLY_DEFAULTS | step | 40 | apply_default | applied->LA.ENFORCE_DESIGN;blocked->LA.HANDLE_ERROR | LA.CHECK_DEPENDENCIES | stop | After dependencies are ready |
