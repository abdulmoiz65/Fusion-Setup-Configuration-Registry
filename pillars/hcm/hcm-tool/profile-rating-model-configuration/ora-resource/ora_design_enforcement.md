# Profile Rating Models Design Enforcement

## Enforcement Order

| Task Code | Task Name | Sequence | Step | What Must Happen |
|---|---|---|---|---|
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | 1 | Business proposal | Resolve business intent, discover patterns, record assumptions, and obtain proposal review before technical normalization |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | 2 | Technical design | Validate the normalized configuration, exact reuse result, component ownership, and supported creation source |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | 3 | Execution boundary | Bind one standalone approval to the exact immutable core.data-loader preview; proposal review is not import authorization |

## Design Rules

| Task Code | Task Name | Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|---|---|
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | BUSINESS_FIRST_INTAKE | Business-first conversational request | Blocking | discover_rating_model_patterns | The flow asks the user to select a skill, Fusion consumer, task, loader route, component, code, or technical field before discovery even though one supported proposal can be produced | Start from outcome, workforce or process context, effective date and exceptions; infer or propose technical values | Interaction fix |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | ASSUMPTION_PROVENANCE | Any consumer or technical value is inferred | Blocking | discover_rating_model_patterns | Value, source, evidence, confidence, materiality or review status is missing, or a generated value is represented as an established standard without evidence | Complete the assumption ledger and expose material assumptions under Review assumptions | Proposal fix |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | GENUINE_AMBIGUITY_ONLY | A follow-up question is proposed | Blocking |  | The requested answer is a technical implementation concept that can be inferred or safely proposed, or the question does not explain the competing business outcomes | Ask one plain-language question only when the answer changes business meaning, population, timing, or reuse-versus-new result | Interaction fix |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | PROPOSAL_REVIEW | Before technical normalization | Blocking | discover_rating_model_patterns | Material assumptions are unreviewed, the summary omits outcome/date/scale/exclusions, or proposal confirmation is treated as permission to import | Confirm or correct the proposal, version it, then normalize; retain a separate immutable Data Loader approval | Re-propose |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | ONE_MODEL | Every request | Blocking |  | More than one model or a bulk row set is requested | Split into independently reviewed requests | Input fix |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | CONSUMER_UNION | Every request | Blocking |  | Blueprint omits a selected-consumer rule or contains an unexplained conflict | Reconcile the union and document component provenance | Blueprint fix |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | EXACT_REUSE | Candidate classified exact | Blocking | find_rating_model_by_exact_identity | Any material value, component, translation, meaning, or read coverage differs | Classify close/unsuitable and propose a new model or separate impact review | Decision fix |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | NO_EXISTING_EDIT | Close or unsuitable candidate exists | Blocking | find_rating_model_by_exact_identity | Plan updates, appends, deletes or repairs the existing model | Leave it unchanged and propose a new model | No |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | COMPONENT_OWNERSHIP | Performance or Compensation distributions are used | Blocking |  | Performance target values are loaded as direct model distributions or Compensation direct values are handed downstream only | Keep Compensation direct values on the model and Performance target values in its handoff | Blueprint fix |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | PERFORMANCE_CALCULATION_OWNERSHIP | Performance uses calculated ratings | Blocking |  | Calculation method, decimal places, decimal rounding rule, mapping metric, mapping method, or Target Ratings Distribution is represented as a rating-model-owned field, or the Performance handoff omits it | Keep numeric rating levels and applicable review points and ranges on the rating model; place the calculation, precision, rounding, mapping, and target-distribution settings in the downstream Performance section handoff | Blueprint fix |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | TALENT_REVIEW_CATEGORY_REQUIREMENT | Talent Review uses the model on an X or Y axis | Blocking |  | The model does not assign rating categories to all applicable levels required for the box-chart matrix | Complete the model's rating categories before handing it to the Talent Review meeting-template owner | Blueprint fix |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | SKILLS_CENTER_ASSOCIATION_LOCK | Skills Center uses the model for a skill content section | Blocking |  | Level identifiers are not unique increasing integers within 1 through 9, or the handoff does not disclose that the content section's rating model cannot be changed after skills are added | Correct the Skills Center scale and record the association constraint before skills are added to the content section | Blueprint fix |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | SUPPORTED_SOURCE | New model | Blocking |  | Current FSM package or Rating Model HDL hierarchy does not prove every blueprint field | Stop with the completed blueprint and refresh metadata | Metadata fix |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | REST_READ_ONLY | Any REST route is considered | Blocking | find_rating_model_by_exact_identity | A create, update, delete or batch write is proposed | Use REST only for proven reads and route creation to core.data-loader | No |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | RELEASE_METADATA_NOT_USER_GATE | Read-only environment preflight | Blocking |  | The user is asked to supply or confirm a quarterly release, its absence blocks an otherwise source-backed capability probe, or a release is inferred from a REST API version, hostname, documentation URL or calendar date | Resolve the environment from active authenticated core context; record quarterly release and source only when trusted metadata already provides them; prove compatibility with the source-backed REST API version, path and bounded request | Interaction fix |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | STRUCTURED_VERIFICATION_ONLY | Environment, access, reuse or post-import verification | Blocking |  | A screenshot, browser or manual UI navigation, address-bar image, exact user reply, loader status or user attestation is requested, required or treated as sufficient proof | Use the active authenticated environment and successful declared read for access, then use fresh structured read-back against the approved blueprint for configuration completion; if the declared evidence is unavailable, stop as blocked, incomplete or failed | Interaction fix |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | IMMUTABLE_PREVIEW | New model immediately before creation | Blocking | verify_rating_model_result | Preview omits target, source, consumers, complete values, exclusions, handoffs, digest or read-back assertions, or approval is absent/stale | Rebuild the immutable core.data-loader preview and use its approval gate | Re-preview |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | READBACK | Reuse or later approved creation | Blocking | verify_rating_model_result | Saved values and coverage do not prove the approved configuration | Return failed/incomplete and reconcile; never retry creation automatically | No |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | DOWNSTREAM_BOUNDARY | Every completion | Blocking |  | The run creates a template, plan, content section, profile association, meeting or other consumer setup | Emit a structured handoff only | No |

## Design Lookup Requirements

| Task Code | Task Name | Resolver | When Required | Values Needed | Source File |
|---|---|---|---|---|---|
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | discover_rating_model_patterns | Every business-first proposal | Candidate patterns, ranking reasons, naming/scale conventions, component exclusions, coverage limitations, and zero/one/multiple-plausible result | ora_reference_lookups.md |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | find_rating_model_by_exact_identity | Every exact reuse or new-model decision | Candidate identity, complete selected-consumer configuration, coverage and differences | ora_reference_lookups.md |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | verify_rating_model_result | Preview assertion design and every reuse or post-import completion | Expected, observed, unavailable fields, differences and verification result | ora_reference_lookups.md |

## Enforcement Outcomes

| Task Code | Task Name | Outcome | When Used | Next Action |
|---|---|---|---|---|
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | business_proposal_confirmed | Business meaning is sufficient and every material assumption is confirmed or corrected | Normalize and technically validate the confirmed proposal |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | business_input_required | Material consumer or scale alternatives remain equally supported | Ask one plain-language business question and create a new proposal version |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | exact_reuse_ready | All exact-reuse and handoff rules pass | Persist reuse evidence and handoffs |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | creation_preview_ready | No exact model exists and all creation/preview gates pass | Enter the core.data-loader approval/import route |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | blocked | Any applicable rule fails | Stop and return the prescribed correction |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | PRM.PROPOSAL | decision | 4 | design_enforcement | confirmed->PRM.INPUT;needs_business_input->PRM.ERROR;blocked->PRM.ERROR | PRM.DEFAULTS | stop | Enforce business-first interaction, consumer evidence, assumption provenance, genuine-ambiguity-only questions, and proposal-review separation before technical normalization |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | PRM.DESIGN | decision | 8 | design_enforcement | exact_reuse_ready->PRM.ROUTE;creation_preview_ready->PRM.ROUTE;blocked->PRM.ERROR | PRM.DEPENDENCIES | stop | Enforce one-model, exact-reuse, component ownership, Performance calculation ownership, Talent Review categories, Skills Center association constraints, optional quarterly release metadata, supported-source, preview, read-only REST and downstream boundaries |
