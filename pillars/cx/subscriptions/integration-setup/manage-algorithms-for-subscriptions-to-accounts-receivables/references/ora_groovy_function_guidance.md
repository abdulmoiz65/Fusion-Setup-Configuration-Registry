# Groovy Function Guidance

## Baseline Language Constructs

Use simple Groovy expressions only when they directly implement the approved business rule.

| Construct | Advisory Use |
|---|---|
| String, number, Boolean, and null literals | Hard-coded business values that the implementer explicitly supplies |
| Property access | Read a seeded or service-mapped attribute, for example Products.ProductName_Custom |
| Map literal | Construct the ARInterface.insert argument map only |
| Comparison and Boolean operators | Test a supplied business condition, including equality, inequality, logical-and, and logical-or |
| if / else | Select mutually exclusive transaction, origin, or flex-context logic |

## Conditional Flow

The legacy guide documents if / else conditional flow. Use it to make business conditions explicit, including selecting invoice-only or credit-memo-only logic and mutually exclusive DFF contexts. For one DFF attribute context, branches must ensure that only one FlexContext executes for a bill line at runtime.

Resolve the transaction class expression from the current Service Mapping XML before drafting any invoice or credit-memo scoped insert. Find the context entity attribute mapping whose `viewObjectAttribute` is `TransactionClass`, then use the exposed Service Mapping alias and attribute name in Groovy. Do not assume the Groovy attribute is named `TransactionClass_Custom`: for example, if the current XML maps `viewObjectAttribute="TransactionClass"` to `attributeName="TransactionType_Custom"` under `BillLines`, the expression is `BillLines.TransactionType_Custom`.

When the same `ARInterface.insert` applies to both invoice and credit memo lines, place it under the "both invoice and credit memo lines" section with no `if` condition and set `TransactionType` to the resolved transaction-class expression:

```groovy
/* Maps an approved source to both invoice and credit memo lines. */
ARInterface.insert([
  AttributeName: '<confirmed_target_name>',
  AttributeValue: <confirmed_source_or_expression>,
  AttributeContext: '<confirmed_attribute_context>',
  FlexContext: '<confirmed_flex_context_when_required>',
  TransactionType: <resolved_transaction_class_alias>
])
```

When an insert is invoice-only or credit-memo-only, guard it with the resolved transaction-class expression. Use mutually exclusive `if` / `else if` branches when the branches are alternatives for the same target, transaction origin, or flex context:

```groovy
if (<resolved_transaction_class_alias> == 'INV') {
  // Invoice-only ARInterface.insert logic
} else if (<resolved_transaction_class_alias> == 'CM') {
  // Credit-memo-only ARInterface.insert logic
}
```

Use separate `if` statements only when the blocks are independent and can validly run apart from each other. Do not hardcode `TransactionType: 'INV'` and `TransactionType: 'CM'` to duplicate the same mapping when the requirement is for both invoice and credit memo lines; use `TransactionType: <resolved_transaction_class_alias>` once instead.

## Contained Entity Cardinality

Read each `contain(...).cardinality(...)` declaration on the selected action before using an alias. For a `ZeroOrOne` alias, generated Groovy must use null-safe navigation for every direct property access:

```groovy
if (<optional_alias>?.<attribute> == <expected_value>) {
  // Conditional logic using the optional value
}
```

An explicit non-null guard may still be used to control whether a block runs, but the guarded block must continue to use `?.` for every direct dereference of that optional alias. Do not write `<optional_alias>.<attribute>` later in the block. The only exception is to assign the null-safe expression to a local variable and then use the local variable:

```groovy
def optionalValue = <optional_alias>?.<attribute>
if (optionalValue != null) {
  // Use optionalValue, not <optional_alias>.<attribute>
}
```

Direct property access is permitted only after the selected action confirms the alias has cardinality `One`, or when using a local variable derived from a null-safe optional alias. Do not hardcode entity names in this guidance; derive aliases and their required handling from the selected action. Stop and request clarification when the selected action does not declare or does not clearly identify an alias cardinality.

When source resolution selects a functional owner whose selected-action cardinality is `ZeroOrOne`, keep that owner in the Groovy and make the access safe. Do not switch to another described same-name candidate from a required or primary source family just to avoid null-safe navigation. For example only, if a detail-owned business term is accepted from an optional detail alias, conditions should use the optional alias with `?.` rather than a copied line-level candidate unless the implementer explicitly selected the line-level source.

## AR Interface Insert Contracts

Use a map literal only for the approved insert contract. A normal AR target mapping contains the current request's confirmed target name, value, context, optional DFF flex context, and transaction scope. Do not add unconfirmed metadata keys.

Use the Standard shape only when the public Oracle `RA_INTERFACE_LINES_ALL` reference confirms the physical target and the current interface contract confirms it is Standard. Omit `FlexContext`. When the confirmed physical target has the RA catalog data type `DATE`, set `AttributeValue` to `toDate(<date_expression>)` and keep any requested date arithmetic inside `<date_expression>`:

```groovy
/* Maps an approved source to a standard AR interface target. */
ARInterface.insert([
  AttributeName: '<confirmed_target_name>',
  AttributeValue: <confirmed_source_or_expression>,
  AttributeContext: 'Standard',
  TransactionType: <resolved_transaction_class_alias_or_confirmed_literal_for_single_scope>
])
```

Use the interface-line DFF shape only when the public Oracle `RA_INTERFACE_LINES_ALL` reference confirms the physical target and the current interface contract identifies it as an interface-line DFF:

```groovy
/* Maps an approved source to an AR interface-line DFF attribute. */
ARInterface.insert([
  AttributeName: '<confirmed_target_from_ra_interface_lines_reference>',
  AttributeValue: <confirmed_source_or_expression>,
  AttributeContext: 'TransactionInterfaceLineDff',
  FlexContext: '<confirmed_deployed_interface_line_dff_context>',
  TransactionType: <resolved_transaction_class_alias_or_confirmed_literal_for_single_scope>
])
```

Before using this shape, resolve the `INTERFACE_LINE_ATTRIBUTE<n>` segment index and apply the interface-line reservation predicate in [RA Interface Lines Target Reference](ora_ra_interface_lines_all_reference.md): reject `n` in `1..4` for `Subscriptions Context`, and reject `n` in `1..8` for `ORA_DOO_ORIGIN_SUBSCRIPTIONS`.

Use the regular line-DFF shape when the current interface contract identifies a physical `ATTRIBUTE*` or `ATTRIBUTE_DATE*` target as `TransactionLineDff`:

```groovy
/* Maps an approved source to an AR regular line DFF attribute. */
ARInterface.insert([
  AttributeName: '<confirmed_ATTRIBUTE_target>',
  AttributeValue: <confirmed_source_or_expression>,
  AttributeContext: 'TransactionLineDff',
  FlexContext: '<confirmed_deployed_line_dff_context>',
  TransactionType: <resolved_transaction_class_alias_or_confirmed_literal_for_single_scope>
])
```

Use the transaction-header DFF shape only when the public Oracle `RA_INTERFACE_LINES_ALL` reference confirms a physical `HEADER_ATTRIBUTE*` target and the current interface contract identifies it as `TransactionInterfaceHeaderDff`. For this context, strip only the leading `HEADER_` prefix from the physical column when setting `AttributeName`:

```groovy
/* Maps an approved source to an AR transaction-header DFF attribute. */
ARInterface.insert([
  AttributeName: '<ATTRIBUTE5_or_ATTRIBUTE_DATE1_or_ATTRIBUTE_NUMBER1>',
  AttributeValue: <confirmed_source_or_expression>,
  AttributeContext: 'TransactionInterfaceHeaderDff',
  FlexContext: '<confirmed_deployed_transaction_header_dff_context>',
  TransactionType: <resolved_transaction_class_alias_or_confirmed_literal_for_single_scope>
])
```

Examples: physical `HEADER_ATTRIBUTE5` becomes `AttributeName: 'ATTRIBUTE5'`; physical `HEADER_ATTRIBUTE_DATE1` becomes `AttributeName: 'ATTRIBUTE_DATE1'`; physical `HEADER_ATTRIBUTE_NUMBER1` becomes `AttributeName: 'ATTRIBUTE_NUMBER1'`. Do not use `HEADER_ATTRIBUTE*` as the `AttributeName` for `TransactionInterfaceHeaderDff` unless the current interface contract explicitly overrides this rule.

Use the DFF shape only when the current request confirms a DFF target and its deployed context code:

```groovy
/* Maps an approved source to an AR descriptive flexfield target. */
ARInterface.insert([
  AttributeName: '<confirmed_dff_attribute_name>',
  AttributeValue: <confirmed_source_or_expression>,
  AttributeContext: '<confirmed_dff_attribute_context>',
  FlexContext: '<confirmed_deployed_flex_context>',
  TransactionType: <resolved_transaction_class_alias_or_confirmed_literal_for_single_scope>
])
```

## Date Target Conversion

For every confirmed Receivables target whose physical RA catalog type is `DATE`, use this shape in the insert map:

```groovy
AttributeValue: toDate(<date_expression>)
```

Keep a required offset inside the expression, for example `toDate(BillLines.CompletionDate_Custom + 1)` or `toDate(today() + 5)`. Do not omit `toDate(...)` merely because the source alias has a date-oriented name or the business rule describes a date. The exception is a confirmed `now()` value: map it directly as `AttributeValue: now()` and do not use `toDate(now())`.

When the current inputs confirm the Subscription AR skip-line control, include `TransactionType`; do not rely on a default. Resolve the transaction class expression from the current Service Mapping XML. If the skip applies to both invoice and credit memo lines, use the resolved expression, for example `BillLines.TransactionType_Custom`. If the skip is invoice-only or credit-memo-only, use a mutually exclusive guard from the resolved expression and set the matching transaction type. Keep the business condition outside the map:

```groovy
if (<approved_skip_condition>) {
  /* Marks the current bill line to be skipped by Subscription AR integration. */
  ARInterface.insert([
    AttributeName: 'SkipBillLines',
    AttributeValue: 'true',
    AttributeContext: 'SubscriptionsSetup',
    TransactionType: <resolved_transaction_class_alias_or_confirmed_literal_for_single_scope>
  ])
}
```

Do not add `FlexContext`, `XsiType`, or `AttributeType` to the skip control. Do not infer the skip condition, source alias, transaction scope, or a replacement Bill Lines property write from this control pattern.

## Document-Reported Helper Functions

The attached legacy Set Transform technical guide reports the following helper functions. They are permitted in an advisory sample only when the business requirement needs them and the implementer confirms they are available in the target Customization Enabled algorithm runtime. Do not present this historical document as proof that a helper is enabled in every Fusion runtime.

| Helper | Intended Use | Advisory Constraint |
|---|---|---|
| ifNull(value1, value2, ...) | Return the first non-null value | Use for an explicit fallback source only; do not hide a required missing value |
| isNullOrEqual(value1, value2) | Test whether the first value is null or equals the second | Use only where its null-as-true semantics are the stated business rule |
| toDate(expression) | Convert the mapped date expression to a Date | Required in `AttributeValue` for a confirmed Receivables `DATE` target except a complete confirmed `now()` value; retain requested date arithmetic inside the expression |
| now() | Obtain the current timestamp | Map a confirmed `now()` value directly; do not wrap it in `toDate(...)`. Do not use for effective-dated or accounting-sensitive logic unless the business rule explicitly requires runtime time |
| today() | Obtain the current date at midnight | Do not use as a substitute for a supplied effective date |
| isInDateRange(startDate, endDate, matchDate) | Evaluate a bounded date range | State the null-boundary behavior in the sample when it matters |
| round(number, precision) | Round a numeric value | State the requested precision and confirm the commercial rounding rule |
| finest, finer, fine, config, info, warning, severe | Emit diagnostic log messages | Keep messages non-sensitive; use a closure only when the expression is expensive |

## Excluded or Confirmation-Required APIs

| API or Pattern | Rule |
|---|---|
| evaluate(string) | Do not generate dynamic Groovy evaluation. The document notes it was not included in its R8 release, and runtime-composed code is outside this advisory contract. |
| getSourceObject() | Do not use. The document marks it as under evaluation and potentially deprecated. |
| move, copy, locate, row-set insert, maximum, minimum, sum, all, exists, delete, dynamicMatrix, Executor.run, and external-service invocation | Do not add these legacy Set Transform APIs to an AR-interface sample without separate current-runtime guidance and an explicit business requirement. |
| getFndMessage, getFndLookupCodeMeaning, getNextId, exit, currentTimeMillis, defaultLanguageCode | Require separate confirmation that the helper is available and needed; do not introduce it solely because it appears in the legacy guide. |

## Source

| Source Name | Source Type | Where to Find It | Used For |
|---|---|---|---|
| Set Transform Algorithm TUD | User-provided legacy Word document | C:\\backupOffice\\Srinivas\\Pricing Algorithms Technical details\\SetTransformAlgorithm_TUD fnl).doc | Conservative helper-function allowlist and exclusions |
