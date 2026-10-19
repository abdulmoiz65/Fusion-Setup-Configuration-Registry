# Read-only prerequisite inspection

Purpose: establish deployed metadata before evaluating creation. Explicitly
approved as a separate read-only route; not a readiness override for the create
Task Hook graph. The graph and all existing business-operation checks remain intact.

1. Require a user-requested prerequisite inspection, selected environment name,
   exact HTTPS origin, existing shared REST client and current properties matching
   both environment and origin. Do not print properties or credentials.
2. Use instructor_workflow.py inspect-prerequisites --expected-environment <name>
   --expected-origin <configured-origin>. Its only external operation is
   GET /hcmRestApi/resources/11.13.18.05/learningInstructors/describe through
   core/fusion-api/rest-api-client/scripts/fusion_rest_client.py, framework 9.
   This is the existing declared resource describe contract. No arbitrary endpoint,
   q query, person identifier, response-link traversal or mutation argument exists.
3. Shared authentication and host/redirect protections remain authoritative.
   If login is necessary, use the selected shared authentication workflow. Never
   substitute browser scraping, a private HTTP client or disabled TLS verification.
4. Report observed resourcesDFF flags and missing information separately. Root
   mandatory-on-create metadata alone cannot prove child/context requiredness,
   absence of required tenant configuration or safe omission/default behavior.
   Read response bytes using shared --output in a private temporary directory,
   separate from authentication/status chatter. Temporary responses are removed
   on completion, not copied into project history.
5. This command cannot satisfy Task Hook, approve an artifact or enable creation.
   Confirmed required values require a verified mapping; incomplete child metadata
   remains unverified, not implicitly optional. Set applicability is a separate check.

Local generated model evidence (not target configuration): WLF_RESOURCE_DFF,
application 10503, ResourceDFFVO customResource1 and __FLEX_Context lack IsNotNull
in the inspected jkaribee_v2 snapshot. ResourceId is system identity, not a custom
value the implementer must supply. Deployed segments may differ.

## Separate flexfield result

The inspection returns `flexfieldAssessment` independently of Set applicability.
It evaluates only the exact instructor resourcesDFF attribute list: required
custom fields/context block missing input or mapping; missing, malformed,
duplicate or conflicting flags remain unknown. ResourceId is parent identity,
not a required custom input. Optional fields return `exposed_fields_optional`,
not create readiness: context defaults and whole-child omission still require
verified contracts. No user-provided boolean can mark those contracts verified.

A project may explicitly defer FDD Set filtering without asserting that the
tenant option is disabled. That scope decision does not clear this DFF check,
change reusable Set requirements, or authorize a load.

## Root-only configuration validation

Run `instructor_workflow.py validate-configuration --input <scope.json>
--expected-environment <name> --expected-origin <origin>`. The scope file contains
only `setFiltering: "deferred"` and `decisionReference` naming the recorded user
decision. The executing agent must read and verify that decision; a fabricated
reference is not consent. This is a scope declaration, not a tenant-disabled flag.
No supplied Set or DFF input is supported or silently discarded.

After the shared planner passes, the command performs the same fixed describe GET.
It requires WLF application 10503 DFF metadata, exact global-segment count, optional
custom/context fields, no advertised custom/context default, and a generated
ResourceId. Required, unknown, non-global, malformed or incomplete evidence blocks.
Success is `configuration_validated`, with target, scope and response fingerprints;
it is not `createReady`, approval, privilege evidence, or proof of live creation.
Task Hook must require this current result before preview, alongside all other rules.

Source basis (jkaribee_v2 core model src/oracle/apps):
`flex/hcm/engagement/learn/core/model/items/resourceDFF/view/ResourceDFFVO.xml`
declares FND_IsChildSharingParentEntity=true and uses ResourceDEO/WLF_RESOURCES_B.
`flexViewLink/hcm/engagement/learn/core/model/items/courses/instructorResourceDFF/view/flex/link/InstructorResourceVOTOResourceDFFVO.xml`
joins on ResourceId. The child represents attributes of the parent entity, not a
separate mandatory business record. Combined with current optional global fields
and optional context, no extra DFF input is required for this narrow preflight.
Do not claim omitted values will stay null: server defaults and actual effects
are verified after an approved load. Keep runtimeOmissionVerified=false until then.
