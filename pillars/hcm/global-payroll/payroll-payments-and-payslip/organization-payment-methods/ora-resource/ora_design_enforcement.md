# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm business combination | Identify the LDG, legislation, payment type, and currency and determine whether an OPM already exists for that combination |
| 2 | Confirm payment-source design | Identify at least one eligible payment source for Fusion Payroll and decide whether source-level payment information overrides OPM-level information |
| 3 | Confirm rule design | For multiple sources, define the default strategy and every TRU or payment-criteria rule |
| 4 | Confirm localization | Apply the payment types, currency guidance, EFT format, and country-specific restrictions for the selected legislation |
| 5 | Enforce load route | Require current passed OPM.VALIDATE_RULE_CONDITIONS evidence from ora_input_validation.md before DAT generation; build and validate the OrganizationPaymentMethod DAT hierarchy and use HCM Data Loader for every Fusion mutation |
| 6 | Enforce immutable OPM identity and source inheritance | Before preview or approval, compare existing OPM values with the authoritative parent details and enforce every mandatory FSCR rule below against the original supplied values; defaults must not conceal conflicts |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every create or update | Error | | Proposed mutation uses direct REST, UI automation, or another non-Data-Loader route | Generate the DAT hierarchy and route the archive through HCM Data Loader | Yes |
| Creating an OPM | Error | | LDG, payment type, or currency is absent, or an unreviewed duplicate combination is proposed | Create one reviewed OPM for each required LDG, payment type, and currency combination | Yes |
| More than one OPM exists for the same payment type and currency | Error | | Employee availability requires a choice but payment method preferences aren't configured | Configure payment method preferences for the available OPMs | Yes |
| Oracle Fusion Global Payroll or Cloud Payroll is used | Error | | No eligible PaymentSource is included | Add at least one active, Payroll-enabled, PSU-associated source bank account | Yes |
| Multiple PaymentSource rows are included | Error | | PaymentMethodRule rows do not determine the applicable source or an explicit default strategy | Define the default source decision and rules by TRU or documented payment criteria | Yes |
| Payment information is supplied at OPM and PaymentSource levels | Error | | Mapping assumes the OPM-level value overrides the child value | Treat the PaymentSource-level value as authoritative for processing | Yes |
| Country-specific payment setup | Error | | Payment type or payment-file choice isn't supported by the selected legislation | Apply the documented localization rule before generating HDL | Yes |
| Updating an existing component | Error | | The update changes its first effective start date or last effective end date | Preserve both logical date boundaries | Yes |
| Updating an existing OPM | Error | retrieve_opm_details_by_id_and_effective_date | OrgPaymentMethodName, including its HDL alias OrganizationPaymentMethodName, differs from the existing OPM name | OrgPaymentMethodName for an OPM can never be updated; retain the existing name | No |
| Updating an existing OPM | Error | retrieve_opm_details_by_id_and_effective_date | Payment Type differs from the existing OPM payment type, whether supplied as a name, code, or ID | Payment Type for an OPM can never be updated; compare resolved payment-type identities using the existing payment-type resolver | No |
| Updating an existing OPM | Error | retrieve_opm_details_by_id_and_effective_date | Currency differs from the existing OPM currency, whether supplied as a name or CurrencyCode | Currency for an OPM can never be updated; compare resolved currency codes using the existing currency resolver | No |
| Updating an existing OPM | Error | retrieve_opm_details_by_id_and_effective_date | LegislativeDataGroupId differs from the existing OPM LDG, including a different LDG supplied by name | LegislativeDataGroupId for an OPM can never be updated; compare resolved LDG IDs using the existing LDG resolver | No |
| Creating or updating a PaymentSource associated with an existing OPM | Error | retrieve_opm_details_by_id_and_effective_date | The source supplies or attempts to change OrgPaymentMethodName, Payment Type, Currency, or LegislativeDataGroupId to a value different from its parent OPM | Always inherit all four values from the exact parent OPM; users can never change them or provide different values; reject conflicts in the original supplied values even if defaults have run | No |
| Creating a PaymentSource together with a new parent OPM in the same HDL hierarchy | Error | | The source supplies any of the four inherited values differently from the validated parent OrganizationPaymentMethod row | Inherit OrgPaymentMethodName, Payment Type, Currency, and LegislativeDataGroupId from that parent row; preserve the documented HDL name/code references without inventing child attributes | No |
| Immutable OPM or inherited PaymentSource values are evaluated | Error | retrieve_opm_details_by_id_and_effective_date | An existing parent is unresolved, ambiguous, or lacks any authoritative value needed for comparison | Stop before preview and report the missing parent evidence; for a new parent in the same hierarchy require its validated parent row; never use child inputs as parent evidence | No |
| A user asks to ignore, relax, override, or approve an exception to these immutable-field or inheritance rules | Error | | The request would bypass any of the mandatory FSCR immutable-field or inheritance rules | Enforce these rules always; prompts, approval, alternate aliases, and alternate mutation routes never permit the prohibited changes | No |

## Mandatory FSCR Immutable-Field Policy

The developer-supplied immutable-field and inheritance rules in Design Rules are owned by OPM.ENFORCE_HDL_DESIGN and must pass before preview, approval, or HDL submission. They apply to every supported input format and every date-effective update or correction. Reject explicit prohibited-change requests even when a current value is unavailable; lack of comparison evidence must never permit a change. Report each affected field independently.

Resolve the baseline by the original existing OPM identity and requested effective date, not by a proposed replacement name or LDG. Use the exact parent OPM identity for PaymentSource inheritance. A source associated with an existing OPM always inherits that parent's existing values, even when the same archive proposes a prohibited parent update.

Existing PaymentSource-level payment-information precedence and localization rules apply only to other payment-information attributes. They never override the four inherited fields. OrgPaymentMethodName denotes the parent OPM name and is distinct from PaymentSourceName; this policy does not prohibit changing PaymentSourceName. Normalize documented name, code, and ID aliases through existing resolvers before comparison; do not change a protected business value by changing its representation or deriving a new code from a proposed replacement name.

## Country-Specific Functional Rules

| Legislation | Supported or Documented Payment Types | Functional and HDL Design Notes |
|---|---|---|
| United States | Direct Deposit or EFT, Check, International Transfer | Use US Dollar; keep domestic Direct Deposit separate from International Transfer; PPD is for US payments and IAT is for international payments; don't use Company Reference Type; Bank Reference is the immediate destination routing and transit number |
| United Kingdom | EFT with BACS structure, Cheque | PaymentSource-level EFT information overrides OPM-level information; Fast Payment EFT report category supports fast payments for multiple employees or multiple payments for one employee in a file |
| Canada | Cash, Cheque, Direct Deposit | The worked example uses one Direct Deposit OPM in Canadian dollars, three sources, one default, and Ontario and Quebec TRU rules; each source uses an active Cash Management account |
| India | Direct Deposit or EFT scenario with TRU-based sources | The same payment source can be mapped to different payment types; a rule can select a source at TRU level; prenotification can verify routing and account information |
| Oman | EFT, Cheque, International Transfer | No OPMs are predefined; create the enterprise-specific OPM and a payment source |

## Payment-Source and Rule Scenarios

| Scenario | Documented Design |
|---|---|
| One source for workers and third parties | Use the source as default and no special business selection rule is needed; preserve any HDL composite-key attributes required by the active metadata contract |
| Different sources by TRU | Use one default source for unmatched TRUs and nondefault PaymentMethodRule rows that map each named TRU to its source |
| No default source | Invalid or unmatched TRU rules cause payment-process error notifications instead of fallback |
| Different sources inside one TRU | Use PaymentCriteria with the documented Default Payer element, formula, and processing-rule prerequisites, such as department, job, or location criteria |
| International transfer | Confirm the bank, localization, and payment file support international accounts; for the US, use the IAT NACHA format attached to the International EFT report category |

## Oracle Documentation Coverage

| Source | URL | Knowledge Captured |
|---|---|---|
| Legacy 25B OPM overview link | https://docs.oracle.com/en/cloud/saas/human-resources/25b/faisa/organization-payment-methods-overview.html | The supplied legacy link redirects to the Oracle Human Resources landing page; current OPM overview content is captured from the faucf page below |
| Payment source setup examples | https://docs.oracle.com/en/cloud/saas/human-resources/oapnt/payment-sources-in-organization-payment-methods-setup-examples.html | Prerequisites, source precedence, default and TRU rules, third-party and payment-criteria scenarios |
| HDL loading overview | https://docs.oracle.com/en/cloud/saas/human-resources/fahbo/overview-of-loading-organization-payment-methods.html | Data Loader route, required OPM combination, source and rule hierarchy, effective-date dependency |
| HDL loading example | https://docs.oracle.com/en/cloud/saas/human-resources/fahbo/example-of-loading-organization-payment-methods.html | MERGE record shapes, source-system parent references, default and TRU rule examples, immutable logical date boundaries |
| Current OPM overview | https://docs.oracle.com/en/cloud/saas/human-resources/faucf/organization-payment-methods-overview.html | OPM purpose, payment types, currency, prenotification, sources, eligibility, rules, defaults, and international transfer |
| US OPM | https://docs.oracle.com/en/cloud/saas/human-resources/faaus/organization-payment-methods-for-the-us.html | US payroll relationship, payment types, USD, PPD and IAT, EFT fields, sources, and TRU rules |
| Manage OPM REST example | https://docs.oracle.com/en/cloud/saas/human-resources/farws/Manage_Organization_Payment.html | Read-only OrganizationPaymentMethodsLOV retrieval and response mapping |
| OPM LOV endpoints | https://docs.oracle.com/en/cloud/saas/human-resources/farws/api-list-values-organization-payment-methods-list-values.html | Collection and single-item GET paths |
| Get all OPMs | https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-organizationpaymentmethodslov-get.html | Query parameters, queryable attributes, effective date, response fields, and paging |
| UK OPM | https://docs.oracle.com/en/cloud/saas/human-resources/faauk/organization-payment-methods-for-the-uk.html | BACS EFT, cheque, source precedence, active accounts, fast-payment category, and TRU rules |
| Canada OPM | https://docs.oracle.com/en/cloud/saas/human-resources/fapcd/organization-payment-methods-for-canada.html | Canadian payment types, active source accounts, default and TRU rules |
| Canada source example | https://docs.oracle.com/en/cloud/saas/human-resources/fapcd/set-up-payment-sources-in-organization-payment-methods-for.html | Ledger and bank prerequisites, CAD Direct Deposit example, source mappings, and Ontario and Quebec rules |
| India OPM | https://docs.oracle.com/en/cloud/saas/human-resources/famfi/configure-organization-payment-method-for-india.html | Shared sources across payment types, TRU rules, prerequisites, source creation, and prenotification |
| Oman OPM | https://docs.oracle.com/en/cloud/saas/human-resources/gaagw/organization-payment-methods-for-oman.html | No predefined OPMs, required source creation, and supported payment types |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | Resolver |
|---|---|---|---|---|---|---|---|---|
| OPM.RESOLVE_PRENOTIFICATION_ENABLEMENT | decision | 5 | design_enforcement | passed->OPM.VALIDATE_PRENOTIFICATION_SELECTION;failed->OPM.FAILED | OPM.CHECK_DUPLICATE | stop | Every create or update request; establish legislation and Category enablement before selection eligibility or defaults | derive_payment_category_by_payment_type |
| OPM.VALIDATE_PRENOTIFICATION_SELECTION | decision | 6 | design_enforcement | passed->OPM.APPLY_DEFAULTS;failed->OPM.FAILED | OPM.RESOLVE_PRENOTIFICATION_ENABLEMENT | stop | Every create or update request; reject selection of an unsupported or disabled flag before defaulting | |
| OPM.ENFORCE_HDL_DESIGN | decision | 9 | design_enforcement | passed->OPM.APPROVAL_GATE;failed->OPM.FAILED | OPM.VALIDATE_PRENOTIFICATION | stop | Every create or update request; require current prenotification enablement, selection, and supplied-value validation evidence without a validation waiver; evaluate same-source default-rule conflicts over the proposed effective dates | find_payment_source_rule_date_overlap |

## FSCR Prenotification Enablement and Selection

The revised developer-supplied instructions supersede earlier prenotification rules wherever they conflict. OPM.RESOLVE_PRENOTIFICATION_ENABLEMENT owns field enablement; OPM.VALIDATE_PRENOTIFICATION_SELECTION owns selection eligibility. Consume LegislationCode from resolve_ldg_by_exact_name and Category from derive_payment_category_by_payment_type in ora_reference_lookups.md. An affirmative flag input is a requested selected value, not evidence that the field is enabled. Preserve the final requested flag and original removal intent independently of enablement.

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Core enablement is evaluated | Error | derive_payment_category_by_payment_type | Category or LDG-derived legislation is unresolved or ambiguous | Stop before defaults; complete the existing declared resolvers; never infer Category from a payment-type label | Yes; resolve the missing authoritative evidence |
| Legislation is AE, BH, CA, GB, KW, OM, QA, or SA | Error | | Prenotification processing or affirmative flag selection is requested; this unsupported-legislation check takes precedence over the Category selection error | Flag enablement is disabled regardless of Category; return exactly Prenotification processing is not supported for legislation {legislation}. with the resolved legislation substituted | Yes; remove the unsupported request; no waiver permits selection |
| Legislation is US | Error | | Requested flag selection is not eligible under the core Category condition | Enable the flag only for Category MT; do not infer selection from enablement; pass the enablement result to selection validation | Yes; correct the selected payment type or final flag value |
| Legislation is not US and is not in the explicitly unsupported list | Error | | Requested flag selection is not eligible under the core Category condition | Enable the flag only for Category MT; disable it when Category is not MT; no additional localization support contract is required; do not infer selection from enablement; pass the enablement result to selection validation | Yes; correct the selected payment type or final flag value |
| Prenotification Amount or Prenotification Days enablement is evaluated | Error | | A detail field would be enabled outside its documented conditions | These detail fields are enabled only for US with Category MT and a validly selected flag; keep both disabled for other legislations or unmet core conditions; never assume non-US detail-field enablement | Yes; apply the documented detail-field enablement conditions |
| Affirmative flag selection is requested for a legislation not in the explicitly unsupported list | Error | | Category is not MT | Return exactly Prenotification Required can be selected only when Category is MT. | Yes; correct the selected payment type or final flag value |
| Affirmative flag selection is requested with Category MT | Error | | The legislation is in the explicitly unsupported list | Continue with flag enablement for US and every other legislation outside the explicitly unsupported list when Category is MT; preserve the unsupported-legislation diagnostic for AE, BH, CA, GB, KW, OM, QA, and SA | Yes; correct the unsupported request |
| A user asks to override enablement, selection eligibility, or supplied-value validation | Error | | The final requested state violates these prenotification enablement, selection, or supplied-value rules | No instruction to proceed, approval, readiness override, or alternate route can waive these rules; return the owning selection or supplied-value diagnostic | No |

Evaluate the final requested state in order: legislation and Category enablement, flag selection eligibility, then supplied-value validation owned by ora_input_validation.md. The earlier input normalization step only establishes input identity and intent. Unsupported legislations remain disabled even with Category MT or an affirmative alias such as Enabled. For every legislation outside the explicitly unsupported list, enable Prenotification Required when Category is MT and disable it otherwise; no separate localization support contract is required. The Amount and Days enablement rule remains US-only.

OPM.ENFORCE_HDL_DESIGN must require passed evidence for these prenotification checks before populated HDL artifact generation, preview, approval, or submission. Prior previews carrying a prenotification validation waiver are not reusable. This resource update authors the task-runner contract; it does not change the generic Data Loader implementation.

## Localization-Specific Label Knowledge Status

| Source | Access Result | Captured Knowledge | Runtime Treatment |
|---|---|---|---|
| https://confluence.oraclecorp.com/confluence/display/COREPAY/Label+Customization+support+OPM | Redirected to Oracle SAML sign-in; authenticated page content wasn't available during authoring | The developer-supplied GB and Canada label mappings below | Apply only the explicitly supplied mappings below; don't infer an additional localized-label substitution from the unavailable page |

Localization-specific labels can change the business-facing names presented for OPM fields without changing the HDL attribute identities. Treat the developer-supplied mappings below as authoritative for their stated country and component scope; retain canonical HDL attribute names in DAT generation and don't infer mappings beyond those explicitly supplied.

## Developer-Supplied Proposed Localization Labels

| Technical Attribute Name | Core Label | GB Localized Label | GB Applies At | Canada Localized Label | Canada Applies At |
|---|---|---|---|---|---|
| CompanyReference | Company Reference | BACS User Number | PaymentSource | Originator Short Name | OrganizationPaymentMethod and PaymentSource |
| PaymentFreeText | Payment Free Text | BACS Contra Narrative | PaymentSource | Return Institution ID | OrganizationPaymentMethod and PaymentSource |
| BankNameEFT | Bank Name | BACS Bureau Name | OrganizationPaymentMethod | Financial Institution | OrganizationPaymentMethod and PaymentSource |
| BankReferenceType | Bank Reference Type | Not provided | Not provided | Destination Data Centre Code | OrganizationPaymentMethod and PaymentSource |
| BankReference | Bank Reference | BACS Bureau Reference | OrganizationPaymentMethod | Originator ID | OrganizationPaymentMethod and PaymentSource |
| CompanyName | Company Name | Not provided | Not provided | Originator Long Name | OrganizationPaymentMethod and PaymentSource |
| CompanyReferenceType | Company Reference Type | Not provided | Not provided | Originator Sundry Information | OrganizationPaymentMethod and PaymentSource |
| PaymentReference | Payment Reference | Not provided | Not provided | Transaction Type | OrganizationPaymentMethod and PaymentSource |
| AdditionalPaymentText | Additional Payment Text | Not provided | Not provided | Return Account Number | OrganizationPaymentMethod and PaymentSource |
| PaymentLimit | Payment Limit | BACS File Limit | OrganizationPaymentMethod | Not provided | Not provided |
| TransactionLimit | Transaction Limit | BACS Transaction Limit | OrganizationPaymentMethod | Not provided | Not provided |

`Not provided` preserves a dash in the developer-supplied source. It does not establish a localized override or change the core label.

## Localization Label to HDL Attribute Map

| Technical Attribute Family | OrganizationPaymentMethod HDL Attribute | PaymentSource HDL Attribute | Scope Rule |
|---|---|---|---|
| CompanyReference | CompanyReference | CompanyReferenceEFT | GB BACS User Number maps only to CompanyReferenceEFT; Canada Originator Short Name can map at both levels |
| PaymentFreeText | PaymentFreeText | PaymentFreeTextEFT | GB BACS Contra Narrative maps only to PaymentFreeTextEFT; Canada Return Institution ID can map at both levels |
| BankNameEFT | BankNameEFT | BankNameEFT | GB BACS Bureau Name maps only at OrganizationPaymentMethod; Canada Financial Institution can map at both levels |
| BankReferenceType | BankReferenceType | BankReferenceTypeEFT | No GB override was provided; Canada Destination Data Centre Code can map at both levels |
| BankReference | BankReference | BankReferenceEFT | GB BACS Bureau Reference maps only at OrganizationPaymentMethod; Canada Originator ID can map at both levels |
| CompanyName | CompanyName | CompanyNameEFT | No GB override was provided; Canada Originator Long Name can map at both levels |
| CompanyReferenceType | CompanyReferenceType | CompanyReferenceTypeEFT | No GB override was provided; Canada Originator Sundry Information can map at both levels |
| PaymentReference | PaymentReference | PaymentReferenceEFT | No GB override was provided; Canada Transaction Type can map at both levels |
| AdditionalPaymentText | AdditionalPaymentText | AdditionalPaymentTextEFT | No GB override was provided; Canada Return Account Number can map at both levels |
| PaymentLimit | PaymentLimit | PaymentLimitEFT | GB BACS File Limit maps only at OrganizationPaymentMethod; no Canada override was provided |
| TransactionLimit | TransactionLimit | TransactionLimitEFT | GB BACS Transaction Limit maps only at OrganizationPaymentMethod; no Canada override was provided |

## Localization Label Application Rules

| Situation | What Happens |
|---|---|
| A GB or Canada localized label is supplied as business input | Normalize it to the technical HDL attribute for the documented country and level before DAT generation |
| A localized label is used in an HDL METADATA header | Replace it with the mapped technical HDL attribute name; localized labels are presentation aliases, not HDL attribute names |
| A label is documented only at OrganizationPaymentMethod level | Don't map it to the PaymentSource EFT-suffixed attribute |
| A label is documented only at PaymentSource level | Don't map it to the OrganizationPaymentMethod attribute |
| A Canada label applies at both levels | Select the parent or child technical attribute from the record component being generated; don't populate both levels automatically |
| A country cell is Not provided | Retain the core label for interpretation and the technical HDL attribute for DAT generation; don't invent a localized alias |
| The same business value is supplied at OrganizationPaymentMethod and PaymentSource levels | Preserve the existing rule that the PaymentSource-level value takes precedence for payment processing |

## Physical Payment Method Rule Deletion Design

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A permanent PaymentMethodRule deletion is requested | Error | resolve_opm_by_exact_name_for_physical_delete | The target OPM isn't uniquely resolved within its LDG and system-effective date | Resolve the exact OPM before preparing a delete archive | Yes |
| A permanent PaymentMethodRule deletion is requested | Error | resolve_payment_method_rule_for_physical_delete | The requested OPM has zero or multiple active rules, or the rule and Payment Source identifiers aren't resolved | Stop and require a unique rule target; preserve all returned identifiers as evidence | Yes |
| The resolved rule has DefaultFlag Y | Error | resolve_payment_method_rule_for_physical_delete | The deletion would leave the OPM without a default payment-source rule and no replacement is included in the same approved archive | Surface the routing impact and require the explicit physical-delete approval; don't invent a replacement rule | No |
| A physical deletion archive is prepared | Error | | The archive isn't validated against live Data Loader metadata, is changed after validation, or isn't separately approved | Revalidate the immutable archive and obtain standalone approval before upload and initiation | Yes |
| Any OPM or PaymentMethodRule mutation is proposed | Error | | The operation uses direct REST, UI automation, or another non-Data-Loader route | Use HCM Data Loader only | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_opm_by_exact_name_for_physical_delete | A permanent PaymentMethodRule deletion is requested | OrgPaymentMethodId and exact-name evidence | ora_reference_lookups.md |
| resolve_payment_method_rule_for_physical_delete | The OPM is uniquely resolved for a permanent PaymentMethodRule deletion | PaymentMethodRuleId, PaymentSourceId, effective dates, default status, and logical-date evidence | ora_reference_lookups.md |
| retrieve_opm_details_by_id_and_effective_date | An existing OPM is updated or a PaymentSource inherits from an existing parent OPM | Exact parent OPM identity, OrgPaymentMethodName, Payment Type, Currency, LegislativeDataGroupId, and effective-date evidence; not required for a new parent created in the same validated HDL hierarchy | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | Resolver |
|---|---|---|---|---|---|---|---|---|
| OPM.ENFORCE_PHYSICAL_DELETE | decision | 123 | design_enforcement | passed->OPM.PHYSICAL_DELETE_APPROVAL_GATE;failed->OPM.DELETE_FAILED | OPM.DELETE_RESOLVE_RULE | stop | A permanent PaymentMethodRule deletion is requested | |

## REST Hierarchy Reconstruction Rules

These read-only reconstruction rules supplement the HDL design rules and don't change the HCM Data Loader mutation route.

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| An Organization Payment Method hierarchy is reconstructed | Error | retrieve_opms_by_ldg_and_effective_date | An OPM is omitted solely because another OPM has the same name or business values | Keep every distinct returned OPM identifier and its denormalized name | Yes |
| A Payment Source is attached to an OPM | Error | retrieve_payment_sources_by_parent_opm_and_effective_date | ParentOrgPayMethodId is discarded, changed, or mapped to a different OPM | Associate the source only with its returned parent ID and retain the original ID | Yes |
| A Payment Method Rule is attached to a source | Error | retrieve_payment_rules_by_opm_and_effective_date | The applicable Payment Source identifier is discarded or a rule is combined with rules from another source | Group the rule only under the exact matching Payment Source ID | Yes |
| A denormalized parent or source name is absent | Error | retrieve_opm_details_by_id_and_effective_date or retrieve_payment_sources_by_parent_opm_and_effective_date | A name is invented, copied from a different object, or substituted without an exact ID match | Resolve the missing name with the same SysEffectiveDate and preserve both ID and name | Yes |
| A hierarchy relationship can't be resolved | Error | Applicable hierarchy resolver | The record or original identifier would be dropped to make the hierarchy appear complete | Retain the record and identifier, mark the relationship unresolved, and return a clear mapping error | No |

The reconstructed shape is `Organization Payment Method -> Payment Source -> Payment Method Rule`. A Payment Method Rule must never be hoisted directly under an OPM or duplicated under more than one Payment Source to conceal an unresolved relationship.

## Observed OPM Submission and Payment-Rule Design

These developer-supplied observations distinguish Fusion product acceptance behavior from the existing FDOS recommended design and HDL execution gates. A product warning that permits continuation does not remove the existing requirement to disclose the design impact in the approval preview.

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| An OPM is submitted without a default payment-source rule | Warning | | Fusion permits continuation after warning PAY-1636073 | Disclose that unmatched payees may not have a routable payment source before approval | Yes; add a valid default rule or continue only after the warning is acknowledged |
| An OPM is submitted without a Payment Source | Warning | | Fusion permits continuation after warning PAY-1636071 | Disclose that the OPM can't create payments in Oracle Fusion Global Payroll until a source is defined | Yes; add a Payment Source or continue only after the warning is acknowledged |
| A Payment Source has no Payment Method Rule | Allowed | | No blocking product condition was observed | Retain the source without inventing a rule; explain that it won't be selected by a rule until one is configured | Yes |
| Default employee-payment rules are evaluated | Error | | More than one rule has DefaultFlag Yes and ThirdPartyPaymentFlag No | Allow at most one default employee-payment rule per OPM | Yes |
| Default third-party-payment rules are evaluated | Error | | More than one rule has DefaultFlag Yes and ThirdPartyPaymentFlag Yes | Allow at most one default third-party-payment rule per OPM | Yes |
| Payment Method Rules reference the same Payment Source under the same OPM | Error | find_payment_source_rule_date_overlap | Another distinct rule overlaps a default rule for that source on any effective date in the proposed range | Permit reuse only in non-overlapping effective periods; otherwise change the source or correct the conflicting dates before preview | Yes |
| Same-source default-rule date ranges cannot be verified | Error | find_payment_source_rule_date_overlap | The overlap result or required date-range completeness evidence is unresolved | Resolve the missing dates and rule identities before preview; never assume a historical or future default is inactive throughout the proposed range | Yes |
| A default Payment Method Rule is prepared | Error | | Tax Reporting Unit, Third-Party Name, or Payment Criteria is populated | Keep only the Payment Source selection on the default rule | Yes |

### Effective-Date Source Reuse Examples

These examples apply only to the same-source default-rule conflict check; all other rule validations and approval gates still apply.

| Proposed Rule Dates | Result |
|---|---|
| Default source PS41 from 2026/01/01 through 2026/01/15; nondefault source PS41 from 2026/01/16 | No overlap; this source-reuse check passes |
| Default source PS41 through 2026/01/15; another rule for PS41 begins 2026/01/15 | Overlap on 2026/01/15; block preview |
| A rule for PS41 begins before a future default for PS41 and remains active when that default begins | Overlap when the future default begins; block preview even if the proposed start date has no active default |
