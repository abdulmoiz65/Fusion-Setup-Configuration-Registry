# Approval Rules Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Approval process | Resolve one exact approval process and retain its ProcessId for analysis. |
| 2 | Rule prerequisites | Confirm the selected participant type and its required setup, such as representative responsibilities or a usable approval group. |
| 3 | Advanced-mode ownership | Confirm that a complex rule is maintained in BPM Worklist rather than the simplified approval-rule UI. |
| 4 | Registered write contract | Obtain a governed REST write adapter with an exact endpoint, request contract, verification contract, and approval gate before any mutation. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| approval_process_identity | Exact approval process | Yes | Always | Lookup | User-supplied process name and read-only process lookup | find_approval_process_by_exact_name | Rules must be associated with one unambiguous process | Provide the exact process name; select one result if the source system returns candidates | ProcessId and process name |
| participant_prerequisites | Participant prerequisites | Conditional | A participant type needs related setup | Verify | Rule design and applicable participant setup | | Some participants require setup outside the rule itself | Confirm the selected participant can be resolved before submitting a policy change | Participant type and required related setup |
| advanced_mode_ownership | Advanced-mode ownership | Conditional | The design exceeds simplified-mode limits or requires complex conditions | Verify | Rule design and Oracle advanced-mode guidance | | Advanced-mode rules are maintained in BPM Worklist | Confirm the intended maintenance surface before continuing | Maintenance surface and rule complexity decision |
| registered_write_contract | Registered write execution contract | Yes | A create, update, delete, or publish action is requested | Verify | User-provided Data Loader Business Object Registration screenshots and writeRulesFile/readRulesFile contract |  | The supplied contract identifies both custom actions, their request fields and headers, POST, the return.description result, a maximum 60-second polling interval, a 100-second total verification timeout, and an approved executor | Build an immutable preview and obtain explicit approval immediately before execution | Write path: /resources/11.13.18.05/businessProcessApprovalRules/action/writeRulesFile; write method: POST; processId: number; rulesJson: java.lang.String; isCommitRequired: boolean; write Content-Type: application/vnd.oracle.adf.action+json; REST-Framework-Version: 9; write response: return.description commit message; verify POST /hcmRestApi/resources/11.13.18.05/businessProcessApprovalRules/action/readRulesFile with Content-Type: application/vnd.oracle.adf.action+json and RuleSetNamae/processId body; poll interval maximum: 60 seconds; total verification timeout: 100 seconds; approved executor: Codex skill invoker or runbook |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| input validation | Required design information is absent or inconsistent | Read-only lookup only after required identity is supplied |
| catalog mismatch | The selected task or business object does not match the available contract | No |
| approval blocker | A mutating action lacks an approved registered write contract or immediate approval | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | Value Source | Resolver | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|---|
| APPROVAL_RULES.VERIFY_WRITE_CONTRACT | decision | 5 | resolve_dependency | contract_missing->APPROVAL_RULES.WRITE_CONTRACT_REQUIRED;contract_available->APPROVAL_RULES.WRITE_CONTRACT_AVAILABLE | APPROVAL_RULES.ENFORCE_DESIGN | stop | A create, update, delete, or publish action is requested | User-provided Data Loader Business Object Registration screenshots and writeRulesFile/readRulesFile contract |  | Write path: /resources/11.13.18.05/businessProcessApprovalRules/action/writeRulesFile; write method: POST; processId: number; rulesJson: java.lang.String; isCommitRequired: boolean; write Content-Type: application/vnd.oracle.adf.action+json; REST-Framework-Version: 9; write response: return.description commit message; verify POST /hcmRestApi/resources/11.13.18.05/businessProcessApprovalRules/action/readRulesFile with Content-Type: application/vnd.oracle.adf.action+json and RuleSetNamae/processId body; poll interval maximum: 60 seconds; total verification timeout: 100 seconds; approved executor: Codex skill invoker or runbook |

## Sources

- [Approver Types](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/approver-types.html#Management-Hierarchy-or-Supervisory-Hierarchy)
- [Configure HCM Approval Rules Using Advanced Mode](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/configure-hcm-approval-rules-using-advanced-mode.html)
- [List Builders](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/list-builders.html#Approval-Group)
- User-provided Data Loader Business Object Registration screenshot for businessProcessApprovalRules and writeRulesFile
- User-provided Data Loader Business Object Registration headers screenshot for writeRulesFile
- User-provided writeRulesFile method and response contract
- User-provided writeRulesFile post-write readRulesFile verification contract
