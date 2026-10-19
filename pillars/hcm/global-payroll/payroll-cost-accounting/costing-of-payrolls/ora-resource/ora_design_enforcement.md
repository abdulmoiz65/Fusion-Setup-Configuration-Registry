# Costing of Payrolls HDL Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Select HDL route | Use only the documented HDL Create, Update, End Date or Zap route. If Correct is requested, stop because no source-backed HDL Correct contract exists; never select a REST fallback. |
| 2 | Verify operation prerequisites | Resolve payroll/LDG identity. Create/Update validate runtime KFF values; Create requires absence. Update/End Date require complete latest-interval history and account baselines; End Date does not revalidate unchanged KFF values. Zap requires complete logical history and all physical account identities; it skips KFF validation. |
| 3 | Preserve template contract | Enforce the explicit operation-specific DAT contract (two members for Create/Update; parent-only for End Date; parent plus resolved account DELETEs for Zap), current loader schema, resolved user keys and subtype-specific account representation. |
| 4 | Apply operation rule | Use MERGE for Create and effective-dated Update; generate SubTypeSequence 1 through N in supplied account-row order and prepend the update-only future-change instruction for every Update. Create defaults its parent end to 4712/12/31; do not apply this to Update or Correct. End Date uses only a parent MERGE with the unchanged start, requested end and ReplaceLastEffectiveEndDate=Y, without SET. Zap uses the dedicated identity-only DELETE contract for the parent and every resolved account. |
| 5 | Apply payroll design guidance | For Create/Update, review suspense and default account coverage without inventing an account. Zap retains every resolved subtype in the deletion scope. |
| 6 | Gate the handoff | Require source/schema and Task Hook success, the immutable archive preview, and core.data-loader's single current approval before submission. |
| 7 | Verify outcome | Require terminal loader success for all submitted objects (two for Create/Update, one for End Date), then compare the exact parent and accounts. Update preserves earlier history and prior interval accounts. End Date preserves history except the selected end, verifies accounts on that end date and verifies absence the next day. Zap instead requires terminal success for every included object and absence across the saved complete history. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every Create, Update, End Date or Zap | Blocker | | A mutation route other than HDL through core.data-loader is selected. | Use the approved HDL archive workflow. Read-only lookup GET is not a mutation route. | Yes |
| Create payroll identity | Blocker | resolve_create_payroll | The payroll is not uniquely resolved in the selected LDG at the requested start, or the canonical HDL key is unresolved. | Resolve one payroll definition and its HDL key before source preparation. | No |
| Create LDG and flex | Blocker | resolve_costing_ldg | The LDG selection is ambiguous, does not match the payroll, or lacks its costing flex discriminator. | Use the canonical LDG name and its CostAllocationIdFlexNumber, also called IdFlexNum. | No |
| Create absence | Blocker | query_payroll_costing | At least one active parent exists for PAY, the resolved PayrollId, LDG, and requested start, or the absence evidence is incomplete. | Stop Create. Offer separately selected Update or same-start Correct; never switch automatically. Correct requires its own future execution contract. | No |
| Create KFF | Blocker | resolve_runtime_costing_kff | Runtime field mapping, order, delimiter, discriminator, or required LOV bindings are unavailable or inconsistent. | Resolve the current descriptor for the selected LDG instead of inferring segments from an example. | No |
| Create account values | Blocker | validate_payroll_costing_segments | Account values fail runtime validation or the Create subtype representation and totals contract. | Correct the source values and rebuild the expected account result before preview. | Yes |
| Correct | Blocker | | This task has no source-backed HDL Correct contract. | Stop as unsupported. Do not invoke or require a REST write, a prior REST failure, a reconciled-failure flag, or fallback approval. | No |
| Create or effective-dated Update HDL member | Blocker | | The source omits the PAY identity, changes METADATA order, or invents a source key, source type, segment, subtype, percentage, or a sequence outside the documented consecutive default. | Preserve the source-backed identity and validated template; generate SubTypeSequence 1 through N in supplied account-row order. | Yes |
| Create or effective-dated Update preparation | Blocker | | A successful prerequisite check, render, archive, or validation step is treated as an intermediate pause. | Continue through defaults, DAT render, source/schema validation, immutable ZIP, and Task Hook preview before requesting fresh approval. | Yes |
| Update | Blocker | query_payroll_costing_history | Complete current state, supported latest-interval scope, full preserved account distribution, explicit changed attributes, or SET PURGE_FUTURE_CHANGES N in either DAT is missing. | Apply the verified Update contract; omit parent EffectiveEndDate and preserve all nonrequested account values. | No |
| Payroll account design | Warning | | Suspense or default account coverage has not been reviewed. | Oracle documents suspense and default accounts at payroll level as a best practice; do not invent them when absent from the approved source. | Yes |
| Before submission | Blocker | | The immutable archive or exact approval is absent, stale, or scoped to another environment or operation. | Recreate the preview and obtain fresh approval. | Yes |
| Create gate freshness | Blocker | | Payroll/LDG selection, start date, account input, source fingerprint, or prerequisite evidence changed since preparation, or the absence evidence is stale. | Restart the declared Create preflight and prepare a new immutable preview. Do not submit using old evidence or repeat the original import. | No |
| End Date | Blocker | query_payroll_costing_history | Latest-row selection, valid date bounds, unchanged start, complete account baseline or exact parent-only contract is missing. | Preserve history and accounts; use one parent MERGE with requested end and ReplaceLastEffectiveEndDate=Y, without SET directives. | No |
| End Date special attribute | Blocker | | Shared loader validation rejects ReplaceLastEffectiveEndDate or it is removed to evade validation. | Retain the authored contract and report the validator error. Do not modify core.data-loader, bypass validation or use a direct import/REST write. Component Details Date Effectivity is the capability authority. | No |
| Zap scope | Blocker | query_payroll_costing_history | The supplied start does not select exactly one logical allocation, or deletion is limited to one split. | Zap deletes the complete CostAllocationId history and all resolved accounts, including dates before and after the selector. Do not reinterpret account-only Delete, Delete (ED Split) or ambiguous Delete as Zap. | No |
| Zap readiness | Blocker | query_payroll_costing_history_accounts | Complete historical parent/account evidence or loader validation of DELETE support, keys and package is missing. | Prepare the exact identity-only DELETE archive and use core.data-loader dependency processing; ZIP order alone does not prove load order. Never assume parent deletion cascades to the separate account business object. | No |
| Zap preparation | Blocker | | A successful lookup or render is treated as an intermediate pause. | Complete defaults, DAT rendering, source/schema validation, immutable ZIP and Task Hook preview before asking for approval; stop only at an actual failure. | Yes |
| Zap execution approval | Blocker | | Approval does not cover the exact environment, entire logical history and all resolved account targets. | Show the complete validated scope and obtain one core.data-loader approval as destructive confirmation. Approval is required at execution, not before source preparation. If scope or artifact changes invalidate the preview and approval; the approved handoff follows core.data-loader integrity checks. | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_costing_ldg | Create/Update identity and KFF resolution; End Date/Zap canonical LDG identity only. | Exact LDG ID, canonical Name, and IdFlexNum. | ora_reference_lookups.md |
| resolve_create_payroll | Create, Update, End Date or Zap identity resolution. | Exact payroll definition, SourceId, and canonical HDL key. | ora_reference_lookups.md |
| query_payroll_costing | Create pre-check, Update/End Date baseline, or post-load verification. | Complete active-state absence before Create; exact parent/account facts after load. | ora_reference_lookups.md |
| resolve_runtime_costing_kff | Create or Update account preparation. | Descriptor, segment columns/order, delimiter, and LOV bindings. | ora_reference_lookups.md |
| validate_payroll_costing_segments | Create or Update account preparation. | Validated component values and full-account representations. | ora_reference_lookups.md |
| query_payroll_costing_history | Update, End Date or Zap preflight and verification. | Complete effective history, operation-specific latest interval and immutable baseline. | ora_reference_lookups.md |
| query_payroll_costing_history_accounts | Zap preflight. | Complete historical parents and physical account identities, or proof of zero children. | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COP.HDL.ENFORCE_ROUTE | decision | 30 | design_enforcement | ready_create->COP.HDL.GATE_CREATE;ready_update->COP.HDL.GATE_UPDATE;blocked->COP.HDL.HANDLE_ERROR | COP.HDL.CHECK_DEPENDENCIES | stop | Before handoff, require the applicable successful source-validation node and all branch-specific lookup facts. Create uses COP.CREATE.VALIDATE_SOURCE; Update uses COP.UPDATE.VALIDATE_SOURCE. |
| COP.END_DATE.ENFORCE | decision | 31 | design_enforcement | ready->COP.END_DATE.GATE;blocked->COP.HDL.HANDLE_ERROR | COP.END_DATE.VALIDATE_SOURCE | stop | Enforce parent-only End Date scope, preserved history/accounts and exact loader-approved source. Approval is obtained only for this immutable archive. |
| COP.ZAP.ENFORCE | decision | 38 | design_enforcement | ready->COP.ZAP.GATE;blocked->COP.HDL.HANDLE_ERROR | COP.ZAP.VALIDATE_SOURCE | stop | Require complete logical history and exact account scope, loader-approved DELETE archive and successful Task Hook rules. Prepare the destructive preview before the single core.data-loader approval gate. |
