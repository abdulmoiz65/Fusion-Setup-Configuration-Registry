# Defaulting Rules

Defaults are reference values only. Never overwrite a user value or silently restore a default.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| ORA_ZCQ_MAX_CANDIDATES | 20 | User explicitly requests the documented default and the live definition confirms SITE eligibility | No | read_cdm_option_definition |
| ORA_ZCQ_BATCHMATCH_DEBUG_LEVEL | INFO | User explicitly requests the documented default and the live definition confirms SITE eligibility | No | read_cdm_option_definition |
| ORA_ZCQ_CONVERTER_FINEST_LOGGING | N | User explicitly requests the documented default and the live definition confirms SITE eligibility | No | read_cdm_option_definition |
| ORA_ZCH_MERGE_MAX_REQUEST_LIMIT | 10 | User explicitly requests the documented default and accepts its concurrency effect | No | read_cdm_option_definition |
| ORA_ZCH_MERGE_REQUEST_BATCH_SIZE_LIMIT | 100 | User explicitly requests the documented default and accepts its batching effect | No | read_cdm_option_definition |
| ZCH_AUTO_LINK_THRESHOLD | 0 | User explicitly requests the documented default and accepts that automatic linking is effectively disabled | No | read_cdm_option_definition |
| ZCH_AUTO_MERGE_THRESHOLD | 100 | User explicitly requests the documented default and accepts the match-score effect | No | read_cdm_option_definition |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CDMO.APPLY_DEFAULT | decision | 5 | apply_default | applied->CDMO.DESIGN_GATE;not_applicable->CDMO.DESIGN_GATE;blocked->CDMO.ERROR | CDMO.DEPENDENCY_READINESS | stop | Apply a documented default only when explicitly requested; otherwise take not_applicable |
