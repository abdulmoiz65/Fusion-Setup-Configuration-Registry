# Manage Import Maps Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| FileType | Text | A create request omits FileType or supplies it as null or a whitespace-only string | No | resolve_import_map_file_type |
| Delimiter | Comma | A create request omits Delimiter or supplies it as null or a whitespace-only string | No | resolve_import_map_delimiter |
| EncodingType | UTF_8 | A create request omits EncodingType or supplies it as null or a whitespace-only string | No | resolve_import_map_encoding_type |
| DateFormat | 1/31/99 | A create request omits DateFormat or supplies it as null or a whitespace-only string | No | resolve_import_map_date_format |
| TimestampFormat | 2001-07-04T12:08:56.235-0700 | A create request omits TimestampFormat or supplies it as null or a whitespace-only string | No | resolve_import_map_timestamp_format |
| Active | true | A create request omits Active or supplies it as null or a whitespace-only string | No |  |
| External | false | A create request omits the External supplier-visible field or supplies it as null or a whitespace-only string | No |  |
| ItemClassName | ItemClass from the exact ROOT_ICC item-class response | A create request omits ItemClassName or supplies it as null or a whitespace-only string | No | resolve_root_item_class |
| Transformation SourceColumns | Current SourceColumn + $!$ + all participating source-column names joined by $&#124;$ | A REST transformation child is prepared | Yes, always derive from the current request and include the current source again in the suffix |  |
| Source IgnoreFlag | Y or N | A source child is prepared | Yes, set Y when no destination child exists; otherwise set N |  |

## Default Application Rules

| Situation | What Happens |
|---|---|
| A create request omits a defaultable field or supplies it as null or a whitespace-only string | Apply that field's documented default independently of the other fields |
| A create request supplies an explicit value | Preserve the explicit value; never replace it with a default |
| An update request omits a field or supplies no replacement value | Preserve the existing record value; never apply a create default |
| A format value is defaulted | Pass the defaulted display value to its existing exact standard-lookup resolver before Data Loader preview |
| Active or External is defaulted | Preserve the documented literal Boolean value without invoking a lookup |
| The request is a create and ItemClassName is absent, null, or whitespace-only | Resolve ROOT_ICC through resolve_root_item_class and set ItemClassName only from the matched response ItemClass value |
| An update request omits ItemClassName or supplies it as null or whitespace-only | Omit ItemClassName from the outgoing working payload so the existing Fusion value is preserved; do not replace it with null, blank, or a default |
| ItemClassName is supplied with a non-whitespace value | Preserve the supplied value and do not invoke resolve_root_item_class |
| A REST transformation child is prepared | Preserve supplied optional transformation values, retain ExpressionCode unchanged, and derive SourceColumns from the current SourceColumn followed by every participating source column in supplied order |
| A REST transformation optional value is absent | Omit the absent optional value; do not invent or default it |
| No REST transformation or expression is supplied | Do not synthesize a transformation child or any transformation-only attribute |
| A source child has no destination child | Emit IgnoreFlag Y for that source child |
| A source child has one or more destination children | Set IgnoreFlag to N for that source child, overriding any supplied value |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MIM.APPLY_DEFAULTS | step | 15 | apply_default | applied_or_not_needed->MIM.RESOLVE_ROOT_ITEM_CLASS;blocked->MIM.HANDLE_ISSUE | MIM.VALIDATE_INPUT | stop | After REST input validation and before resolving a missing create-request ItemClassName or supplied or defaulted import-map format values |
| MIM.DERIVE_TRANSFORMATION_SOURCE_COLUMNS | step | 86 | apply_default | applied_or_not_needed->MIM.DEFAULT_SOURCE_IGNORE_FLAG;blocked->MIM.HANDLE_ISSUE | MIM.RESOLVE_TRANSFORMATION_RETURN_ATTRIBUTE | stop | Derive SourceColumns and preserve supplied optional transformation values when REST transformation children are present; otherwise return not needed |
| MIM.DEFAULT_SOURCE_IGNORE_FLAG | step | 87 | apply_default | applied_or_not_needed->MIM.CHECK_LOOKUP_READINESS;blocked->MIM.HANDLE_ISSUE | MIM.DERIVE_TRANSFORMATION_SOURCE_COLUMNS | stop | After destination and transformation resolution and before REST Data Loader readiness |
