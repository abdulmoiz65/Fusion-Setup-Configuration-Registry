# Conditional Action Serialization

## When to use

Use this reference when the selected nonprotected active Algorithm version has
no declarative action and the workflow must add a separate
`CONDITIONAL_ACTION`. It is a structural contract derived from an approved
Algorithm BO sample. The sample proves element order and required containers
only; never copy its business entities, aliases, joins, action names,
expressions, sequence values, or identifier values.

## Ownership Rule

The missing action is owned by this skill. After the business contract, review
approval, and any provisional-continuation gate pass, create the canonical action
from this reference. Do not ask the user to provide an existing action, a
structural sample, or a schema solely because the eligible export contains only
`RUN_SCRIPT`.

## Required structure

Add a `StepSetupVORow` after the unchanged `RUN_SCRIPT` step, with the next
available `SeqNum` and these fields:

```xml
<StepName><NEW_ACTION_NAME></StepName>
<StepCategory>SETTRANSFORMATIONMETHOD</StepCategory>
<StepType>CONDITIONAL_ACTION</StepType>
<Comments null="true"/>
<Condition null="true"/>
<ForCollection null="true"/>
<ForVariable null="true"/>
<TargetLookupSet null="true"/>
<ParentName null="true"/>
<ExceptionHandler null="true"/>
<HierDirection>DOWN</HierDirection>
<ScriptBlock null="true"/>
<SplitMergeToSet null="true"/>
<SubAlgorithmName null="true"/>
```

Add `StepSetSetup` with:

1. One primary `StepSetSetupVORow` for `SubscriptionOM.OSSTransactions`,
   `SetSeqNum=1`, `PrimarySetFlag=Y`, and null cardinality/join fields.
2. One contained row for each target, owner, and EFF entity, ordered in proven
   lineage. Use `PrimarySetFlag=N`, `Cardinality=ZERO_OR_ONE`, and the
   assessment's exact bracketed `JoinSpecExpr`.
3. A fresh unique `SetNumber` for every set row.

Add `StepActionSetup` with exactly one `StepActionSetupVORow` containing
`ActionType=CONDITIONAL_ACTION`, `ActionSeqNum=1`, a request-specific action
name, the guarded expression, null action/break conditions, and a fresh unique
`ActionNumber`.

Follow the action container with null `StepVarSetup`, `ConnectBySetup`,
`GroupBySetup`, and `SubAlgorithmSetup` fields.

## Invariants

- Preserve every selected-version step that pre-existed the change, including
  the delivered `RUN_SCRIPT`, byte-for-byte and in its existing order.
- Do not modify Versions 0 or 1 or any nonselected version subtree.
- Use only source, target, alias, join, and Boolean behavior from the current
  Service Mapping assessment; do not reuse these values from the structural
  sample.
- Generate fresh identifiers for `SetNumber` and `ActionNumber`; do not reuse
  sample identifiers.
- If any current-request lineage or guarded expression input is unresolved,
  stop for the applicable mapping prerequisite. Absence of an action step by
  itself is never a blocker or a user error.
