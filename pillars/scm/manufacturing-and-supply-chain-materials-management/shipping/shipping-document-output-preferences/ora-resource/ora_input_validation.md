# Input Validation

| Input Group | Accepted Input | Canonical Field | Route Output | If Invalid or Missing |
|---|---|---|---|---|
| Header dates | ISO date accepted by the selected Data Loader contract | StartDateActive, EndDateActive | Data Loader-owned physical representation | Stop and return the Data Loader validation result |
| Attach document | Boolean true or false only | AttachShippingDocumentFlag | REST/Data Loader Boolean | Stop before handoff for a non-Boolean value |
| Print orientation | Meaning or LookupCode | PrintOrientationCode | LookupCode returned by resolve_print_orientation | Stop on no match, ambiguity, or conflicting meaning and code |
| Print side | Meaning or LookupCode | PrintSideCode | LookupCode returned by resolve_print_side | Stop on no match, ambiguity, or conflicting meaning and code |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SDOP.VALIDATE_INPUT | step | 1 | validate_input | orientation_supplied->SDOP.LOOKUP_ORIENTATION;side_only->SDOP.LOOKUP_SIDE;no_print_lookup->SDOP.DONE | none | stop | Always |
