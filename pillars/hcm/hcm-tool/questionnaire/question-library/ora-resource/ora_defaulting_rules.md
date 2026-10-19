# Defaulting Rules

Do not promote values observed in a sample DAT, FSM export, another subscriber, REST default, database default, or older source implementation into an HDL default. The approved business design and current target HDL contract govern every emitted value.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| SubscriberName, QuestionCode, and QstnVersionNum | No default | Always | No | |
| Target environment | FSCR | No target environment is explicitly selected for Question Library work | No | |
| QuestionText, QuestionType, ResponseTypeName, CategoryName, Status, PrivacyFlag, and OwnerPersonNumber | No default | Always | No | |
| Approved QuestionType and ResponseTypeName correction | Exact canonical pair selected from the current target candidate catalog | QuestionType or ResponseTypeName was blank or non-exact, the user explicitly approves one complete proposed pair, and the live permitted-type and exact-pair lookups both succeed again immediately before preview | No | propose_question_response_type_pair |
| Approved suggestion-capable reference correction | Exact canonical value or complete compatible value set selected from the declared current-target catalog | The original exact resolver returned zero, the user approved the bound candidate, and the original exact resolver plus compatibility checks succeed again immediately before preview | No | propose_reference_value |
| Question control, scoring, conditional, Recruiting-context, and attachment values | No default | Always | No | |
| AnswerCode, answer text, score, correctness, feedback, and rating values | No default | Always | No | |
| Approved AnswerCode correction | QuestionCode_QstnVersionNum_OriginalAnswerCode | A nonblank AnswerCode has failed uniqueness validation, the composed proposal satisfies the live contract and both uniqueness checks, and the user explicitly approves the exact old-to-new mapping | No | propose_question_specific_answer_code |
| Existing required values | Preserve the exact approved current target value | A change omits a field that must remain present and preservation is allowed by the live operation | No | |
| New Answer sequence | Deterministic approved source order | A new answer set omits explicit SequenceNumber and the live contract permits the value | No | |
| New context sequence or internal identifiers | No default | Always | No | |
| Loader or product default | Do not materialize locally | A route-specific default exists but the approved design does not explicitly select a value | No | |
| UpdateAllowed | Preserve the exact approved target value; no create-time default | A supported update includes the field | No | |

Any value filled from current target state is preservation or an explicitly approved correction, not a universal default. Show original, preserved, approved-correction, and explicitly supplied values separately in the preview. Approval of one proposed reference never authorizes any other inferred or corrected field.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| QLIB.APPLY-DEFAULTS | step | 30 | apply_default | applied_or_not_needed->QLIB.ENFORCE-DESIGN;invalid_default_request->QLIB.HANDLE-ISSUE | QLIB.CHECK-DEPENDENCIES | stop | Dependencies are ready |
