# Payment Terms Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Action | Infer only from an explicit business verb or an exact create-versus-existing-state result | Request does not clearly distinguish create, update, or end-date | No | find_payment_term_exact |
| Reference data set | Use the sole current candidate or one exact approved display/business-unit mapping; otherwise no default | Set is omitted and current evidence proves exactly one candidate or mapping | No | resolve_payment_term_set |
| Base language | No inferred default; require one customer-selected current target language and a base row with matching Language and SourceLang | Every create | No | inspect_payment_term_package |
| DFF context | No inferred default | A flexfield value is requested | No | inspect_payment_term_package |
| Unsupported template fields | Omit and block when requested behavior depends on them | Field is absent from the current template | No | inspect_payment_term_package |
| Child parent name | Copy the approved parent Name exactly | A line, translation, or discount row is generated | Yes, only to repair generated linkage to the same approved parent |  |
| Child parent set | Copy the approved parent SetCode exactly | A line, translation, or discount row is generated | Yes, only to repair generated linkage to the same approved parent |  |
| Service-owned audit columns | Leave LastUpdateDate, LastUpdatedBy, CreationDate, CreatedBy, and LastUpdateLogin blank; use exported values only as read-only evidence | Every create, update, or end-date import candidate | Yes, only to remove copied service-owned values | inspect_payment_term_package |
| Import date representation | Convert source-evidenced metadata dates to ISO `YYYY-MM-DD` and date-times to ISO date-time before writing candidate rows | Every create, update, end-date, or atomic batch candidate | Yes; semantic date value is preserved | inspect_payment_term_package |
| Unchanged fields on update | Preserve the approved current export value | A partial update package is generated | No | find_payment_term_exact |
| Unspecified child rows on update | Preserve every current line, translation, and discount row | A partial update omits a current child | No | find_payment_term_exact |
| Base translation description | Copy the explicitly requested base Description to both the header and the exactly resolved base-language row | A base Description is created or updated | Yes, only to keep the two representations consistent | inspect_payment_term_package |
| Simple Net N schedule | Normalize to BaseAmount 100 with one line of RelativeAmount 100 and DueDays N | The customer explicitly requests Net N or the entire balance due in N days and does not request installments, fixed dates, day-of-month handling, or another allocation | Yes, before preview |  |
| BaseAmount | 100, explicitly labeled as the installment-ratio denominator rather than a currency amount | Create request supplies installment percentages/ratios without another denominator | No |  |
| Credit check | N | Create request does not ask to associate the term with credit checking and the current template supports CreditCheckFlag | No | inspect_payment_term_package |
| In use | N | Create request and current create-model default evidence support the field | No | inspect_payment_term_package |
| Allow discount on partial payments | N | Customer does not request partial-payment discounts | No | verify_partial_discount_option |
| Prepayment | N | Customer does not request a prepayment term | No | inspect_payment_term_package |
| Discount basis | Invoice Amount (`I`) | Create has no discount rows and the field is absent; the entity requires a non-null header value | No | inspect_payment_term_package |
| Tax/freight installment option | Include tax and freight in the first installment (`INCLUDE`) | Create has exactly one payment line and FirstInstallmentCode is absent; the entity requires a value and the only line is also the first | No | inspect_payment_term_package |
| Discount basis date | APPLICATION_DATE | Create omits the field and does not choose Receipt Date or Deposit Date; the current create model supports the product default | No | inspect_payment_term_package |
| Print lead days | No inferred default | More than one payment line exists | No |  |
| Tax/freight installment option | No inferred default | More than one payment line exists | No | inspect_payment_term_package |
| Discount basis | No inferred default | One or more discount rows exist | No | inspect_payment_term_package |
| Discount rows | No discount rows | The customer does not request an early-payment discount | Yes, before preview |  |
| Child removal | No inferred deletion; omission means preserve | An update does not mention an existing child row | No | find_payment_term_exact |
| Missing business choice | No inferred default | Zero or multiple candidates, conflicting evidence, or more than one valid business design remains | No |  |
| Final confirmation | No inferred confirmation | Offline candidate generation is requested | No |  |
| Batch membership, names, or values | No default | A count or multi-operation outcome is requested | No | inspect_payment_term_package |

## Default Disclosure Rules

| Situation | Required Behavior |
|---|---|
| One evidence-backed value is filled | Show the business display value, implementation code when useful, and evidence source before package preparation. |
| A user supplied value conflicts with the resolved value | Preserve the user's value as unresolved, show the conflict, and ask which outcome is intended. |
| A default would change business behavior | Do not apply it; ask for the business decision. |
| The target, release, template, export, or request changes | Discard affected defaults and resolve them again. |
| The normalized design is complete | Show the full business summary and wait for the orchestration-owned design confirmation; do not create the ZIP from the original request or an earlier clarification. |
| An update is normalized | Show before/after changed fields, added rows, preserved-field count, and all translation descriptions; removed rows must be empty or the design is blocked. |
| Any default is applied | List the field, implementation value, and business meaning in the preview; a default hidden only in CSV is invalid. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PT.DEFAULTS | step | 40 | apply_default | normalized->PT.ENFORCE;blocked->PT.BLOCKED | PT.LOOKUP_PARTIAL | stop | Required lookups completed or were not applicable |
