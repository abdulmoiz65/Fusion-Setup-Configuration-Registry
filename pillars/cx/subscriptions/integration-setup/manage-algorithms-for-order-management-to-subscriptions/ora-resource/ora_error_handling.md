# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| The supplied Service Mapping XML is malformed or its contextName is not OMIntegration | Stop before using it as algorithm evidence and request valid OMIntegration source XML |
| The validated mapping assessment evidences an existing direct mapping and no independent logic requirement | Return algorithm_not_required and do not create a draft or artifact |
| The validated mapping assessment reports a mapping gap, metadata blocker, or incompatibility | Return the Service Mapping prerequisite and do not use an Algorithm as a substitute. A mapping gap with a complete exact three-tab UI plan may support a clearly labelled approval-ready provisional draft; on an explicit request for code without that plan, return only a placeholder-only provisional source draft |
| Source and target are available but the assessment has no direct assignment evidence | Return an inline Algorithm draft that states the proposed OSSTransactions-first declarative action, `ZeroOrOne` cardinalities, joins, and blank, overwrite, amendment, and cancellation behavior before requesting approval. Put the source in a fenced Groovy code block and do not create a human-readable Markdown draft file |
| A direct target-to-source key supports a product-level action | Establish and use the OSSTransactions bridge first. Preserve the delivered RUN_SCRIPT, add a separate ConditionalAction, and use the direct key only as supplementary match evidence; do not replace interface-table correlation with it |
| A desired declarative action has no existing Algorithm_BO XML representation | Treat it as a mandatory skill-owned action-creation case, not a user error or a blocker. Add one new separate CONDITIONAL_ACTION after the delivered RUN_SCRIPT using `references/ora_conditional_action_serialization.md`, preserve RUN_SCRIPT unchanged, and assign the next available sequence number. Do not ask the user for a structural sample, schema, or existing action; do not append cross-entity logic to RUN_SCRIPT or create a human-readable Markdown draft file |
| A Custom EFF source or target lacks the complete validated Service Mapping contract | Return the exact Service Mapping prerequisite. A complete exact three-tab UI plan may support an approval-ready provisional source draft. On an explicit request for code, return a placeholder-only source draft for unknown technical identifiers, but never an artifact unless the normal plan, approval, warning, and continuation gates all pass |
| A custom-indicator request omits source or target technical values | Return a mapping-information request. A code request may receive only a literal placeholder-only source draft; do not infer a field, conversion, or permission. |
| A Custom EFF action lacks the confirmed source/target aliases, `ZeroOrOne` cardinalities, joins, action container, or per-field source-null/blank guard | Return the missing mapping or rule contract; do not infer it. If the only absence is a declarative action step, create a new separate canonical CONDITIONAL_ACTION without disturbing RUN_SCRIPT |
| A P or N version contains a relevant Custom EFF action but no nonprotected active version exists | Use the historical action only as structural reference; create a new active version only when its base structure can be safely derived |
| Algorithm_BO.xml is malformed or identifies another algorithm | Stop and request the correct FOM-to-OSS export |
| No nonprotected active version remains for a requested draft or artifact | Create the next unused numeric nonprotected version with ActiveFlag Y when a base structure can be safely derived; otherwise request a valid export |
| A requested target is Version 0 or 1 | Refuse the change and preserve both protected versions unchanged |
| An algorithm recommendation or change lacks a validated companion assessment | Stop before determining algorithm necessity and request the assessment |
| A draft removes or reorders the selected baseline downstream terminal action without explicitly approved scope | Stop artifact preparation and return the draft correction required |
| The completed draft is not explicitly approved | Return the inline reviewable draft only; do not create Algorithm_BO.xml, SubscriptionManagementandOrderManagementIntegration.zip, or a human-readable Markdown draft file |
| A provisional draft is approved but the user has not explicitly answered yes after the required warning | Display the exact warning and ask whether to continue; do not create Algorithm_BO.xml |
| A provisional artifact is missing its warning metadata or contains a non-schema provisional XML marker | Do not return it; record the warning and `provisional=true` only in the validation result and artifact registry, then revalidate the XML |
| The XML or archive is malformed, misnamed, changes a nontarget version, generates P state, has extra archive entries, or the archive XML differs from the validated local file | Do not return either output; correct and revalidate the active-target XML and SubscriptionManagementandOrderManagementIntegration.zip before reassessment |
| A request includes import, publication, deployment, or runtime testing | Refuse as out of scope |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input-context blocker | Mapping XML is absent, malformed, or not OMIntegration | Request valid source XML |
| Algorithm not required | The assessment evidences an existing direct mapping and no independent logic requirement | Return the no-change recommendation |
| Mapping prerequisite | The assessment has a mapping gap, metadata blocker, or incompatibility | Return the Service Mapping prerequisite; permit an approval-ready provisional draft only with a complete exact three-tab UI plan, or a placeholder-only source draft when the user explicitly requests code |
| Input-version blocker | Algorithm identity, active-target selection, or new-active-version selection for a draft or artifact is invalid | Request a valid export |
| Assessment blocker | Algorithm recommendation or change lacks a valid companion assessment | Request a validated applicable assessment |
| Algorithm-contract blocker | A possible Algorithm change lacks a confirmed source or target, expected outcome, target scope, or declared API assumptions | Request the missing contract before drafting or artifact creation |
| Baseline-flow blocker | A draft changes an established downstream terminal action without explicit documented scope and approval | Correct the review draft before artifact creation |
| Approval blocker | Exact draft approval is missing | Return the draft and wait |
| Provisional-continuation blocker | A provisional artifact is requested before the prescribed warning is displayed and separately accepted | Show the warning, ask whether to continue, and return no artifact |
| Support-artifact blocker | Local output does not meet filename, XML, archive-content, byte-identity, or unchanged-version integrity checks | Correct the artifact and archive before return |
| Scope blocker | Request would perform a Fusion change | Return the non-mutation boundary |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Mapping context blocker | Observed contextName and required OMIntegration value without unrelated XML contents |
| No-change recommendation | Mapping status, direct-assignment evidence, and the absence of an independent logic requirement |
| Version blocker | Candidate VersionNum and ActiveFlag values, selected latest active target or new active VersionNum, and confirmation that Versions 0 and 1 remain unchanged |
| Assessment blocker | Missing assessment field or incompatibility with the requested outcome |
| Approval blocker | That no Algorithm_BO.xml artifact was returned and explicit draft approval is required |
| Inline-draft contract blocker | That the complete draft, including a fenced Groovy code block, was returned in chat and no human-readable Markdown draft file was created |
| Provisional-continuation blocker | The unapplied Service Mapping prerequisite, the exact warning, that an affirmative continuation is required, and that no Algorithm_BO.xml was returned |
| Support-artifact blocker | Structural failure and the required exact filename Algorithm_BO.xml |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Service Mapping XML is not OMIntegration | Do not reuse its entities or attributes for algorithm reasoning |
| The assessment evidences an existing direct mapping and no independent logic requirement | Do not draft, approve, or create an Algorithm_BO.xml solely to duplicate the mapping |
| The assessment reports a metadata blocker or incompatibility | Do not use an Algorithm to bypass the Service Mapping prerequisite |
| The assessment reports a mapping gap without a complete exact three-tab UI plan | Do not create an Algorithm artifact to bypass the Service Mapping prerequisite. A user who explicitly requests code may receive only a labelled placeholder-only Groovy source draft |
| A provisional draft has been approved but the warning is not explicitly accepted | Do not create a local output artifact |
| Version 0 or 1 is present | Do not modify, replace, remove, reformat, or select either protected version |
| No nonprotected active version exists | Create only a next numeric ActiveFlag Y version when a safe base structure exists; never generate P state |
| A Custom EFF action is represented only in a P or N version | Use it as structural evidence only; edit the latest active version or create a new active version from an eligible base |
| Draft approval is absent | Do not create a local output artifact |
| A reviewable Algorithm draft is needed | Do not create a human-readable Markdown draft file; present the source and safeguards directly in chat |
| The proposed Algorithm action has unverified API assumptions | Do not create Algorithm_BO.xml until the review draft is explicitly approved |
| A draft removes or reorders a selected baseline downstream terminal action without approval | Do not create or return Algorithm_BO.xml |
| A nontarget source version differs | Do not return the artifact |
| Fusion import or deployment is requested | Do not import, publish, deploy, or execute runtime testing; the approved local ZIP packaging step remains permitted |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OMSUBALGO.RETURN.NO_CHANGE | terminal | 5 | terminal | none | OMSUBALGO.ENFORCE.DESIGN | stop | The validated assessment shows that no Algorithm change is required |
| OMSUBALGO.APPROVAL.GATE | decision | 6 | execution_gate | approved-standard->OMSUBALGO.RETURN.ARTIFACT;approved-provisional-warning-not-accepted->OMSUBALGO.RETURN.ISSUES;approval-missing-or-out-of-scope->OMSUBALGO.RETURN.ISSUES | OMSUBALGO.ENFORCE.DESIGN | stop | A reviewable draft exists, a safe target is selected, and an artifact request is in scope |
| OMSUBALGO.RETURN.ARTIFACT | terminal | 7 | terminal | none | OMSUBALGO.APPROVAL.GATE | stop | An approved, validated local Algorithm_BO.xml artifact is ready; provisional output remains not ready to import |
| OMSUBALGO.RETURN.ISSUES | terminal | 8 | terminal | none | none | stop | Any blocking validation, dependency, mapping prerequisite, design, approval, artifact, or scope outcome occurs |

## Sources

- User-approved FOM-to-OSS version rule: exclude Versions 0 and 1 from every target selection.
- User-approved FOM-to-OSS artifact rule: return Algorithm_BO.xml after approval only, edit only the latest active target or add a new active version, and never generate P state.
- User-approved FOM-to-OSS provisional rule: approved provisional drafts require the stated warning and a separate explicit continuation before local artifact generation.
