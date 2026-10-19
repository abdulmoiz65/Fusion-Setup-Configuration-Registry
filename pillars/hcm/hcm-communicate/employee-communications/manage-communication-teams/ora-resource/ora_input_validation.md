# Manage Communication Teams Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Import route | Target Environment; registered communicateUICommTeams capability result | Stop before import preparation only when the target environment is missing | Select REST only for one exact usable current registration; otherwise record the capability result and select FSM fallback | A setup-data import is requested | resolve_communication_team_import_route |
| Communication team type | Communication Team; ORA_CAMP_COMM_TEAM; Express Communication Team; ORA_BU_COMM_TEAM | Stop before Data Loader preparation | Supply one documented team type | A top-level team row is created through the selected import route | |
| Team identity | Team Name; TeamName | Stop before Data Loader preparation | Supply a nonblank trimmed team name that passes the transport and duplicate checks below | A top-level team row is created or verified | |
| Creator membership intent | `include_persisted_creator` | Stop before the REST parent archive preview | Confirm that Fusion's persisted creator must be added as a Team Member after parent readback and exact worker resolution; this is request intent, not approval of the future child archive | A REST top-level team create is requested | |
| FSM import context | Target Environment; current task-export archive with ASM_SETUP_CSV_METADATA.xml; requested operation Create; execution intent live | Stop before immutable preview | Preserve the current task-export package and use only its six-field top-level CSV contract | An FSM-fallback live top-level import is requested | |
| REST Data Loader context | Target Environment; usable current communicateUICommTeams metadata; requested operation Create; execution intent live | Stop before immutable preview | Resolve the exact environment and use the current registered business-object metadata for the create row | A REST-capable live top-level import is requested | |
| Lifecycle target | Target Environment; confirmed REST communicateUICommTeams capability; current communicateUICommTeams_updateTeamDetails POST metadata; Team Name; requested action Activate or Inactivate; current StatusCode | Stop before lifecycle preview | Resolve exactly one team from a fresh export and establish its current status. Validate the requested activate or inactivate action payload. Do not use FSM fallback. | Activate or Inactivate is explicitly requested | resolve_communication_team_import_route |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A usable exact registered communicateUICommTeams capability selects REST, or unavailable/unusable capability selects recorded FSM fallback; TeamName passes all field checks, TypeCode is documented, the current export contains no normalized exact TeamName match, and REST create rows use POST | Ready | Continue to selected-route dependency readiness | find_team_by_exact_name_in_export |
| Registered communicateUICommTeams capability is absent, inaccessible, ambiguous, malformed, or cannot produce usable current metadata | Ready with FSM fallback | Record the capability result and reason; do not infer REST from a release label, static manifest, or historical workbook | resolve_communication_team_import_route |
| TeamName is blank after trimming, has leading or trailing whitespace, contains a pipe, line break, NUL, or another control character, or exceeds 240 characters | Blocked | Supply a corrected team name; show the rejected condition without silently rewriting the requested value | |
| The current export contains a normalized exact TeamName match for a create request | Blocked | Stop; do not prepare a duplicate Data Loader archive | find_team_by_exact_name_in_export |
| The current export contains only a case-insensitive TeamName collision | Review required | Show the existing name and require the requester to confirm a distinct final name before preparing the archive | find_team_by_exact_name_in_export |
| TypeCode is ORA_BU_COMM_TEAM and SubscriberCode is EMP_EVENT | Ready | Continue with the Express-team row | |
| TypeCode is ORA_BU_COMM_TEAM and SubscriberCode is not EMP_EVENT | Blocked | Set SubscriberCode to EMP_EVENT | |
| A child association is requested with FSM fallback | Blocked | Stop; the FSM task-CSV route is top-level only | |
| A child association is requested with confirmed REST capability | Required | Use the current generated child sheet, exact resolved parent TeamId, exact current dependency values, and RestAction POST; do not infer fields from an example DAT | |
| A REST top-level team create omits `include_persisted_creator` | Blocked | Capture the creator-membership intent before preparing the parent archive. Do not treat the parent-archive approval as approval of the later child archive. | |
| A REST parent team create succeeded and its required child archive is prepared | Required | Read the persisted CreatedBy and CreatedByDisplayName, resolve exactly one active worker and primary assignment through workersLov, and include the resulting Team Members row. Do not use the OAuth login identity as a substitute or omit the creator on an explicit empty member list. | find_team_member_by_word |
| A Contact Preferences child association is requested with confirmed REST capability | Required | Require the exact effective ORA_IRC_COMMUNICATE_CONTACT_PREFERENCE profileValues item to return ProfileOptionValue `Y` before resolving the contact type or preparing the worksheet row; never apply this check to lifecycle activation | verify_contact_preference_profile_option |
| Activate is requested for exactly one ORA_DRAFT team and confirmed REST capability exposes communicateUICommTeams_updateTeamDetails with POST and the verified activate action payload | Ready | Prepare only the activation action row and exact-archive preview | |
| Inactivate is requested for exactly one ORA_ACTIVE team and confirmed REST capability exposes communicateUICommTeams_updateTeamDetails with POST and the user-confirmed inactivate action payload | Ready | Prepare only the inactivation action row and exact-archive preview | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Team type mapping | Map Communication Team to ORA_CAMP_COMM_TEAM and Express Communication Team or BU team to ORA_BU_COMM_TEAM; reject other values | A team type is supplied | |
| TeamName presence | Require a nonblank value after Unicode-aware trimming; reject leading or trailing whitespace rather than silently changing the requested value | A top-level team row is prepared | |
| TeamName transport safety | Reject `&#124;`, CR, LF, NUL, and other control characters that cannot be represented safely in the generated Data Loader row | A top-level team row is prepared | |
| TeamName length | Require a `VARCHAR(240)` value: reject a TeamName longer than 240 characters | A top-level team row is prepared | |
| TeamName duplicate check | Compare the proposed trimmed name with a fresh task-level CSV export; block a normalized exact match and require review for a case-insensitive collision | A create request is prepared | find_team_by_exact_name_in_export |
| FSM task-CSV package | Require the current task-export archive, exactly one ASM_SETUP_CSV_METADATA.xml member, and the top-level ORA_IRC_EMP_CAMP_COMM_TEAMS_DATA.csv member | An FSM fallback archive is prepared | |
| FSM task-CSV field scope | Permit only TeamName, StatusCode, TeamId, DownloadFlag, SubscriberCode, and TypeCode in ORA_IRC_EMP_CAMP_COMM_TEAMS_DATA.csv | An FSM fallback archive is prepared | |
| StatusCode | Require ORA_DRAFT for a new top-level create row. For activation, require current exported status ORA_DRAFT and verify ORA_ACTIVE afterward. For inactivation, require current exported status ORA_ACTIVE and verify ORA_INACTIVE afterward. StatusCode is not a field in the current updateTeamDetails workbook. | A selected-route create or lifecycle row is prepared | |
| TeamId | Require blank for a new top-level row | A selected-route create row is prepared | |
| Express subscriber | Require EMP_EVENT for ORA_BU_COMM_TEAM | An Express Communication Team row is prepared | |
| REST Data Loader metadata shape | Require the current generated `communicateUICommTeams` workbook schema of exactly 10 fields; do not use an example DAT as an executable schema | A REST-capable top-level Data Loader archive is prepared | |
| REST create field scope | Permit only TeamId, RestAction, StatusCode, StatusCodeMeaning, TeamName, TeamDescription, DownloadFlag, TypeCode, TypeCodeMeaning, and SubscriberCode; use the current generated communicateUICommTeams workbook and standard Data Loader validator | A REST-capable top-level create archive is prepared | |
| RestAction | Require POST for every create row and for activation or inactivation through communicateUICommTeams_updateTeamDetails. Do not reuse the create action or a placeholder action from a generated sample | A REST-capable create or lifecycle Data Loader row is prepared | |
| Child-association scope | Encode requested associations only in their matching current generated child sheet; retain blank unspecified fields and do not claim child readback from import counts | A REST-capable child Data Loader archive is prepared or validated | |
| Creator Team Member | Require a TeamMembers row for the exact persisted creator for every REST parent create; include TeamId, PersonId, AssignmentId, MemberName, EmailAddress, and RestAction only as exposed by current generated metadata | A REST parent create's required child archive is prepared | find_team_member_by_word |
| Activation payload | Use the current communicateUICommTeams_updateTeamDetails workbook header order. Require RestAction POST, action activate, and attributes serialized as a JSON array with exactly one object containing the exact persisted TeamId. When the workbook exposes top-level TeamId, require it to match the inner TeamId. Keep optional Content-Type and REST-Framework-Version blank unless current metadata requires values. Reject SAMPLE_VALUE placeholders and create or child fields. Do not add a StatusCode column to this action archive. | A REST activation archive is prepared | |
| Inactivation payload | Use the current communicateUICommTeams_updateTeamDetails workbook header order. Require RestAction POST, action inactivate, and attributes serialized as a JSON array with exactly one object containing the exact persisted TeamId. When the workbook exposes top-level TeamId, require it to match the inner TeamId. Keep optional Content-Type and REST-Framework-Version blank unless current metadata requires values. Reject SAMPLE_VALUE placeholders and create or child fields. Do not add a StatusCode column to this action archive. The user supplied the action shape and expected ORA_INACTIVE result; the example TeamId is never the target. | A REST inactivation archive is prepared | |

## User-Facing Validation Messages

| Validation result | Message |
|---|---|
| Blank name | Enter a team name. |
| Leading or trailing spaces | Remove spaces at the beginning or end of the team name. |
| Pipe, line break, NUL, or control character | Remove line breaks or unsupported characters such as `&#124;`. |
| TeamName exceeds 240 characters | Shorten the team name to 240 characters or fewer. |
| Existing normalized exact name | A team with this name already exists. Choose a different name. |
| Case-insensitive collision | A similarly named team already exists. Review the existing name before continuing. |

## Post-Action Validation

| Action | Verification Check | If Evidence Is Missing or Fails | Next Action |
|---|---|---|---|
| Selected-route Data Loader import initiation | Fusion returns an accepted initiation response for the approved immutable FSM or REST archive | Do not claim that the team exists | Stop without retrying and perform a fresh task-level CSV export when verification is requested |
| Task-level CSV readback | Exactly one row has the requested TeamName, ORA_DRAFT, the approved TypeCode, and the approved SubscriberCode | Report the mismatch and do not resubmit automatically | Review the readback and prepare a new immutable preview only if another change is required |
| Lifecycle status update | A fresh task-level CSV export has exactly one requested TeamName with the approved expected StatusCode | Report the mismatch and do not resubmit automatically | Review the readback and prepare a new immutable preview only if another change is required |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MCT.VALIDATE_INPUT | decision | 2 | validate_input | valid->MCT.CHECK_DEPENDENCIES;invalid->MCT.HANDLE_ERROR | MCT.RESOLVE_IMPORT_ROUTE | stop | A selected-route top-level Data Loader import, lifecycle action, export review, or validation request is evaluated |
| MCT.EVALUATE_RESULT | decision | 7 | evaluate_result | verified->MCT.RETURN_SUCCESS;issues->MCT.HANDLE_ERROR | MCT.EXECUTION_GATE | stop | A supported FSM or REST Data Loader import result, fresh task-level CSV readback, or approved lifecycle result is evaluated |

## Open TBD Items

| TBD Item | Owner | Blocker | Next Action |
|---|---|---|---|
