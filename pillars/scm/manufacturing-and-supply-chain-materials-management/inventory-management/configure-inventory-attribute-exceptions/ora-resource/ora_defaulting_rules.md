# Configure Inventory Attribute Exceptions Defaulting Rules

## Source Evidence

| Source | Used For |
|---|---|
| User-approved defaulting policy | Always set InvAttributeCode to COUNTRY_OF_ORIGIN_CODE on create, including when the request supplies another value. |
| User-approved scope policy | Derive the exception type from an unambiguous item or catalog/category scope, and request clarification for ambiguous scope. |

## Approved Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| InvAttributeCode | COUNTRY_OF_ORIGIN_CODE | Every create request for Configure Inventory Attribute Exceptions. | Yes. Replace any supplied value with COUNTRY_OF_ORIGIN_CODE. | |
| InvAttributeExceptionType | I | A create request omits InvAttributeExceptionType, provides ItemNumber, and does not provide CatalogName or CategoryName. | No. Preserve an explicit supplied value unless it conflicts with the supplied scope. | |
| InvAttributeExceptionType | C | A create request omits InvAttributeExceptionType, provides both CatalogName and CategoryName, and does not provide ItemNumber. | No. Preserve an explicit supplied value unless it conflicts with the supplied scope. | |

## Defaulting Behavior

| Input Shape | What Happens |
|---|---|
| InvAttributeCode is omitted on create | Set InvAttributeCode to COUNTRY_OF_ORIGIN_CODE. |
| InvAttributeCode is explicitly supplied on create | Replace the supplied value with COUNTRY_OF_ORIGIN_CODE. |
| ItemNumber is supplied; CatalogName and CategoryName are absent; InvAttributeExceptionType is omitted | Set InvAttributeExceptionType to I. |
| CatalogName and CategoryName are supplied; ItemNumber is absent; InvAttributeExceptionType is omitted | Set InvAttributeExceptionType to C. |
| ItemNumber and either CatalogName or CategoryName are supplied | Do not derive a type. Request scope clarification. |
| Only CatalogName or only CategoryName is supplied | Do not derive a type. Request scope clarification. |
| ItemNumber, CatalogName, and CategoryName are all absent while InvAttributeExceptionType is omitted | Do not derive a type. Request scope clarification. |
| InvAttributeExceptionType is explicitly supplied | Preserve the supplied value. REST/BO owns compatibility validation against the supplied scope. |
| Operation is update | Do not apply these task-local defaults. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IAE.APPLY_ATTRIBUTE_CODE_DEFAULT | step | 10 | apply_default | applied->IAE.DERIVE_EXCEPTION_TYPE;overridden->IAE.DERIVE_EXCEPTION_TYPE;not_applicable->IAE.DERIVE_EXCEPTION_TYPE | none | stop | Set InvAttributeCode to COUNTRY_OF_ORIGIN_CODE before Data Loader preparation for a create request. |
| IAE.DERIVE_EXCEPTION_TYPE | step | 20 | apply_default | item_scope->IAE.DONE;category_scope->IAE.DONE;explicit_supplied->IAE.DONE;ambiguous->IAE.REQUEST_SCOPE_CLARITY;incomplete->IAE.REQUEST_SCOPE_CLARITY;missing_scope->IAE.REQUEST_SCOPE_CLARITY | IAE.APPLY_ATTRIBUTE_CODE_DEFAULT | stop | Derive I or C only for an omitted type with an unambiguous scope; preserve an explicit type and leave compatibility validation to REST/BO. |
