# Defaulting Rules

## Source Precedence

| Sequence | Source | Use |
|---|---|---|
| 1 | Complete same-task FSM CSV export and ASM_SETUP_CSV_METADATA.xml | Reuse populated technical values, internal codes, and accepted value forms |
| 2 | Supported read-only Fusion metadata | Resolve target-specific identifiers or lookups absent from the full export |
| 3 | COA Attributes workbook | Apply required, derived, constant, and fallback default rules |
| 4 | Oracle functional and EDM documentation | Resolve documented semantics only |

Template-only exports may supplement the complete export for file shape, but must not replace the complete export.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Source |
|---|---|---|---|---|
| KeyFlexfieldCode | GL# | User leaves it blank | No | COA Attributes workbook: Instances row 2 |
| ApplicationId | 101 | User leaves it blank | No | COA Attributes workbook: Instances row 3 |
| StructureInstanceCode | COA name with spaces replaced by underscores | User leaves it blank | No | COA Attributes workbook: Instances row 4 |
| StructureInstanceIdentifier | Derive from StructureInstanceCode: uppercase the first letter and lowercase all remaining letters when it contains only letters and digits; otherwise remove each special character and uppercase its immediately following letter while lowercasing all other letters and preserving digits | Structure instance identifier is blank and every special character in StructureInstanceCode is immediately followed by a letter | No | User-provided StructureInstanceIdentifier derivation rule |
| Name | Referenced structure Name | User leaves it blank | No | COA Attributes workbook: Instances row 6 |
| Description | Derived instance description | User leaves it blank | Yes | COA Attributes workbook: Instances row 7 |
| EnabledFlag | Y | User leaves it blank | Yes | COA Attributes workbook: Instances row 8 |
| DynamicCombinationCreationAllowed | Y | User leaves it blank | Yes | COA Attributes workbook: Instances row 9 |
| ShorthandAliasEnabledFlag | N | User leaves it blank | Yes | COA Attributes workbook: Instances row 10 |
| StructureCode | Referenced structure StructureCode | User leaves it blank | No | COA Attributes workbook: Instances row 16 |
| SegmentCode | Referenced structure SegmentCode | Instance override is supplied | No | COA Attributes workbook: Instance Segments row 5 |
| RequiredFlag, DisplayFlag | Y, Y | Instance override is supplied | Yes | COA Attributes workbook: Instance Segments rows 7–8 |
| BIEnabledFlag | N | Instance override is supplied and field is blank | Yes | COA Attributes workbook: Instance Segments row 12 |
| QueryRequiredType | OPTIONAL | Instance override is supplied and field is blank | Yes | COA Attributes workbook: Instance Segments row 13 |
| ValueSetCode | Referenced ValueSetCode | Instance override is supplied | No | COA Attributes workbook: Instance Segments row 19 |
| Segment value length | Referenced value-set MaximumLength; use 6 only when the upstream value set was created without an explicit segment length | Referenced segment length is needed for validation | No | User-provided default-length rule; referenced value-set metadata |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COAINS.DEFAULT | step | 5 | apply_default | complete->COAINS.BULK | COAINS.LOOKUP | stop | Object absent |
