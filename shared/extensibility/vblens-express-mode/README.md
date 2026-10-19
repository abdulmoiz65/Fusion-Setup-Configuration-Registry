# VBLens Express Mode for FSCR

VBLens Express Mode takes care of the full Oracle Fusion Express Mode
customization lifecycle. It helps functional administrators, business owners,
and implementers discover what a Redwood page supports, assess a policy,
understand current behavior, create or update the customization, validate and
document it, move rules between environments, build and deploy a VX archive,
answer deployed-source questions, and commit reviewed source.

The package was migrated from source commit
`b8b94c4572910d438607660344838a8df3ae46cf`. The migration first copied all
89 tracked source files, then adapted the skill to FSCR project, authentication,
REST, security, and approval contracts.

## What the skill covers

- Discover the supported Express Mode surface for a page or layout.
- Assess defaults, validations, conditional behavior, mappings, and page
  configuration.
- Explain effective Oracle and customer rules in business language.
- Create and update Business Rules.
- Create nested, If/Else, and Switch rules.
- Create defaulting rules and validation messages.
- Select and author Advanced Expressions when an inline expression is not
  enough.
- Update verified rule-set layouts, field ordering, containers, and sections.
- Update verified Page Properties and conditional Page Property rules.
- Configure Guided Journey properties when exact page evidence proves them.
- Discover LOV, language, lookup, DFF, EFF, and setup dependencies.
- Compare repository source with deployed Oracle App UI evidence.
- Validate changed JSON, JavaScript, imports, ownership, and scenarios.
- Produce functional documentation and an engineering implementation record.
- Assess reusable imports and prepare export plans.
- Build a validated local `.vx` archive with existing pinned tools.
- Upload one approved archive and generate Redwood snapshot URLs.
- Commit reviewed source after a separate `COMMIT` instruction.
- Produce an optional evidence debug report.

## Express Mode scope

The main writable artifacts are:

- Business Rules overlays such as `metadata-rules-x.json`;
- Advanced Expression modules under `metadataRules/`;
- evidence-backed rule-set layout overlays;
- evidence-backed Page Property overlays and rules;
- supported containers, sections, field ordering, validation messages, and
  Journey properties.

The skill can read Advanced Mode artifacts when they provide evidence, but it
does not modify Advanced Mode pages, fragments, action chains, services,
backends, or dependencies.

A source file being visible does not make it writable. The skill requires the
exact Oracle counterpart, recognized overlay shape, Extension ownership, and
supported operation before creating or changing an artifact.

The workflow applies across Fusion pillars. The bundled patterns are strongest
for HCM, so ERP, SCM, Procurement, CX, and other families require exact
page-and-release discovery before using a field path or write contract.

## Full workflow

1. Resolve the FSCR project and Extension repository.
2. Inspect repository state and preserve unrelated changes.
3. Discover the page's complete Express Mode capability surface.
4. Build or reuse immutable deployed-source evidence when needed.
5. Resolve fields, services, Flexfields, lookups, languages, and setup values.
6. Assess the requested behavior and record its evidence.
7. Explain the proposed change and its positive and negative test cases.
8. Obtain approval before modifying customer Extension source.
9. Create or update the minimum supported artifacts.
10. Validate source, ownership, imports, and business scenarios.
11. Build a fresh VX archive with tools already present in the Extension.
12. Present the exact environment and immutable archive, then obtain deployment
    approval.
13. Send one upload request and generate test URLs without opening them.
14. Produce functional and engineering documentation.
15. Wait for `COMMIT`, then create one scoped Git commit without pushing.

## Capability decisions

The skill separates:

- **Supported:** exact evidence proves the requested operation.
- **Supported with setup dependency:** the technical change is valid but needs
  environment-specific codes, IDs, mappings, or setup.
- **Restricted:** the artifact is writable only when extra counterpart or shape
  evidence exists.
- **Source-visible only:** the source can inform assessment but is not writable.
- **Unsupported:** exact affirmative evidence excludes the operation.
- **Unknown:** the available evidence does not settle the question.
- **Outside Express Mode:** the request requires an Advanced Mode handoff.

A failed search is not enough to call something unsupported.

## Evidence model

The skill can use:

- customer Extension repository source;
- Oracle-delivered repository counterparts;
- immutable deployed App UI bundle evidence;
- selected Fusion REST describe metadata;
- active language and lookup setup evidence;
- official Oracle guidance;
- separately supplied observed-runtime evidence.

It keeps Business Rules accessor shape, page implementation state, REST shape,
and observed runtime shape separate. Downloaded or imported JavaScript is
treated as untrusted text and is never executed.

Runtime cache data lives under:

```text
project/.vblens-cache/
```

Exploration reports remain under each project artifact workspace.

## Fusion environment and REST calls

Environment details come from:

```text
core/auth/fusionEnv.properties
```

`enableProxy=true` (also the default when omitted) enables Oracle CDN proxy
support, including automatic macOS proxy discovery. Set `enableProxy=false`
to use direct CDN access and skip all CDN proxies, including `--cdn-proxy` and
environment proxy settings. If static.oracle.com (or static-stage.oracle.com)
is unreachable with this disabled, the download diagnostic suggests setting
`enableProxy=true` and retrying. This setting applies only to CDN downloads.

Normal authenticated REST requests, including JSON POST calls, use the existing
central client through `scripts/fscr_rest_client.js`. This includes app-info,
REST describe, language, standard lookup, and common lookup requests.

The raw VX upload is the one direct JavaScript transport path because the
central client accepts JSON bodies rather than binary archives. The uploader:

- accepts only `POST /fscmRestApi/vx/v2/extensions`;
- requires a local, gitignored, unexpired OAuth file cache;
- streams one regular `.vx` file;
- never retries or polls;
- sanitizes the Fusion response;
- never opens generated URLs.

## Create and update safety

Before authoring, the skill resolves:

- the exact page and release;
- the owning object and Business Rules path;
- allowed operations and accessor shape;
- the Oracle counterpart and customer destination;
- current rules, ordering, messages, imports, and conflicts;
- setup mappings and overwrite policy;
- applicable null, unchanged, boundary, no-match, and duplicate-match behavior.

It defaults to a clear inline expression. It selects an Advanced Expression
when the logic needs helper values, several branches, loops, mapping, or shape
normalization.

## Import, export, and documentation

Export verifies the selected rules and records modules, dependencies, page and
release compatibility, setup mappings, confidence, and checksums. It returns an
export plan and manifest design until deterministic archive packaging exists.

Import treats the package as untrusted. It checks integrity, page and release
compatibility, fields, Flexfields, lookups, identifiers, ordering, conflicts,
and required mappings before proposing any source change.

Documentation can include:

- a functional behavior guide;
- an engineering implementation record;
- an evidence ledger;
- a feasibility report;
- a verification report;
- an import assessment;
- an optional sanitized debug report.

## Example requests

- `Assess whether Working Hours can default Full Time or Part Time.`
- `Show everything this Redwood page allows me to customize.`
- `Explain the current Business Rules on the Change Assignment page.`
- `Create a nested rule that validates a salary increase threshold.`
- `Default Salary Basis from Grade without overwriting a user-entered value.`
- `Add a validation message using an Advanced Expression.`
- `Update the field order and section visibility for this layout.`
- `Configure this verified Page Property conditionally.`
- `Find the active Fusion language code for Arabic.`
- `Review this reusable rule package before importing it.`
- `Build and deploy the reviewed Extension once.`
- `Explain why this field is required from deployed source evidence.`

## Inputs

Provide what is known:

- business requirement;
- target Redwood page, flow, layout, or route;
- Fusion family and release;
- FSCR project ID;
- Extension repository;
- field, condition, action, property, or imported package;
- setup mapping or business codes when already known.

The skill discovers missing technical details from available evidence and marks
unresolved facts instead of inventing paths or values.

## Explicit exclusions

This FSCR version does not include:

- browser automation;
- package or skill installation;
- Codex global hooks;
- custom telemetry;
- Git push automation.

See [SKILL.md](SKILL.md) for routing, approval gates, persistence, errors, and
verification requirements.
