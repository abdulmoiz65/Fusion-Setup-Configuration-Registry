# Reference Lookups

Use `core.fusion-api.apps-common.value-sets` first for every root, validation-table, and child-value operation. The only direct collection route allowed here is the restricted read-only root-pagination fallback defined below. Never use curl, browser automation, FSM, or another transport as a fallback.

## Baseline Metadata

| Source | Location | Version or Date | Included | Excluded |
|---|---|---|---|---|
| Recruiting and Candidate Experience Supported Modules | `https://confluence.oraclecorp.com/confluence/display/FRCE/Recruiting+and+Candidate+Experience+-+Lookups%2C+Valuesets%2C+Profile+Options#RecruitingandCandidateExperienceLookups%2CValuesets%2CProfileOptions-SupportedModules` | Complete table provided 2026-10-06 | Every concrete LBA ModuleId row | Rows marked `Not found in IRC seed artifacts`, duplicate headers, and the APPLICATION/IRC registration row |

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| match_recruiting_module_id | A current root response is evaluated for Recruiting ownership | Current API ModuleId and the complete Recruiting ModuleId Allowlist below | Require one exact ModuleId match; the ModuleId is the authority and the display name is baseline-derived unless returned by the API | In-scope decision, exact ModuleId, baseline-derived module display name, module key, and baseline version | Missing ModuleId, zero matches, or multiple matches blocks the request; never infer ownership from code, name, prefix, description, or export |

## Recruiting ModuleId Allowlist

| Module Display Name | Module Key | ModuleId |
|---|---|---|
| Agency Container | HcmRecruitingAgency | 7D6A51B0706570DBE0533380F50AA527 |
| Candidate Experience | HcmRecruitingCandidateExp | 0EC43113C4D24A8CE050F00A172044FC |
| Candidate Experience Client | HcmRecCandidateExpJet | 16B40731291088BBE050F00A172033A6 |
| Candidate Experience Core | HcmRecCandidateExpCore | 0EC43113C4D94A8CE050F00A172044FC |
| Candidate Experience Setup | HcmRecCandidateExpSetup | 0EC43113C4DA4A8CE050F00A172044FC |
| Candidate Job Application Flow | HcmRecSetupApplyFlow | 2F0607E35226D7D9E050F00A17205BF9 |
| Candidate Job Applications Core | HcmRecHiringSubsCore | 16B3E42361402EDFE050F00A17203181 |
| Candidate Job Applications Disqualification | HcmRecHiringDisQual | 2F0607E3521DD7D9E050F00A17205BF9 |
| Candidate Job Applications Setup | HcmRecHiringSubsSetup | 16B3F684C903905EE050F00A1720339D |
| Candidate Pools | HcmRecSourcingCandPools | 16B40731290E88BBE050F00A172033A6 |
| Candidates | HcmRecSourcingCandidates | 16B40731290D88BBE050F00A172033A6 |
| Chatbot Container | HcmRecruitingChatbot | DEEF9868B04471DBE0534CA56C643CBB |
| Diversity | HcmRecHiringDiversity | 2F0607E3521ED7D9E050F00A17205BF9 |
| Employee Events Container | HcmEmployeeEvents | 2ABF3578FC174967E0634CA56C64D04A |
| Express Hiring | HcmRecHiringExpress | 20B27F907ADA2FA1E0634CA56C646E4C |
| Hiring | HcmRecruitingHiring | 0EC43113C4D14A8CE050F00A172044FC |
| Hiring Core | HcmRecHiringCore | 0EC43113C4D74A8CE050F00A172044FC |
| Hiring Setup | HcmRecHiringSetup | 0EC43113C4D84A8CE050F00A172044FC |
| Initiative Container | HcmRecruitingInitiatives | 63B46620F6E6761FE0531720F00A1E99 |
| Initiative Container Core | HcmRecInitiativesCore | 63B46620F6E7761FE0531720F00A1E99 |
| Initiative Container Setup | HcmRecInitiativesSetup | 63B46620F6E8761FE0531720F00A1E99 |
| Internal Candidate Experience | HcmRecruitingIntCandExp | 2F0607E35223D7D9E050F00A17205BF9 |
| Internal Candidate Job Application | HcmRecIntCandExpApply | 2F0607E35225D7D9E050F00A17205BF9 |
| Internal Candidate Job Search | HcmRecIntCandExpJobs | 2F0607E35224D7D9E050F00A17205BF9 |
| Interview Management Core | HcmRecHiringIntrMgmtCore | 16B40731290B88BBE050F00A172033A6 |
| Interview Management Setup | HcmRecHiringIntrMgmtSetup | 16B40731290C88BBE050F00A172033A6 |
| Job Distribution | HcmRecJobDistribution | 4F9ED59CEC1A606FE0531720F00AA85A |
| Job Offers Core | HcmRecHiringOffersCore | 16B3F684C904905EE050F00A1720339D |
| Job Offers Setup | HcmRecHiringOffersSetup | 16B3F684C905905EE050F00A1720339D |
| Job Requisition Security Profiles | HcmRecruitingSecProfiles | 2F0607E35222D7D9E050F00A17205BF9 |
| Job Requisitions Core | HcmRecHiringReqsCore | 16B3E423613E2EDFE050F00A17203181 |
| Job Requisitions Setup | HcmRecHiringReqsSetup | 16B3E423613F2EDFE050F00A17203181 |
| Message Tracking | HcmRecMessageTracking | 4F33D87BDB0133A0E0531720F00ADE1F |
| Onboarding | HcmRecruitingOnboarding | 0EC43113C4D34A8CE050F00A172044FC |
| Onboarding Core | HcmRecOnboardingCore | 0EC43113C4DB4A8CE050F00A172044FC |
| Onboarding Setup | HcmRecOnboardingSetup | 0EC43113C4DC4A8CE050F00A172044FC |
| Process Flexibility | HcmRecProcessLifecycle | 2F0607E35227D7D9E050F00A17205BF9 |
| Profile Import | HcmRecSourcingProfImport | 2F0607E35221D7D9E050F00A17205BF9 |
| Prospects | HcmRecHiringProspects | 2F0607E3521FD7D9E050F00A17205BF9 |
| Recruiting Activity Center | HcmRecActivityCenter | E9CE41772E780206E0534CA56C64C1BA |
| Recruiting Assessments | HcmRecAssessments | 68E5EDCFE3F40F29E0531720F00A2C88 |
| Recruiting Background Check | HcmRecBackgroundCheck | 541331ECF6533148E0531720F00A604A |
| Recruiting Chatbot | HcmRecCandidateExpChatbot | 4F33B8923D112CA0E0531720F00A8ABB |
| Recruiting Common | HcmRecruitingCommon | 0EC43113C4D54A8CE050F00A172044FC |
| Recruiting Communicate | HcmRecruitingCommunicate | 42B81527FF3F4182E0634CA56C64115F |
| Recruiting Communicate Common | HcmRecCommunicateCommon | 42B85848D5D6478FE0634CA56C64625C |
| Recruiting Communicate Core | HcmRecCommunicateCore | 42BA33B139F37C62E0634CA56C64B228 |
| Recruiting Communicate Employee Communities | HcmRecCmtEmpCommunities | 42E75ABAEF557C60E0634CA56C64BB98 |
| Recruiting Communicate My Communications | HcmRecCommunicateMyComms | 42BA33B139F67C62E0634CA56C64B228 |
| Recruiting Communicate Setup | HcmRecCommunicateSetup | 42BA33B139F47C62E0634CA56C64B228 |
| Recruiting Direct Apply | HcmRecDirectApply | 0A07124C0D611DBCE0634CA56C644657 |
| Recruiting Events Container | HcmRecruitingEvents | DEEFA17A4DC27442E0534CA56C646179 |
| Recruiting Home Page | HcmRecruitingHome | 16B40731290F88BBE050F00A172033A6 |
| Recruiting LinkedIn Integration | HcmRecLinkedInIntegration | 83757A378FC43D57E0533380F50AE8F1 |
| Recruiting Matching | HcmRecruitingMatching | 5761AA1D45752405E0531720F00A77F6 |
| Recruiting Matching Core | HcmRecMatchingCore | 5761AA1D45762405E0531720F00A77F6 |
| Recruiting Matching Setup | HcmRecMatchingSetup | 5761AA1D45772405E0531720F00A77F6 |
| Recruiting Message Designer | HcmRecMessageDesigner | 4F9C58D820D003DBE0531720F00A6B03 |
| Recruiting Message Designer Core | HcmRecMsgDesignerCore | 4F9C58D820D203DBE0531720F00A6B03 |
| Recruiting Message Designer Jet UI | HcmRecMsgDesignerJet | 4F9C58D820D103DBE0531720F00A6B03 |
| Recruiting Opportunity Market Place | HcmRecOppMarket | 961541084E545547E0533380F50A88AD |
| Recruiting Setup | HcmRecruitingSetup | 0EC43113C4D64A8CE050F00A172044FC |
| Recruiting Source Tracking | HcmRecSourceTracking | 541331ECF6553148E0531720F00A604A |
| Recruiting Source Tracking Core | HcmRecSrcTrackingCore | 541331ECF6563148E0531720F00A604A |
| Recruiting Talent Network | HcmRecruitingTalentNetwork | 04010C2B40CA7A0EE0634CA56C649EB2 |
| Recruiting Talent Network Common | HcmRecTalentNetworkCommon | 040111CA0E847CD1E0634CA56C6450E0 |
| Recruiting Talent Network Core | HcmRecTalentNetworkCore | 040111CA0E857CD1E0634CA56C6450E0 |
| Recruiting Talent Network Setup | HcmRecTalentNetworkSetup | 040111CA0E867CD1E0634CA56C6450E0 |
| Recruiting Tax Credits | HcmRecTaxCredits | 83757A378FC53D57E0533380F50AE8F1 |
| Recruiting Third Party | HcmRecruitingThirdParty | 4F9C58D820D303DBE0531720F00A6B03 |
| Recruiting Third Party Common | HcmRecThirdPartyCommon | 4FB2BCF25DB135AFE0531720F00A1567 |
| Recruitment Campaigns | HcmRecruitingCampaigns | 4F33B8923D122CA0E0531720F00A8ABB |
| Recruitment Campaigns Core | HcmRecCampaignsCore | 4F33D87BDAFF33A0E0531720F00ADE1F |
| Recruitment Campaigns Runtime | HcmRecCampaignsRuntime | 4F33D87BDB0033A0E0531720F00ADE1F |
| Referrals | HcmRecSourcingReferrals | 2F0607E35220D7D9E050F00A17205BF9 |
| Sourcing | HcmRecruitingSourcing | 0EC43113C4D44A8CE050F00A172044FC |
| Sourcing Core | HcmRecSourcingCore | 0EC43113C4DD4A8CE050F00A172044FC |
| Sourcing Setup | HcmRecSourcingSetup | 0EC43113C4DE4A8CE050F00A172044FC |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| discover_recruiting_value_sets | Root listing is requested | Root collection request and complete maintained ModuleId allowlist | First use Common Value Sets root discovery; only when it returns `hasMore=true` without a safe continuation contract, use read-only `GET /fscmRestApi/resources/11.13.18.05/valueSets` and continue using each response's offset and limit | Only root fields actually present, including returned root identifier, ValueSetCode, Description, ModuleId, validation metadata, data characteristics, and protection or security indicators | Process every page until `hasMore=false`, de-duplicate by returned root identifier, then retain roots whose current ModuleId exactly matches the allowlist | Complete Recruiting-owned root list with API ModuleId and baseline-derived display module name | Empty final collection is valid; `hasMore=true` without usable offset or limit is a pagination blocker; never guess continuation parameters |
| read_value_set_by_exact_code | A particular root, validation definition, child list, or child mutation is requested | Exact user-provided ValueSetCode | Common Value Sets exact-root read with the unchanged ValueSetCode passed as `valueSets_Id` | Only fields actually present, including returned root identifier, ValueSetCode, Description, ModuleId, validation metadata, data characteristics, and protection or security indicators | Require one exact current root whose ValueSetCode equals the supplied code and whose ModuleId resolves through the allowlist | Exact parent identity, ownership, validation behavior, protection state, and supported child capability | No match, multiple matches, missing ModuleId, or a nonallowlisted ModuleId blocks; do not run prior numeric-ID discovery |
| read_value_set_validation_metadata | Validation-table details are explicitly requested or needed to explain current behavior | Exact current parent read and its returned identifiers | Common Value Sets validation-table list or exact read for the parent | Only validation-table metadata fields actually returned | Require metadata to belong to the exact current parent; de-duplicate by returned validation-table identifier | Response-grounded validation explanation and child-management readiness | Empty metadata is reported as empty; ambiguity or mismatch blocks explanation or mutation |
| resolve_value_set_child | Child values are listed or a child create, update, or delete is requested | Exact current parent, requested business value, and returned child identifiers | Common Value Sets child-value list and, for update or delete, exact child read through the returned child identifier | Only child fields, identity, protection, dates, and other metadata actually returned | De-duplicate by returned child identifier; for create require the proposed child absent; for update or delete require exactly one fresh exact child read by returned identifier | Current child list or immutable exact child state, supported fields, protected fields, and minimal delta basis | Incomplete list, collision, no match, many matches, missing returned identifier, or uncertain protection metadata blocks mutation |
| verify_value_set_child_change | One approved child mutation has returned | Exact parent ValueSetCode, returned affected child identifier when it still exists, approved delta, and approval fingerprint | Common Value Sets fresh exact child read, or supported current child list to verify deletion absence | Only fields and identifiers actually returned | Create or update must match the approved post-change state; delete must prove the exact returned child identifier is absent | Verified result, preserved-field comparison, and sanitized diagnostic evidence | Missing, conflicting, ambiguous, or uncertain verification blocks completion; never retry the mutation automatically |

## Exact ValueSetCode Routing

| User Input | Provider Parameter | Effective Provider Route |
|---|---|---|
| Exact `Country1` | `valueSets_Id=Country1` | `/fscmRestApi/resources/11.13.18.05/valueSets/Country1` |
| Exact `Country1`, child values requested | `valueSets_Id=Country1` | `/fscmRestApi/resources/11.13.18.05/valueSets/Country1/child/values` |

These examples document parameter mapping. The wrapper passes the exact code to Common Value Sets and does not invoke these routes directly except for the separately defined root-pagination fallback.

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Common Value Sets provides complete pagination | Follow its result and continuation procedure; do not use the restricted fallback. |
| Common Value Sets returns `hasMore=true` without safe continuation | Use only the read-only root collection fallback, consume response offset and limit page by page, and stop if either is unusable. |
| Particular value set lacks an exact user-provided ValueSetCode | Ask for the exact code; do not treat a partial code, description, display name, or inferred value as exact. |
| Current root ModuleId matches | Authorize review and supported child CRUD without another crosswalk, per-value-set baseline, seed mapping, or task-page proof. |
| Current response omits a field | Omit that field from the result and do not infer its value or editability. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RVS.DISCOVER_ROOTS | decision | 2 | reference_lookup | complete->RVS.MATCH_SCOPE;pagination_blocked->RVS.LOOKUP_ISSUES;issues->RVS.LOOKUP_ISSUES | RVS.VALIDATE | stop | A complete Recruiting value-set list is requested |
| RVS.READ_PARENT | decision | 3 | reference_lookup | found->RVS.MATCH_SCOPE;issues->RVS.LOOKUP_ISSUES | RVS.VALIDATE | stop | An exact root or its validation or children are requested |
| RVS.MATCH_SCOPE | decision | 4 | evaluate_result | root_review->RVS.DONE_ROOT_REVIEW;validation->RVS.READ_VALIDATION;children->RVS.RESOLVE_CHILD;create_child->RVS.RESOLVE_CHILD;update_child->RVS.RESOLVE_CHILD;delete_child->RVS.RESOLVE_CHILD;blocked->RVS.OWNERSHIP_ISSUES | none | stop | Current root ModuleId values must be filtered or authorized |
| RVS.READ_VALIDATION | decision | 5 | reference_lookup | reviewed->RVS.DONE_VALIDATION;issues->RVS.LOOKUP_ISSUES | RVS.MATCH_SCOPE | stop | Validation-table metadata is requested or required for explanation |
| RVS.RESOLVE_CHILD | decision | 6 | reference_lookup | reviewed->RVS.DONE_CHILD_REVIEW;create_ready->RVS.ENFORCE;update_ready->RVS.ENFORCE;delete_ready->RVS.ENFORCE;issues->RVS.LOOKUP_ISSUES | RVS.MATCH_SCOPE | stop | Child values are listed or a supported child mutation is requested |
| RVS.VERIFY_CHILD | decision | 9 | reference_lookup | verified->RVS.DONE_CHANGE;mismatch->RVS.POST_CHANGE_ISSUES;uncertain->RVS.POST_CHANGE_ISSUES | RVS.VALIDATE | stop | A delegated child mutation requires fresh verification |
