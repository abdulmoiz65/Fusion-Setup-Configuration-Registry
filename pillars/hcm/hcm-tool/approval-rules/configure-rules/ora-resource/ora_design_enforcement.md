# Approval Rules Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Select the maintenance surface | Use the FSM HCM Approval Rules UI for supported straightforward rules. Use BPM Worklist for Advanced Mode, complex rules, approval groups, notification or process settings, or unsupported simplified-UI tasks. |
| 2 | Resolve existing rule scope | Resolve one ProcessId, one ruleset, and the current rule file before summarizing or changing a rule. |
| 3 | Define conditions | Configure IF conditions with complete AND or OR logic; use Advanced Mode collection patterns where every rule condition must be evaluated. |
| 4 | Design participants | Select supported participant types and configure the associated management, job-level, position, user, group, role, or AOR attributes. |
| 5 | Configure routing | Use Single, Serial, Parallel, or FYI according to the required behavior. For Parallel, select First Responder Wins or configure voting percentages and the default outcome. |
| 6 | Gate mutation | Build a complete ruleset graph, fresh immutable preview, and explicit approval before one verified write. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A rule was created in BPM Worklist Advanced Mode | Blocker |  | The user attempts to edit it in the HCM simplified UI | Continue maintenance in BPM Worklist | Yes |
| Multiple rules apply to one task | Blocker |  | Rule priorities are not intentionally ordered, ties are relied on for deterministic behavior, the shared IF does not path to every unique RULE node, or a rule lacks its own condition, THEN, or participant branch | Assign distinct priorities and retain one complete local branch for every rule | Yes |
| Every rule | Blocker |  | Rule status, priority, and condition type are incomplete; a conditional rule does not default to High unless overridden; or a payload condition omits documented operand metadata and expression text | Set active or inactive status, use High for a new conditional rule unless overridden, and retain complete source-backed condition logic | Yes |
| A payload condition is serialized | Blocker |  | The condition does not serialize lhsOperand as the supplied payload path, lhsOperandId as Task.payload plus that path, lhsOperandType as Attribute, ruleNodeAlwaysValidFlag and alwaysValid as true, String rhsOperandId and rhsOperand as quoted JSON-string literals with escaped quotes, testInCode with the fully qualified Task.payload path, testInText with the supplied path, and the requested comparison operator | Retain the complete payload-condition serialization from the supplied rules JSON guidance | Yes |
| A process is summarized or changed | Blocker | find_approval_process_by_exact_name | The process is absent or ambiguous | Resolve one exact process before presenting or changing rules | Yes |
| A resolved process is summarized or changed | Blocker | find_ruleset_by_process_id | The ruleset finder returns no single nonblank ruleset name, or the current rule file has not been read | Resolve one ruleset name with find_ruleset_by_process_id, then read the current rule file before presenting or changing rules | Yes |
| Multiple IF conditions are used | Blocker |  | AND or OR logic is incomplete or does not express the required condition grouping | Define the complete condition expression before configuring the Then action | Yes |
| Nullable payload object or attribute is evaluated | Blocker |  | Null handling is absent for a supported Change Personal Information condition | Use Automatically build a null condition and review the resulting condition expression | Yes |
| Management hierarchy routing is used | Blocker | resolve_approval_chain_users | A common approval user has not been resolved, or the participant omits a documented SupListBuilder field or graph path | Resolve the user expression and retain the exported SupListBuilder contract | Yes |
| Management hierarchy or job-level routing is used | Blocker | find_supervisor_types | The selected supervisor type is not returned by the current lookup | Select one returned supervisor type before serializing the participant | Yes |
| Position routing is used | Blocker | find_position_hierarchies | The Position Hierarchy participant omits a documented PosListBuilder field, uses a hierarchy not returned by the current lookup, or lacks the graph path required by the selected participant sequence | Use the exported PosListBuilder contract and populate the selected hierarchy from the current lookup | Yes |
| Position routing bounds are used | Blocker | find_positions_by_tree_code | The starting or top position is not returned for the selected hierarchy | Populate the selected bounds from the current position lookup and retain action, inclusion, compatibility, dimension, and path fields | Yes |
| Job-level routing is used | Blocker | find_supervisor_types | Approval chain, starting and top approvers, inclusion behavior, a documented JobListBuilder field, or the graph path is not defined | Retain the environment-generated JobListBuilder contract: nodeText Job-Level-Based Line Manager Hierarchy; listBuilderType JobListBuilder; jobListApprovalCompatible true; jobListBuilderActionType Approval Required; jobListBuilderApprovalChainOf and jobListBuilderUptoApprover Task.payload.transactionApprovalRequest.Requestor; jobListBuilderUptoApproverUser and jobListBuilderTopApproverUser empty strings; jobListBuilderStartWith User; jobListBuilderMinimumJobLevel 1; jobListBuilderTopApprover Manager; jobListBuilderIncludeApprovers IncludeApproversType.LAST; jobListBuilderUserTree Task.payload.transactionApprovalRequest.Requestor; and an explicit paths array. | Yes |
| Responsibility holder is used | Blocker | find_representative_types | The representative type is not returned or assigned for the transaction subject, the participant uses an incorrect approver type, or it omits a documented Representative ResListBuilder field or graph path | Select one returned responsibility type and retain the exported Representative participant contract | Yes |
| Approval group is used | Blocker | find_approval_groups | ApprovalGroupListBuilderGroup is not one exact current lookup result, or the PARTICIPANT node omits nodeText Approval Groups, listBuilderType ApprovalGroupListBuilder, approverType ApprovalGroup, ApprovalGroupListBuilderallowEmpty as the String true, ApprovalGroupListBuilderActionType Approval Required, or the required graph path; or the node includes dimensionId | Select one returned approval group, confirm its valid composition, omit dimensionId, preserve ApprovalGroupListBuilderallowEmpty as the JSON String true, and use a unique end-edge path to the next in-ruleset participant when one is selected. Do not copy the sample group name into another rule | Yes |
| Application role is used | Blocker | find_application_roles | The selected application role is not returned by the lookup | Select one returned application role | Yes |
| Ignore Participant is selected | Blocker |  | The ignored participant remains relied upon by another route or outcome | Confirm that the rule condition is intended to omit the participant | Yes |
| Self Auto Approve is selected | Blocker |  | The rule does not explicitly state that approval should be automatic without routing to approvers | Use Self Auto Approve only for the documented condition that requires no actual approver | Yes |
| Participant type is Parallel | Blocker |  | Bypass Approvals is enabled, or the supported parallel method and required voting values are incomplete | Disable Bypass Approvals and complete exactly one supported parallel approval method | Yes |
| Participant type is Serial, Sequence, or FYI | Blocker |  | A valid rule set is not specified for the participant | Assign the intended valid rule set before submission | Yes |
| A single- or multiple-rule or participant candidate is prepared | Blocker |  | The candidate is a partial patch, does not retain the exact finalJsonResponse ruleset, omits a shared-IF path to an included RULE, reuses a graph-node or condition-node ID, has duplicate rule or condition names, changes a source-generated routing wrapper, or contains a path whose target node is absent | Build one complete ruleset graph from the fresh baseline and preserve UI-generated routing exactly | Yes |
| A multiple-participant routing shape is serialized | Blocker |  | A selected participant omits a documented builder field or required path, or requires a field absent from both the exported contract and fresh baseline | Retain documented builder fields and explicit paths; obtain an environment-generated example for an undocumented routing field | No |
| Automatic approval or rejection is used | Blocker |  | Routing is not Workflow System or Submitter, Auto Action Enabled is not True, or Auto Action is not APPROVE or REJECT | Complete the automatic-action Then configuration | Yes |
| A live Approval Rules write is requested | Blocker |  | No fresh baseline, immutable preview, exact approval record, or post-write read-back verification is available | Use the separately gated write adapter; do not call writeRulesFile from a summary workflow | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_approval_process_by_exact_name | Before summarizing or changing a process | Exact ProcessId and process name | ora_reference_lookups.md |
| find_ruleset_by_process_id | After an exact ProcessId resolves and before reading or changing rules | One nonblank ruleset name | ora_reference_lookups.md |
| resolve_approval_chain_users | Before building common approval-user hierarchy settings | Process-specific fully qualified approval-user expression | ora_reference_lookups.md |
| find_position_hierarchies | Before using a position hierarchy | Selected position tree code | ora_reference_lookups.md |
| find_positions_by_tree_code | After selecting a position hierarchy | Valid starting and top positions | ora_reference_lookups.md |
| find_supervisor_types | Before management or job-level hierarchy routing | One returned supervisor type | ora_reference_lookups.md |
| find_representative_types | Before a Representative participant | One returned responsibility or representative type | ora_reference_lookups.md |
| find_application_roles | Before an Application Role participant | One returned application role | ora_reference_lookups.md |
| find_approval_groups | Before an Approval Group participant | One returned approval group | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| APPROVAL_RULES.ENFORCE_DESIGN | decision | 4 | design_enforcement | passed->APPROVAL_RULES.VERIFY_WRITE_CONTRACT;blocked->APPROVAL_RULES.DESIGN_ISSUE | APPROVAL_RULES.APPLY_DEFAULTS | stop | A Configure Rules design has passed initial validation |

## Sources

- Legacy Approval Rules Configure Rules design-enforcement guidance
- User-provided serialized Approval Rules JSON examples
