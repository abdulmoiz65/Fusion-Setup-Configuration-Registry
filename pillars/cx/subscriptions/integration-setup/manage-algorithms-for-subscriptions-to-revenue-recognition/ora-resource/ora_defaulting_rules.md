# RMCS Algorithm Defaulting Rules

## Scope

This node fills the approved local changeset, not an on-disk XML file. The primary runbook alone prepares the artifact after its approval and persistence gates. No other algorithm, source, target, runtime or mapping value is defaulted.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Highest selected version's CustomizationFlag DefaultValue | true | rule_phase is approved_change; the exact approved local artifact scope includes the XML guide's required customization flag update | No silent override; an incompatible requested value blocks and must be resolved before approval | verify_rmcs_approval_evidence |

The canonical mutation scope is in [approval and local artifact](../resources/ora_algorithm_xml_guidance.md#approval-and-local-artifact). During intake, proposal and artifact_result, this node records Not Applicable and changes nothing. Artifact-result comparison independently verifies the already-created flag.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RMCSALG.APPLY_DEFAULT | step | 60 | apply_default | applied->RMCSALG.EVALUATE_CHECKPOINT;not_applicable->RMCSALG.EVALUATE_CHECKPOINT;blocked->RMCSALG.REPORT_ISSUES | RMCSALG.CHECK_EXECUTION_CONTRACT | stop | Fill only the phase-applicable approved changeset value; no file write or Fusion operation. |
