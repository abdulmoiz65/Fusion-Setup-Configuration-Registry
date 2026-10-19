# RMCS Groovy and Function Guidance

Read after [input preflight and action selection](ora_algorithm_xml_guidance.md). This file owns existing-code handling, action-local cardinality, RMCS Groovy layout, runtime/helper policy, function-backed source use and conflicting-output review. Output-field eligibility and insertion contexts belong only to the [data-model guide](ora_rmcs_data_model_reference.md).

## Existing action handling

Determine active Groovy with comment-aware lexical inspection: ignore // line comments and /* ... */ block comments, but preserve comment-looking text inside quoted, multiline or slashy strings. If uncertain whether text is code or a string/comment, request clarification; do not use a destructive regex to rewrite it.

- If the selected action contains only the delivered commented sample and no active code, omit that sample from the proposed new expression.
- If it contains active code, ask whether to replace it or place the new logic above it, and ask separately whether formatting is allowed. Preserve existing behavior unless its change is approved.
- If asked to copy from another version, treat the named source as read-only and propose copying into the eligible highest version only. Ask about formatting. If formatting is declined, preserve copied code verbatim and append the new documented logic after it.
- If copied code would overwrite active target code, resolve that collision explicitly; a copy request does not silently choose between two customizations.
- Show all retained and new code together for approval. If exact preservation conflicts with mandatory section layout, explain the conflict and obtain a layout decision before editing. Do not silently reformat retained customer code.

Existing commented examples do not prove a custom attribute exists or that a function is safe to call. Existing customer code is not authority to repeat a defect in new logic.

## Cardinality and source ownership

Before drafting, read every action-local dataset's contain/cardinality declaration or equivalent XML row using the [scope-map rules](ora_algorithm_xml_guidance.md#select-the-action-by-structure). Resolve the actual alias; do not hardcode the source owner from an example.

Every business source used by new Groovy must have the companion-owned [source-resolution record](../../manage-service-mappings-for-subscriptions-to-revenue-recognition/resources/ora_service_mapping_guidance.md#source-resolution-record). Consume its accepted source and type evidence; do not treat a sole semantic match, a copied example or a generic assumption as source acceptance. Keep that record canonical rather than creating a second source-decision schema here.

| Resolved binding | New Groovy requirement |
|---|---|
| ZeroOrOne / ZERO_OR_ONE | Use alias?.property for every direct access in conditions, calculations, function arguments and RMCSInterface.insert values |
| One / ONE | Direct property access is permitted |
| Many / MANY collection | Define an explicit iteration, aggregation or user-approved selection rule; never treat a collection as a scalar or silently select the first item |
| Confirmed primary or nested-action current row | Use its established current-row alias for that action; do not infer a scalar binding for other MANY datasets |
| Missing, conflicting or unknown | Stop and obtain cardinality/binding evidence |

An explicit non-null guard does not permit a later unsafe optional-alias dereference. A local value obtained with null-safe access may be used afterward, with its null behavior handled. Chained method calls, substring ranges, numeric conversions and optional function arguments also need explicit null/type/range behavior; ?. on the first property alone is not a guarantee that later calls are safe.

Retain the functional owner selected by the implementer. Do not switch to a same-name attribute on a required or primary object just to avoid optionality. Business literals, null defaults, rounding, concatenation and aggregation must come from the requirement or an accepted decision.

For the header action, input values may come only from Subscription or HeaderSalesCredits. Other available datasets do not authorize header calculations from Products, Charges, BillLines or ProductAssociations. The established RmcsDoc current row still supplies the output identity and existing target/control values. HeaderSalesCredits collection semantics must be resolved, not guessed.

For line/subline actions, use only providers and bindings actually available in the selected action. In the inspected form, Charges and ProductAssociations are optional; Subscription and Products are ONE; BillLines and sales-credit datasets are MANY. Those are inspection findings, not substitutes for the current request's metadata. Do not rewrite existing provider/join expressions merely to normalize their spelling; separately proposed provider changes require structural approval.

## Runtime constructs and helper policy

Choose a construct because it implements the accepted business rule and is supported for this RMCS algorithm, not because it appears in the AR guide or a historical example.

| Category | Permitted use and evidence boundary |
|---|---|
| Ordinary Groovy constructs | Literals, verified property access, comparisons, Boolean conditions and if/else may express the accepted rule; retain the cardinality, type and null requirements above |
| RMCSInterface.insert | Only the header/line output operation defined by the [RMCS output contract](ora_rmcs_data_model_reference.md#header-and-line-insert-contract); a map literal does not authorize another API or a subline insert |
| Algorithm-defined VO lookup functions | Resolve the selected version's function and consuming dataset using [function-backed sources](#function-backed-sources); a declared lookup does not establish unrelated runtime helpers |
| Platform/runtime helpers and conversions | Require RMCS-specific availability, signature, input/output types and relevant null/error behavior; apply the explicit DATE/timestamp rule below and keep other unproven helpers unresolved. The RMCS skill-level date rule permits `toDate` for DATE values and `today()` for current-date DATE comparisons; timestamp current-time comparisons use `now()` |

Do not generate dynamic evaluation or runtime-composed code, external-service/network invocation, file/process operations, Executor calls, arbitrary row-set insertion/deletion, or other unsupported mutating APIs. These exclusions do not prohibit the specifically supported RMCS output insert or an approved assignment to an existing writable output. A helper name appearing in retained code or the AR reference is not sufficient evidence for newly generated use.

Use a nontrivial string/date/number helper only after its supported behavior is established. A Boolean or identifier label does not establish a conversion. Do not invent fallback values, locale/time-zone behavior, rounding precision or current-time semantics. If a required helper remains unsupported, return the precise evidence gap to the primary without substituting another function. Supported diagnostic logging must omit customer values, business payloads, identifiers and secrets; do not add logging merely to inspect data.

### DATE and timestamp value handling

Resolve the accepted source/expression type, target type, intended context and null behavior before selecting a conversion. The user's RMCS-specific value rule is:

| Confirmed value kind | Proposed value expression |
|---|---|
| DATE field value used as an assigned/inserted value | `toDate(<date field value>)`, used as the value for the supported insert or mapped assignment |
| DATE field value or DATE-derived expression used in a comparison | Compare the converted DATE expression, for example `toDate(<derived date value>) > today()` when the business rule means later than the present date |
| TIMESTAMP field value or timestamp expression, including an applicable `now()` | Preserve the timestamp expression without a `toDate` wrapper; timestamp comparisons may compare to `now()` when the business rule means current timestamp |
| String, numeric, ambiguous or incompatible value | Obtain the required RMCS conversion/type contract; do not classify it as DATE from its label or cast it by analogy with AR |

The DATE rule supplies the named `toDate` contract for DATE values and `today()` as the current-date comparator for this workflow; it is not a general approval for other platform helpers or arbitrary string-to-date parsing. Preserve approved date arithmetic inside the date-value expression only when the operations and resulting type are supported. For an optional source, keep every dereference null-safe and establish whether null should suppress the write, produce an allowed null or use an explicitly accepted fallback; do not assume `toDate` accepts null.

Do not turn a timestamp into a DATE merely because the physical target is named with a date suffix. If the implementer identifies a source as TIMESTAMP, keep it unwrapped and compare it to `now()` only when runtime-current timestamp is the accepted business value and RMCS runtime availability is established. If the type is DATE or an accepted assumption says DATE, use `toDate(<derived date value>)` before comparing, and compare to `today()` for present-date checks. Do not replace an effective, transaction or accounting date with current time. Number/date conversions beyond the explicit rule still require RMCS-specific evidence.

## Mandatory layout

Every proposed selected ActionExpression must contain these exact section comments, each followed by a blank line even if its section has no statements:

```groovy
/* Sending additional details to the Revenue Recognition */

/* Modifying the values Present in  Service Mapping */

```

Put eligible header/line RMCSInterface.insert([ ... ]) calls in the first section. Immediately precede each insert with exactly one concise one-line /* ... */ comment describing that insertion only. Do not paste a generic repeated explanation or a stack of comments before each insertion.

Put assignments to existing mapped output attributes in the second section. A confirmed writable same-row output can be a single assignment when the accepted rule needs only that value movement; add conditionals, null guards, conversions or collection handling only when the source evidence or requirement requires them. Conditions and supporting calculations stay with the operation they serve. In a subline expression the first section remains present but contains no insert. Do not infer an empty section means an operation has been approved.

Use = for assignments; == is a comparison. The prompt's date example containing == is not assignment syntax. Do not silently repair that or other retained customer code without approval. Preserve actual alias/attribute casing; placeholders in these guides are not executable Groovy.

## Function-backed sources

ProductAssociations and BillLines can be supplied by algorithm VIEW_OBJECT_LOOKUP functions, not Service Mapping entities. Absence from active mapping XML alone is not an exposure failure and does not require a _Custom alias. XML comments mentioning those entities do not activate them.

Inspect the selected version's FunctionSetup/FunctionSetupVORow, FunctionArgSetup/FunctionArgSetupVORow, VOQuerySetup/VOQuerySetupVORow and BindVarSetup/BindVarSetupVORow, and the consuming StepSetSetup rows. Verify function spelling, argument, VO, criterion, bind, caller path, type and cardinality before proposing a provider change.

| Function seen in the supplied exports | Argument | VO / criterion | Bind |
|---|---|---|---|
| filterPAbyCoveredLevelId | coveredLevelId | PricingAssociations / ByCoveredLevelIdVC | bindCoveredLevelId=coveredLevelId |
| filterPAbyProductId | productId | PricingAssociations / findByProductIdVC | bindProductId=productId |
| filterBillLinesbyChargeId | chargeId | BillLinesVO / FilterByChargeIdVC | bindChargeId=chargeId |
| filterBillLinesbyProductId | productId | BillLinesVO / FilterByProductIdVC | bindProductId=productId |

In both inspected exports, filterPAbyCoveredLevelId(Charges.ProductAssociationId) is already bound to ProductAssociations with ZERO_OR_ONE, and filterBillLinesbyChargeId(Charges.ChargeId) is already bound to BillLines with MANY. The prompt's claim that the latter is unbound does not match the exports. Check the current version instead of adding duplicate datasets.

The product-level functions are available but not bound in those examples. Product-level associations and product-/charge-level bill lines can have multiple rows; require collection handling when selecting them. Null ReturnType, ArgType and SingleRowFlag in the inspected function metadata do not establish scalar return types. A replacement function needs verified result cardinality in its consuming dataset; never copy ZERO_OR_ONE from a different lookup.

A supported dataset/provider argument may use a real VO attribute without inventing a Service Mapping custom field for that algorithm-only provider. For example, an evidenced function-backed value such as BillLines.Amount can be referenced through the selected BillLines dataset when its function binding, cardinality, type and null behavior are verified; it does not first need a Service Mapping entity definition. This does not waive source-type evidence, caller scope or join requirements. Use the companion's [describe discovery route](../../manage-service-mappings-for-subscriptions-to-revenue-recognition/resources/ora_service_mapping_guidance.md) for metadata questions, then return the findings to the primary for computation/provider decisions. Do not build a second REST/auth client in this skill.

## Conflicting output review

Review retained and proposed logic together before requesting approval. Textually different aliases or routes can address the same semantic target; two actions can also affect the same record. Use the accepted source/target bindings to compare operations, not attribute spelling alone.

1. Identify each operation's selected action/current-row scope, semantic and physical target, actual mapped output alias where applicable, SourceId and TransactionType for inserts, and relevant attribute/flex contexts. Use the [final traceability matrix](ora_use_case_resolution.md#final-traceability-and-configuration-handoff) as the operation inventory, not a second competing schema.
2. Check whether retained and proposed conditions can overlap for that record and target. Include repeated inserts, repeated assignments, alias-equivalent direct-write/insert attempts, competing context values and skip/reset branches. Different record levels or demonstrably disjoint predicates are not conflicts merely because column names match.
3. For competing writes, require accepted mutually exclusive conditions or an explicitly supported RMCS precedence decision. Separate independent conditions are appropriate only when both operations can validly apply together. Never assume first-write-wins or last-write-wins from script order, insert order or AR behavior.
4. If target equivalence, predicate overlap or precedence cannot be established, report the precise collision and request the missing evidence or a business decision. Do not silently drop an operation, alter a context or rewrite retained customer logic. Any changed expression returns through the [approval procedure](ora_algorithm_xml_guidance.md#approval-and-local-artifact).

This is an ambiguity and proposal-review gate, not a new RMCS runtime rule about the number of FlexContexts permitted. Existing output-access and no-subline-insert restrictions still apply even if the implementer accepts a proposed precedence.

## Proposal checks

Before asking for approval, check the canonical source-resolution decisions, exact section layout, one insertion comment per insert, optional access throughout new logic, explicit collection/null behavior, supported runtime helpers and DATE/timestamp handling, header source restrictions, actual writable output names, correct record-level identity, resolved output collisions and no subline insert. Reconcile the complete expression with the [final traceability and configuration handoff](ora_use_case_resolution.md#final-traceability-and-configuration-handoff), then use the canonical [approval procedure](ora_algorithm_xml_guidance.md#approval-and-local-artifact). Report what was checked statically; do not claim the Groovy ran in Fusion.
