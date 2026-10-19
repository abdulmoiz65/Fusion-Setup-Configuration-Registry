# Time Consumer Sets Input Validation

## Source Basis

- Time Consumer Sets authoring pack: 01-functional-specification.md, 02-ui-rest-field-mapping.md, 03-authoring-guardrails.md, and 06-rest-describe-evidence.md.
- Time Consumers Technical Design Document for FSCR, Confluence page 21738724710, version 3, as recorded in the authoring pack.
- Developer-provided business-only Complete Summary requirements, 2026-09-09.

## Complete Summary Input Contract

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Verified summary source | Use only populated structured business values that completed input validation, applicable lookup resolution, and defaulting or preservation | A Complete Summary is prepared | |
| User selections | Include every verified user-facing business value explicitly supplied by the user | Every Complete Summary | |
| Applied defaults | Include every user-facing default that was actually applied in a separate Defaults Applied section | Every Complete Summary | |
| Blank and metadata values | Omit blank, null, unused, metadata-only, and internal execution values. Never display Worker approval or ApprovalWorkflowForWorkersFlag. | Every Complete Summary | |
| Populated children | Show populated child records using business labels only; do not render an empty child section | A child record has values | |
| Summary readiness | Generate and display the Complete Summary and Defaults Applied immediately before requesting provider-owned approval | A create or update request is ready for provider approval | |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Environment release support | environment_version_details from shared.baseline-assessment.topology-manager.environment-info | Block all Time Consumer Sets processing when the target release is before 27A | Retrieve the exact target environment release before validation, lookup, REST sample generation, or provider approval | Every request | resolve_environment_release_support |
| REST capability | One exact usable current timeConsumerSets Data Loader registration and metadata set | Block readiness when the release is 27A or later, or release details are unavailable, and the capability cannot be confirmed | Resolve the live registration and current metadata before validation | Every request that is not blocked as before 27A | resolve_time_consumer_sets_rest_capability |
| Parent identity | Name | Block readiness | Request the Time Consumer Set Name | Create |  |
| Approval workflow and routing | ApprovalWorkflowForWorkersFlag and AbsenceApprovalRoutingCode | Block readiness for a new Consumer Set; preserve verified current values for an existing Consumer Set update | Request the values only for create; resolve the existing Consumer Set before update | Create or update | search_time_consumer_sets_by_criteria |
| Time consumer selection | At least one configuration for PJC or PYR | Block readiness | Request Project Costing, Payroll, or both | Create or update |  |
| Project Costing configuration | TimeConsumerId, TimeConsumerCode PJC, and TimeCategoryId | Block readiness | Resolve the selected Time Category before preparing the configuration | Project Costing is selected | resolve_time_category |
| Payroll configuration | TimeConsumerId, TimeConsumerCode PYR, and TimeCategoryId | Block readiness | Resolve the selected Time Category before preparing the configuration | Payroll is selected | resolve_time_category |
| Parent-child local correlation | TimeConsumerSetId on the parent and every new configuration | Block preview and upload | For a create, generate one unique numeric local TimeConsumerSetId and repeat it in every new configuration row. For an update, use only the persisted ID returned by Fusion. | Create or update with new configurations | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A Time Consumer Sets request starts | Retrieve environment_version_details before any task validation, lookup, REST sample generation, or provider approval | If the release is before 27A, inform the user that Time Consumer Sets is not available through this skill for environments before release 27A and stop | resolve_environment_release_support |
| The release is 27A or later, or release details are unavailable | Require one exact usable current timeConsumerSets Data Loader registration and metadata set | Continue only after the capability is confirmed; when release details are unavailable, record that result and use no alternate route | resolve_time_consumer_sets_rest_capability |
| A selected configuration has a Time Category business value | Require one resolved Time Category result before accepting TimeCategoryId | Continue only with the returned identifier and verified display name | resolve_time_category |
| A Time Category lookup is unavailable or ambiguous | Treat the configuration as unresolved | Stop before preview and obtain a single exact TcatName match from timeCategoriesLOV | resolve_time_category |
| A search or update is requested | Require at least one search parameter; compare every supplied parameter before presenting candidates | Retrieve all pages, show candidates meeting every supplied condition, and obtain a selection when more than one candidate matches | search_time_consumer_sets_by_criteria |
| A new Consumer Set is prepared or submitted | Require the duplicate check to try exact Name, then partial Name. Only when neither matches, compare every applicable user-supplied parent and configuration parameter against existing records and retrieve complete candidate details as needed. | If an equivalent record is found, present it and wait for the user's use-existing or create-new choice before preparing, submitting, or creating anything | search_time_consumer_sets_by_criteria |
| An existing Consumer Set is updated | Require a selected candidate that meets every supplied search condition and a complete current-record read before preparing the update | Preserve current parent settings and existing configurations; add only the requested consumer | search_time_consumer_sets_by_criteria |
| A create or update request is ready for provider approval | Require a Complete Summary formed only from verified structured business values | Generate the summary before the provider-owned approval process | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Description is omitted | Preserve a null or omitted optional Description according to the selected write contract | Create or update |  |
| TimeConsumerCode is supplied | Accept only PJC for Project Costing or PYR for Payroll | A configuration is prepared |  |
| ApprovalWorkflowForWorkersFlag or EntryLevelApprovalFlag is supplied | Require a Boolean value and require the final Data Loader DAT to serialize it as lowercase true or false | An XLSX source is converted to the upload archive |  |
| EntryLevelApprovalFlag is supplied | Require a Boolean value | A configuration is prepared |  |
| AbsenceApprovalRoutingCode is supplied | Accept only ORA_ABS_MGMT_APPRVL_RULES or ORA_TL_APPRVL_RULES | Create or update |  |
| ConfigurationId is supplied | Retain it only for an existing child configuration; do not use it for a new child | Update of an existing configuration |  |
| New configuration TimeConsumerSetId | Require a nonblank numeric value that exactly equals the parent TimeConsumerSetId; treat the values as DAT-local correlations, not persisted Fusion IDs | Create |  |
| Update TimeConsumerSetId | Accept only the persisted ID returned by the verified Fusion parent read; do not generate, replace, or infer an ID | Update | search_time_consumer_sets_by_criteria |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TCS.VALIDATE_INPUT | step | 10 | validate_input | valid->TCS.SEARCH_TIME_CONSUMER_SETS;missing->TCS.HANDLE_ERROR;invalid->TCS.HANDLE_ERROR | TCS.CHECK_REST_CAPABILITY | stop | A Time Consumer Sets name search, create, or update request passed the release and REST-capability gates |
