# Business-First Intake and Proposal

Use this contract for conversational Profile Rating Model requests. Keep the
initial conversation in business language and retain the existing normalized
requirements schema as the technical contract after proposal review.

## Intake Modes

| Mode | User Supplies | Skill Behavior |
|---|---|---|
| Business-first | Desired outcome, workforce or process context, effective date, and exceptions | Resolve consumers, discover patterns, propose technical values, and ask only genuine business ambiguities |
| Expert | Complete JSON, generated workbook, or reviewed customer workbook | Preserve explicit values, run discovery and exact comparison, then apply all normal validation and approval gates |

Never require the user to name the skill, setup task, Fusion consumer, model
component, loader route, or downstream object during business-first intake.

## Business Intent Record

Capture:

- `outcome`: what managers, employees, or an HCM process must be able to do;
- `workforce_context`: who or what will be rated and where the rating is used;
- `effective_date`: when the business behavior should begin;
- `scale_semantics`: explicit number, direction, labels, or meaning when stated;
- `exceptions`: deviations from the established organizational pattern; and
- `explicit_constraints`: values the user insists on preserving.

Ask only for a missing value that changes business behavior. Effective date,
population, and an unresolved choice between materially different scale
meanings are valid questions. Model code, consumer name, input format, component
field, and loader route are not valid initial questions when they can be
resolved or proposed.

## Consumer Resolution

| Business Language | Consumer Hypothesis | Clarify Only When |
|---|---|---|
| Rate proficiency or qualification on job, person, or model profiles | Profile Management | The request could instead mean employee-owned Skills Center progression |
| Calculate, round, map, or summarize evaluation scores | Performance Management | The scale is descriptive only and no calculation is required |
| Assess potential, succession readiness, or box-chart dimensions | Talent Review and Succession | The request mentions performance without stating whether a talent-review category is needed |
| Calibrate compensation ratings or direct rating distributions | Compensation | The request could mean downstream Performance target distribution instead |
| Show employee skill progression or proficiency in Skills Center | Skills Center | The request could instead mean profile content maintained by HR specialists |

Resolve multiple consumers when the business outcome explicitly spans them.
Do not infer a consumer association from rating-model header or level data
alone. Use explicit user intent, approved project decisions, or evidence from
the owning downstream skill.

## Evidence and Proposal Precedence

Use this order for every proposed value:

1. Valid explicit user value or technical override.
2. Approved current-project requirement or design decision for the same use.
3. One clearly dominant current-environment pattern compatible with the stated
   business meaning and effective date.
4. Documented Oracle product rule or safe component exclusion.
5. Deterministic review-only generation, such as a code derived from the
   proposed name or increasing whole-number levels for a stated ordered scale.

Never silently select among equally supported patterns. Never call a generated
value an enterprise standard when no comparable evidence exists.

## Assumption Ledger

Record one row for every inferred consumer or technical value:

| Field | Meaning |
|---|---|
| Value | Proposed normalized value |
| Source | Explicit user value, project decision, comparable model, Oracle rule, or deterministic generation |
| Evidence | Sanitized artifact, resolver, or rule reference |
| Confidence | High, medium, or low |
| Materiality | Whether changing it alters the business outcome or downstream behavior |
| Review Status | Confirmed, review required, corrected, or rejected |

High confidence does not remove review when the value is material. Low
confidence or equally supported material alternatives require one business
question before normalization.

## Proposal Format

Lead with one short paragraph covering the outcome, population or process,
effective date, proposed scale, and important exclusions. Then show only
material assumptions and exceptions. Keep full technical fields under `Review
assumptions`.

Example:

> I found a five-level proficiency pattern compatible with job-profile use. I
> will prepare a Profile Management model effective September 1, 2026, using
> Beginner through Expert. It will not include Performance calculation ranges,
> Talent Review categories, or Compensation distributions.

Use `Prepare model` and `Review assumptions` before the immutable artifact
exists. Use `Create model` only as the standalone approval action bound to the
exact `core.data-loader` preview. Proposal confirmation never authorizes an
import.
