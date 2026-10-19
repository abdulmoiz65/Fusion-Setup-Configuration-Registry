# Provider Gap and Proposal Results

## Error Situations

| Situation | What Should Happen |
|---|---|
| A consuming-skill lookupType, provider evidence, or validation is unavailable | Return a missing-input or provider gap and stop before a configuration proposal. |
| A provider-owned change is not required or is not explicitly confirmed | Return the before/after comparison and stop before provider execution. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MCL.PROPOSAL_READY | terminal | 3 | terminal | none | MCL.COMPARE_PROVIDER_STATE | stop | Current and recommended states are compared and any provider change remains subject to user confirmation |
| MCL.PROVIDER_GAP | terminal | 4 | terminal | none | none | stop | A runtime lookupType, provider response, validation result, or approval requirement is unresolved |
