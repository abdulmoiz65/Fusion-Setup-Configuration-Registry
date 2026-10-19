# Approval Rules Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Approval process name is missing | Classify as input validation; ask for the exact approval process name. |
| Process lookup finds no match | Classify as catalog mismatch; show the submitted name and ask the user to verify it. |
| Process lookup finds multiple matches | Classify as input validation; show candidates and require an explicit selection. |
| Participant prerequisites are incomplete | Classify as input validation; show the selected participant type and missing prerequisite. |
| A simplified rule exceeds documented limits or needs advanced conditions | Classify as input validation; direct maintenance to BPM Worklist advanced mode. |
| Read-only lookup fails | Classify as auth/authz, transport/environment, or Fusion API as applicable; preserve a redacted diagnostic. |
| A mutation is requested without a registered write contract | Classify as approval blocker; do not infer an endpoint, payload, or verification method. |
| writeRulesFile returns HTTP 200 but read-back does not yet show the approved rule file | Poll only the declared readRulesFile verification path for the same ProcessId at intervals no greater than 60 seconds, up to 100 seconds total; do not resend the write. |
| The 100-second post-write polling timeout expires without a matching rule file | Classify as process timeout; preserve the last sanitized status and stop without retrying the write. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input validation | Missing rule, participant, automatic-action, or parallel-approval inputs | Return the exact missing inputs and correction guidance. |
| catalog mismatch | No exact configured process matches the supplied name | Verify the task and process name against the source environment. |
| auth/authz | A supported read-only lookup is denied | Confirm identity and privileges; refresh a cached token once only when the workflow permits it. |
| transport/environment | A supported read-only lookup cannot reach the selected environment | Record environment and operation; retry only through the governed workflow. |
| Fusion API | Fusion returns a read-only API error | Preserve redacted status/error details and report the recommended correction. |
| approval blocker | No approved write adapter or immediate execution approval is available | Stop before any state-changing request. |
| process timeout | The 100-second readRulesFile verification timeout expires | Report ProcessId, last sanitized read status, elapsed wait, and a safe next-check path; do not resend writeRulesFile. |
| process failed | readRulesFile returns a complete rule file that does not match the approved candidate | Preserve a sanitized structural comparison and require a new preview and approval before any further write. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Lookup failure | Environment, read-only operation, failure category, and redacted error/status details. |
| Ambiguous process | Submitted name, returned candidates, and the required selection action. |
| Write-contract blocker | Business object, missing contract elements, and the next authoring action; never show or construct a speculative payload. |
| Post-write verification | HTTP status, sanitized return.description, ProcessId, polling elapsed time, last read status, and verification outcome. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A write endpoint or payload is absent from the registered contract | Do not infer REST paths, request bodies, headers, actions, or verification behavior from UI screenshots or a read-only lookup. |
| Immediate explicit approval is absent | Do not create, update, delete, publish, import, or invoke a state-changing action. |
| Multiple processes match | Do not select a process automatically. |
| A write returns HTTP 200 but the rule file is not yet visible | Do not resend writeRulesFile; use only the bounded readRulesFile verification path for the same ProcessId. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| APPROVAL_RULES.INPUT_ISSUE | terminal | 6 | terminal | none | APPROVAL_RULES.VALIDATE_INPUT | stop | Required design information is absent or invalid |
| APPROVAL_RULES.DESIGN_ISSUE | terminal | 7 | terminal | none | APPROVAL_RULES.ENFORCE_DESIGN | stop | A documented design gate blocks the requested rule |
| APPROVAL_RULES.PROCESS_ISSUE | terminal | 8 | terminal | none | APPROVAL_RULES.RESOLVE_PROCESS | stop | No exact process match exists or multiple matches need selection |
| APPROVAL_RULES.LOOKUP_ISSUE | terminal | 9 | terminal | none | APPROVAL_RULES.RESOLVE_PROCESS | stop | A supported read-only lookup fails |
| APPROVAL_RULES.WRITE_CONTRACT_REQUIRED | terminal | 10 | terminal | none | APPROVAL_RULES.VERIFY_WRITE_CONTRACT | stop | A mutation is requested without a registered write contract |
| APPROVAL_RULES.WRITE_CONTRACT_AVAILABLE | terminal | 11 | terminal | none | APPROVAL_RULES.VERIFY_WRITE_CONTRACT | stop | The registered write contract is complete; obtain a current immutable preview and explicit approval before execution |
