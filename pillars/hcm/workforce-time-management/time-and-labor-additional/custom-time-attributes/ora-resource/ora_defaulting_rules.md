# Custom Time Attributes Defaulting Rules

## Source Basis

- User-provided automatic Name and Value Location behavior.
- User-provided numbered Value Location mappings for Text, Number, Date, and Time stamp; use the lowest unused positive number from the fresh same-task export.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Name | Display Name converted to uppercase | Name is automatically generated for a parent or dependent attribute | No | |
| Value Location | AttributeVarchar(n) | New parent or dependent attribute with Data Type Text and a resolved Attribute Category, after fresh export | No | resolve_value_location |
| Value Location | AttributeNumber(n) | New parent or dependent attribute with Data Type Number and a resolved Attribute Category, after fresh export | No | resolve_value_location |
| Value Location | AttributeDate(n) | New parent or dependent attribute with Data Type Date and a resolved Attribute Category, after fresh export | No | resolve_value_location |
| Value Location | AttributeTimestamp(n) | New parent or dependent attribute with Data Type Time stamp and a resolved Attribute Category, after fresh export | No | resolve_value_location |

Uppercase conversion is the only supplied Name transformation. Do not invent
space replacement, punctuation removal, truncation, or duplicate-name handling.
No defaults were supplied for Classification, Data Type, Unit of Measure, the
two data sources, or Attribute Category.

## Export-Dependent Defaulting

Name can be generated during business preparation. Value Location selection
runs only after a fresh same-task export is available and its actual CSV member,
Attribute Category, and Value Location column are identified. Before export, defer this default;
do not block solely because that future artifact has not yet been obtained.
The invoking workflow must resolve and populate it before package preview.
This new-attribute rule does not authorize relocating an existing attribute.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CTA.APPLY_DEFAULTS | step | 18 | apply_default | defaulted->CTA.ENFORCE_FSM;blocked->CTA.HANDLE_ISSUE | CTA.RESOLVE_VALUE_LOCATION | stop | Generate Name; derive Value Location for new parent and dependent attributes only at the post-export stage |
