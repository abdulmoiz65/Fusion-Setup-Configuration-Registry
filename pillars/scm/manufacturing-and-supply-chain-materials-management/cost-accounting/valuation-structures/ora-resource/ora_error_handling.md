# Error Handling

## Source

| Source | Location | Used For |
|---|---|---|
| Oracle Valuation Structures | https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/valuation-structures-and-valuation-units.html | Post-transaction immutability and cost-method restrictions |
| Oracle Valuation Structure Rules | https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/valuation-structure-rules.html | Mandatory and optional attribute conflict behavior |
| FDOS Data Loader | core/data-loader/SKILL.md | Live business-object validation, immutable preview, approval, upload, and initiation routing |

## Error Situations

| Situation | What Should Happen |
|---|---|
| A required definition input is missing or invalid | Stop and request the missing identity, type, costing attributes, valuation-unit mode, or valuation structure set. Cost-profile context is not required to create the valuation structure. |
| The valuation structure type or mode has no exact standard-lookup Meaning match | Stop and request one exact valuation structure type or mode. |
| The Cost Valuation Granularity has no exact type-dependent flexfield-structure match | Stop and request an exact Cost Valuation Granularity Name valid for the resolved valuation structure type. |
| FlexFieldStructure is populated with StructureInstanceCode instead of the resolved Name | Stop before preview, populate FlexFieldStructure with the exact returned Name, and retain StructureInstanceCode only as lookup evidence. |
| A CONSIGNED valuation structure has no user-supplied mode | Default the Valuation Structure Mode Code to AUTO. |
| A CONSIGNED valuation structure has a resolved mode code other than AUTO | Stop and correct the mode to AUTO. |
| The Valuation Structure Set Name has no exact costing-set match | Stop and request one exact set name. |
| The valuation structure conflicts with inventory attributes or cost-method limits | Stop and redesign the costing attributes before any transaction uses the structure. |
| Project or Task is selected without Project-Driven Supply Chain readiness | Stop and complete the opt-in and setup, or remove Project and Task from the definition. |
| A change adds or deletes costing attributes after transactions were performed | Stop; do not make the change because Oracle documents unpredictable results. |
| A mandatory costing attribute is absent on an item | Stop association of the valuation structure to the item until the design is corrected. |
| Data Loader source or Business Object validation fails | Stop before preview, correct the source data, and revalidate it through core.data-loader. |
| Upload or initiation is requested without an immutable Data Loader approval preview and a later standalone approve | Stop before the first POST. |
| Data Loader REST submission is requested | Route the operation through core.data-loader for upload and initiation; do not construct a direct REST request. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A required definition field is missing or invalid | Correct the supplied definition. |
| Defaulting | The resolved type is CONSIGNED and no mode was supplied | Use the AUTO mode-code default. |
| Design enforcement | The resolved type is CONSIGNED and the resolved mode code is not AUTO | Correct the mode to AUTO. |
| Reference lookup | The supplied valuation structure type or mode has zero or multiple exact standard-lookup matches | Correct the type or mode; do not select a partial or first result. |
| Reference lookup | The supplied Cost Valuation Granularity has zero or multiple exact type-dependent flexfield-structure matches | Correct the granularity name; do not select a partial or first result. |
| Reference lookup | FlexFieldStructure differs from the exact returned Name or contains StructureInstanceCode | Use the returned Name for FlexFieldStructure and regenerate the source before preview. |
| Reference lookup | The supplied Valuation Structure Set Name has zero or multiple exact costing-set matches | Correct the set name; do not select a partial or first result. |
| Dependency readiness | Required flexfield, inventory-attribute, or Project-Driven Supply Chain readiness is absent | Complete the prerequisite setup and revalidate. |
| Design enforcement | The definition violates granularity, cost-method, mandatory-attribute, or processed-history rules | Redesign without changing processed history. |
| Data Loader validation | The source or costAccountingValuationStructures Business Object does not pass Data Loader validation | Correct the source data and generate a new immutable approval preview. |
| Approval blocker | Upload or initiation is requested without a current immutable approval preview and later standalone approve | Stop before upload; obtain a new preview and then send approve in a separate message. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation, dependency, or design failure | The affected Valuation Structure input, violated rule, and corrective action. |
| Data Loader validation failure | The affected source data, validation result, and corrective action. |
| Data Loader approval gate | The immutable preview and required standalone approve action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Processed valuation structure | Do not add or delete costing attributes. |
| Data Loader validation or approval gate is incomplete | Do not upload, initiate, retry, or construct a direct REST request. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| VS.COMPLETE | terminal | 9 | terminal | none | VS.ENFORCE_DESIGN | stop | Task-local Valuation Structure validation and readiness checks completed |
| VS.HANDLE_ISSUE | step | 10 | error_handler | disclosed->RETURN_ISSUES | none | stop | A prior node reports invalid, blocked, or failed |
| RETURN_ISSUES | terminal | 11 | terminal | none | none | stop | Error disclosure completed |
