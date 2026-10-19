# Manage Communication Teams Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Explicit input behavior | Resolver |
|---|---|---|---|---|
| TypeCode | ORA_CAMP_COMM_TEAM | A new standard Communication Team top-level row is prepared through the selected route | Preserve an explicitly requested supported team type | |
| StatusCode | ORA_DRAFT | A new top-level row is prepared through the selected route | Use the standard draft default unless the selected service supports and the user explicitly requests another creation status | |
| CampaignPurposes | `ORA_GENERAL` and `ORA_GET_RESPONSE` only | A REST-capable standard Communication Team child-association load is prepared and the request omits Campaign Purposes | Resolve both exact enabled values through Manage Communicate Lookups from Common Lookup type `ORA_IRC_EMP_CAMP_PURPOSE`, then automatically prepare those child rows after parent TeamId resolution. An explicit Campaign Purposes list, including an explicit empty selection, replaces this default | resolve_campaign_purposes_from_communicate_lookups |
| Templates | One exact active `Blank` template for each ORA_BASIC, ORA_ADVANCED, and ORA_HTML editor type | The first REST team create omits Templates | Automatically prepare the child rows after parent TeamId resolution. An explicit Templates list, including an explicit empty selection, replaces this default; never apply on FSM fallback | resolve_default_blank_templates |
| TeamMembers | One Team Members child row for the recorded parent creator | A REST parent team create is requested with `include_persisted_creator`, then succeeds | Before the parent preview, record the creator-membership intent. After parent readback, read CreatedBy and CreatedByDisplayName, resolve exactly one active worker and primary assignment, and merge that creator with any requested distinct members. This requirement cannot be removed by an explicit empty Team Members selection; never apply on FSM fallback. The later child archive still requires its own immutable approval. | find_team_member_by_word |
| SubscriberCode | EMP_EVENT | A new Express Communication Team or ORA_BU_COMM_TEAM row is prepared | Apply only to the Express-team type; do not add it to a standard team | |
| RestAction | POST | A REST-capable top-level, child association, Activate, or Inactivate row is prepared for REST Data Loader | Use POST for a requested create or lifecycle action through communicateUICommTeams_updateTeamDetails. Use the requested documented activate or inactivate payload; never reuse a placeholder from a generated sample | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MCT.APPLY_DEFAULTS | decision | 4 | apply_default | applied->MCT.ENFORCE_DESIGN;preserved->MCT.ENFORCE_DESIGN;blocked->MCT.HANDLE_ERROR | MCT.CHECK_DEPENDENCIES | stop | For a new standard Communication Team, apply ORA_CAMP_COMM_TEAM and ORA_DRAFT through either route. With confirmed REST capability, also apply POST, resolve omitted CampaignPurposes through Manage Communicate Lookups from ORA_IRC_EMP_CAMP_PURPOSE only to ORA_GENERAL and ORA_GET_RESPONSE, and after parent creation resolve the recorded creator to one active worker and primary assignment and prepare its Team Members child row; also resolve omitted Templates to the Basic, Advanced, and HTML active Blank defaults. On FSM fallback, preserve the FSM task-CSV shape and do not add REST fields or child rows. Apply EMP_EVENT only for ORA_BU_COMM_TEAM without changing unrelated supplied values. |

## Open TBD Items

| TBD Item | Owner | Blocker | Next Action |
|---|---|---|---|
