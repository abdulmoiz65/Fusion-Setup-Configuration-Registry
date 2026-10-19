# Input Validation

Validate the exact native `_PLN.zip`, its nested ZIP CRCs, safe member paths,
batch sequence, XML readability, Plan presence, effective date, and embedded
export-log inventory before building an approval preview. Reject any package
containing nonempty Benefits program setup rows; this task supports plan imports
only.

## Task Nodes

`BEN_PLAN_CONFIG.VALIDATE_INPUT` passes only when local validation completes.
