# Manage Communication Teams Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Registered communicateUICommTeams capability is absent, inaccessible, ambiguous, malformed, or cannot produce usable current metadata | Record the capability result and select the FSM fallback route; do not infer REST from a release label, static manifest, or historical workbook |
| TeamName is blank, has surrounding spaces or unsupported transport characters, exceeds a current live limit, or already exists in the current export | Stop before preparation and return the matching plain-language validation message |
| An Express-team row does not use ORA_DRAFT and EMP_EVENT | Correct the top-level row before Data Loader archive preparation |
| A requested value is not represented by the current generated `communicateUICommTeams` metadata | Stop before preview; do not omit the value silently or claim it will be imported |
| A REST parent create omits the `include_persisted_creator` request intent | Stop before the parent archive preview. Capture that intent first; do not treat initial intent or parent approval as approval of the future resolved child archive. |
| A REST parent create's recorded creator is absent, unreadable, zero-match, or multiple-match in workersLov | Stop the separate child archive. Keep the verified parent unchanged, disclose that its creator could not be safely added, and require corrected identity evidence before a new child preview and approval. |
| A Contact Preferences child association is requested and the exact effective ORA_IRC_COMMUNICATE_CONTACT_PREFERENCE profileValues item does not return ProfileOptionValue `Y` | Stop only the Contact Preferences section; do not use a UI observation, CSV value, or recruitingUISettings as proof. This gate does not apply to lifecycle activation |
| An FSM fallback request lacks ASM_SETUP_CSV_METADATA.xml, has a malformed task-CSV package, or contains a child association | Stop before preview; rebuild the current FSM task-export archive and keep the request top-level only |
| A Data Loader archive differs from current generated metadata, the reviewed top-level row, or the approved archive | Stop before upload and rebuild the immutable preview from the current generated metadata |
| Fusion rejects a top-level Communication Team row | Return: "Fusion rejected the Communication Team record. Review the returned diagnostic, correct the top-level values, and prepare a new approved archive." Do not retry automatically |
| Import initiation result is uncertain | Do not submit again until a fresh task-level CSV export establishes the current value |
| Fresh task-level CSV readback does not contain exactly one approved row | Report the current and requested values; do not prepare another change without a new preview and approval |
| Activate is requested when the exact team is not unique, current status is not ORA_DRAFT, or confirmed REST capability does not expose communicateUICommTeams_updateTeamDetails POST metadata | Stop without changing the team; do not use FSM fallback |
| Inactivate is requested when the exact team is not unique, current status is not ORA_ACTIVE, or confirmed REST capability lacks communicateUICommTeams_updateTeamDetails POST metadata | Stop without changing the team; do not use FSM fallback |
| Fusion returns `IRC_INACT_TEAM_ACT_CAM` or another inactivation error | Report the actual returned code and message, preserve the diagnostic, and stop without an automatic retry. Do not assert that a specific campaign condition exists before Fusion returns it. |
| A REST activation archive omits POST, communicateUICommTeams_updateTeamDetails, action=activate, or the exact matching TeamId in attributes and exposed top-level field; contains placeholders or unrelated fields; or Fusion reports a primary-key ambiguity | Stop without changing the team. Export the exact current row, rebuild a new activate action archive from current metadata, and require new exact-archive approval before submission |
| A REST inactivation archive omits POST, communicateUICommTeams_updateTeamDetails, action=inactivate, or the exact matching TeamId in attributes and exposed top-level field; contains placeholders or unrelated fields; or Fusion reports a primary-key ambiguity | Stop without changing the team. Export the exact current row, rebuild a new inactivate action archive from current metadata, and require new exact-archive approval before submission |
| A lifecycle result is uncertain | Export the exact team's current row; do not submit the status update a second time automatically |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required top-level fields are missing or invalid | Correct only the identified input and rerun validation |
| Catalog mismatch | The task does not resolve exactly once, the selected route's FSM task package or REST Business Object is invalid, its metadata does not match, or REST lacks one exact usable current registration | Stop and correct the task selection, route-specific source, metadata, or archive; use FSM fallback for unavailable or unusable REST capability |
| Scope blocker | An FSM fallback request contains child associations, a REST child row lacks current generated metadata, exact parent TeamId, exact persisted creator identity, or exact dependency lookup, or Contact Preferences lacks the required effective profile value `Y` | Keep FSM imports top-level only, or rebuild the REST child row from current metadata and resolve the missing value before preview |
| Approval blocker | The exact environment, operation, archive, SHA-256, or explicit approval is missing or stale | Regenerate the immutable preview and obtain explicit approval |
| Fusion API | Fusion rejects the Data Loader upload or import initiation | Preserve the returned diagnostic and correct the documented cause before a new approved attempt |
| Process failed | The Data Loader import process reports failure when status is explicitly requested | Retrieve the ProcessLog, disclose the failure, and require a new preview before retry |
| Verification blocker | A fresh task-level CSV export is unavailable or does not match the approved top-level row | Report the unverified boundary and do not retry automatically |
| Lifecycle blocker | The exact lifecycle identity, status, action, or approval is missing | Correct the preflight and present a new exact lifecycle preview |

## Public Documentation for Unknown or Final Lifecycle Failures

Use Oracle's public documentation to confirm user-interface setup, roles, and feature prerequisites. These documents do not establish a REST Data Loader `communicateUICommTeams_updateTeamDetails` lifecycle contract and must not be used to infer a retry or alternate API path.

| Situation | Public Oracle Documentation | Required Response |
|---|---|---|
| Unknown Manage Communication Teams or final lifecycle failure | [Create a Communication Team](https://docs.oracle.com/en/cloud/saas/human-resources/fauat/create-a-communication-team.html) | Confirm the documented UI setup and prerequisites. Preserve the target environment, task code, team identity, current status, REST metadata and action evidence, immutable archive SHA-256, request ID, and exact diagnostic before escalation. |
| Authorization or unavailable task | [HCM Communicate Roles](https://docs.oracle.com/en/cloud/saas/human-resources/fauat/hcm-communicate-roles.html) | Verify the documented Campaign Administrator and implementation role prerequisites; do not infer a missing REST privilege from a successful UI role check. |
| Contact Order Preference is absent or fails validation | [Add Alternative Contact Details](https://docs.oracle.com/en/cloud/saas/human-resources/fauat/create-alternative-contact-details.html) | Verify `ORA_IRC_COMMUNICATE_CONTACT_PREFERENCE` is enabled at site level and re-run the exact profile-option check. |
| HCM Communicate or Employee Communications is unavailable | [Enable HCM Communicate](https://docs.oracle.com/en/cloud/saas/human-resources/fauat/enable-hcm-communicate.html) | Verify the offering and Employee Communications opt-in before a new attempt. |

When the documented prerequisites are satisfied but the REST lifecycle result remains unknown or fails, stop without retrying and open an Oracle Support request with the preserved evidence. Do not substitute an FSM lifecycle import, direct REST call, or internal ADF operation.

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before upload and import initiation | Exact target environment, registered capability result, selected FSM or REST create route, FSM fallback reason when applicable, task code, route-specific source and row scope, immutable archive path, SHA-256, and the requirement for explicit approval. For a REST parent create, also show the recorded `include_persisted_creator` intent and state that the resolved Team Members child archive requires a later exact-artifact approval; for a lifecycle action show REST, communicateUICommTeams_updateTeamDetails, POST, the requested action=activate or action=inactivate, and exact TeamId in attributes and exposed top-level field, with no FSM fallback |
| After accepted initiation | Data Set Name, Content ID, and Request ID returned by Fusion; do not poll automatically |
| During requested verification | The exact top-level row and TeamId from a fresh task-level CSV export, followed by the exact parent-and-child response from read_communication_team_with_children |
| Before Activate | Exact environment, confirmed REST capability and communicateUICommTeams_updateTeamDetails POST metadata, team identity, current ORA_DRAFT status, action=activate with exact TeamId, expected ORA_ACTIVE status, immutable archive, verification method, and fresh explicit approval |
| Before Inactivate | Exact environment, confirmed REST capability and communicateUICommTeams_updateTeamDetails POST metadata, team identity, current ORA_ACTIVE status, action=inactivate with exact TeamId, expected ORA_INACTIVE status, immutable archive, verification method, and fresh explicit approval |
| When continuation is blocked | Failure class, affected field or action, verified evidence boundary, and one safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Internal ADF operation bindings or internal sender-profile REST calls are found | Do not treat them as supported customer APIs |
| A parent TeamId is unavailable or ambiguous | Do not call the by-ID readback route or guess an identifier; resolve it from the fresh task export first |
| An example DAT, source accessor, or TASK_CSV export is available | Do not treat it as a Data Loader child import, lookup, parent-reference, import-success, or readback contract |
| An FSM fallback route is selected | Do not generate a REST sample, add RestAction, or prepare child-association rows |
| Generic Data Loader workbook conversion reports that REST-excluded `TeamId` is configured as a key, or that the UCM template has no `METADATA` section | Do not use the returned diagnostic text as a DAT source and do not modify generic Data Loader code. Treat the registration as unpublished or invalid, correct and publish the registration, then regenerate the current workbook and revalidate. |
| The archive or approval no longer matches | Do not upload; generate a new immutable preview and approval |
| A live import has an uncertain outcome | Do not retry until task-level CSV readback establishes the current value |
| An Activate or Inactivate lifecycle action has not been explicitly requested, exactly previewed, and freshly approved | Do not submit a lifecycle status-update archive |
| A requested child association lacks a current resolved parent or dependency value | Do not silently omit it, guess an ID, or hand-build a payload outside the generated child-sheet contract |
| A REST parent create has no creator TeamMembers row in its child archive | Do not submit the child archive; resolve the persisted creator exactly and rebuild it with that row |
| A required contract is TBD | Do not invent a field, service, role, permission, payload, dependency resolver, default, or action |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MCT.EXECUTION_GATE | decision | 6 | execution_gate | evidence_available->MCT.EVALUATE_RESULT;blocked->MCT.HANDLE_ERROR | MCT.ENFORCE_DESIGN | stop | An exact immutable selected-route FSM or REST Data Loader archive and current approval or verification evidence, or a fully gated lifecycle preview, is evaluated |
| MCT.HANDLE_ERROR | step | 8 | error_handler | disclosed->MCT.RETURN_ISSUES | none | stop | Any input, lookup, dependency, design, lifecycle, approval, execution, or verification condition is blocked |
| MCT.RETURN_SUCCESS | terminal | 9 | terminal | none | MCT.EVALUATE_RESULT | stop | The routed FSM or REST Data Loader action, requested top-level readback, or approved lifecycle action completed with the required evidence |
| MCT.RETURN_ISSUES | terminal | 10 | terminal | none | MCT.HANDLE_ERROR | stop | One or more blockers prevent safe completion |
