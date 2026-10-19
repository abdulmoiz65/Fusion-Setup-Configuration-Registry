# Shipping Exceptions Input Validation

Source: Shipping Exceptions Redwood page, dynamic layout, and approved task-authoring contract.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Exception Type identity | ExceptionType or ExceptionTypeCode | Stop before Data Loader handoff | Supply an exact Type meaning, an exact Type code, or both matching values. | A Type is supplied | resolve_shipping_exception_type_code |
| Exception Severity identity | ExceptionSeverity or ExceptionSeverityCode | Stop before Data Loader handoff | Supply an exact Severity meaning, an exact Severity code, or both matching values. | A Severity is supplied | resolve_shipping_exception_severity_code |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Type meaning and code | Accept ExceptionType, ExceptionTypeCode, or both. When both are supplied, require the same single Type lookup row. | Type input is supplied | resolve_shipping_exception_type_code |
| Severity meaning and code | Accept ExceptionSeverity, ExceptionSeverityCode, or both. When both are supplied, require the same single Severity lookup row. | Severity input is supplied | resolve_shipping_exception_severity_code |
| Active flag normalization | Accept only true or false and retain the Boolean value for ActiveFlag. Do not apply the Redwood creation default when the input is blank. | ActiveFlag is supplied | |
| Backend-owned attributes | Do not derive ExceptionCode, RestAction, audit attributes, ExceptionDefinitionId, PredefinedFlag, or DFF values locally. Current Data Loader metadata and Fusion own their validation and required-value behavior. | Any of these attributes is absent or supplied | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SE.VALIDATE_INPUT | step | 10 | validate_input | passed->SE.RESOLVE_TYPE;failed->RETURN_ISSUES | none | stop | Shipping Exceptions input is prepared for validation or Data Loader handoff |
