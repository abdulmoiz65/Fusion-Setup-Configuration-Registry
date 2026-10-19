# Reference Lookups

Delegate every effective-value, profile-definition, configured-value, and user-identity read to `core.fusion-api.apps-common.profile-options`. Do not construct REST URLs, call curl, manage OAuth, use browser automation, or duplicate Common Profile Options transport.

## Baseline Metadata

| Source | Location | Version or Date | Included | Excluded |
|---|---|---|---|---|
| Recruiting and Candidate Experience Supported Modules | `https://confluence.oraclecorp.com/confluence/display/FRCE/Recruiting+and+Candidate+Experience+-+Lookups%2C+Valuesets%2C+Profile+Options#RecruitingandCandidateExperienceLookups%2CValuesets%2CProfileOptions-SupportedModules` | Complete table provided 2026-10-06 | Every concrete LBA ModuleId row | Rows marked `Not found in IRC seed artifacts`, duplicate headers, and the APPLICATION/IRC registration row |

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| resolve_profile_option_ownership_crosswalk | Every effective, definition, configured-value, or mutation request | Exact ProfileOptionName plus an approved versioned crosswalk containing ProfileOptionName, approved Recruiting ModuleId, display module name, evidence source, and evidence version; complete ModuleId allowlist below | Require exactly one exact ProfileOptionName row; its ModuleId must match exactly one current allowlist row; do not infer from prefixes, descriptions, values, or effective results | Approved exact ProfileOptionName, ModuleId, display module name, crosswalk source/version, and baseline version | Missing, stale, duplicate, unmapped, or nonallowlisted evidence blocks every profile-specific result and mutation |
| resolve_product_application_scope | A Product-level configured value is requested | Exact application short name or scope key from approved versioned evidence | Require exactly one supported technical key; a display label alone is never a match | Exact Product LevelValue or item key and evidence version | Missing, stale, no-match, or many-match evidence blocks the Product operation |

## Required Ownership Crosswalk Contract

| Field | Requirement |
|---|---|
| ProfileOptionName | Exact internal profile code; unique within the crosswalk. |
| Approved Recruiting ModuleId | Exact value from the complete current ModuleId allowlist. |
| Display module name | Human-readable name paired with that ModuleId in the approved evidence. |
| Evidence source | Reviewable approved source location or artifact reference. |
| Evidence version | Immutable version or effective date used for freshness evaluation. |

No approved ProfileOptionName crosswalk is present on the referenced Confluence page. The skill must receive a separately approved current crosswalk satisfying this contract before returning profile-specific values or permitting a mutation.

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
| read_effective_profile_values | Effective values are requested for the authenticated current session | Current authenticated session and approved ownership crosswalk | Delegated Common Profile Options effective-values read | Only identity and effective-value fields actually returned | De-duplicate by returned profile identity, then retain only exact ProfileOptionName values that each match one approved crosswalk row; redact sensitive values | Business label when available, exact name, approved module mapping, effective scope, and redacted value summary | Missing crosswalk match excludes the row and blocks any claim of Recruiting ownership; ambiguous identity blocks the result |
| read_profile_option_definition | A definition, configured value, or mutation is requested | Exact ProfileOptionName from one approved crosswalk row | Delegated Common Profile Options exact definition read | Business label when available, ProfileOptionName, SiteLevelEnabled, SiteLevelUpdatable, ProductLevelEnabled, ProductLevelUpdatable, UserLevelEnabled, UserLevelUpdatable, and configured child links/metadata actually returned | Require one exact definition whose name equals the approved crosswalk identity | Exact definition, level eligibility, configured-value resources, and redacted current summary | No match, many matches, ownership mismatch, or missing required level metadata blocks configured-value mutation |
| resolve_configured_profile_value | A Site, Product, or User configured value is read or mutated | Exact approved ProfileOptionName, selected level, exact scope key, and current definition metadata | Delegated Common Profile Options level-specific child list and exact item read | Only configured-value, identity, level, scope, and protection fields actually returned | Require Site item `SITE`, exact approved Product LevelValue, or exact UserName item; require one fresh current item for update/delete and exact absence for create | Current redacted state, returned item identity, exact level/scope, supported delta, and preservation basis | No match blocks read/update/delete but may establish create absence; collision blocks create; many matches or uncertain state blocks mutation |
| resolve_profile_user_identity | A User-level configured value is requested | Exact user identity selected by the user | Delegated Common Profile Options profile-user resolution | Returned exact UserName item identity and user GUID required as create LevelValue | Require exactly one provider-resolved current user; never treat a display name as the GUID | User item identity and create GUID; redact unnecessary personal data | No match, many matches, or missing GUID blocks create; unresolved item identity blocks read/update/delete |
| verify_profile_value_change | One approved configured-value mutation has returned | Exact approved ProfileOptionName, level, scope, returned item identity, approved delta or deletion, and approval fingerprint | Delegated Common Profile Options fresh exact configured-value read | Only identity, scope, and configured-value fields actually returned | Create/update must match the approved state; delete must prove exact-item absence; redact sensitive values | Verified result, preserved identity/scope, and sanitized evidence | Missing, mismatched, ambiguous, or uncertain verification blocks completion; never retry mutation automatically |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Effective-value collection is requested | Read for the current session, then filter only through the approved crosswalk; do not treat the effective result as ownership evidence. |
| Site level is selected | Require SiteLevelEnabled and SiteLevelUpdatable `Y`; use only the `SITE` item. |
| Product level is selected | Require ProductLevelEnabled and ProductLevelUpdatable `Y` plus one exact approved product/application key. |
| User level is selected | Require UserLevelEnabled and UserLevelUpdatable `Y` plus exact provider-resolved user identity and GUID where create needs it. |
| Sensitive value is returned | Show and persist only a redacted summary sufficient to compare current and proposed state. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RPO.READ_EFFECTIVE | decision | 3 | reference_lookup | found->RPO.MATCH_OWNERSHIP;issues->RPO.LOOKUP_ISSUES | RPO.CHECK_EVIDENCE | stop | Effective profile values are requested for the authenticated current session |
| RPO.MATCH_OWNERSHIP | decision | 4 | evaluate_result | effective_review->RPO.DONE_EFFECTIVE;exact->RPO.READ_DEFINITION;blocked->RPO.OWNERSHIP_ISSUES | none | stop | Profile identities must be matched to one approved current crosswalk row |
| RPO.READ_DEFINITION | decision | 5 | reference_lookup | definition_review->RPO.DONE_DEFINITION;configured->RPO.RESOLVE_SCOPE;create->RPO.RESOLVE_SCOPE;update->RPO.RESOLVE_SCOPE;delete->RPO.RESOLVE_SCOPE;issues->RPO.LOOKUP_ISSUES | RPO.MATCH_OWNERSHIP | stop | An exact approved definition and current level metadata are required |
| RPO.RESOLVE_SCOPE | decision | 6 | reference_lookup | reviewed->RPO.DONE_CONFIGURED;create->RPO.ENFORCE;update->RPO.ENFORCE;delete->RPO.ENFORCE;issues->RPO.LOOKUP_ISSUES | RPO.READ_DEFINITION | stop | Site, Product, or User configured-value scope and current state are required |
| RPO.VERIFY_VALUE | decision | 9 | reference_lookup | verified->RPO.DONE_CHANGE;mismatch->RPO.POST_CHANGE_ISSUES;uncertain->RPO.POST_CHANGE_ISSUES | RPO.VALIDATE | stop | A delegated configured-value mutation requires fresh exact verification |
