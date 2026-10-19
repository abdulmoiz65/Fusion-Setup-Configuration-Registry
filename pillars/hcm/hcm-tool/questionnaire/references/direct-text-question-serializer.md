# Direct Questionnaire Question Normalization Procedure

Use this procedure to create a Question inside one Questionnaire hierarchy.
It does not create a Question Library root or a reusable-question placement.
This procedure validates and normalizes a direct-question definition into the
parent build specification. It does not construct pipe-delimited DAT text.
Final rendering and round-trip validation must use
`../scripts/questionnaire_dat_serializer.py`.

## Preconditions

Before rendering, prove the current target Questionnaire `Question` and
`Answer` components, their `MERGE` operations, and the exact live template
attribute order. Resolve one compatible questionnaire category, the response
type for the selected question type, and the supplied template's response-type
capability when a template exists. Stop if any fact is absent, ambiguous, or
incompatible.

## Supported types

Use `mode: direct` for a new direct question. `mode: direct-text` remains a
compatibility alias for `mode: direct` with `QuestionType=TEXT` only.

| QuestionType | Direct support | Answer rows | V1 boundary |
| --- | --- | --- | --- |
| `TEXT` | Yes | Prohibited | Plain text, rich text, date, and length/date limits require exact current target metadata. Do not infer optional controls. |
| `1CHOICE` | Yes | Required | Provide approved selectable responses. Scoring, rating models, images, feedback, conditions, and attachments remain unsupported unless separately added to the live contract. |
| `MULTCHOICE` | Yes | Required | Provide approved selectable responses. Minimum/maximum selections may be emitted only when present in the target contract and explicitly supplied. |
| `NONE` | Yes | Prohibited | Instructional text only; use the target-confirmed no-response display type. |

## Required direct-question definition

Record these values in the immutable Markdown preview. Do not infer a value,
use an ID, or leave a required row blank.

| Attribute | Approved value | Evidence ID |
| --- | --- | --- |
| QuestionCode |  |  |
| QstnVersionNum | 1 |  |
| QuestionText |  |  |
| QuestionType | `TEXT`, `1CHOICE`, `MULTCHOICE`, or `NONE` |  |
| ResponseTypeName |  |  |
| Status |  |  |
| PrivacyFlag |  |  |
| CategoryName |  |  |
| QstnSequenceNumber |  |  |
| Mandatory |  |  |
| AdhocQstn |  |  |
| SectionSeqNum |  |  |
| QuestionnaireCode |  |  |
| QstnrVersionNum |  |  |
| SubscriberName |  |  |

`ResponseTypeName` is the direct question response format. It is not the
optional `QstnrQstnResponseTypeName` placement override used by a reusable
question. Do not emit both unless the current target template explicitly
requires the override.

The version and all sequence values must be positive integers. `Status` must
be target-confirmed. `PrivacyFlag`, `Mandatory`, and `AdhocQstn` must be `Y` or
`N`. Reject a value containing `|`, a line break, or a generated ID, including
`QuestionnaireId`, `QstnrSectionId`, `QstnrQuestionId`, or `SubscriberId`.

## Choice-answer definition

For `1CHOICE` or `MULTCHOICE`, provide one or more approved answer rows. Each
row must use a unique, target-valid `AnswerCode` and a positive unique answer
sequence. The Answer parent hierarchy must exactly match the direct Question.

| Attribute | Approved value | Evidence ID |
| --- | --- | --- |
| QuestionCode |  |  |
| QstnVersionNum |  |  |
| AnswerCode |  |  |
| LongText |  |  |
| AnsSequenceNumber |  |  |
| SectionSeqNum |  |  |
| QuestionnaireCode |  |  |
| QstnrVersionNum |  |  |
| SubscriberName |  |  |

Include `Score`, correctness, feedback, attachments, images, or another
answer attribute only when the current target Answer metadata registers it and
the approved design supplies a compatible value. Do not add those controls by
default. For `TEXT` and `NONE`, reject every answer row.

## Structured normalization and rendering

After the live template is available, copy its `Question` metadata columns in
their exact returned order into the immutable review preview. Put the
corresponding approved value in the adjacent cell. Include no column that has
no approved value. For choice questions, create a separate table in the exact
current `Answer` metadata order for every answer row. After review, place those
name/value mappings into the canonical request's `render_sections`; do not join
them with pipes manually.

| Current `Question` metadata column, in exact order | Approved direct-question value |
| --- | --- |
| `<first current column>` | `<value>` |
| `<next current column>` | `<value>` |

| Current `Answer` metadata column, in exact order | Answer 1 | Answer 2 |
| --- | --- | --- |
| `<first current column>` | `<value>` | `<value>` |
| `<next current column>` | `<value>` | `<value>` |

Perform this checklist before invoking the executable serializer:

1. Confirm every required definition appears exactly once in its current
   metadata table and each type matches its response type and template
   capability.
2. Confirm the Question component is registered for `MERGE`, all parent keys
   match the preceding Questionnaire and Section rows, and—when required—the
   Answer component is registered for `MERGE`.
3. For `1CHOICE` and `MULTCHOICE`, confirm every answer has complete matching
   parents, a unique valid AnswerCode, and a positive unique sequence. For
   `TEXT` and `NONE`, confirm there is no Answer row.
4. Confirm no row contains a generated ID, source reference, delimiter, line
   break, attachment, translation, condition, rating, or scoring field that is
   not both target-registered and explicitly approved.
5. Add the Question attributes to the single `Question` entry in
   `render_sections`. For a choice question, add each answer to the single
   `Answer` entry. Keep components in live parent-before-child order and make
   every inherited parent key explicit. Let the executable serializer emit the
   `METADATA` and `MERGE` lines.
6. If any check fails, mark the direct question `UNSUPPORTED` and stop before
   generating `Questionnaire.dat`.

Oracle documents the four question types—Text, Single Choice, Multiple Choice,
and No Response—and documents importing questionnaire choice responses. The
current target Data Loader template remains authoritative for the emitted
columns and values.
