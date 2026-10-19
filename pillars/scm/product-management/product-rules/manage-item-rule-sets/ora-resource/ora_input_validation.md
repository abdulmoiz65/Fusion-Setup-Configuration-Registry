# Input Validation

Sources:

- User-confirmed Fusion import failure on 2026-09-23 with JBO-27040.
- Oracle Fusion SCM table [EGO_RL_RULE_SETS_B](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26b/oedsc/egorlrulesetsb-8962.html) for rule-set base fields.
- Oracle Fusion SCM table [EGO_RL_RULE_SETS_TL](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26a/oedsc/egorlrulesetstl-10664.html) for translated rule-set fields.
- Oracle Fusion SCM table [EGO_RL_USER_RULES_B](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/25c/oedsc/egorluserrulesb-19589.html) for rule fields.
- Oracle Fusion SCM [Item Rule Sets REST schema](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26a/fasrp/op-itemrulesets-get.html) for Composite and IsDraft accepted values.

Validate both the normalized task input and the generated archive. Limits that
apply to technical fields must be checked after mappings such as
ITEM_DESCRIPTION to ITEM_DESC have been applied.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Rule-set identity and type | RulesImplementation, RuleSetName, RuleSetDisplayName, RuleSetType, Composite, AssociationContext | Stop before preparing or importing the archive | Supply the missing business value or correct the transformation that generates the technical value | Every EGO_RULE_SET_DEFINITION row | |
| Rule identity and order | RuleName, Sequence | Stop before preparing or importing the archive | Supply a nonblank RuleName and Sequence | Every EGO_RULE row | |
| Serialized rule definition | RuleXml | Stop before importing the archive | Regenerate a nonblank, well-formed rule definition from the normalized rule input | Every generated EGO_RULE row | |
| Translation identity | Language, SourceLang | Reject the affected translation row | Supply valid language codes of four characters or fewer | Every generated rule-set or rule translation row | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| An EGO_RULE row is generated | The rule-set implementation and rule-set name must exactly identify the parent EGO_RULE_SET_DEFINITION row | Stop and rebuild the archive when the parent row is missing or does not match | |
| A rule-set translation row is generated | Its rule-set identity must exactly match one generated parent rule-set row | Reject the orphan translation row and rebuild the archive | |
| A rule translation row is generated | Its rule-set identity and RuleName must exactly match one generated EGO_RULE row | Reject the orphan or ambiguous translation row and rebuild the archive | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| RulesImplementation is nonblank and contains no more than 20 characters | Reject the rule-set row before archive preparation or upload and report the actual length | Every normalized or generated rule-set row | |
| RuleSetName is nonblank and contains no more than 50 characters | Reject the rule-set row before archive preparation or upload and report the actual length | Every normalized or generated rule-set row | |
| RuleSetDisplayName is nonblank and contains no more than 50 characters | Reject the rule-set row before archive preparation or upload and report the actual length | Every normalized or generated rule-set row | |
| RuleSetType is nonblank and contains no more than 50 characters | Reject the rule-set row before archive preparation or upload and report the actual length | Every normalized or generated rule-set row | |
| Composite is Y or N | Reject any other value before archive preparation or upload | Every normalized or generated rule-set row | |
| AssociationContext is nonblank and contains no more than 30 characters | Reject the rule-set row before archive preparation or upload and report the actual length | Every normalized or generated rule-set row | |
| AssociationType contains no more than 10 characters | Reject the rule-set row before archive preparation or upload and report the actual length | AssociationType is supplied | |
| AssociationCode1 contains no more than 30 characters | Reject the rule-set row before archive preparation or upload and report the actual length | AssociationCode1 or Association1KeyValue is supplied | |
| AssociationCode2 contains no more than 80 characters | Reject the rule-set row before archive preparation or upload and report the actual length | AssociationCode2 or Association2KeyValue is supplied | |
| Draft is Y or blank/null and contains no more than 2 characters | Reject any other value before archive preparation or upload | Draft or IsDraft is supplied | |
| Sequence is present and fits NUMBER(18) | Reject a blank, noninteger, or greater-than-18-digit sequence before archive preparation or upload | Every normalized or generated rule row | |
| RuleName is nonblank and contains no more than 30 characters | Reject the rule row before archive preparation or upload, report the actual length and the maximum of 30, and require a corrected RuleName | Every normalized or generated rule row | |
| RunOn contains no more than 30 characters | Reject the generated rule row and report the actual length | RunOn is generated | |
| The transformed ReturnType contains no more than 15 characters | Apply the documented logical-to-technical mapping first, then reject the generated rule row if the technical value exceeds 15 characters | ReturnType is supplied; for example validate ITEM_DESC after mapping ITEM_DESCRIPTION | |
| TargetBusinessEntity contains no more than 40 characters | Reject the generated rule row and report the actual length | TargetBusinessEntity is generated | |
| TargetAttrGroupType contains no more than 30 characters | Reject the generated rule row and report the actual length | TargetAttrGroupType is generated | |
| TargetAttrGroupName contains no more than 80 characters | Reject the generated rule row and report the actual length | TargetAttrGroupName is generated | |
| TargetAttrName contains no more than 30 characters | Reject the generated rule row and report the actual length | TargetAttrName is generated | |
| Severity contains no more than 50 characters | Reject the generated rule row and report the actual length | Severity is generated | |
| DefaultChangeOrderType contains no more than 30 characters | Reject the generated rule row and report the actual length | DefaultChangeOrderType is generated | |
| Single-character rule flags contain no more than one character | Reject the generated rule row; HasAlternateCatalogs, HasContextAttrs, HasMultirowAttrs, HasVariantAttrs, HasStructAttrs, and HasClassChangeFunction must also be present | A rule flag is generated | |
| Version contains no more than 10 characters | Reject the generated rule row and report the actual length | Version is generated | |
| PrimaryIfExpression, SecondaryIfExpression1 through SecondaryIfExpression5, and ValidationConditionForAudit each contain no more than 1900 characters | Reject the generated rule row and identify every expression that exceeds its limit | An audit expression is generated | |
| SecondaryIfReturnValue1 through SecondaryIfReturnValue5 each contain no more than 800 characters | Reject the generated rule row and identify every return value that exceeds its limit | A secondary return value is generated | |
| RuleXml is nonblank and well-formed XML | Reject the generated rule row before ZIP assembly or upload | Every generated EGO_RULE row | |
| Language and SourceLang are nonblank and contain no more than 4 characters | Reject the affected translation row | Every generated translation row | |
| RuleSetDisplayName in a translation row contains no more than 50 characters | Reject the affected rule-set translation row and report the actual length | A translated display name is generated | |
| Rule-set Description contains no more than 256 characters | Reject the affected rule-set translation row and report the actual length | A rule-set description is generated | |
| Any validated input or generated archive content change invalidates prior archive approval | Rebuild the FSM archive, rerun all validations, calculate a new archive hash, and require approval for that exact hash before upload | A validated value or generated archive file changes after validation or approval | |

The data dictionary does not by itself prove that a reference value or
combination such as AssociationType plus AssociationCode1 exists in the target
Fusion environment. Treat those as runtime reference-data checks rather than
local schema validation. It also does not establish RuleName or Sequence
uniqueness, so do not claim those checks as dictionary constraints.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MIRS.VALIDATE_INPUT | decision | 10 | validate_input | valid->MIRS.READY;invalid->MIRS.HANDLE_INPUT_ERROR | none | stop | A Manage Item Rule Sets input or generated archive is prepared or validated |
