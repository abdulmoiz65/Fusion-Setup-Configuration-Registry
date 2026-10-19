# Conditional references and complete-set development validation

These local checks address GROW-8692, GROW-8703 and GROW-8708 without changing
the currently verified execution shapes. Enter through the parent skill and
use the selected project. Python 3.10+ is required; examples use Python 3.11.

## Proficiency references

The intake normalizer reports a missing model on the exact local parent row
and rejects two descriptions for the same parent/level, even with different
local keys. It preserves supplied values and omitted levels without copying
shared model definitions. External parents need an exact item-to-model binding.

After normalization, the local helper may compare a sanitized snapshot already
obtained through the owning Rating Model/item lookup workflow:

```text
python3.11 scripts/validate_proficiency_reference_evidence.py intake.json references.json --target-environment-alias <reviewed-target-alias> --as-of <current-operation-rfc3339>
```

Run relative to this skill folder, or prefix the script with its repository
path. Replace both placeholders before running; never reuse a historical as-of
timestamp for a current operation. Historical timestamps are only for explicitly
labeled offline replay tests and do not establish current evidence validity.
The JSON evidence contract requires exactly:

| Field | Meaning |
|---|---|
| schema_version | 1.0 |
| target_environment_alias | Same safe alias as the reviewed request |
| source_fingerprint | SHA-256 of the normalized intake's original source |
| intake_fingerprint | Canonical SHA-256 of the complete normalized intake JSON; binds every value and source row |
| captured_at / valid_through | Explicit timezone timestamps covering as-of |
| complete | true only for complete coverage of the requested references |
| evidence_references | Nonempty sanitized references to owning-workflow evidence |
| models | Objects with exact code and nonempty unique string level_codes |
| item_model_bindings | Objects with item_reference, model_code and evidence_reference |

For a supplied parent, item_reference is its request-local key and its supplied
rating_model_code must match. For an externally referenced parent, use the exact
parent reference. Each binding's evidence_reference must be in the declared
source-reference list. The binding must establish applicability to that item;
a model inventory, user assertion or similar name is insufficient.

Do not fabricate this snapshot or treat the helper as its source authority. It
does not fetch evidence, verify remote privileges or establish a missing
applicability lookup route. When that owning route is missing, report the gap.
Synthetic fixtures prove comparison logic only.

Output references_verified means only that these supplied reference assertions
are consistent. field_mapping_status remains blocked_provider_mapping_unproven;
no conditional description is promoted to supported capture or persistence.
Missing/ambiguous models, missing levels and item-model conflicts have distinct
row results. Invalid, sensitive, stale or differently bound input is rejected.

## Complete blocked preview

```text
python3.11 scripts/build_profile_content_library_preview.py preview contract.json --target-environment-alias TEST_TARGET --review-blocked
```

The usual complete canonical contract, confirmed mappings, validation and exact
checks are still required. For unavailable provider shapes, the result preserves
all 14 groups, source, mappings, dependencies and exact results with a material
fingerprint. It has lifecycle_status preview_blocked, requested_approval null,
creation_authorized false and explicit provider blockers; CLI exit is 2.
Approval and submission reject it. For supported shapes, output is unchanged.
Use the existing preliminary review contract for unresolved mappings/dependencies
and exact-report for duplicates; this flag does not waive those validations.

## New catalog with supplied children: validation only

Add --validate-new-catalog-set to the existing package helper command and retain
all of its normal inputs, fingerprints, same-target fresh complete export,
baseline and safe unused output paths. It checks exactly one new catalog and
one or more supplied children against the existing portable CSV shape. It also
checks every child's parent aliases, context, supplier, dates, grouping, generated
fields, global code collisions and same-catalog names, plus duplicates within
the supplied children. Rating descriptions and advanced fields remain rejected.

On a valid candidate it returns candidate_validation_only with counts and bound
fingerprints, but writes neither ZIP nor readiness file. No Task Hook handoff
or live call occurs. The declared output paths are reserved/validated only.
The default builder still enforces the verified existing-parent/single-child
shape. This option is not a bypass or an import preparation route.

Source basis: ItemCatalogMigrationAMImpl.importData imports the base root graph;
ContentItemVOImpl.resolveAttributes obtains ContentValueSetId from the parent
logical row in its second phase. This supports investigating the complete-set
shape, not promoting runtime capability. Root and translation commit phases
must not be represented as all-or-nothing or automatically rolled back.

The separately implemented [new catalog set contract](new-catalog-set-contract.md)
has its own complete preview, binding and controlled package-preparation modes.
This original candidate mode remains non-executable. Profiles/Core contract
review and runtime certification remain separate gates; neither is inferred
from the existing one-child canaries or successful local tests.
