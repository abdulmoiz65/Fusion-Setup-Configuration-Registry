# Explaining effective configuration

Use this reference for the Explain and Document workflows.

## Rule inventory

For each rule, capture:

- Source layer
- Identifier and label
- Description
- Status
- Sequence or evaluation order
- Condition
- Actions and defaults
- Validation messages
- Referenced fields
- Imported modules
- Page and release evidence
- Confidence and unresolved dependencies

## Business-language translation

Translate technical configuration into:

> When `<business condition>` is true, the page `<action>`. The rule affects
> `<fields or regions>` and shows `<message or user-visible result>`.

Explain codes with labels only when metadata or lookup evidence supports the
mapping. Retain the technical code in the implementation record.

## Overlap analysis

Flag:

- Two active rules writing the same field
- Broad conditions that subsume later rules
- Validation rules with contradictory results
- Inactive imports or orphaned expression files
- Referenced fields that are hidden or unavailable
- Setup-specific identifiers without a target-environment mapping

Do not infer a conflict solely because two rules mention the same field. Compare
conditions, actions, status, and order.

## Source distinction

Use these labels:

- Oracle-delivered
- Customer extension
- Imported candidate
- Unknown source

Use “unknown source” rather than guessing when only a flattened or partial
configuration is available.

## Deployed dynamic-component precedence

For a runtime page question, first resolve the component's metadata provider,
service owner, named layout, and ordered rules. The first matching rule selects
the layout variant. Apply object-level Business Rules and report their supported
field-property overrides as effective over rule-set layout values. Properties
fixed in the Layout Fields tab remain non-overridable. Evaluate Page
Properties as a separate ordered layer, with customer rules after built-in
rules. If the condition inputs or customer overlays are unavailable, report
the alternatives rather than selecting one.
