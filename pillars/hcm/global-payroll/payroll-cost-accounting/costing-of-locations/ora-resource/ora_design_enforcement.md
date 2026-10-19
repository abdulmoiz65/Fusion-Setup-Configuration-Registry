# Location Costing Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Fix operation | Preserve the operation selected before the first lookup; Create may stop for an explicit Update-or-Correct choice but may not switch silently. |
| 2 | Validate branch evidence | Require only the exact lookup outputs declared for that operation and reject evidence from another branch. |
| 3 | Enforce costing policy | Validate effective dates, distributions, physical identity, history scope, and destructive intent. |
| 4 | Gate handoff | Require an active authorized import workflow, current template validation, immutable preview, and fresh approval. This resource does not build or execute the import. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Query | Error | query_location_costing | The request attempts a mutation, current-state identity is ambiguous, or the response cannot be normalized. | Return the one read-only result or an explicit empty result without a second GET. | Yes |
| Create | Error | resolve_location_source | Location evidence is not the complete no-Costing pattern, account input is empty or invalid, the total exceeds 1, or required Set and KFF dependencies are absent. | Continue only from complete Create-absence evidence; otherwise require an explicit Update or Correct request. | Yes |
| Update | Error | query_location_costing | Exact current state, SetCode, KFF layout, effective date, nonempty replacement distribution, generated sequence, or future-change directive is missing. | Use the one resolved current state and validate the full replacement collection before handoff. | Yes |
| Correct account MERGE | Error | query_location_costing | Exact physical account scope, resolved SourceSubType, a positive resolved or explicit SubTypeSequence, current KFF layout, or one-action scope is missing. | Preserve returned identity and sequence; when REST omits the sequence, ask for one positive explicit value. | Yes |
| Correct child DELETE | Error | query_location_costing | The child is not selected from the exact current-state response, physical identity is incomplete, every current child would be removed, or confirmation is not literal true. | Delete one bound child only; treat removal of the complete allocation as Zap. Do not require runtime KFF. | Yes |
| End Date | Error | query_location_costing_history | History is incomplete, the target is not the latest effective parent, the requested end is outside the returned range, ReplaceLastEffectiveEndDate is not Y, or confirmation is not literal true. | Recompute the target from the same complete history and re-preview. | Yes |
| Zap | Error | query_location_costing_history_accounts | History is incomplete, a historical parent lacks one exact bound detail response, returned physical child identity cannot be preserved, template validation fails, or confirmation is not literal true. | Use complete history and its bound account fan-out, then validate the returned child fields with the current loader template. | Yes |
| Delete or ED Split | Error | | No supported standard contract was provided. | Stop without substituting direct REST or another business object. | No |
| Mutation handoff | Error | | The active workflow, template validation, immutable artifact, target environment, or fresh exact approval is missing. | Remain at the handoff gate. The ora-resource files do not construct DAT or ZIP files and do not call Data Loader. | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_location_source | Create | CreatePresenceResult; LocationId; LocationCode. | ora_reference_lookups.md |
| query_location_costing | Query, Update, or Correct | CurrentParent; CurrentAccounts; PhysicalAccountIdentity; ReturnedSubTypeSequence. | ora_reference_lookups.md |
| query_location_costing_history | End Date or Zap | EffectiveHistory; HistoricalParentKeys; LatestEffectiveParent. | ora_reference_lookups.md |
| query_location_costing_history_accounts | Zap | ZapHistoryParents; ZapHistoryAccounts; CompleteHistoryAccountFanout. | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LCP.ENFORCE_DESIGN | decision | 720 | design_enforcement | ready_create->LCP.GOVERNED_DATALOADER_HANDOFF;ready_update->LCP.GOVERNED_DATALOADER_HANDOFF;ready_correct->LCP.GOVERNED_DATALOADER_HANDOFF;ready_end_date->LCP.GOVERNED_DATALOADER_HANDOFF;ready_zap->LCP.GOVERNED_DATALOADER_HANDOFF;blocked->LCP.HANDLE_ERROR | LCP.APPLY_DEFAULTS | stop | Enforce only the selected mutation policy and preserve its outcome for a distinct handoff terminal. |
