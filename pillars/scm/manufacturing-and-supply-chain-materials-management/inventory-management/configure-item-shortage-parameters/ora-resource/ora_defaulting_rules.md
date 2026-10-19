# Configure Item Shortage Parameters Defaulting Rules

## Source Evidence

| Source | Used For |
|---|---|
| Source Provenance in this resource | Pins the parameter-context-to-RuleType mapping and Module default to exact Redwood source artifacts, digests, and line ranges |

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| RuleType | ITEM_CATEGORY | The Item Shortage Parameter context is Category | No; reject a supplied conflicting RuleType | |
| RuleType | SHORTAGE_THRESHOLD | The Item Shortage Parameter context is Shortage threshold | No; reject a supplied conflicting RuleType | |
| RuleType | AVERAGE_DEMAND_PERIOD | The Item Shortage Parameter context is Average demand period | No; reject a supplied conflicting RuleType | |
| RuleType | OPEN_SUPPLY_PERIOD | The Item Shortage Parameter context is Open supply period | No; reject a supplied conflicting RuleType | |
| RuleType | OPEN_DEMAND_PERIOD | The Item Shortage Parameter context is Open demand period | No; reject a supplied conflicting RuleType | |
| RuleType | SHORTAGE_THRESHOLD_FOR_KANBAN | The Item Shortage Parameter context is Shortage Threshold for Kanban | No; reject a supplied conflicting RuleType; retain the feature applicability gate | |
| Module | SHORTAGE | A ruleConfigurationHeaders header is prepared and Module is omitted | No; reject an explicit value other than SHORTAGE | |

## Defaulting Rules

| Situation | What Happens |
|---|---|
| A recognized Item Shortage Parameter context is supplied without RuleType | Fill RuleType from the exact approved context mapping before Data Loader preparation |
| RuleType is supplied with a recognized Item Shortage Parameter context | Continue only when it equals the mapping for that context; reject a conflict |
| Module is omitted | Fill Module with SHORTAGE before Data Loader preparation |
| Module is supplied | Continue only when it equals SHORTAGE; reject any other value |
| The context is not one of the approved values | Do not infer RuleType; stop and request one approved context value |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ISP.APPLY_CONTEXT_DEFAULTS | step | 10 | apply_default | applied->ISP.VALIDATE_INPUT;blocked->ISP.HANDLE_ERROR | none | stop | Before validating a ruleConfigurationHeaders header for Data Loader preparation |
