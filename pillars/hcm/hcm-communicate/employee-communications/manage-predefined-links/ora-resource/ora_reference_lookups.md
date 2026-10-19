# Manage Predefined Links Reference Lookups

Source: Confluence page 21736675148.

No runtime API lookup is used for FSM link creation. The create request must explicitly provide ObjectType and Action.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| get_active_predefined_links | A named already-active link is inspected outside the FSM export query route | Active-link identifier supplied by the requester | GET /hcmRestApi/resources/11.13.18.05/communicatePredefinedLinksLOV | DeepLinkId, DisplayName, Action, ObjectType, StatusCode, URL | Use the documented response only to inspect active-link fields; do not infer an undocumented UI-to-service mapping | DeepLinkId, DisplayName, Action, ObjectType, StatusCode, URL | Report the read boundary and do not claim a matched link without sufficient response evidence |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A current count of Active predefined links is requested | Use the FSM export-and-inspect route; do not substitute the active-link REST resource for the task export |
| A Draft link must be read or validated | Stop; the documented resource covers active predefined links only |
| The UI service communicateUIDeepLinksLOV is discovered | Do not treat it as a supported customer API without Oracle documentation |
| Create, update, activate, or inactivate is requested | Do not infer a write route from the read-only lookup |

## Open TBD Items

| TBD Item | Owner | Blocker | Next Action |
|---|---|---|---|
| Deterministic identity match for active-link REST readback | Oracle HCM REST owner | Limits exact API readback only | Provide documented finder or exact match semantics |
