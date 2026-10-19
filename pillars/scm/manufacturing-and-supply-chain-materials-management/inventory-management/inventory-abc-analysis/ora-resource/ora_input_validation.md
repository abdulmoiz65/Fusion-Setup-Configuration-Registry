# Inventory ABC Analysis Input Validation

## Source Evidence

| Source | Used For |
|---|---|
| Redwood ABC Analysis classification sets page and standard lookup action chains | Confirms Meaning is the friendly display value and LookupCode is the canonical value for item scope and compile type |
| User-approved resolver contracts | Limits task-local friendly-value resolution to item scope and compile type |
| Live Data Loader metadata for abcClasses, abcClassifications, and abcAssignmentGroups | Confirms user-settable business-date fields and that ABC Assignment Groups exposes only backend-managed audit dates |

## Scope Boundary

| Boundary | What Happens |
|---|---|
| Local validation ownership | Resolve only approved friendly values for ContentScopeCode and CompileTypeCode before Data Loader handoff |
| Backend-owned validation | Data Loader and Fusion own required fields, keys, lengths, uniqueness, server-side domains, cross-record rules, and final field enforcement |
| REST execution | Do not create direct REST write guidance; core.data-loader owns execution |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Item scope input | Resolve every supplied item-scope code or friendly value against the approved lookup and fill ContentScopeCode from the single matched row | abcClassifications input includes an item-scope representation | item_scope_lookup |
| Compile type input | Resolve every supplied compile-type code or friendly value against the approved lookup and fill CompileTypeCode from the single matched row | abcClassifications input includes a compile-type representation | compile_type_lookup |
| Conflicting code and friendly value | Stop when supplied code and friendly values resolve to different lookup rows | Both representations are supplied for the same field |  |

## Date Format Validation

| Field | Required Format | What Happens | Applies When |
|---|---|---|---|
| abcClasses.EnableDate | YYYY-MM-DD | Accept only a zero-padded four-digit year, two-digit month, and two-digit day; preserve blank for the approved default | A value is supplied |
| abcClasses.DisableDate | YYYY-MM-DD | Accept only a zero-padded four-digit year, two-digit month, and two-digit day; preserve blank | A value is supplied |
| abcClassifications.CompileDate | YYYY-MM-DD | Accept only a zero-padded four-digit year, two-digit month, and two-digit day; preserve blank | A value is supplied |
| abcClassifications.StartDate | YYYY-MM-DD | Accept only a zero-padded four-digit year, two-digit month, and two-digit day; preserve blank | A value is supplied |
| abcClassifications.EndDate | YYYY-MM-DD | Accept only a zero-padded four-digit year, two-digit month, and two-digit day; preserve blank | A value is supplied |

## Date Validation Rules

| Rule | What Happens |
|---|---|
| Format match | Match the supplied value exactly to YYYY-MM-DD; do not accept locale-specific dates, timestamps, or implicit conversions |
| Blank value | Preserve the blank value unless the approved abcClasses.EnableDate default applies |
| Invalid format | Stop before Data Loader handoff and identify the field and required format |
| Audit dates | Do not locally validate CreationDate or LastUpdateDate fields; Data Loader and Fusion own backend-managed audit values |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ABC.VALIDATE_INPUT | step | 10 | validate_input | valid->ABC.APPLY_DEFAULT;invalid->ABC.HANDLE_ERROR | none | stop | Before Data Loader preparation, evaluate approved lookup representations and all user-settable business-date formats |
