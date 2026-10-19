# User-Defined Tables HDL Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| EffectiveEndDate | Fusion end-of-time date | EffectiveEndDate is omitted from a UserDefinedTableRow or UserDefinedTableColumnInstance record | No | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| UDT.APPLY_DEFAULTS | step | 2 | apply_default | applied_or_not_needed->UDT.DEPENDENCY_GATE;blocked->UDT.RETURN_ISSUES | UDT.VALIDATE_INPUT | stop | Apply only the source-documented EffectiveEndDate default when the field is omitted. |

## Sources

- /scratch/UDT/UserDefinedTableRow.csv (SHA-256 2f7f39ffc2768e12b0cd5b8f5240f6bebe903b67986381a0b9ad86f2ae1f0f98)
- /scratch/UDT/UserDefinedTableColumnInstance.csv (SHA-256 9b74ba8df057f97cb7bad91a21f41dd8541ff3ec40d55e32909e76fea7604f2f)
