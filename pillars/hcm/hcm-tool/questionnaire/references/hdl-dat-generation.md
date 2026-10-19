# Questionnaire HDL DAT Generation Contract

Read this reference whenever a Questionnaire functional-area or task skill creates, changes, duplicates, versions, reviews, or hands off an HDL DAT artifact.

## Scope and safety boundary

This contract covers setup definitions only:

1. Question Library
2. Questionnaire Templates
3. Questionnaires

It does not cover questionnaire participants, questionnaire responses, question responses, consumer linkage, or lookup maintenance. The task builder may make authorized read-only metadata and reference requests and may write local project artifacts. It must not upload to UCM, initiate Data Loader, or otherwise change Fusion.

## Sources of truth

Keep business intent and technical validity separate.

### Business values

1. The user-approved business specification is authoritative for intended new or changed values.
2. Exact current target readback is authoritative for values preserved during an update, version, duplicate, or delete-impact review.
3. An FSM export or supplied DAT may provide source evidence, but it does not authorize copying target-specific IDs, defaults, or display values.

### Technical contract

Use this precedence immediately before every build:

1. Current target Data Loader business-object detail, components, attributes, user keys, mandatory indicators, registered operations, and freshly downloaded UCM DAT template.
2. Current target read-only reference or LOV evidence for subscriber, category, response type, owner, rating model, question/version, answer, template, language, and Recruiting context values.
3. Loader source from the same release as the target for behavioral rules not exposed by metadata.
4. The target validation response and exact-object readback for the attempted payload.
5. Oracle documentation, the maintained Questionnaire runbook, and field-validation matrix.
6. Supplied DAT templates and FSM exports as dated evidence only.

If a higher-precedence source is unavailable, ambiguous, or conflicts with a lower-precedence source, stop with `TBD` or `Blocked`. Do not silently fall back to an old template, a sample-observed default, a guessed label, or another subscriber's behavior.

## Task scope and conditional artifact order

Question Library, Questionnaire Templates, and Questionnaires are independently executable task scopes. Build and validate only the tasks in the approved scope. Use the following order only for artifacts that explicitly reference another artifact created by the same delivery:

| Sequence | Task | Primary DAT | Registered sections in supplied evidence | Optional translation DAT |
|---:|---|---|---|---|
| 1 | Question Library | `Question.dat` | `Question`, `Answer`, `QuestionContext` | `QuestionTranslation.dat` with `QuestionTranslation` |
| 2 | Questionnaire Templates | `QuestionnaireTemplate.dat` | `QuestionnaireTemplate`, `Section`, `Question`, `Answer`, `TemplateAttachment` | Registered evidence may expose `QuestionnaireTemplateTranslation.dat`; current procedure returns `UNSUPPORTED` |
| 3 | Questionnaires | `Questionnaire.dat` | `Questionnaire`, `QuestionnaireAttachment`, `Section`, `Question`, `Answer` | `QuestionnaireTranslation.dat` with `QuestionnaireTranslation` |

Use the exact current target filename/discriminator and component registration when it differs from the supplied evidence. A translation DAT follows its successfully resolved parent and is generated only when the target registers the translation business object and intended operation.

For a reusable-question placement, resolve one exact active same-subscriber Question/version in the target. For a questionnaire template reference, resolve one exact active same-subscriber Template in the target. Those target objects may predate, or be delivered outside, the current project task; a prior Question Library or Questionnaire Templates task is not a prerequisite to start this task. Do not substitute a locally generated or unsuccessfully imported candidate for required target readback. A template task is unnecessary when it is out of scope and the selected target HDL/subscriber contract permits a template-less questionnaire.

## Live gates before building

Follow [HDL Metadata Discovery](hdl-metadata-discovery.md) for the business-object
gate. Its no-product-area rule applies to pillar-authored discovery, not to
rejecting the unchanged shared helper based on source inspection. Both discovery
and shared-loader validation must resolve the same exact current registration;
an actual helper omission or schema failure remains a blocker.

Do not render a loadable DAT until all applicable gates pass:

1. Resolve exactly one target environment and release without persisting credentials. For the Question Library status-only inactivation route, an independently verified application-release label may be unavailable only under the schema-2 impact-review contract: record it as null, retain the explicit limitation, and bind the current live template and operation/component contract hashes. Do not apply this exception to any other operation.
2. Resolve the exact top-level business object without an unsupported finder or first-match choice.
3. Read the current target component hierarchy, attribute metadata, user keys, mandatory indicators, registered operations, and UCM template.
4. Confirm the intended operation for every root, child, attachment, and translation component. Never invent `UPDATE`, `DELETE`, or another instruction.
5. Resolve every target reference exactly. Zero matches is missing; multiple exact matches is ambiguous. Both block generation.
6. Detect duplicate submitted business keys and collisions with existing target keys according to the intended create, update, version, duplicate, or delete operation.
7. Confirm lifecycle and mutability state for seeded, private, locked, draft, active, inactive, latest-version, and in-use objects.
8. Validate operation-specific required fields. A global metadata mandatory flag is evidence, not permission to require that attribute for every operation and section.
9. Exclude generated and source-pod IDs unless the live operation explicitly requires an exact current target ID, such as a documented attachment update or delete.
10. Stop when a delimiter, line break, binary, translation, attachment, or source-reference value cannot be represented using a confirmed target contract.

## Deterministic build specification

Create a machine-readable `hdl_dat_build_specification` before serialization. It must contain:

- target environment identifier and release, without credentials; only the Question Library status-only inactivation exception above may use a null release;
- task code and task name;
- top-level discriminator and exact DAT filename;
- intended operation and operation evidence;
- source artifact identities and hashes;
- live metadata/template retrieval evidence;
- ordered sections and their selected attributes in current-template order;
- ordered parent and child rows with complete portable business keys;
- reference-resolution and duplicate-validation results;
- explicit values, preserved target values, disclosed defaults, and exclusions;
- translation and attachment decisions;
- blockers, warnings, and required post-load readback checks.

The deterministic executable procedure consumes only this specification. It must:

1. Emit sections in live parent-before-child order.
2. Emit each `METADATA` row with exact case-sensitive section and attribute names in current-template order.
3. Emit data rows with the registered instruction, exact section discriminator, and exactly one value for each selected metadata attribute.
4. Preserve the normalized row order and explicitly supplied sequence values; never derive identity from display text or source row position.
5. Omit unknown attributes, copied generated IDs, audit values, and unsupported source-reference fields.
6. Use only a confirmed DAT representation for delimiters, line breaks, dates, nulls, files, and CLOB/BLOB content. Block instead of inventing escaping or quoting.
7. Produce byte-stable output from the same build specification and record a SHA-256 for every DAT and final ZIP.

If the documented executable procedure cannot consume the build specification for the selected target contract, return the specification and an `UNSUPPORTED` procedure gap. Do not freehand a loadable DAT or use a generic sample with placeholders as the business payload.

## Executable deterministic build procedure

Build the version 1 canonical request from the approved business specification,
exact target DAT header template, and validation evidence. After all business,
reference, lifecycle, and update gates pass, normalize the approved rows into
`render_sections` and invoke
`../scripts/questionnaire_dat_serializer.py`. The serializer is the only
Questionnaire-pillar component permitted to construct pipe-delimited DAT rows.
Do not freehand a row, use a sample DAT as payload, or substitute a generic CSV
conversion utility.

The serializer requires the exact freshly downloaded template, verifies its
SHA-256 and registered filename, fills omitted optional attributes with blank
cells in live metadata order, rejects unknown or nonportable attributes, and
calls `questionnaire_dat_validator.py` in memory before writing anything. It
publishes the DAT and `hdl-dat-validation-receipt.json` together only when
metadata/value parity, component ordering, portable-value checks, task-local
semantics, required attributes, and round-trip equality all pass. Either output
already existing is an overwrite blocker.

Add this normalized structure to the completed canonical request after mapping
the task-specific `records` hierarchy. Parent values inherited during
normalization must be explicit in every child row. Components occur once and in
the exact live template order; every row contains only an `attributes` object:

```json
{
  "render_sections": [
    {
      "component": "<live root discriminator>",
      "rows": [
        {
          "attributes": {
            "<live attribute name>": "<approved value>"
          }
        }
      ]
    }
  ]
}
```

Run from the functional-area skill directory:

```bash
python3 scripts/questionnaire_dat_serializer.py \
  --spec <canonical-build-specification.json> \
  --template <exact-live-template-path> \
  --output-dir <new-versioned-run-directory>
```

For review of an existing candidate without publication, run:

```bash
python3 scripts/questionnaire_dat_validator.py <candidate.dat> \
  --template <exact-live-template-path> \
  --spec <canonical-build-specification.json> \
  --expected-filename <registered-file-name>
```

The Question Library canonical request has this shape:

```json
{
  "contract_version": 1,
  "task": "question-library",
  "intent": "create",
  "operation": "MERGE",
  "validation_evidence": {
    "target": "<target environment identifier>",
    "release": "<target release>",
    "checked_at": "<RFC 3339 timestamp with timezone>",
    "evidence_ids": [
      "<immutable metadata evidence ID>",
      "<immutable reference-validation evidence ID>",
      "<immutable response-type evidence ID>"
    ],
    "main_template": {
      "file_name": "Question.dat",
      "sha256": "<lowercase SHA-256 of the exact live template bytes>",
      "merge_registered": true
    },
    "component_contract": {
      "Question": {
        "user_keys": ["SubscriberName", "QuestionCode", "QstnVersionNum"],
        "required_attributes": [
          "SubscriberName",
          "QuestionCode",
          "QstnVersionNum",
          "Status",
          "QuestionText",
          "QuestionType",
          "ResponseTypeName",
          "PrivacyFlag"
        ],
        "required_reference_types": ["resolve_question_subscriber"],
        "merge_registered": true
      }
    },
    "response_type_pairs": [
      {
        "question_type": "<exact target QuestionType>",
        "response_type_name": "<exact target HDL display Name>",
        "resolver": "resolve_live_question_response_type",
        "evidence_id": "<immutable response-type evidence ID>"
      }
    ],
    "reference_results": [
      {
        "component": "Question",
        "row_key": {
          "SubscriberName": "<resolved subscriber>",
          "QuestionCode": "<approved code>",
          "QstnVersionNum": "1"
        },
        "resolver": "resolve_question_subscriber",
        "reference_key": {"SubscriberName": "<resolved subscriber>"},
        "status": "passed",
        "evidence_id": "<immutable reference-validation evidence ID>"
      }
    ],
    "evidence_bundle_sha256": "<canonical request-bound SHA-256>"
  },
  "records": [
    {
      "attributes": {
        "SubscriberName": "<resolved subscriber>",
        "QuestionCode": "<approved code>",
        "QstnVersionNum": 1,
        "Status": "<approved status>",
        "QuestionText": "<approved text>",
        "QuestionType": "<resolved type>",
        "ResponseTypeName": "<resolved HDL LOV value>",
        "PrivacyFlag": "N"
      }
    }
  ],
  "translations": []
}
```

For an explicit Question Library update, use the same version 1 request shape
with `intent: "update"` and `operation: "MERGE"`, and add this update contract:

```json
{
  "update_contract": {
    "existing_identity_status": "passed",
    "update_allowed": true,
    "current_state_evidence_id": "<immutable exact readback evidence ID>",
    "current_state_checked_at": "<RFC 3339 timestamp with timezone>",
    "changed_fields": ["<approved mutable attribute>"],
    "preserved_fields": ["<unchanged emitted attribute>"],
    "affected_child_rows": [
      {
        "component": "Answer",
        "row_key": {
          "SubscriberName": "<resolved subscriber>",
          "QuestionCode": "<existing code>",
          "QstnVersionNum": "<existing version>",
          "AnswerCode": "<existing or new answer code>"
        },
        "intent": "update",
        "existing_identity_status": "passed",
        "current_state_evidence_id": "<immutable child readback evidence ID>",
        "changed_fields": ["<approved mutable child attribute>"],
        "preserved_fields": ["<unchanged emitted child attribute>"]
      }
    ]
  }
}
```

For a schema-2 approved status-only inactivation, `validation_evidence.release`
may be JSON null only when `release_evidence.status` is `unavailable`. Bind that
null in `evidence_bundle_sha256`, retain the live `Question.dat` and contract
hashes, and emit only the approved root Status change. Never infer a release or
reuse this exception for another update.

The update request must resolve exactly one existing root by
`SubscriberName + QuestionCode + QstnVersionNum`, and each affected existing
child by its complete live user key. `changed_fields` must be non-empty and may
name only live-registered mutable attributes. It must not contain a root or
child user-key attribute, generated ID, audit field, source reference, or an
attribute that the current target does not register for `MERGE`. Every emitted
non-key value that is not changed must equal the exact current readback and be
listed in `preserved_fields`. A submitted existing AnswerCode is valid only
when it resolves exactly once to that same question/version and is declared as
an affected existing child; a new AnswerCode must have zero target matches.
Omitting an existing Answer or QuestionContext preserves it. Update never
means delete, detach, rename, reparent, or create a new question version.

### Questionnaire Template canonical request

For `questionnaire-templates`, use the following complete create request shape.
The example places an existing reusable Question Library question; it
does not create an embedded question. Replace the documented component keys,
required attributes, and column names when current target metadata proves a
different registered contract. Do not silently adapt them.

```json
{
  "contract_version": 1,
  "task": "questionnaire-templates",
  "intent": "create",
  "operation": "MERGE",
  "validation_evidence": {
    "target": "<target environment identifier>",
    "release": "<target release>",
    "checked_at": "<RFC 3339 timestamp with timezone>",
    "evidence_ids": [
      "<immutable QuestionnaireTemplate metadata evidence ID>",
      "<immutable template reference-validation evidence ID>"
    ],
    "main_template": {
      "file_name": "QuestionnaireTemplate.dat",
      "sha256": "<lowercase SHA-256 of the exact live template bytes>",
      "merge_registered": true
    },
    "component_contract": {
      "QuestionnaireTemplate": {
        "user_keys": ["QuestionnaireCode", "SubscriberName"],
        "required_attributes": [
          "QuestionnaireCode",
          "SubscriberName",
          "Name",
          "Status",
          "PrivacyFlag",
          "OwnerPersonNumber",
          "AllowFormatChg",
          "AllowIntroChg",
          "AllowQstnOrderChg",
          "AllowRespOrderChg",
          "AllowSectionChg"
        ],
        "required_reference_types": [
          "resolve_template_subscriber",
          "resolve_template_existing_identity",
          "resolve_template_owner"
        ],
        "merge_registered": true
      },
      "Section": {
        "user_keys": [
          "SubscriberName",
          "QuestionnaireCode",
          "SectionSeqNum"
        ],
        "required_attributes": [
          "SubscriberName",
          "QuestionnaireCode",
          "SectionSeqNum",
          "Name"
        ],
        "required_reference_types": [],
        "merge_registered": true
      },
      "Question": {
        "user_keys": [
          "SubscriberName",
          "QuestionnaireCode",
          "SectionSeqNum",
          "QuestionCode",
          "QstnVersionNum",
          "SeqNum"
        ],
        "required_attributes": [
          "SubscriberName",
          "QuestionnaireCode",
          "SectionSeqNum",
          "QuestionCode",
          "QstnVersionNum",
          "SeqNum",
          "Mandatory",
          "AdhocQstn"
        ],
        "required_reference_types": ["resolve_template_question_version"],
        "merge_registered": true
      }
    },
    "reference_results": [
      {
        "component": "QuestionnaireTemplate",
        "row_key": {
          "SubscriberName": "<resolved subscriber>",
          "QuestionnaireCode": "<approved template code>"
        },
        "resolver": "resolve_template_subscriber",
        "reference_key": {"SubscriberName": "<resolved subscriber>"},
        "status": "passed",
        "evidence_id": "<immutable subscriber evidence ID>"
      },
      {
        "component": "QuestionnaireTemplate",
        "row_key": {
          "SubscriberName": "<resolved subscriber>",
          "QuestionnaireCode": "<approved template code>"
        },
        "resolver": "resolve_template_existing_identity",
        "reference_key": {
          "SubscriberName": "<resolved subscriber>",
          "QuestionnaireCode": "<approved template code>"
        },
        "status": "passed",
        "evidence_id": "<immutable identity-collision evidence ID>"
      },
      {
        "component": "Question",
        "row_key": {
          "SubscriberName": "<resolved subscriber>",
          "QuestionnaireCode": "<approved template code>",
          "SectionSeqNum": "1",
          "QuestionCode": "<existing reusable question code>",
          "QstnVersionNum": "1",
          "SeqNum": "1"
        },
        "resolver": "resolve_template_question_version",
        "reference_key": {
          "SubscriberName": "<resolved subscriber>",
          "QuestionCode": "<existing reusable question code>",
          "QstnVersionNum": "1"
        },
        "status": "passed",
        "evidence_id": "<immutable reusable-question readback evidence ID>"
      },
      {
        "component": "QuestionnaireTemplate",
        "row_key": {
          "SubscriberName": "<resolved subscriber>",
          "QuestionnaireCode": "<approved template code>"
        },
        "resolver": "resolve_template_owner",
        "reference_key": {
          "SubscriberName": "<resolved subscriber>",
          "OwnerPersonNumber": "<approved owner person number>"
        },
        "status": "passed",
        "evidence_id": "<immutable owner readback evidence ID>"
      }
    ],
    "evidence_bundle_sha256": "<canonical request-bound SHA-256>"
  },
  "records": [
    {
      "attributes": {
        "Name": "<approved template name>",
        "AllowIntroChg": "N",
        "AllowFormatChg": "N",
        "AllowSectionChg": "N",
        "AllowQstnOrderChg": "N",
        "AllowRespOrderChg": "N",
        "RandomQstns": "N",
        "RandomAnswers": "N",
        "QuestionnaireCode": "<approved template code>",
        "Status": "<approved status>",
        "PrivacyFlag": "N",
        "OwnerPersonNumber": "<approved owner person number>",
        "SubscriberName": "<resolved subscriber>"
      },
      "sections": [
        {
          "attributes": {
            "Name": "<approved section name>",
            "SectionSeqNum": 1,
            "NewPage": "N",
            "QuestionOrder": "FIXED",
            "ResponseOrder": "FIXED",
            "Mandatory": "N",
            "AllowAdhoc": "N"
          },
          "questions": [
            {
              "mode": "reference",
              "attributes": {
                "SeqNum": 1,
                "QstnVersionNum": 1,
                "AdhocQstn": "N",
                "Mandatory": "Y",
                "QuestionCode": "<existing reusable question code>"
              },
              "answers": []
            },
            {
              "mode": "direct",
              "attributes": {
                "QuestionCode": "<new direct question code>",
                "QstnVersionNum": 1,
                "QuestionText": "<approved text>",
                "QuestionType": "TEXT",
                "ResponseTypeName": "<resolved target response type>",
                "Status": "<approved status>",
                "PrivacyFlag": "N",
                "CategoryName": "<resolved question category>",
                "QstnSequenceNumber": 2,
                "Mandatory": "N",
                "AdhocQstn": "N"
              },
              "answers": []
            }
          ]
        }
      ]
    }
  ],
  "translations": []
}
```

For an explicit Questionnaire Template update, use the same version 1 request
shape with `intent: "update"` and `operation: "MERGE"`, and add this update
contract:

```json
{
  "update_contract": {
    "existing_identity_status": "passed",
    "full_template_readback_status": "passed",
    "update_allowed": true,
    "in_use": "<current target value>",
    "mutability_evidence_id": "<immutable release-specific evidence ID>",
    "current_state_evidence_id": "<immutable full hierarchy readback evidence ID>",
    "current_state_checked_at": "<RFC 3339 timestamp with timezone>",
    "root_changed_fields": ["<approved mutable root attribute>"],
    "root_preserved_fields": ["<unchanged emitted root attribute>"],
    "affected_child_rows": [
      {
        "component": "Section",
        "row_intent": "existing",
        "row_key": {
          "SubscriberName": "<resolved subscriber>",
          "QuestionnaireCode": "<existing template code>",
          "SectionSeqNum": "<existing section sequence>"
        },
        "current_state_evidence_id": "<immutable child readback evidence ID>",
        "changed_fields": ["<approved mutable child attribute>"],
        "preserved_fields": ["<unchanged emitted child attribute>"]
      }
    ]
  }
}
```

The update request must resolve exactly one full template by
`SubscriberName + QuestionnaireCode`; a `questionnaireTemplatesLOV` match alone
is insufficient. Prove the target-registered `MERGE`, root update permission,
current seeded/locked/status/in-use state, and the exact editable fields and
child operations for the selected release. The aggregate of
`root_changed_fields` and every child `changed_fields` must be non-empty. Each
changed attribute must be live-registered and proven mutable in the observed
state. Every emitted unchanged value must equal exact current readback and be
listed as preserved.

Each affected `Section`, `Question`, and `Answer` row must declare
`row_intent: "existing"` or `row_intent: "new"`. Existing rows require one
exact full-key match and immutable live user keys. New rows require zero key
matches and a live-registered add-through-`MERGE` contract. Changing a section
sequence, moving or resequencing a question placement, changing a reusable
question/version identity, or changing an answer key is not an update. Omitted
children are preserved; omission never means delete, detach, move, reorder, or
replace. Attachments, embedded-question creation, destructive changes, and
template translation remain unsupported.

When the template is in use, require current release-specific proof that every
changed field and child operation is editable in that exact state. The declared
live downstream-usage REST resolver is partial and cannot by itself authorize
an in-use hierarchy or lifecycle mutation. If full impact or mutability proof
is unavailable, retain the validated specification and return `Blocked`.

### Questionnaire canonical request

For `questionnaires`, use the following complete create request shape.
The questionnaire may reference a validated template and may place an existing
reusable Question Library question. `CategoryName` and `TemplateQstnrCode` are
conditional: omit each attribute and its resolver only when the approved
business specification and current live contract do not require that
reference.

```json
{
  "contract_version": 1,
  "task": "questionnaires",
  "intent": "create",
  "operation": "MERGE",
  "validation_evidence": {
    "target": "<target environment identifier>",
    "release": "<target release>",
    "checked_at": "<RFC 3339 timestamp with timezone>",
    "evidence_ids": [
      "<immutable Questionnaire metadata evidence ID>",
      "<immutable questionnaire reference-validation evidence ID>",
      "<immutable reusable-question readback evidence ID>"
    ],
    "main_template": {
      "file_name": "Questionnaire.dat",
      "sha256": "<lowercase SHA-256 of the exact live template bytes>",
      "merge_registered": true
    },
    "component_contract": {
      "Questionnaire": {
        "user_keys": [
          "QuestionnaireCode",
          "QstnrVersionNum",
          "SubscriberName"
        ],
        "required_attributes": [
          "QuestionnaireCode",
          "QstnrVersionNum",
          "SubscriberName",
          "QuestionnaireName",
          "Status",
          "InUse",
          "PrivacyFlag"
        ],
        "required_reference_types": [
          "resolve_questionnaire_subscriber",
          "resolve_questionnaire_existing_identity",
          "resolve_questionnaire_category",
          "resolve_questionnaire_template"
        ],
        "merge_registered": true
      },
      "Section": {
        "user_keys": [
          "QuestionnaireCode",
          "QstnrVersionNum",
          "SectionSeqNum",
          "SubscriberName"
        ],
        "required_attributes": [
          "QuestionnaireCode",
          "QstnrVersionNum",
          "SubscriberName",
          "SectionSeqNum",
          "Name"
        ],
        "required_reference_types": [],
        "merge_registered": true
      },
      "Question": {
        "user_keys": [
          "QuestionCode",
          "QstnVersionNum",
          "SectionSeqNum",
          "QuestionnaireCode",
          "QstnrVersionNum",
          "SubscriberName"
        ],
        "required_attributes": [
          "QuestionCode",
          "QstnVersionNum",
          "SectionSeqNum",
          "QuestionnaireCode",
          "QstnrVersionNum",
          "SubscriberName",
          "QuestionType",
          "ResponseTypeName",
          "QstnSequenceNumber",
          "Mandatory"
        ],
        "required_reference_types": [
          "resolve_questionnaire_question_version"
        ],
        "merge_registered": true
      }
    },
    "response_type_pairs": [
      {
        "question_type": "<exact reusable-question QuestionType>",
        "response_type_name": "<exact reusable-question HDL display Name>",
        "resolver": "resolve_live_questionnaire_question_version",
        "evidence_id": "<immutable reusable-question readback evidence ID>"
      }
    ],
    "reference_results": [
      {
        "component": "Questionnaire",
        "row_key": {
          "SubscriberName": "<resolved subscriber>",
          "QuestionnaireCode": "<approved questionnaire code>",
          "QstnrVersionNum": "1"
        },
        "resolver": "resolve_questionnaire_subscriber",
        "reference_key": {"SubscriberName": "<resolved subscriber>"},
        "status": "passed",
        "evidence_id": "<immutable subscriber evidence ID>"
      },
      {
        "component": "Questionnaire",
        "row_key": {
          "SubscriberName": "<resolved subscriber>",
          "QuestionnaireCode": "<approved questionnaire code>",
          "QstnrVersionNum": "1"
        },
        "resolver": "resolve_questionnaire_existing_identity",
        "reference_key": {
          "SubscriberName": "<resolved subscriber>",
          "QuestionnaireCode": "<approved questionnaire code>",
          "QstnrVersionNum": "1"
        },
        "status": "passed",
        "evidence_id": "<immutable identity-collision evidence ID>"
      },
      {
        "component": "Questionnaire",
        "row_key": {
          "SubscriberName": "<resolved subscriber>",
          "QuestionnaireCode": "<approved questionnaire code>",
          "QstnrVersionNum": "1"
        },
        "resolver": "resolve_questionnaire_category",
        "reference_key": {"CategoryName": "<resolved category>"},
        "status": "passed",
        "evidence_id": "<immutable category evidence ID>"
      },
      {
        "component": "Questionnaire",
        "row_key": {
          "SubscriberName": "<resolved subscriber>",
          "QuestionnaireCode": "<approved questionnaire code>",
          "QstnrVersionNum": "1"
        },
        "resolver": "resolve_questionnaire_template",
        "reference_key": {
          "SubscriberName": "<resolved subscriber>",
          "TemplateQstnrCode": "<validated template code>"
        },
        "status": "passed",
        "evidence_id": "<immutable template readback evidence ID>"
      },
      {
        "component": "Question",
        "row_key": {
          "SubscriberName": "<resolved subscriber>",
          "QuestionnaireCode": "<approved questionnaire code>",
          "QstnrVersionNum": "1",
          "SectionSeqNum": "1",
          "QuestionCode": "<existing reusable question code>",
          "QstnVersionNum": "1",
          "QstnSequenceNumber": "1"
        },
        "resolver": "resolve_questionnaire_question_version",
        "reference_key": {
          "SubscriberName": "<resolved subscriber>",
          "QuestionCode": "<existing reusable question code>",
          "QstnVersionNum": "1"
        },
        "status": "passed",
        "evidence_id": "<immutable reusable-question readback evidence ID>"
      }
    ],
    "evidence_bundle_sha256": "<canonical request-bound SHA-256>"
  },
  "records": [
    {
      "attributes": {
        "QuestionnaireCode": "<approved questionnaire code>",
        "QstnrVersionNum": 1,
        "Status": "<approved status>",
        "InUse": "N",
        "QuestionnaireName": "<approved questionnaire name>",
        "PrivacyFlag": "N",
        "SubscriberName": "<resolved subscriber>",
        "CategoryName": "<resolved category>",
        "TemplateQstnrCode": "<validated template code>"
      },
      "sections": [
        {
          "attributes": {
            "Name": "<approved section name>",
            "SectionSeqNum": 1,
            "NewPage": "N",
            "QuestionOrder": "FIXED",
            "ResponseOrder": "FIXED",
            "Mandatory": "N",
            "AllowAdhoc": "N"
          },
          "questions": [
            {
              "mode": "reference",
              "attributes": {
                "QuestionCode": "<existing reusable question code>",
                "QstnVersionNum": 1,
                "QuestionType": "<resolved question type>",
                "SubscriberName": "<resolved subscriber>",
                "ResponseTypeName": "<resolved HDL response type>",
                "QstnSequenceNumber": 1,
                "Mandatory": "Y",
                "AdhocQstn": "N"
              },
              "answers": []
            }
          ]
        }
      ]
    }
  ],
  "translations": []
}
```

For an explicit Questionnaire update, use the same version 1 request shape
with `intent: "update"` and `operation: "MERGE"`, and add this update contract:

```json
{
  "update_contract": {
    "existing_identity_status": "passed",
    "full_questionnaire_readback_status": "passed",
    "update_allowed": true,
    "latest_version": true,
    "in_use": "<current target value>",
    "responses_exist": "<current proven value>",
    "template_linkage_intent": "preserve",
    "mutability_evidence_id": "<immutable release-specific evidence ID>",
    "current_state_evidence_id": "<immutable full hierarchy readback evidence ID>",
    "current_state_checked_at": "<RFC 3339 timestamp with timezone>",
    "root_changed_fields": ["<approved mutable root attribute>"],
    "root_preserved_fields": ["<unchanged emitted root attribute>"],
    "affected_child_rows": [
      {
        "component": "Question",
        "mode": "reference",
        "row_intent": "existing",
        "row_key": {
          "SubscriberName": "<resolved subscriber>",
          "QuestionnaireCode": "<existing questionnaire code>",
          "QstnrVersionNum": "<existing questionnaire version>",
          "SectionSeqNum": "<existing section sequence>",
          "QuestionCode": "<existing reusable question code>",
          "QstnVersionNum": "<existing question version>",
          "QstnSequenceNumber": "<existing placement sequence>"
        },
        "current_state_evidence_id": "<immutable child readback evidence ID>",
        "changed_fields": ["<approved mutable child attribute>"],
        "preserved_fields": ["<unchanged emitted child attribute>"]
      }
    ]
  }
}
```

The update request must resolve exactly one authoritative full questionnaire
by `SubscriberName + QuestionnaireCode + QstnrVersionNum`, including its
current hierarchy. Prove the target-registered `MERGE`, root update permission,
latest-version state, seeded/locked/status/in-use state, response existence,
template linkage, and exact editable fields and child operations for the
selected release. The aggregate of `root_changed_fields` and every child
`changed_fields` must be non-empty. Each changed attribute must be
live-registered and proven mutable in the observed state. Every emitted
unchanged value must equal exact current readback and be listed as preserved.

Each affected `Section`, `Question`, and `Answer` row must declare
`row_intent: "existing"` or `row_intent: "new"`; Question rows must also retain
their approved `mode: "reference"` or `mode: "direct"`. Existing rows require
one exact complete-key match and immutable live user keys. New rows require
zero key matches and a live-registered add-through-`MERGE` contract. Changing
a section sequence, moving or resequencing a question placement, replacing a
reusable question/version, changing a direct-question identity, or changing an
answer key is not an update. Omitted children are preserved; omission never
means delete, detach, move, reorder, or replace. Template linkage is preserved
unless current target evidence explicitly proves the requested linkage change
mutable and impact-safe.

When the questionnaire is in use or has responses, require current
release-specific proof that every changed field and child operation is editable
in that exact state and complete impact evidence for hierarchy, scoring,
template-linkage, status, or lifecycle change. The declared lifecycle REST
resolver is partial and cannot by itself authorize those mutations. Existing
translation update, attachments, destructive changes, and downstream consumer
linkage remain unsupported. If full state, impact, or mutability proof is
unavailable, retain the validated specification and return `Blocked`.

For both hierarchical requests, root business-key values are inherited into
the emitted child DAT rows. If the request repeats a parent value at a child
level, it must match exactly. An `answers` collection is optional; when used,
every answer must supply the exact live answer business key and an explicit
answer sequence, and the request must add the live `Answer` component contract
and any required row-bound resolver results. Attachments remain unsupported.
Direct Question creation requires the exact additional contract described
below.

The component contract must exactly cover every emitted section. For each component it binds the live user-key order, create-required attributes, required row-level resolvers, and MERGE registration. Every required resolver needs exactly one `passed` result bound to the emitted deterministic row key and one declared evidence ID, unless the explicit run-scoped validation-waiver contract below permits that exact result to be `overridden`. A deterministic row key may differ from the exact current live-key order, or include an explicit hierarchy discriminator such as placement sequence or translation language, only through an exact task/component profile reviewed against current target metadata. The builder rejects arbitrary subsets, reordered keys outside those profiles, unknown keys, and surrogate-key substitutions.

### Explicit run-scoped validation waiver

Use this path only when the user explicitly directs the current run to proceed
despite one or more identified reference, lookup, collision-readback, design,
or task-readiness failures. It is an exception record, not a successful lookup.

Add `validation_evidence.validation_waivers` to the canonical request. Each
entry must contain a unique `waiver_id`, the exact affected resolver or rule
resource, `status: "overridden"`, the original failure classification and
evidence ID, a sanitized user-authorized reason, the run identifier, and the
explicit scope. The corresponding row-bound result must retain its original
key and evidence ID, use `status: "overridden"`, and name that `waiver_id`.
Do not replace the failed evidence, claim a match count, infer that a key is
absent from a failed or zero-row export, or mark the result `passed`.

The evidence digest binds the waiver records and overridden results exactly as
it binds passed results. Publication is allowed only when every non-passing
required result has one exact waiver record and no unwaived blocker remains.
Record `validation_status: "OVERRIDDEN"`, the affected resolvers/resources,
original evidence IDs, and warnings in the generation manifest and immutable
handoff. Carry the same exceptions into Data Loader Task Hook rule results as
`status: "overridden"`, with their failure evidence and waiver reason, and use
its readiness-override option only for that reviewed run.

The following checks are never waivable through this path: target environment
identity; current live HDL business-object registration, template/schema,
component, attribute, user-key, and operation checks; portable key and
parent-child integrity; duplicate submitted keys; safe path and file selection;
UTF-8, delimiter, line-break, null, attachment, and unsupported-content rules;
deterministic DAT and ZIP hashes; unchanged-artifact verification; and the
separate standalone Data Loader approval immediately before any Fusion write.
Any change to the source, target, schema, DAT, ZIP, waiver scope, or failure
evidence invalidates the exception and requires a new preflight.

`evidence_bundle_sha256` binds the target, release, timestamp, evidence IDs,
task, intent, operation, templates, component contract, row-bound reference
results, and business request. Compute it after the request is complete by
removing only `validation_evidence.evidence_bundle_sha256`, serializing the
remaining request as UTF-8 JSON with object keys sorted lexicographically and
no insignificant whitespace, then taking the lowercase SHA-256 digest. Insert
that digest into the request and do not alter the request afterward.

This hash proves internal integrity only. It does not prove that the evidence came from Fusion, is current, or resolved every required business reference. The manifest therefore labels the result `CALLER_ATTESTED_CANDIDATE_AWAITING_CORE_REVALIDATION`; `core.data-loader` must independently recollect and revalidate the live contract before preview or upload.

For `questionnaire-templates` and `questionnaires`, records use `sections`, each section may use `questions`, and each question may use `answers`. Supply every `SectionSeqNum`, placement sequence, and answer sequence explicitly. A Question must use `mode: reference` or, for Questionnaires only, `mode: direct`. Direct mode creates a `TEXT`, `1CHOICE`, `MULTCHOICE`, or `NONE` Question inside its Questionnaire hierarchy; it does not create a Question Library definition. `mode: direct-text` is a compatibility alias for direct `TEXT` only. Direct mode requires the exact current component contract plus the [direct-question normalization procedure](direct-text-question-serializer.md), followed by the executable serializer and validator. `QuestionTranslation.dat` and `QuestionnaireTranslation.dat` may be generated only with an exact registered translation template and component contract. `QuestionnaireTemplateTranslation.dat` is currently `UNSUPPORTED` because its `VersionNumber` cannot be proven against the version-unqualified portable template parent key.

### No-write preflight

Before generating a DAT, verify all of the following and record the results in
the `validation_result` workspace output:

1. The supplied main and optional translation templates contain metadata and
   comments only; their exact filenames, root discriminators, section order,
   attribute order, and SHA-256 values match `validation_evidence`.
2. The task, supported intent, `operation: MERGE`, record collection, component
   contract, and row-bound reference results are complete and bound by the
   evidence digest. Supported intent is `create` for every task, or `update`
   for Question Library, Questionnaire Templates, and Questionnaires with their
   complete update contracts above. Each
   required result is either `passed` or is exactly paired with an explicit
   run-scoped `overridden` waiver as defined above. Update identity, operation,
   mutability, current-state readback, portable-key integrity, and preserved
   values are non-waivable.
3. Each root and child has its documented portable business key. Parent values
   agree when supplied at more than one level; every section, placement, and
   answer sequence is explicit; and no duplicate root, section, placement,
   answer, or context key exists.
4. Every emitted attribute occurs in the matching template section. Each
   emitted component has a uniform attribute shape; generated IDs, source
   references, audit fields, attachments, null tokens, delimiters, and line
   breaks are absent.
5. A template placement is an existing reusable-question reference. A
   questionnaire placement is either an existing reusable-question reference
   or a complete `mode: direct` definition rendered with the approved
   direct-question normalization procedure. Translation rows are allowed only for the parent and
   registration cases defined below.

If any non-waived check fails, return `Blocked` with the field path and do not
write a DAT. For a successful or explicitly overridden preflight, create an
in-memory rendering preview: list each
DAT filename, root discriminator, ordered metadata columns, normalized row
keys, row count, byte count, and SHA-256 of the proposed UTF-8 bytes. This
preflight performs no file write.

### DAT rendering and publication

After a reviewed successful preflight, invoke
`scripts/questionnaire_dat_serializer.py` with the immutable canonical build
specification and exact live template. The executable retains the exact
template comments and `METADATA` rows. For each populated template section it
emits normalized parent-before-child `MERGE|<section>|...` rows with exactly one
value for every metadata attribute in exact template order. It does not quote,
escape, or invent a representation for values that failed preflight. Emit
translation sections only in their own exact translation template.

Encode the DAT as UTF-8, calculate a SHA-256 for each DAT, and create
`hdl-generation-manifest.json` with the task, evidence digest, source template
hashes, DAT hashes, row counts, normalized row-key summaries, warnings, the
hash-bound `hdl-dat-validation-receipt.json`, and the boundary
`CALLER_ATTESTED_CANDIDATE_AWAITING_CORE_REVALIDATION`. Publish
only to a new versioned directory under
`project/<project_id>/artifacts/pillars/hcm/hcm-tool/questionnaire/<task>/current/<run_id>/`.
Never overwrite an existing artifact or handoff. Publication requires the
serializer's `status: passed` receipt and exact receipt SHA-256 match; visual
inspection is supplemental and cannot replace executable validation.

The current executable safe scope is deliberately narrower than every component that may appear in a live template:

- Create and explicit update `MERGE` for all three task scopes under their complete task-specific contracts above. Implicit create-to-update conversion, key changes, destructive child changes, `DELETE`, and an invented `UPDATE` instruction are rejected.
- Question Library roots, answers, and Recruiting contexts.
- Template and questionnaire roots, sections, existing reusable-question placements, direct questionnaire Question rows of the four supported types, and answer rows required by direct choice questions.
- Question and ordinary-questionnaire translation roots only when exact live registration and template evidence are supplied; template translation is blocked.
- Explicit key-bearing sequences only; array position never becomes identity or business order.
- No BLOB/CLOB/attachment packaging, copied/generated IDs, audit fields, source references, JSON null, `#NULL`, or mixed row shapes. Direct `TEXT` and `NONE` rows must not have answers; direct choice rows must have target-valid answers.

When the requested design exceeds this scope, retain the validated build specification and return `UNSUPPORTED`. Do not weaken this procedure or route around `core.data-loader`.

## Task-specific corrections

### Question Library

- `Question` identity is `SubscriberName + QuestionCode + QstnVersionNum` under the current reviewed HDL contract.
- For update, require exactly one current root, `update_allowed: true`, a non-empty approved changed-field set, exact readback of every emitted current value, and immutable root and child keys. Preserve omitted children; do not infer delete or replacement from omission.
- For an existing Answer row in an update, an AnswerCode match is valid only when it resolves exactly once to the same resolved Question/version. A match under another parent is a collision. A new AnswerCode must remain target-wide unique.
- Resolve `ResponseTypeName` together with `QuestionType`; never convert an FSM `ResponseTypeCode` or guessed English label into the HDL value.
- Bind every emitted pair to `validation_evidence.response_type_pairs`, sourced from the exact live target lookup or reusable-question readback. The executable validator rejects a missing, partial, or nonmatching pair before writing a DAT.
- `AnswerCode` is the current reviewed HDL answer key. Supply the approved sequence explicitly; do not substitute sequence for the target user key.
- Recruiting context and classification fields apply only to an exactly resolved Recruiting subscriber.
- Generate `QuestionTranslation.dat` only when registered; use its complete parent key plus installed `Language` and the operation returned by target metadata.

### Questionnaire Templates

- The root portable identity is the exactly resolved `SubscriberName + QuestionnaireCode` contract returned by the target.
- For update, require one authoritative full-template and hierarchy readback, exact root and per-component mutability, current in-use/seeded/locked state, a non-empty aggregate changed-field set, immutable keys, and explicit existing/new child intent. A lightweight LOV row cannot authorize mutation.
- Preserve omitted children. Existing section, placement, and answer keys cannot be changed; new rows require zero collisions. Do not model removal, movement, resequencing, or replacement as `MERGE` update.
- An in-use template may be updated only where current release-specific evidence proves the exact changed fields and child operations editable. Partial direct-usage REST evidence is insufficient for an in-use hierarchy or lifecycle change.
- An existing reusable-question placement needs its exact question code/version, parent section, and sequence. A blank `QstnResponseTypeName` means inherit.
- Require category and embedded-question definition fields only when the hierarchy is creating a missing question and current target metadata/source confirms that operation.
- Response format codes identify the format; they are not automatically valid values for the individual HDL `...Response` allow/deny fields.
- Keep template translation generation blocked until its target `VersionNumber` can be bound to an exact backing-template version readback; registration and `TemplateFlag=Y` alone are insufficient.
- Treat backing version, latest-version state, and template flag as loader-managed unless the live DAT schema explicitly exposes them as writable attributes.

### Questionnaires

- Root identity is `SubscriberName + QuestionnaireCode + QstnrVersionNum` under the current reviewed HDL contract.
- For update, require one authoritative full questionnaire and hierarchy readback, exact root and per-component mutability, current latest/in-use/seeded/locked/response state, a non-empty aggregate changed-field set, immutable keys, and explicit existing/new child intent.
- Preserve omitted children. Existing section, reusable/direct question, and answer keys cannot be changed; new rows require zero collisions. Do not model removal, movement, resequencing, reusable-question replacement, or direct-question replacement as `MERGE` update.
- Preserve template linkage unless current target evidence proves the requested linkage change mutable and impact-safe. In-use or response-bearing hierarchy, scoring, linkage, status, or lifecycle changes require complete impact proof; partial lifecycle REST evidence is insufficient.
- `TemplateQstnrCode` is conditional: require it only when supplied or when the selected target HDL operation/subscriber contract marks it mandatory. Whenever supplied, resolve one exact active compatible template in the same subscriber.
- A reusable question's `ResponseTypeName` is not the questionnaire placement override. `QstnrQstnResponseTypeName` is optional; blank means inherit. Resolve it from the target LOV only when an override is explicitly requested.
- When current target metadata/runtime evidence requires reusable-question response context on a create placement, supply the exactly resolved `QuestionType` and reusable-question `ResponseTypeName` as a complete pair. The procedure accepts the pair as reference context, rejects a partial pair, and still excludes embedded-question definition fields.
- Bind every emitted reusable or direct `QuestionType`/`ResponseTypeName` pair to `validation_evidence.response_type_pairs` using an immutable evidence ID listed in `validation_evidence.evidence_ids`. Never populate that catalog from an FSM `ResponseTypeCode` column.
- A Questionnaire `mode: direct` Question must use `QuestionType=TEXT`, `1CHOICE`, `MULTCHOICE`, or `NONE` and its exact resolved target `ResponseTypeName`. It also requires `QuestionText`, `Status`, `PrivacyFlag`, `CategoryName`, hierarchy keys, positive sequence, and compatible template capability when a template is supplied. Direct `1CHOICE` and `MULTCHOICE` Questions require complete target-valid Answer rows; direct `TEXT` and `NONE` Questions prohibit Answer rows. Normalize it with the direct-question procedure, then render it through the executable serializer in exact live template column order. `QstnrQstnResponseTypeName` remains blank unless the target contract explicitly requires an override.
- A questionnaire translation must resolve its ordinary questionnaire parent and include the target-required identity, including `TemplateFlag=N` when registered.
- Consumer linkage remains a separate downstream task and never becomes a child row in `Questionnaire.dat`.

## FSM evidence boundary

`csv_export_import_supported_flag: Y` does not change the selected `dataloader_import_mode: HDL`.

An Oracle-generated FSM export may be used to:

- establish a read-only source baseline;
- inspect supported FSM graph relationships, source codes, and natural keys;
- reconcile pre-load and post-load state;
- identify fidelity gaps that require verification.

It must not be used to:

- upload the FSM ZIP as this skill's mutation artifact;
- prove a target HDL display name, operation, or mandatory attribute;
- copy source-pod numeric IDs;
- convert an arbitrary CSV into an FSM package;
- infer deletion from an omitted row.

## Immutable approval and upload boundary

The task builder stops after producing local, validated, hashed DAT artifacts and the immutable handoff. Generation approval does not authorize a Fusion write.

When the user separately requests a live load:

1. Give the unchanged artifacts and task context to `core.data-loader`.
2. Let that workflow revalidate the exact live metadata, sources, DAT members, ZIP bytes, and task rules.
3. Present the exact immutable upload artifact and SHA-256.
4. Stop before the first POST and require the later standalone approval required by `core.data-loader`.
5. Upload and initiate only through `core.data-loader` after it verifies the unchanged approved hash.

Any change to business values, metadata, mapping, DAT bytes, member order, ZIP bytes, target environment, operation, or task context invalidates the preview and approval. Never retry or substitute a corrected payload without a new validation and approval cycle.
