# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? |
|---|---|---|---|
| job_definition_id | JobDefinition://oracle/apps/ess/cdm/foundation/geographies/HZ-HZGEOCODER | Every new submission | No |
| application | CrmEss | Every new submission | No |
| regenerate_geocode | N | The parameter is omitted | Do not inject it for a fully parameterless request; use an explicit user value when supplied |
| batch_size | 50 | The parameter is omitted | Do not inject it for a fully parameterless request; accept an explicit value up to 100 |
| batch_size | 100 | The supplied value is greater than 100 | Yes, cap at 100 and disclose it in preview |
| wait_seconds | 300 | The caller omits a polling window | Yes, accept another positive bounded value |
| poll_interval | 10 | The caller omits a polling interval | Yes, accept another positive value not greater than wait_seconds |
| ESS retries | 0 | Every new submission | No automatic retry |
| request parameter type | STRING | Any geocode parameter is sent | No |

## Parameter Position Defaults

| Position | Technical Name | Business Parameter | Omitted Value When A Later Position Is Supplied |
|---|---|---|---|
| 1 | submit.argument1 | Country Code | Empty string |
| 2 | submit.argument2 | Start Date | Empty string |
| 3 | submit.argument3 | End Date | Empty string |
| 4 | submit.argument4 | Regenerate Geocode | Empty string, allowing the process default N |
| 5 | submit.argument5 | Batch Size | Omit when trailing; empty string only when required to preserve a later position |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GEOCODE.DEFAULTS | step | 3 | apply_default | ok->GEOCODE.READINESS;failure->GEOCODE.FAILED | GEOCODE.VALIDATE | stop | Normalize parameter values, effective defaults, polling options, and the fixed ESS job contract |
