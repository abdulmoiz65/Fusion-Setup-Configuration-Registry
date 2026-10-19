# Profile Management dependency handoffs

This skill loads and maintains Profile Management data. It does not configure
the setup prerequisites that give that data meaning. A create, update, or
migration request must retain exact, read-only evidence for every dependency it
uses before an immutable HCM Data Loader artifact is prepared.

| Dependency | Owning scope | Required evidence before artifact preparation | This skill's behavior when unavailable |
| --- | --- | --- | --- |
| Model Profile configuration | Profile Types and Content Section Configuration | Exactly one Profile Type code/ID, each requested additional-information flag enabled, each requested active Section ID/Name, and exactly one applicable Value Set or `not-applicable` evidence | Block all model-profile artifact preparation |
| Content Section | Profile Types and Content Section Configuration | Exactly one `profileTypeSectionsLOV` result for the selected type and section, including `SectionId` and `SectionContext` | Block a future Profile Item route |
| Content Item | Profile Management Content Library Configuration | Exactly one `contentItemsLOV` result for the returned item ID and name, plus the downloaded Content Item template showing Value Set ID and Value Set Name | Block Content Item artifact preparation |
| Rating Model / item values | Profile Rating Model Configuration or Content Library owner | Exact owner-provided configuration evidence for the selected item and rating values | Block rows requiring ratings or constrained item values |
| Translation language | Language setup owner | Exactly one installed `LanguageCode` from `languagesLOV` | Block translation artifact preparation |
| `HRT_PROFILE_ITEMS` DFF context and value | Application Flexfield Foundation | Deployed context and segment/value contract for the target environment, with live `FLEX:HRT_PROFILE_ITEMS` metadata | Block DFF-bearing `ProfileItem` rows; never use `ATTRIBUTE_CATEGORY` as a substitute |
| Attachment data type | Application Attachment Foundation | Downloaded and target-validated Talent Profile attachment template, plus exact supported type and file-processing contract | Block `ProfileAttachment` preparation |
| Relationship target | Workforce Structures / Profile Management owner | Exactly one supported target identity and relationship contract | Block `ProfileRelation` preparation |
| Data Loader access | Data Load and Migration Foundation | Read access for validation and upload/initiation access only after explicit final-artifact approval | Block live execution but permit local guidance and validation |
| Profile search/index synchronization | Profile Management platform operations | Separately approved `Update Profile Search Keywords` followed by `Synchronize Profile Search Keywords Index`; include optimization only when specifically required, with monitoring and verification contract | Out of scope for data load unless explicitly routed as a separate operation |
| Security roles | Security Console | Owner-confirmed role/privilege assignment | Report authorization blocker; never attempt role changes |

## Evidence contract

Each dependency record supplied to the HDL adapter must identify the child
record, dependency name, expected value, and an `exactly-one` outcome. The
adapter rejects missing, ambiguous, or stale/incomplete records. A completed
dependency handoff is not upload approval; immutable archive preview and
explicit final approval remain separate gates.

## Baseline boundary

Foundation setup, search initialization, security configuration, and scheduled
operations are prerequisite or operations-scope deliverables. This skill can
consume their evidence but must not configure them. Root and child profile data
loading are master-data capabilities that may be phased after the foundation
baseline.
