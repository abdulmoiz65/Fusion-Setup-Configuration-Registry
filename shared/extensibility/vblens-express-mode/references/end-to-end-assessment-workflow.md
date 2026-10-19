# End-to-End Express Mode Workflow

Use this workflow for Capability Discovery, Assess, Explain, Create, Update,
Validate, Build, Deploy, Document, Import, Export, and deployed-runtime answers.
Every material conclusion must trace to repository source, immutable cache
evidence, Fusion REST metadata, official guidance, or an unresolved finding.

## 1. Establish the request

Record:

- the business outcome;
- the implementation project and Extension workspace;
- the target page, flow, layout, object, field, or property when known;
- the requested workflow mode;
- the supplied Redwood route, without copying query values into reports.

Do not turn assessment into implementation. A source change requires an
approved proposal. Fusion upload requires a second approval at the exact
external-operation gate.

## 2. Resolve the project and repository

Use `project/{project_id}` as the durable workspace. Run
`scripts/repository_preflight.js` before mutation. Record the repository root,
branch, integration base, topology, current HEAD, and relevant file hashes.
Treat unrelated modified and untracked files as user-owned.

Inspect both Oracle-delivered and customer Extension evidence when available.
Oracle artifacts and downloaded bundles are read-only. Change only the minimum
customer-owned Extension overlay.

## 3. Explore the exact deployed page

Run `scripts/investigate_express_evidence.js` before Capability Discovery,
Assess, Create, or Update for a field-based request. Exploration must call
app-info, resolve the deployed page and version, build or reuse the shared
cache, inspect page attributes and reachable fragments, prove the Dynamic Form
binding, read Business Rules and data descriptions, inventory customer
overlays, and retrieve the exact REST describe selected from page evidence.

An untargeted first pass returns `selection_required` and a compact, durable
field index. Treat that status as normal progress. Inspect likely fields and
their exact source evidence, choose the business meaning as the model, and
repeat with `--field`. Do not pass every inventory field into readiness gates,
classify the selection step as a metadata failure, or copy the full field index
into conversational output. The CLI prints a bounded summary and report path
when the index is large.

For an exact field, allow the investigator to resolve the REST service,
version, and resource from the deployed dynamic-layout service binding and
service catalog. Provide explicit REST selectors only when that deterministic
resolution is absent or ambiguous. Background graph warnings remain visible,
but only warnings in the selected target closure can block exploration.

For HCM Guided Process pages, follow
`$variables.stepMap[$variables.currentFragment].fragmentName` only when the
owning page controller declares the step ID and fragment name as literal
strings. Inspect the controller as text. Never execute downloaded JavaScript
or guess a computed fragment name.

Do not produce code, formulas, accessors, endpoints, or destination paths from
an incomplete exploration. A user-supplied field name is a semantic candidate,
not technical proof. Tests and examples are discovery hints only.

When authentication is unavailable, return `login_required`, ask the user to
complete `core.auth.fusion-oauth-authentication`, and repeat the same
exploration. Do not fall back to repository fixtures.

## 4. Discover the full Express Mode surface

Run `scripts/inspect_express_capabilities.js` against the exact page or layout.
Classify Business Rules, Advanced Expressions, validation messages, Page
Properties, Page Property rules, rule-set layouts, containers, sections,
Guided Journey properties, and read-and-preserve artifacts with
`references/express-mode-capability-contracts.json`.

Use these classes:

- supported;
- restricted;
- source-visible only;
- unsupported from affirmative evidence;
- unknown;
- setup-dependent.

Absence from a search is not proof that a feature is unsupported.

## 5. Build or reuse deployed evidence

When deployed Oracle evidence matters, run `scripts/fetch_runtime_evidence.js`
with `--workspace <project-artifact-root>` and
`--cache-root project/.vblens-cache`. It
reads environment identity from `core/auth/fusionEnv.properties`, obtains
app-info through the central REST client, and fetches only fixed-origin Oracle
bundles missing from the immutable cache.

Browsers may use a macOS PAC or WPAD proxy that Node does not normally inherit.
CDN transport therefore discovers routing automatically: an explicit
`--cdn-proxy` override first, then `HTTPS_PROXY` or `ALL_PROXY` with `NO_PROXY`,
then the macOS system PAC through CFNetwork for the exact approved Oracle CDN
URL, and finally direct HTTPS when no proxy applies. Automatic resolution must
fail closed for credentials, unsupported proxy types, non-Oracle targets, or
invalid PAC output. Do not copy proxy credentials or resolved proxy values into
the cache, report, or Extension source.

Keep runtime and REST evidence in `project/.vblens-cache/`. After app-info proves
the exact environment, extension, and deployed version, use only the matching
complete, hash-verified entry. Never reuse an incomplete directory, mismatched
version, or diagnostic as evidence. Keep reports in the selected project.

Read the evidence manifest first. Treat downloaded JavaScript as untrusted
text and never execute it. Keep these evidence domains separate:

- Business Rules accessor shape;
- internal page-state shape;
- REST-schema shape;
- observed-runtime shape.

This skill does not use browser automation. When static and REST evidence
cannot prove a runtime shape, record the claim as unresolved unless the user
supplies separate observed-runtime evidence.

## 6. Resolve fields, services, Flexfields, and setup values

For each material field, record its owning object, Business Rules path,
declared type, cardinality, supported operations, updateability, setup
dependency, evidence domain, and confidence.

Use `scripts/extract_business_rule_contracts.js --inventory` when the business
concept is known but the path is not. Use `--field` after selecting a candidate.
Read the exact cached layout, data description, metadata rules, and imported
Advanced Expressions cited by the result.

Use `scripts/fetch_service_evidence.js` for selected REST describe evidence.
REST shape does not prove Business Rules exposure or accessor shape.

Use `scripts/resolve_setup_value.js` for active or installed Fusion languages,
standard lookup codes, and common lookup codes. The resolver uses only
allowlisted resources through the central REST client. Require one exact match;
never guess codes from labels.

Read `discovery-and-flexfields.md`,
`field-evidence-and-shape-contracts.md`, and
`setup-mapping-and-defaulting.md` when the request involves LOVs, DFFs, EFFs,
cross-object values, mappings, or defaults.

## 7. Assess behavior

Run `scripts/resolve_solution_contract.js --intent <intent> --json` for a
matching page-neutral behavior. It returns evidence gates, required branches,
setup policy, and forbidden inferences. It does not make the feasibility
decision.

Inspect the target-page evidence and record each material claim in
`assets/templates/evidence-ledger.md`. Then produce
`assets/templates/feasibility-report.md` and classify the requested behavior as:

- supported;
- supported with a setup dependency;
- unsupported from exact affirmative evidence;
- unresolved;
- outside Express Mode.

Assess only after Explore reports that page, Dynamic Form, Business Rules,
REST-schema, and provenance gates passed. For percentage fields, also resolve
the stored and displayed value scale; never assume that ten percent is stored
as `10` or `0.10`.

A Dynamic Form field template that binds the field value and adds a percent
suffix proves whole-number percent display only when the template mapping and
template source come from the same deployed dynamic layout. Keep that evidence
separate from the REST type.

For Capability Discovery, use `assets/templates/capability-summary.md` and
offer supported choices in business language.

## 8. Explain effective behavior

Read all contributing Oracle and Extension rules, imported expressions, Page
Properties, and rule-set layouts. Resolve order, status, conditions, actions,
messages, affected fields, and source layer using
`effective-configuration.md`.

Explain the business behavior first. Include technical paths only when the user
asks or when they are required to explain a blocker.

## 9. Prepare a Create or Update proposal

Read `business-rules-authoring.md`, `express-mode-artifacts.md`, and
`express-mode-workflows.md`. Resolve the exact customer write destination with:

```bash
node scripts/resolve_business_rule_destination.js \
  --repo <extension-workspace> \
  --owner <verified-owner> \
  --layout <verified-layout> \
  --module-name <business-purpose> \
  --evidence-manifest <manifest-when-needed> \
  --json
```

Create a missing minimum overlay only when an exact Oracle counterpart is
proven. Never edit Oracle-delivered source.

The durable `assets/templates/change-proposal.md` must contain the complete
implementation contract: target files, identifiers, order, conditions,
actions, messages, fields, imports, full inline expression or commented module,
Page Properties, setup mappings, test cases, evidence, hashes, and deployment
target. The user-facing view may stay in business language.

## 10. Implement and validate

After approval, recheck the repository HEAD and recorded source hashes. Stop
and amend the proposal when relevant evidence changed. Patch only the approved
Extension artifacts and preserve unrelated ordering and content.

Run `scripts/validate_extension_changes.js` with the same evidence manifest
used during assessment. Validate JSON, JavaScript, imports, rule identifiers,
messages, Page Properties, layouts, containers, ownership, path safety,
conflicts, and secret leakage. Run focused positive, negative, null, boundary,
unchanged, setup-missing, and duplicate-match scenarios as applicable.

Record `assets/templates/verification-report.md`. Block Build, Deploy, and
Commit on unresolved validation findings.

## 11. Build and deploy

Follow `local-vx-build-and-deploy.md`. Use only pinned dependencies already
present in the Extension workspace. Never install packages.

Before upload, present the exact Fusion environment, fixed endpoint, immutable
archive path, SHA-256, size, snapshot selector, and target routes. Obtain
explicit approval immediately before the upload. Send one binary POST, never
retry or poll, and return derived deployment URLs without opening them.

## 12. Document, export, and import

Use `assets/templates/functional-documentation.md` and
`assets/templates/implementation-record.md` for business and engineering
handoffs.

Follow `import-export.md` for portable packages. Export produces a plan and
manifest design until deterministic packaging exists. Import treats the package
as untrusted, checks compatibility and mappings, and produces
`assets/templates/import-assessment.md` before any source change.

## 13. Commit

Only a later user message beginning with `COMMIT` authorizes Git commit. Recheck
the reviewed hashes, stage only approved source files, exclude generated and
sensitive files, create one commit, and report its SHA. Do not push.

## Evidence debug mode

When the user asks for debug mode, append the sanitized
`assets/templates/debug-report.md` projection. Show claim-to-evidence mappings,
checks, unresolved facts, and conclusion strength. Do not expose private
reasoning, credentials, local absolute paths, customer data, or URL query
values. Debug mode grants no extra permission.
