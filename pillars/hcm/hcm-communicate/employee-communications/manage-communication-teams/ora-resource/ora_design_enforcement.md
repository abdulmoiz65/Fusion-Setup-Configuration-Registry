# Manage Communication Teams Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Enforce import route | Resolve the live registered communicateUICommTeams capability for setup-data import and communicateUICommTeams_updateTeamDetails separately for lifecycle updates; select REST only when the scope-specific registration is usable |
| 2 | Enforce team identity and type | Require a nonblank unique TeamName and one documented TypeCode |
| 3 | Enforce current import scope and creator membership | On FSM fallback, change only the FSM task CSV's six top-level fields; with confirmed REST capability, change only current generated communicateUICommTeams root or child metadata and require the persisted creator's TeamMembers row after a parent create |
| 4 | Enforce immutable archive | Bind the selected FSM or REST create archive, or confirmed REST activation archive, to its exact SHA-256; require POST for REST create and POST with communicateUICommTeams_updateTeamDetails for activation |
| 4 | Enforce lifecycle updates | Permit REST activation only from ORA_DRAFT with action=activate and verify ORA_ACTIVE afterward. Permit REST inactivation only from ORA_ACTIVE with action=inactivate and verify ORA_INACTIVE afterward. Use communicateUICommTeams_updateTeamDetails POST with the exact TeamId in attributes for each action |
| 5 | Bound validation claims | Treat current child-sheet metadata as an import contract, but do not claim individual-child readback from Data Loader counts or the top-level TASK_CSV export |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A setup-data import is prepared | Blocker | resolve_communication_team_import_route | Target environment is missing, or REST is selected without one exact usable current communicateUICommTeams registration | Record the unavailable or unusable capability result and select FSM fallback; do not infer REST from a release label, static manifest, or historical workbook | No undocumented automatic fix |
| A top-level team create is prepared | Blocker | find_team_by_exact_name_in_export | TeamName is blank, TypeCode is unsupported, RestAction is not POST, or the current export contains an exact TeamName match | Correct the identity, type, or action and rebuild from the supplied communicateUICommTeams metadata | Yes |
| An Express Communication Team or ORA_BU_COMM_TEAM row is prepared | Blocker | | StatusCode is not ORA_DRAFT or SubscriberCode is not EMP_EVENT | Set the documented create status and Express subscriber before preview | Yes |
| A REST Data Loader archive is prepared | Blocker | | A create archive does not use communicateUICommTeams, an activation archive does not use communicateUICommTeams_updateTeamDetails, its metadata/data row does not have the current generated order, RestAction is not POST, the archive contains unreviewed files, or an unrequested top-level value changes | Rebuild the immutable archive from current metadata and apply only the approved row | Yes |
| An FSM fallback archive is prepared | Blocker | | ASM_SETUP_CSV_METADATA.xml is absent, the top-level CSV is not ORA_IRC_EMP_CAMP_COMM_TEAMS_DATA.csv, a row uses fields outside TeamName, StatusCode, TeamId, DownloadFlag, SubscriberCode, and TypeCode, or a child association is requested | Rebuild from the current task export and keep the import top-level only | Yes |
| A member, purpose, sender profile, audience, template, contact preference, Slack, or Microsoft Teams association is requested in the same import | Blocker | | The child sheet, exact parent `TeamId`, or referenced dependency was not resolved from current generated metadata and documented LOVs | Rebuild from the current generated child sheet and resolve every dependency exactly | Yes |
| A REST parent create's child archive is prepared | Blocker | find_team_member_by_word | Fresh parent readback lacks CreatedBy or CreatedByDisplayName, workersLov does not yield one exact active creator PersonId/AssignmentId pair, or the TeamMembers sheet lacks the creator row | Resolve the persisted creator exactly and rebuild the separate child archive; never substitute the OAuth login identity or omit the creator | No undocumented automatic fix |
| A Contact Preferences association is requested | Blocker | verify_contact_preference_profile_option | The exact effective ORA_IRC_COMMUNICATE_CONTACT_PREFERENCE profileValues item is missing, ambiguous, unreadable, or its ProfileOptionValue is not `Y` | Do not prepare the ContactPreferences worksheet row until the exact effective value is freshly verified; this check does not apply to lifecycle activation | No |
| Activate is requested | Blocker | | The exact team is not uniquely resolved, current status is not ORA_DRAFT, current REST metadata lacks communicateUICommTeams_updateTeamDetails POST, action is not activate, attributes lacks one exact TeamId, exposed top-level TeamId differs, optional headers contain placeholders, or unrequested fields are present | Rebuild only the activate action row from current metadata; keep optional headers blank, validate through Data Loader, and verify ORA_ACTIVE after approval and submission | Yes |
| Inactivate is requested | Blocker | | The exact team is not uniquely resolved, current status is not ORA_ACTIVE, or the current communicateUICommTeams_updateTeamDetails POST metadata is unusable | Stop before archive preparation; resolve current identity, status, and metadata | No undocumented automatic fix |
| An inactivation archive is prepared | Blocker | | RestAction is not POST, action is not inactivate, attributes lacks one exact TeamId, exposed top-level TeamId differs, optional headers contain placeholders, or create or child fields are present | Rebuild only the inactivate action row from current metadata; keep optional headers blank unless required and verify ORA_INACTIVE after one approved submission | Yes |
| Delete is requested | Blocker | | Team status is not ORA_DRAFT | Do not delete; Delete is documented only for a draft team | No |
| A lifecycle action is ready for execution | Blocker | | The exact environment, team, current status, action, expected status, verification method, and fresh explicit approval are not all present | Present the exact preview and obtain action-bound approval immediately before the lifecycle action | No undocumented automatic fix |
| A direct REST call, internal ADF lifecycle update, or FSM lifecycle import is proposed | Blocker | | It bypasses the REST Data Loader immutable archive, validation, and approval gate | Use only a confirmed REST Data Loader communicateUICommTeams_updateTeamDetails action archive | No |
| Full configuration readback is claimed from Data Loader counts, source-accessor evidence, or a TASK_CSV export alone | Blocker | | The evidence establishes child import shape, not individual child-record readback | Report import result separately from association readback | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_communication_team_import_route | Before every setup-data import | Registered capability result, selected FSM or REST route, and fallback reason when applicable | ora_reference_lookups.md |
| find_team_by_exact_name_in_export | Before a top-level create preview and during requested verification | Zero exact matches for create; one exact matching row for verification | ora_reference_lookups.md |
| verify_contact_preference_profile_option | Before a Contact Preferences child row is prepared | Exact effective ORA_IRC_COMMUNICATE_CONTACT_PREFERENCE profileValues item with ProfileOptionValue `Y` | ora_reference_lookups.md |
| find_team_member_by_word | After every successful REST parent create before its child archive preview | Persisted CreatedBy, CreatedByDisplayName, and one exact active PersonId/AssignmentId pair | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MCT.ENFORCE_DESIGN | decision | 5 | design_enforcement | passed->MCT.EXECUTION_GATE;blocked->MCT.HANDLE_ERROR | MCT.APPLY_DEFAULTS | stop | After import route, top-level inputs, exact-name evidence, dependencies, and defaults are evaluated |

## Open TBD Items

| TBD Item | Owner | Blocker | Next Action |
|---|---|---|---|
