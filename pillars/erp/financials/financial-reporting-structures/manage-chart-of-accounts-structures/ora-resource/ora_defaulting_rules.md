# Defaulting Rules

## Source Precedence

| Sequence | Source | Use |
|---|---|---|
| 1 | Complete same-task FSM CSV export and ASM_SETUP_CSV_METADATA.xml | Reuse populated technical values, internal codes, column names, and accepted value forms |
| 2 | Supported read-only Fusion metadata | Resolve target-specific identifiers or lookups absent from the full export |
| 3 | COA Attributes workbook | Apply required, derived, constant, and fallback default rules |
| 4 | Oracle functional and EDM documentation | Resolve documented semantics only |

Template-only exports may supplement the complete export for file shape, but must not replace the complete export.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Source |
|---|---|---|---|---|
| KeyFlexfieldCode | GL# | User leaves it blank | No | COA Attributes workbook: Structures row 2 |
| ApplicationId | 101 | User leaves it blank | No | COA Attributes workbook: Structures row 3 |
| StructureCode | COA name with spaces replaced by underscores | User leaves it blank | No | COA Attributes workbook: Structures row 4 |
| Name | COA name | User leaves it blank | Yes | COA Attributes workbook: Structures row 5 |
| Description | Derived COA description | User leaves it blank | Yes | COA Attributes workbook: Structures row 6 |
| Delimiter | - | User leaves it blank | Yes | COA Attributes workbook: Structures row 7 |
| EnabledFlag | Y | User leaves it blank | Yes | COA Attributes workbook: Structures row 8 |
| SegmentCode, Name, Prompt | User-provided segment name | Segment field is blank | No | COA Attributes workbook: Structure Segments rows 5, 8, and 10 |
| SegmentIdentifier | Derive from SegmentCode: lowercase the complete code when it contains only letters and digits; otherwise remove each special character and uppercase its immediately following letter while lowercasing all other letters and preserving digits | Segment identifier is blank and every special character in SegmentCode is immediately followed by a letter | No | User-provided SegmentIdentifier derivation rule |
| ColumnName | Same-task full export; otherwise SEGMENT plus the user-supplied ordinal position | User leaves it blank | No | Complete FSM export first; COA Attributes workbook: Structure Segments row 7 |
| SequenceNumber | The ordinal in ColumnName: SEGMENT1 → 1, SEGMENT2 → 2, SEGMENT3 → 3, and so on | User leaves it blank | No | User direction; enforce one-to-one column and sequence alignment only for defaulted values |
| Explicit ColumnName and SequenceNumber | Preserve explicit user or workbook values even when they do not match the default ordinal rule | Both fields are supplied explicitly | No | User direction; readiness report must flag the mismatch and require approval |
| ShortPrompt | First three letters with initial capital for one word; initials for multiple words | User leaves it blank | Yes | COA Attributes workbook: Structure Segments row 11 |
| EnabledFlag | Y | Segment enabled flag is blank | Yes | COA Attributes workbook: Structure Segments row 13 |
| DisplayWidth | 6 | User leaves it blank | Yes | COA Attributes workbook: Structure Segments row 14 |
| Segment value length | 6 | User leaves segment length blank | No | User-provided default-length rule; pass the resolved length to the referenced value set as MaximumLength |
| DefaultValueSetCode | Verified referenced ValueSetCode | User leaves it blank after a successful value-set lookup | No | Read-only value-set metadata; COA Attributes workbook: Structure Segments row 21 |
| SegmentLabelCode | GL_BALANCING for Primary Balancing, FA_COST_CTR for Cost Center, GL_ACCOUNT for Natural Account, GL_INTERCOMPANY for Intercompany | User supplies the business classification but not an internal code | No | Same-task export first; Oracle qualified segment-label documentation when the export has no matching qualified row |
| StructureInstanceCode | COA name with spaces replaced by underscores | User leaves it blank | No | COA Attributes workbook: Instances row 4 |
| StructureInstanceIdentifier | Uppercase the first letter, lowercase remaining letters, remove separators, and uppercase the following letter | User leaves it blank and every separator is immediately followed by a letter | No | COA Attributes workbook: Instances row 5 |
| Structure instance Name | Structure Name | User leaves it blank | No | COA Attributes workbook: Instances row 6 |
| Structure instance Description | Blank | User leaves it blank | Yes | COA Attributes workbook: Instances row 7 does not provide a concrete default |
| Structure instance EnabledFlag | Y | User leaves it blank | Yes | COA Attributes workbook: Instances row 8 |
| DynamicCombinationCreationAllowed | Y | User leaves it blank | Yes | COA Attributes workbook: Instances row 9 |
| ShorthandAliasEnabledFlag | N | User leaves it blank | Yes | COA Attributes workbook: Instances row 10 |
| Structure instance StructureCode | Resolved StructureCode | User leaves it blank | No | COA Attributes workbook: Instances row 16 |
| Instance segment TreeCode | Blank | No approved hierarchy or tree design is supplied | Yes | COA Attributes workbook: Instance Segments row 6 |
| Instance segment RequiredFlag | Y | User leaves it blank | Yes | COA Attributes workbook: Instance Segments row 7 |
| Instance segment DisplayFlag | Y | User leaves it blank | Yes | COA Attributes workbook: Instance Segments row 8 |
| Instance segment DefaultType and DefaultValue | Blank | No approved segment default is supplied | Yes | COA Attributes workbook: Instance Segments rows 9 and 10 |
| Instance segment BIEnabledFlag | N | User leaves it blank | Yes | COA Attributes workbook: Instance Segments row 12 |
| Instance segment QueryRequiredType | OPTIONAL | User leaves it blank | Yes | COA Attributes workbook: Instance Segments row 13 |
| Instance segment ValueSetCode | Verified referenced ValueSetCode | User leaves it blank after successful value-set lookup | No | COA Attributes workbook: Instance Segments row 19 |
| Basic segment design | Company as Primary Balancing, Cost Center as Cost Center, Account as Natural Account, and Intercompany as Intercompany | User makes a vague create request with no structural details; present as a proposal and wait for confirmation | No | User-provided vague-request rule |
| Additional segments | No default | Always | No | User-provided design boundary; additional segments must come from the user or an approved design source |
| COA identity | No default | COA Name and StructureCode are both absent | No | User-provided design boundary; ask the user to identify the chart of accounts |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COASTR.DEFAULT | step | 5 | apply_default | complete->COASTR.BULK | COASTR.LOOKUP | stop | Object absent |
