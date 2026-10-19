# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operational attribute identity | AttrName or AttrDispName; AttrGroupName is required only when the attribute maps to more than one group | Stop before lookup | Provide an attribute name or display name; provide Group Name when requested | Any update request | resolve_attribute_group_by_attribute |
| Requested change | ControlLevel; MaximumDecimalDigits is optional | Stop before preview | Provide a supported control level; provide maximum decimal digits only when it must change | Any update request | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Attribute identity is supplied | Accept AttrName or AttrDispName | Any update request | resolve_attribute_group_by_attribute |
| AttrName is nonblank and at most 30 characters when supplied | Reject invalid input | AttrName is supplied | |
| AttrGroupName is nonblank and at most 30 characters when supplied | Reject invalid input | Group Name is supplied to resolve ambiguity | |
| ControlLevel normalization | Convert Master Level, Master, M, or m to M; convert Child, Organisation Level, C, or c to C; reject any other value | ControlLevel is supplied | |
| MaximumDecimalDigits is an integer when supplied | Reject invalid input | MaximumDecimalDigits is supplied | |
| Attribute and group confirmation | Compare the resolved AttrGroupName, AttrGroupDispName, AttrName, and AttrDispName to the supplied identity values | Target is resolved | resolve_operational_attribute_control |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OAC.VALIDATE_INPUT | step | 10 | validate_input | passed->OAC.RESOLVE_ATTRIBUTE_GROUP;invalid->OAC.RETURN_ISSUES | none | stop | Any operational attribute control update request |
