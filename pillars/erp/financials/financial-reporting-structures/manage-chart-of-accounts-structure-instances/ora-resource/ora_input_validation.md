# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve |
|---|---|---|---|
| Instance identity | COA Name or StructureInstanceCode | Block | Derive StructureInstanceCode from COA Name with spaces replaced by underscores |
| Required instance attributes | KeyFlexfieldCode, ApplicationId, StructureInstanceCode, StructureInstanceIdentifier, Name, EnabledFlag, DynamicCombinationCreationAllowed, ShorthandAliasEnabledFlag, StructureCode | Block | Derive StructureInstanceIdentifier from StructureInstanceCode using the documented normalization rule; apply workbook constants or referenced structure values for the remaining fields, then report the source |
| Required override attributes | KeyFlexfieldCode, ApplicationId, StructureInstanceCode, SegmentCode, RequiredFlag, DisplayFlag, BIEnabledFlag, QueryRequiredType, ValueSetCode | Block only when an override is requested | Derive only from complete export, workbook, or referenced setup |
| Structure and value-set readiness | Verified structure identity and exactly one compatible ValueSetCode with datatype and MaximumLength for every inherited or override segment | Block | Resolve the referenced structure and value-set metadata before package generation. |
| Import contract | Complete same-task FSM CSV export and ASM_SETUP_CSV_METADATA.xml | Block | Obtain complete same-task export; template-only output is supplementary only |

## Field Validation

| Check | What Happens |
|---|---|
| COA name | Reject values longer than 30 characters. |
| StructureInstanceCode | Reject values longer than 30 characters, including codes derived from COA Name. |
| StructureInstanceIdentifier length | Reject values longer than 30 characters after validating or deriving the identifier. |
| StructureCode | Reject values longer than 30 characters. |
| Segment name | Reject values longer than 30 characters. Do not modify the supplied name. |
| SegmentCode | Reject values longer than 30 characters. |
| Segment length | If supplied, require the segment value length to be a numeric integer from 1 through 150. Otherwise inherit MaximumLength from the referenced value set; that upstream value defaults to 6 only when no explicit segment length was supplied. |
| Delimiter | Allow only exclamation mark, asterisk, plus sign, hyphen, period, colon, equals sign, caret, tilde, or vertical bar. |
| StructureInstanceIdentifier | Require a nonblank identifier. Derive it from StructureInstanceCode by uppercasing the first letter and lowercasing all remaining letters when the code contains only letters and digits. When a special character occurs, remove it and uppercase the immediately following letter; lowercase all other letters and preserve digits. Reject the derivation when the code is blank or a special character is not immediately followed by a letter. Validate an explicitly supplied StructureInstanceIdentifier against the same rule before package generation. |
| Segment default-value datatype | When an instance segment default is supplied, require DefaultType and resolve the referenced value-set datatype. For a numeric value set, use DefaultValueNumber and leave DefaultValue blank; for a nonnumeric value set, use DefaultValue and leave DefaultValueNumber blank. Reject conflicting or simultaneously populated default-value fields. |
| Vague create request | Propose Company, Cost Center, Account, and Intercompany; ask for COA identity, confirmation or revision of the proposed set, segment lengths, and any additional user-designed segments. Do not create artifacts, value sets, or values before confirmation. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COAINS.VALIDATE | step | 2 | validate_input | valid->COAINS.READY | COAINS.COLLECT | stop | Always |
