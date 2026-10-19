# Setup mapping and defaulting

Use this reference for defaults or validations that translate one or more
environment-specific source values into a target value.

## Mapping intake

Never infer a mapping because source and target resources contain similarly
named fields. Obtain or verify:

- stable source IDs or codes;
- stable target IDs or codes;
- every composite-key component;
- active status and effective dates;
- no-match and duplicate-match behavior;
- fallback behavior;
- mapping owner and expected change frequency;
- whether a user-entered target may be overwritten.

Ask for the missing setup-specific map when the environment evidence proves the
fields but not their business relationship. Labels may be recorded for review,
but must not replace stored IDs or codes.
`
## Code every case, not every value

Generate complete control flow for every confirmed behavior even when customer
mapping entries are unavailable. Code blank, unchanged, exactly-one-match,
no-match, duplicate-match, inactive, out-of-date, preserve-user-value,
authorized-overwrite, and runtime-unavailable branches as applicable.

Do not invent or embed customer IDs, codes, effective dates, calendars,
thresholds, or relationships. Represent them with clearly named placeholders
or read them from a setup source proven accessible on the exact page. Missing
mapping values create a setup dependency; they do not justify returning only an
intake checklist when the technical code contract is otherwise confirmed.

## Direct expression versus setup-driven mapping

Use a direct Advanced Expression map only when the mapping is small, stable,
release-reviewed, and maintained by the extension team. Treat every map entry
as a target-environment dependency.

Prefer a setup-driven UDT or equivalent administrator-owned source when the map
is large, frequently changing, effective-dated, shared across rules, or owned by
functional administrators. Verify that the exact page can read the setup source
without introducing an unsupported service call. If it cannot, return a setup
or Advanced Mode handoff rather than embedding an unmaintainable approximation.

## Composite mappings

For a multi-key lookup:

1. Resolve and normalize every key independently.
2. Use stable IDs or codes and an unambiguous delimiter or structured key.
3. Define whether blank keys skip defaulting or produce a validation error.
4. Require exactly one active effective match.
5. Treat duplicate matches as a configuration error.
6. Keep each target assignment independent so one unavailable target does not
   silently corrupt another.

## Default overwrite policy

The safe default is non-destructive:

1. Compare current and initial source values with verified accessors.
2. Recalculate only when a relevant source changes or the target is blank and
   initial defaulting is explicitly required.
3. Preserve a nonempty user-entered target value.
4. Overwrite only when the requirement explicitly authorizes it.
5. Do not reapply a default during unrelated Business Rules evaluations.
6. Leave the target unchanged when no valid map entry exists unless the policy
   requires a blocking validation.

If the runtime exposes a user-modified indicator, verify and use it. Otherwise,
compare current and initial target values conservatively and document the limit.

## Validation and test scenarios

Cover at least:

- each mapped positive case;
- unchanged source values;
- blank source or target;
- missing map entry;
- duplicate active map entries;
- inactive and out-of-date entries;
- user-entered target preservation;
- explicitly authorized overwrite;
- partial composite keys;
- runtime data unavailable during evaluation.
