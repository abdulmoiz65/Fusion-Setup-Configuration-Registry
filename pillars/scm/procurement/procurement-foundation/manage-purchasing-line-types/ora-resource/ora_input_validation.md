# Input Validation

Use this guidance for `Manage Purchasing Line Types`. It performs only client-side presence, type, length, format, and supplied-value checks. It does not perform live lookups, duplicate checks, business-object schema discovery, or REST calls. The Data Loader business object and the approved REST execution own those validations.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Create identity | LineType, LineTypeCode, LineTypeDescription | Stop before preview | Provide all three nonblank values | Create | |
| Update identity | LineTypeId and one intended mutable field | Stop before preview | Provide the supplied identity and requested change; the Data Loader or REST execution resolves the record | Update | |
| List filter | LineTypeContains | Stop client-side validation | Provide a nonblank text fragment; an approved read route performs any retrieval | Read-only list | |
| Purchasing basis | `PurchaseBasisCode` or `PurchaseBasis` when explicitly supplied | Stop before preview | Require nonblank text only; the Data Loader business object validates lookup membership | Create with an explicit purchase basis | |
| Flexfield context | DFF values and their intended parent identity | Stop the DFF portion before preview | Require a nonblank parent linkage. The Data Loader converter derives a deployed global context from its DFF header and does not write its display value to the technical `__FLEX_Context` field; the business object resolves the remaining DFF attributes and context. | DFF is supplied | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| LineType is a string of at most 30 characters | Reject a missing or oversized value | Create | |
| LineTypeCode is a string of at most 30 characters and does not start with ORA_ | Reject a missing, oversized, or reserved-prefix value | Create | |
| LineTypeDescription is a string of at most 240 characters | Reject a missing or oversized value | Create | |
| Line type and code uniqueness | Do not call a live lookup; preserve the supplied values and let the Data Loader business object reject duplicates | Create | |
| CreditLineFlag is blank or boolean text | Reject a supplied value other than true or false | Create or update where allowed | |
| DefaultReceiptCloseTolerancePercent is numeric and from 0 through 100 | Reject a nonnumeric or out-of-range value | Create; update when CreditLineFlag is false | |
| DefaultUOMCode is at most 3 characters | Reject an oversized value | Create or update where purchase basis permits a UOM | |
| EndDate is a valid `YYYY-MM-DD` date | Reject a missing, malformed, or calendar-invalid value | Create or update where the record is not seeded | |
| DFF parent linkage is nonblank when a DFF row is supplied | Reject a DFF row with no parent identity; the Data Loader business object validates DFF attributes, context, and segment shape | DFF is supplied | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Update | The LineTypeId and a mutable field are supplied | Continue to defaults and client-side design enforcement; the Data Loader or REST execution resolves the record | |
| Update | The LineTypeId or requested change is absent | Stop and correct the client input | |
| Create | No existing item lookup is needed to address an item | Continue to defaults and design enforcement | |
| Read-only list | LineTypeContains is nonblank | Complete client-side validation only; an approved read route performs any retrieval | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PLT.VALIDATE_INPUT | step | 10 | validate_input | valid_create_or_update->PLT.APPLY_DEFAULTS;valid_list->PLT.DONE_LIST;invalid->RETURN_ISSUES | none | stop | Every create, update, or read-only list request |
