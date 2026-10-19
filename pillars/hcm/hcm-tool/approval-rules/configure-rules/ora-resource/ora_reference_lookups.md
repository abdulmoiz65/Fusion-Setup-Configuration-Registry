# Approval Rules Reference Lookups

Only the following read-only lookups are supported by the supplied sources. Do
not derive a mutation endpoint from a discovery request.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_approval_process_by_exact_name | An exact approval process name is supplied for analysis | Approval process name | /hcmRestApi/resources/11.13.18.05/businessProcessApprovalOptions?finder=findByProcessName;Name={url_encoded_approval_process} | Name, ProcessId, and returned process-configuration flags needed for review | Exact process-name match; retain one selected process | ProcessId and process name | No match: report process not found. Many matches: present candidates and require user selection; do not choose one automatically. |
| find_ruleset_by_process_id | An exact approval process has resolved to one ProcessId and rules must be read or changed | ProcessId | /hcmRestApi/resources/11.13.18.05/businessProcessApprovalRuleConditions?finder=findByParentNameAndProcessId;ProcessId={process_id} | Returned ruleset name | Retain exactly one nonblank ruleset name returned by the finder | RuleSetNamae for the rule-file action and resolved ruleset name for the run record | No nonblank ruleset name: stop and report ruleset not found. More than one distinct nonblank ruleset name: stop and require an explicit ruleset selection; do not choose one. |
| resolve_approval_chain_users | Approval-chain or hierarchy-tree settings use Worker, Requestor, Worker's Current Line Manager, or Worker's Proposed Line Manager | ProcessId | POST /hcmRestApi/resources/11.13.18.05/businessProcessApprovalBuilderRules/action/getUsersForApproval with Content-Type application/vnd.oracle.adf.action+json and body processId | getApprovalUsers for the supported common approval users | Use the nonblank fully qualified expression returned for the selected common approval user; do not substitute or infer an expression | Approval-chain and hierarchy-tree user paths | Stop when the action fails, the requested user key is absent or blank, or incompatible values are returned. |
| find_position_hierarchies | A Position Hierarchy list builder is selected | None documented | POST /hcmRestApi/resources/11.13.18.05/businessProcessApprovalBuilderRules/action/getPositionhierarchies | Returned position hierarchies | User selects exactly one returned hierarchy | Position tree code | Stop until exactly one returned hierarchy is selected. |
| find_positions_by_tree_code | A position hierarchy was selected | Position tree code | POST /hcmRestApi/resources/11.13.18.05/businessProcessApprovalBuilderRules/action/getPositions | Valid positions in the selected tree | Use the selected exact tree code to retrieve valid starting and top positions | Starting and top position IDs | Stop when the tree has no valid positions or either selected position is absent. |
| find_supervisor_types | A Management Hierarchy or Job Level Based Line Manager Hierarchy participant is selected | lookupType=PER_SUPERVISOR_TYPE | POST /hcmRestApi/resources/11.13.18.05/businessProcessApprovalBuilderRules/action/getRepresentativeTypes with Content-Type application/vnd.oracle.adf.action+json | Returned supervisor types | User selects exactly one returned supervisor type | Selected supervisor type | Stop until exactly one returned supervisor type is selected. |
| find_representative_types | A Representative participant is selected | lookupType=PER_RESPONSIBILITY_TYPES | POST /hcmRestApi/resources/11.13.18.05/businessProcessApprovalBuilderRules/action/getRepresentativeTypes with Content-Type application/vnd.oracle.adf.action+json | Returned responsibility and representative types | User selects one supported returned responsibility or representative type | Selected representative type | Stop until one returned representative type is selected. |
| find_application_roles | An Application Role participant is selected | None documented | POST /hcmRestApi/resources/11.13.18.05/businessProcessApprovalBuilderRules/action/getApplicationRoles with Content-Type application/vnd.oracle.adf.action+json | Returned application roles | User selects exactly one returned application role | Selected application role | Stop until exactly one returned application role is selected. |
| find_approval_groups | An Approval Group participant is selected | None documented | POST /hcmRestApi/resources/11.13.18.05/businessProcessApprovalBuilderRules/action/getApprovalGroups with Content-Type application/vnd.oracle.adf.action+json | Returned approval groups | Return nonblank group names and require the user to select exactly one | Selected approval group name | Stop when the result is absent, malformed, empty, or no exact selection is supplied. |
| read_rules_file_for_process_and_ruleset | A resolved exact ProcessId and ruleset name require rule-file analysis or a separately approved writeRulesFile operation requires verification | ProcessId and RuleSetNamae from find_ruleset_by_process_id | POST /hcmRestApi/resources/11.13.18.05/businessProcessApprovalRules/action/readRulesFile; Content-Type: application/vnd.oracle.adf.action+json; body: RuleSetNamae and processId | Returned rules file for sanitized candidate comparison | Use the exact ProcessId and the single nonblank ruleset name resolved by find_ruleset_by_process_id | Sanitized current or verification rule file | For analysis, stop and report an empty or malformed rule file. After a write, poll only this read-only request with no more than 60 seconds between calls and stop after 100 seconds total; do not resend writeRulesFile. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Read-only discovery succeeds | Use the returned ProcessId only for analysis and validation. |
| The lookup returns an authorization or transport error | Stop; record the redacted diagnostic and return the environment, operation, and error category. |
| A write is requested after discovery | Stop at the registered-write-contract dependency; discovery does not authorize or define a write. |
| A writeRulesFile operation returned HTTP 200 | Use read_rules_file_for_process_and_ruleset for the same ProcessId and RuleSetNamae; do not issue another write while polling. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | Resolver |
|---|---|---|---|---|---|---|---|---|
| APPROVAL_RULES.RESOLVE_PROCESS | decision | 2 | reference_lookup | resolved->APPROVAL_RULES.APPLY_DEFAULTS;not_found->APPROVAL_RULES.PROCESS_ISSUE;ambiguous->APPROVAL_RULES.PROCESS_ISSUE;lookup_failed->APPROVAL_RULES.LOOKUP_ISSUE | APPROVAL_RULES.VALIDATE_INPUT | stop | An exact approval process name is supplied | find_approval_process_by_exact_name |

## Sources

- Exported internal Word document: `C:\Users\magupta\Downloads\HCM+Config+Task+UI+screenshots+and+REST+calls+for+BPM+based+flows.doc` (inspected locally; its process-discovery call is reflected above without copying screenshots or payloads)
- [How You Define an HCM Approval Policy](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/how-you-define-an-hcm-approval-policy.html#Summary-of-the-Tasks)
