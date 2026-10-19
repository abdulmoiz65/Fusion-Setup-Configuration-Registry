# Post-import eligibility evaluation

Use this optional workflow only after the Plan Copy import has reached verified
terminal `SUCCESS`. It evaluates every participant eligibility profile named in
the imported `benefits_eligibility.zip`, one profile per evaluator request.

## Conversation and approval flow

1. Offer evaluation after a successful import and ask for the person's display
   name when the user accepts.
2. Run the `evaluate` subcommand without `--approve-evaluation`. This performs
   only GET requests, resolves the imported profile names and the person's
   primary assignment, and emits `evaluation_preview_ready`.
3. Show the target, person, primary assignment, effective date, and profile
   names. Ask for explicit approval immediately before evaluation.
4. Only after approval, rerun the same command with `--approve-evaluation`.
   POST requests are not retried. A partial failure stops the remaining
   profiles and reports the stage; do not create replacement requests without
   new approval.

If Fusion accepts an evaluation action but the client stops on an unexpected
success response, verify the request and its `ExecutionStatus` with read-only
GETs. After fixing the response contract, add `--completed-profile` for each
profile proven successful, preview the remaining profiles, and obtain new
approval. Never duplicate the verified request merely to simplify recovery.

```bash
/usr/bin/python3.11 \
  pillars/hcm/benefits-configuration/benefits-eligibility/eligibility-profiles/scripts/eligibility.py \
  evaluate \
  --zip "project/example-project/artifacts/pillars/hcm/benefits-configuration/benefits-eligibility/eligibility-profiles/current/benefits_eligibility.zip" \
  --person-name "<exact display name>" \
  --effective-date "<YYYY-MM-DD>" \
  --properties "core/auth/fusionEnv.properties" \
  --token-cache auto
```

If the display name matches multiple primary assignments, ask for the person
number and add `--person-number`. Never guess among duplicate people.

## Reviewed REST contract

All paths are relative to `/hcmRestApi/resources/11.13.18.05` and use REST
framework version 9.

- Resolve each imported profile with the `eligibilityProfilesLOV` `findByName`
  finder. Require one exact, active `PRTP` match and read `EligyPrflId`.
- Resolve the person with `personHeaders`, exact `DisplayName`,
  `PrimaryFlag='Y'`, and the evaluation effective date. Read `PersonId` and
  `AssignmentId` from that same primary row.
- Create `formulaEvaluations` with `AssignmentId`, `EligibilityProfileId`,
  `RunTime`, and `EvaluationType='ORA_ELPRO'`.
- Invoke `formulaEvaluations/action/evaluateEligibility` with the returned
  `evaluationRequestId`, `personId`, `effectiveDate`, and `evalType='C'`.
- Retrieve child rows for fixed `DataTypeCd` values `L`, `OPE`, `ED`, `FC`, and
  `IP`. Read each payload from its `MessageDetails` enclosure. Never construct a
  result filter from user input.
- For each `FC` detail, map `IneligibleCriteria` to the criterion label,
  `CriteriaValue` to `expectedValue`, and `PersonOrAssignmentValue` to
  `actualValue`. These values come from `BEN_FF_EVAL_RSLT.MSG_DTLS` through the
  reviewed `MessageDetails` REST enclosure; do not query the table directly.
- A result row can legitimately have no `MessageDetails` enclosure, such as an
  eligible profile with no failed criteria. Treat enclosure HTTP 404 as an
  empty detail only for that existing row; retain a non-empty scalar `Value` or
  `MessageText` when supplied. Other enclosure failures remain fatal.

These paths and attributes were verified against the selected target environment's live OpenAPI
metadata. The evaluator design is also aligned with the supplied Postman
collection, the Plan Design UI implementation, and the Eligibility and Formula
Evaluator REST TDD.

## Summary and data handling

`evaluation_completed` reports the selected person and assignment, evaluation
date, overall eligible/ineligible counts, and one row per profile. Each row
contains the overall outcome, ineligibility reason when returned, criterion
expected/actual value comparisons, input count, and whether a log was
produced. In the user-facing report, show every returned criterion comparison
with columns for profile, criterion, expected value, and actual value alongside
the profile outcome. Display an explicit `No comparison returned` for a profile
without `criteriaResults`; do not infer an expected or actual value. Raw `L`,
`OPE`, `ED`, `FC`, and `IP` payloads can contain
sensitive diagnostic or person data; do not print or persist them.
