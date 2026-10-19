# Input Validation

## Input Normalization Contract

Initial input validation checks request scope and the shape of supplied values.
It must not reject an omitted value that has a documented default, declared
lookup, or server derivation. After APPLY_DEFAULTS and reference resolution,
payload preflight checks completeness of the prepared payload. Request user
input only for required values still unresolved at that point.

Normalize only the listed labels, ignoring case, spaces, underscores, and
hyphens in a label. An input label that exactly matches a published JSON field
name is already canonical. Record every normalization in the preview. Do not
fuzzy-match values or silently discard a field. Canonical REST field names and
reference alternatives are defined in ../references/project-template-rest-contract.md.

| Input shape | Accepted values | If missing or invalid | Resolver |
|---|---|---|---|
| Operation | `create`, `update`, `end_date`, `validate`, `create_child`, `update_child`, `delete_child` | Stop and request one supported operation. `duplicate`, `copy`, `create_from`, and root `delete` are unsupported. | verify_template_route |
| Target | Explicit target environment/connection | Stop. A route cannot be inferred from a template name. | verify_template_scope |
| Create identity | `TemplateName`/`ProjectTemplateName` and a unique `TemplateNumber`/`ProjectTemplateNumber` | Stop if the target already has the exact supplied identity or the required published POST field is absent. | find_project_template |
| Mutation identity | Exact `ProjectTemplateName` plus `ProjectTemplateNumber`, or a returned canonical item URI | Stop on zero or multiple rows. Do not accept a constructed ID/path. | find_project_template |
| Core fields | Only the canonical fields and aliases in ../references/project-template-rest-contract.md | Stop with every unrecognized field and its expected canonical REST name. | resolve_template_references |
| Child request | One listed child family, an explicit action, and an object/list using that family's published operation schema | Stop on an unsupported family/verb, unknown child field, duplicate row, or missing child identity for mutation. For root create with nested Tasks, a preexisting parent or child URI is not required. | resolve_template_sections |
| Dates | `YYYY-MM-DD` for template availability, root project schedule, and task schedule dates | Reject ambiguous slash dates such as `1/1/11`; do not guess century, locale, time zone, or substitute template availability for project schedule bounds. |  |
| Reference representation | Exactly one documented name/ID/code alternative for each supplied reference; customer-supplied names are first-class values | Stop on missing required representation or conflicting alternatives. Do not demand an ID when the operation publishes the supplied name field. Fusion POST validates existence, status, and compatibility. | resolve_template_references |
| Approval | Customer-readable target, business values, operation, and exact request body; internal payload checksum | Ask the customer only to approve or decline the described business change. Bind approval internally to the exact payload checksum; never ask the customer to compare technical digests. | verify_template_route |
| Deterministic payload preflight | Exact request JSON and fresh target operation metadata | Run `scripts/validate_project_template_payload.py --payload ... --describe-json ... --validation-output ...`; use the freshly computed checksums as authoritative and replace stale validation output. The validator enforces operation-metadata-required fields and root project schedule bounds for dated tasks. Stop unless it passes. | verify_template_route |

## Operation-Aware Payload Preflight

Use scripts/validate_project_template_payload.py with --operation create for a
root POST (the backward-compatible default), update for root PATCH, end_date
for an end-date-only PATCH, or create_child/update_child/delete_child plus
--child-family for a documented direct child operation. The prepared payload file
is the exact body; child DELETE uses JSON null or an empty object to represent no body.
Never fill omitted PATCH fields merely to satisfy create requirements.

Root create accepts generic Resources.projectTemplates describe data for attribute shape only, or an operationMetadata envelope identifying method POST, surface projectTemplates and the complete writable create resource. Only fresh operation-specific target create metadata may add required fields; generic root/child required or mandatory flags are ignored. Published required identity/reference/task groups remain validated after documented defaults. Read-only audit fields and generated IDs are excluded from writable/required create fields.
Operation-specific required fields apply to every supplied nested child family.
For direct task create, collapse TaskOrganizationName/TaskOrganizationId requiredness
when both are writable alternatives in the exact operation schema. A genuinely
ID-only schema still requires a proven ID. For nested template create, leave omitted task organization fields absent as
specified in ora_defaulting_rules.md and verify Fusion-derived values from task
readback. Direct task create retains its explicit/evidenced organization contract.
If operation-specific create metadata marks an omitted project-type-derived
AllowCapitalizedInterestFlag or AssetAllocationMethodCode required, stop with a
contract conflict. Reconcile the metadata with the documented create contract;
do not ask for these values or insert them to defeat derivation. Explicitly
supplied values remain subject to normal type and enum validation.
For non-create operations, the metadata file must contain operationMetadata with method
POST/PATCH/DELETE, surface projectTemplates or the exact child family, and
resource containing attributes and required fields narrowed to that published
operation and fresh target contract. This envelope records selected structural
evidence; it does not prove canonical URI, write permission or consumer safety.
The workflow must obtain that evidence through its existing declared route.

The operationMetadata resource must describe the complete selected writable
operation, including nested child attributes. Generic describe is not such an
envelope. Record its target/source, collection time and SHA-256 in workflow
evidence; a local JSON file alone cannot prove that target metadata is fresh.

For create preparation, pass --prepared-payload-output with a separate file.
All output paths must differ from every input and from one another, including
symlink/hard-link aliases. Invalid metadata or input JSON blocks preparation.
The validation record contains defaults, redacted priority resolutions, source
payload_sha256 and prepared_payload_sha256. Preview/approval/submission bind to
the prepared artifact. A changed or still-unnormalized approved artifact fails
the optional --expected-payload-sha256 handoff check; never normalize it silently
under an old approval. Omitted create defaults are not applied to PATCH.
Retain the original preparation record with its defaults/resolutions and source
digest. Revalidation of an already prepared approval artifact writes a separate
record; it must not replace the evidence of the user's original supplied name.
The validate-only business operation uses the selected underlying POST/PATCH
preflight schema and requires no mutation approval or validation REST endpoint.

For example, an end-date preflight metadata envelope has method PATCH, surface
projectTemplates and a resource attributes entry for writable date
ProjectTemplateEndDate. Direct child creates enforce that family's required
fields; PATCH validates supplied fields while preserving omitted values. Reject
unsupported family/verb pairs, mismatched metadata, unknown/nonwritable fields
and child DELETE bodies. The validation record includes operation and child
family alongside the payload/metadata checksums. Still evaluate effective dates
against the fresh baseline, required conditional references and child/use impact
in the task's existing validation/design gates; local shape validation alone
cannot certify those facts.

## Dependency-Aware Validation

| Applies when | Result | Next action | Resolver |
|---|---|---|---|
| Every requested core field and nested child action has a published operation schema and authenticated target read access | `direct_writable_rest` | Record REST capability, then verify the active workflow classification/executor before approval. Imports enter core.data-loader and require its adapter/registration checks; capability does not authorize a generic POST. A selected direct non-import task operation uses the supported shared client after approval. | verify_template_route |
| A requested field or child action is absent from the published operation schema, or an operation-required ID cannot be resolved from a customer-supplied name through a target-proven standalone resolver | `unsupported_rest_surface` | Stop before preview; list the exact gap. A supplied root name does not require pre-resolution when its documented name attribute is writable. Absence of write links in a zero-row collection GET is not such a gap. | verify_template_route |
| Root create with child rows | Conditional | Choose valid root nested arrays or an explicit ordered root-then-child REST list; do not silently change approach. | resolve_template_sections |
| Setup option supplied | Conditional | Validate documented field shape and prerequisite child data. Fusion validates supplied reference eligibility on POST. | resolve_template_references |
| Existing template changed/end-dated | Conditional | Validate documented consumer/use evidence; unknown semantic impact blocks. | resolve_template_use |

## Field and Child Validation

| Check | What happens | Applies when | Resolver |
|---|---|---|---|
| Name/number resolves to zero or one target row | Create accepts zero exact matches; mutation accepts one; otherwise reject. | Create/update/end-date/child CUD | find_project_template |
| Start date is on/before end date | Accept; otherwise block. | Both dates supplied |  |
| Supplied project/task date pairs | Require ordered supplied start/finish dates. Check tasks against known project bounds as an FSCR consistency overlay; missing project dates alone are not new create requirements. Keep availability dates distinct | Root/nested/direct-child create and PATCH | resolve_template_sections |
| Business unit, project unit, project type, owning organization, and legal entity each use one documented name-or-ID representation; status uses one documented name/code | For create, require every context field required by the target operation. Do not call an existing template's contextual child LOV to accept, reject, or convert a submitted value. | Create/core update | resolve_template_references |
| Project plan type name supplied as `ProjectPlanTypeName`, `PlanType`, or `PlanTypeName` | Normalize to canonical `ProjectPlanType`; show the normalization and exact supplied value in the preview. Never serialize `ProjectPlanTypeName`. | Create/update | resolve_project_plan_type |
| Project plan type supplied by name or ID | Require exactly one of `ProjectPlanType` and `ProjectPlanTypeId` and validate that exact attribute against the target operation schema. Submit a supported customer-supplied name directly; Fusion validates its target context on POST. | Create/update | resolve_project_plan_type |
| Project plan type and project unit supplied together | Require one canonical plan-type representation and validate the target operation schema. Fusion validates the contextual association on POST. | Create/update | resolve_project_plan_type |
| `IntialStatus` supplied | Normalize to `InitialProjectStatus`; show the correction in preview. | Create/update |  |
| A display value resembles a code or internal label | Preserve its documented representation. Convert a display name only through a declared resolver with unique target evidence; project priority uses resolve_project_priority. Never guess an ID/code from spelling or case. | Create/update | resolve_template_references |
| Existing-template contextual child LOV | Do not call it while validating a new-template create. It is scoped to its existing parent and cannot accept, reject, or convert a new template's reference values. | Create | resolve_template_references |
| Child action is present in the CUD matrix and its path is documented | For nested children on root create, accept the published nested schema without a parent URI. For post-create child CUD, require the returned parent/child URI. | Child collection supplied | resolve_template_sections |
| Task create | Validate TaskName and required task booleans after documented inheritance. Omitted nested task organization remains omitted for Fusion derivation; validate supplied alternatives and fresh operation-specific requirements. Direct task create retains its existing organization contract. ExternalTaskId requiredness in Oracle remains operation-specific; nested-create missing IDs are prepared by the declared FSCR defaulting policy. Work type is required only by fresh operation-specific evidence. Validate supplied identifiers and task hierarchy | Nested/direct task create | resolve_template_sections |
| Boolean serialization | Apply documented defaults/inheritance before requiredness checks and preserve supplied JSON booleans. Reject quoted boolean flags. Transaction-control indicator codes are documented strings and are not boolean flags | All supplied boolean fields | resolve_template_sections |
| Project priority display name | Accept one ProjectPriority or ProjectPriorityName, or canonical ProjectPriorityCode. Resolve a name only after the selected workflow proves the expected target type/key and obtains complete enabled/effective evidence; emit only the returned code | Root create/update | resolve_project_priority |
| AssetAllocationMethodCode | Accept only AU, CC, EC, SC, SE, CE, N; omit when absent for project-type derivation | Root create/update | |
| Nested task identifiers and hierarchy | Supplied ExternalTaskId is nonblank, at most 100 characters and unique; nested-create omitted IDs are generated by the defaulting policy; supplied blank, malformed or duplicate IDs are rejected. Supplied TaskNumber is unique; any supplied ExternalParentTaskId must resolve to another supplied external ID and the relationships must be acyclic | Root create with Tasks | resolve_template_sections |
| Fixed dates and derived schedules | Validate ISO dates and supplied schedule alternatives; do not force an explicit schedule merely because a fixed date is supplied when the schedule can derive from project type/project/parent task | Supplied schedule fields | resolve_template_references |
| Documented code-only display names | Accept only the explicit aliases listed in the REST reference, resolve through the documented lookup types, and emit canonical codes. Supported API name/hint representations need no ID/code conversion | A registered display-name alias is supplied | resolve_template_code_values |
| Classifications/customers/provider units | Validate documented name/ID/number alternatives; reject conflicts. Class percentage must be within 0..100; target category evidence governs any sum-to-100 condition | Requested child rows | resolve_template_sections |
| Team members | Use documented PersonEmail/PersonId/PersonName and ProjectRoleId/ProjectRoleName fields, not invented project-resource fields. Validate percentage range, boolean type and ordered dates; resource eligibility remains target-dependent | Requested team-member rows | resolve_template_sections |
| Quick Entries | FieldCode accepts only TEAM_MEMBER, CLASSIFICATION, LEGAL_ENTITY_ID, CARRYING_OUT_ORGANIZATION_ID, PARTNER_ORG, PRIORITY_CODE, CUSTOMER_NAME, DESCRIPTION, PROJECT_STATUS_CODE, SUPPLIER_ORG. Specification is required for TEAM_MEMBER/CLASSIFICATION and inapplicable otherwise | Requested quick entries | resolve_template_sections |
| Setup options | POST accepts one OptionName/OptionCode and optional JSON DisplayFlag; direct PATCH accepts only DisplayFlag. Do not map an outline UI label or TaskSequence into a write field | Requested setup options | resolve_template_sections |
| Project/task transaction controls | Validate documented code/hint and name/ID alternatives. Job requires a person representation; organization requires person and job. Billable/Capitalizable codes are N/T; Chargeable is Y/N; preserve supported hint names directly | Requested controls | resolve_template_sections |
| Child body uses only the exact family/method schema and no read-only values | Accept; otherwise block. | Child create/update | resolve_template_sections |
| Root PATCH includes child arrays | Block: a nested field schema alone does not prove row binding or update semantics. Plan supported direct-child operations before approval; unsupported direct methods require reviewed nested-binding evidence, never a guessed fallback | Requested nested PATCH | resolve_template_sections |
| Route covers every requested field and remains unchanged from preview | Accept; otherwise block. | Execution | verify_template_route |
| Existing use permits semantic/end-date change | Accept; otherwise refuse. | Update/end-date | resolve_template_use |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PTMPL.VALIDATE_INPUT | step | 1 | validate_input | valid->PTMPL.APPLY_DEFAULTS;invalid->PTMPL.RETURN_ISSUES | none | stop | Every request: scope and supplied-value shape only; prepared completeness is checked after defaults and resolution |
| PTMPL.ROUTE_OPERATION | decision | 5 | evaluate_result | supported->PTMPL.RESOLVE_DEPENDENCIES;unsupported->PTMPL.RETURN_REFUSAL;invalid->PTMPL.RETURN_ISSUES | PTMPL.RESOLVE_SECTIONS | stop | After identity/reference/section/route resolution |
