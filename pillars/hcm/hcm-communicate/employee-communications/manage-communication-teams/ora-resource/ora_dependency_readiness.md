# Manage Communication Teams Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Import route | Resolve the live registered communicateUICommTeams capability for setup-data import; resolve communicateUICommTeams_updateTeamDetails separately for lifecycle updates; select REST only when the scope-specific registration is usable |
| 2 | Current task baseline | Use a current Manage Communication Teams task-level CSV export for exact-name checking and readback |
| 3 | Route-specific source | For FSM, use the current task-export package and ASM_SETUP_CSV_METADATA.xml; for REST, use current generated communicateUICommTeams metadata |
| 4 | Team identity, creator-membership intent, and child scope | For REST, record `include_persisted_creator` before parent preview, then resolve the persisted parent TeamId, creator, and dependencies through documented LOVs; for FSM, allow only top-level fields |
| 5 | Immutable Data Loader archive | Validate the exact route-specific archive and bind fresh approval to its SHA-256 before upload and initiation |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| MCT-IMPORT-ROUTE | Registered Data Loader capability and import route | Yes | A setup-data import is prepared | Satisfied after capability lookup or recorded fallback | Current target dataLoaderBusinessObjects registration and generated metadata workbook | resolve_communication_team_import_route | Selects REST only for a usable communicateUICommTeams setup-data capability; otherwise preserves the FSM top-level contract | Record the absent, inaccessible, ambiguous, malformed, or unusable capability result and use FSM fallback | Capability result; FSM or REST route; fallback reason when applicable |
| MCT-FSM-ARCHIVE | FSM task-export package | Yes | An FSM fallback import is prepared | Satisfied | Current Manage Communication Teams task export | | Preserves the task's FSM metadata and top-level CSV contract | Require ASM_SETUP_CSV_METADATA.xml and only ORA_IRC_EMP_CAMP_COMM_TEAMS_DATA.csv top-level fields | Validated package and top-level row |
| MCT-REST-METADATA | Scope-specific REST Data Loader metadata | Yes | A top-level team create or lifecycle package is prepared | Satisfied | Current generated communicateUICommTeams workbook for setup-data import, or communicateUICommTeams_updateTeamDetails workbook and action metadata for lifecycle | | Establishes the current create or lifecycle column order | Require POST for create through communicateUICommTeams. For lifecycle, require POST through communicateUICommTeams_updateTeamDetails with action=activate or action=inactivate as requested and a one-object attributes JSON array containing the exact TeamId. FSM fallback is create-only | Validated metadata, business object, operation, and row shape |
| MCT-CURRENT-EXPORT | Current task-level CSV export | Yes | A top-level team create, lifecycle update, or readback is prepared | Satisfied | Current Manage Communication Teams TASK_CSV export | find_team_by_exact_name_in_export | Prevents an exact duplicate create and supplies the current row for lifecycle status verification | Require zero exact TeamName matches for create and exactly one for lifecycle/update verification | Exact-name match count and current top-level values |
| MCT-CHILD-SCOPE | Child REST Data Loader scope | Yes | A child association is requested with confirmed REST capability | Satisfied | Current generated communicateUICommTeams workbook | | Confirms the child sheets and direct `TeamId` parent reference | Populate only the requested child sheets, use the exact existing `TeamId`, and retain blank unspecified fields | Validated child rows |
| MCT-CREATOR-MEMBER | Creator-membership intent and persisted identity | Yes | A REST top-level team create is requested, then its required child archive is prepared | Intent satisfied before parent preview; identity satisfied only after lookup | Request intent `include_persisted_creator`; fresh parent-and-children readback CreatedBy and CreatedByDisplayName; current workersLov response | find_team_member_by_word | Makes creator membership a declared initial requirement while ensuring the later child row uses Fusion's actual creator rather than a guessed login identity | Require `include_persisted_creator` before preparing the parent archive, then one exact active creator PersonId/AssignmentId pair from persisted evidence; stop on zero or multiple matches | Intent record; TeamId, PersonId, AssignmentId, MemberName, EmailAddress |
| MCT-CHILD-FEATURES | Sender Profile, Slack App, and Microsoft Teams Bot feature enablement | Conditional | A Sender Profile, Slack App, or Microsoft Teams Bot child row is requested | Satisfied only after lookup | Current recruitingUISettings rows | get_communication_team_child_feature_status | Prevents a child row for a disabled or unavailable feature | Require the matching ORA_IRC_CAMP_SENDER_PROF_ENABLED_FLAG, ORA_HCO_SLACK_ENABLED, or ORA_HCO_MSTEAMS_ENABLED setting to have exactly one Y value; route enablement to Manage External Integrations | Required setting code and Enabled result |
| MCT-CONTACT-PREFERENCE-FEATURE | Contact Preferences profile-option enablement | Conditional | A Contact Preferences child row is requested; not a lifecycle action | Satisfied only after lookup | Exact effective ORA_IRC_COMMUNICATE_CONTACT_PREFERENCE item from profileValues | verify_contact_preference_profile_option | Prevents Contact Preferences rows when the product feature is not enabled | Require exactly one readable exact item with case-sensitive ProfileOptionValue `Y`; missing, ambiguous, unreadable, or non-Y blocks | Exact profile value item and ProfileOptionValue `Y` |
| MCT-CHILD-DEPENDENCIES | Campaign purposes, sender profiles, eligibility profiles, HCM lists, and contact preferences | Conditional | A matching child row is requested | Satisfied only after lookup | Current documented LOV response; Manage Communicate Lookups for `ORA_IRC_EMP_CAMP_PURPOSE` and `ORA_HCO_CHANNEL_TYPE` | resolve_communicate_lookup_dependencies | Prevents stale or guessed dependency identities | Require exactly one current match for each requested referenced object; require enabled campaign-purpose and channel codes from their exact Communicate Lookup types | Current ID, display name, and description where returned |

## Dependency Classification

| Result Category | When Used | Can Continue? |
|---|---|---|
| Satisfied | The selected route's source, current export, exact-name check, and top-level field scope are valid | Yes |
| Not Applicable | No child association is requested | Yes |
| Blocked | The target environment is missing; the selected FSM package lacks ASM_SETUP_CSV_METADATA.xml; an FSM fallback request contains child associations; or REST metadata, a communicateUICommTeams_updateTeamDetails POST lifecycle action, parent TeamId, persisted creator identity, dependency, required child feature setting, required Contact Preferences profile option, or RestAction is invalid | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MCT.RESOLVE_IMPORT_ROUTE | decision | 1 | resolve_dependency | fsm_create->MCT.VALIDATE_INPUT;fsm_lifecycle->MCT.HANDLE_ERROR;rest->MCT.VALIDATE_INPUT;blocked->MCT.HANDLE_ERROR | none | stop | Invoke core.data-loader capability resolution before a setup-data import or lifecycle update. Route FSM only for a create; route an FSM lifecycle request directly to MCT.HANDLE_ERROR. For Activate or Inactivate, continue only on REST when current metadata exposes communicateUICommTeams_updateTeamDetails with POST and the requested documented action payload. When REST is absent, inaccessible, ambiguous, malformed, or unusable, stop rather than selecting FSM fallback. |
| MCT.CHECK_DEPENDENCIES | decision | 3 | resolve_dependency | ready->MCT.APPLY_DEFAULTS;not_required->MCT.APPLY_DEFAULTS;blocked->MCT.HANDLE_ERROR | MCT.VALIDATE_INPUT | stop | After import-route selection, route-specific source validation, and exact-name evaluation against the current task-level CSV baseline |

## Open TBD Items

| TBD Item | Owner | Blocker | Next Action |
|---|---|---|---|
