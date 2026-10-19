# Referral Descriptive Flexfields Design Enforcement

For copy, update, and disable, ask only for Segment Name when missing, then validate a fresh exact-task export for this request; if unavailable or empty, use the qualified Global fallback proposal instead of stopping; label older evidence UNVERIFIED. For new create, use a validated matching package or export fresh when absent. Follow the required-values table, confirmation, optional-values table, confirmation sequence in ../SKILL.md.

These gates apply before preview or any approved CSV/FSM import handoff for IRC_RF_REFERRALS_DFF.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm exact target | Match the Referral task, IRC_RF_REFERRALS_DFF, application 821, and Global or EMPLOYEE_REFERRAL scope |
| 2 | Resolve current-definition evidence | For copy, update, and disable, ask only for Segment Name when missing, then validate a fresh exact-task export for this request; if unavailable or empty, use the qualified Global fallback proposal instead of stopping; label older evidence UNVERIFIED. For new create, use a validated matching package or export fresh when absent. Follow the required-values table, confirmation, optional-values table, confirmation sequence in ../SKILL.md. Preserve the supported scope and exact-identity guards. |
| 3 | Enforce scope and protected context | Preserve EMPLOYEE_REFERRAL and reject every other context or context lifecycle change |
| 4 | Collect and enforce design | Ask for the name first when missing. Then apply the name-based design rules in ../SKILL.md and present a type-compatible proposal from the validated package. Preserve supplied types and clarify ambiguous names. In fallback mode, require explicit confirmation of the complete Global design and disclose that duplicate, storage-occupancy, sequence-occupancy, and target value-set existence checks are unverified |
| 5 | Build and freeze archive | Build and validate the final FSM CSV/ZIP from the analysed package or qualified historical archive-derived contract plus one confirmed Global delta, freeze its bytes, and calculate its SHA-256 checksum; never infer a different package contract or carry historical custom rows into the delta |
| 6 | Bind preview and approval | Route the immutable archive through core.data-loader, show its complete preview, and obtain standalone approval bound to the exact checksum |
| 7 | Submit and monitor | After approval, let core.data-loader revalidate, upload, and initiate once; suppress the acceptance report, monitor to terminal state, download and read the ProcessLog, and return only the final success or error result without retrying submission |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every request | Error | | Task, DFF, application, or scope differs from the exact supported identity | Return UNSUPPORTED or the exact missing identity | No |
| scope = EMPLOYEE_REFERRAL | Error | | The protected context is missing, ambiguous, disabled without approved evidence, or would be created, renamed, or deleted | Preserve exact seeded context EMPLOYEE_REFERRAL; permit only segment-level planning within it | No |
| Inspect requests for Referral DFF segments | Error | | An included context code is not exactly EMPLOYEE_REFERRAL, its displayed context name is not exactly Employee Referral, or the result contains Agency Referral or another unsupported context's rows | Return Global segments plus context-sensitive segments from the exact Employee Referral context | No |
| New Global PlanCreate after a failed, timed-out, or header-only export | Error | | The historical contract checksum/structure is unavailable, any required design value is unconfirmed, the preview hides unavailable current-state checks, or the archive includes historical custom rows as current configuration | Use the verified archive-derived contract, require complete requester confirmation, show unverified duplicate/column/sequence/value-set checks, and build one delta-only Global row | Yes, before approval |
| Inspect, copy, update, disable, verify, or EMPLOYEE_REFERRAL after a failed or header-only export | Error | | The historical Global contract is proposed as current-state evidence | Stop and require a valid populated current-definition package | No |
| scope = Global | Error | | The supplied segment configuration is demonstrably limited to Employee Referral or another unsupported context | Use EMPLOYEE_REFERRAL when the field is Employee Referral-specific | Yes, by revising the approved design |
| PlanCreate or PlanUpdate | Error | | Segment code or business purpose duplicates or overlaps an existing segment | Present the conflict and require an explicit design decision | Yes, by revising the approved design |
| PlanCreate | Error | | Segment code is blank or exceeds 30 characters | Propose a valid code within 30 characters and require requester confirmation; never truncate silently | Yes, before approval |
| PlanCreate | Error | | API Name / SegmentIdentifier is blank, exceeds 30 characters, doesn't begin with an English letter, contains a character other than an English letter or digit, or is a reserved word | Propose a valid alphanumeric API Name such as the source API Name followed by `Copy` with no separator, then require requester confirmation | Yes, before approval |
| PlanCreate or PlanUpdate | Error | | Proposed storage column is occupied or incompatible with the data type; or fallback mode presents a requester-confirmed column as verified unused | Resolve an unused compatible column when current evidence exists. In fallback mode require a compatible requester-confirmed column and mark occupancy `UNVERIFIED`; never overwrite knowingly | Yes, before approval |
| PlanCreate FSM row | Error | | ShortPrompt is blank, SequenceNumber is blank or nonpositive, or the sequence conflicts with a validated local baseline; or fallback mode presents a confirmed sequence as verified unused | Confirm a nonempty short prompt and one positive sequence, disclose unverified occupancy in fallback mode, rebuild the archive, and generate a new checksum preview | Yes, before approval |
| Segment uses an existing value set | Error | | The displayed value-set code or name is missing, ambiguous, or incompatible with the segment data type, table column, or display control | Select one exact compatible existing value set; resolve internal identifiers only through the approved execution adapter | Yes, before approval |
| Segment creates a value set | Error | | Value Set Code, Module, Validation Type, or Value Data Type is missing; an enum is unsupported; or its data type is incompatible with the segment | Collect the next required UI field and use only the supported UI enumerations; API Name and Description remain optional | Yes, before approval |
| Optional required behavior is selected | Error | | Impact on existing referral channels, integrations, or existing data has not been explicitly reviewed | Complete and approve the impact analysis | Yes, before approval |
| Optional default is selected | Error | | Default produces multiple values or is incompatible with the segment type | Use None or one explicit correctly typed default | Yes, before approval |
| Optional BI Enabled = Yes | Error | | BI label or analytics acceptance criteria are absent | Complete the optional reporting configuration | Yes, before approval |
| PlanDisable | Error | | Impact, rollback plan, current usage, or approval is missing; or the target is the protected context | Limit the plan to an exact segment and complete impact and rollback review | Yes, for a supported segment only |
| A copy or duplicate source is omitted | Error | | Source selection is attempted without the conditional task CSV export | Export and list the supported source segments, then require the requester to select one | No |
| PlanCreate or PlanUpdate reaches artifact preparation | Error | | No established package contract or deterministic builder exists, or the archive fails filename, header, encoding, metadata, structure, delta, or checksum validation | Return an artifact-preparation blocker; never invent or submit the package | No |
| A state-changing submission is ready | Error | | The immutable preview is missing, approval is missing or stale, or the archive checksum differs from the approved preview | Rebuild the preview and obtain standalone approval for the exact unchanged archive | Yes, by re-previewing |
| Approved create, update, or copy import was accepted | Error | | Completion monitoring, terminal status reconciliation, or ProcessLog review is omitted | Continue through core.data-loader task-scoped completion monitoring; do not retry or resubmit | No |
| Upload or initiation failed or is uncertain before an accepted request ID exists | Error | | An automatic retry, replay, or replacement submission is proposed | Return the failed or uncertain initiation result and stop | No |
| Direct REST or DFF API access, browser or URL debugging, database DML, automated deployment outside core.data-loader, or automatic retry is requested | Error | | The request bypasses the declared workflow and approval gates | Stop and return the supported workflow | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| REFERRAL_DFF.ENFORCE_DESIGN | decision | 40 | design_enforcement | passed->REFERRAL_DFF.APPROVAL_GATE;blocked->REFERRAL_DFF.RETURN_ISSUES;conflict->REFERRAL_DFF.RETURN_ISSUES;unsupported->REFERRAL_DFF.RETURN_ISSUES | REFERRAL_DFF.CHECK_READINESS | stop | Every supported request |
