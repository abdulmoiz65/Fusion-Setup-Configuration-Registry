# Receiving Parameters Error Handling

## Error Rules

| Condition | Classification | Required Handling |
|---|---|---|
| Standard lookup returns no exact match or multiple exact matches | Input validation | Stop and request the exact display value or backend code. Do not guess or select the first result. |
| Standard lookup returns inactive or disabled value | Input validation | Stop and request an active value or backend code accepted by Fusion. |
| Standard lookup read fails | Auth/authz, transport/environment, or Fusion API | Stop before Data Loader handoff; report the failure class and do not substitute stale values. |
| Display value conflicts with a supplied backend code | Input validation | Stop and request one unambiguous value. |
| Job Set lookup returns no exact match or multiple distinct exact matches across `JobSetDisplayName` and `JobSetName` | Input validation | Stop and request the exact Job Set display name or backend `JobSetName`. Do not guess or select the first result. |
| Job Set lookup read fails or supplied display and Job Set names resolve to different rows | Auth/authz, transport/environment, Fusion API, or input validation | Stop before Data Loader handoff; report the failure class and do not substitute stale values. |
| Data Loader or Fusion rejects a field not locally normalized | Data Loader or Fusion validation | Preserve the reported diagnostic and do not duplicate the backend rule locally. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| RCV_PARAMS.DATALOADER_HANDOFF | terminal | 40 | terminal | none | RCV_PARAMS.RESOLVE_JOB_SET | continue | Local readiness and all applicable standard lookup and Job Set resolution have passed; hand off to `core.data-loader`. |
| RCV_PARAMS.RETURN_ISSUES | terminal | 90 | terminal | none | none | continue | Local normalization, readiness, or standard lookup resolution is blocked or fails. |
