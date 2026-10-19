# Profile Rating Model Requirements Workbook

The bundled helper generates a deterministic `.xlsx` intake workbook and uses
the same normalized contract for JSON and workbook validation.

## Template-Only Generation

Use `generate-template` when the user asks for guidance, a questionnaire, or a
fillable workbook before complete requirements exist. This route requires only
an output path and performs no Fusion read or write:

```bash
python3 scripts/profile_rating_model_requirements.py generate-template \
  --output <writable-directory>/profile-rating-model-intake-template.xlsx
```

Add one `--consumer <supported-consumer>` for each consumer already resolved
from the user's business context. Add `--level-count <n>` only when the user
wants a number of scale rows other than the default five.

The template includes Instructions, Field Guidance, fillable Model
Requirements and Rating Scale sheets, Translations, Consumer Handoffs, and the
applicable conditional sheets. With no resolved consumer, it is a universal
template and includes every conditional sheet explicitly marked optional. Blank
conditional sheets do not assert requirements and are ignored during later
normalization. Field Guidance contains synthetic examples only and is not part
of the normalized implementation contract.

Template generation does not require or prove an initialized project,
environment identity, Fusion access, quarterly release, role, existing-model
lookup, implementation readiness, or approval. Run normal workbook validation
only after the user returns the completed file.

## Sheets

| Sheet | When included | Purpose |
|---|---|---|
| Instructions | Always | Version, supported consumers, completion and resubmission rules |
| Model Requirements | Always | Request, source, identity, purpose, population, dates, languages and selected consumers |
| Rating Scale | Always | Ordered levels, descriptions and numeric values |
| Review Points and Ranges | Calculated Performance or explicit review-point requirement | Review point and contiguous range per level |
| Rating Categories | Talent Review category requirement | Category code/name and level membership |
| Rating Distributions | Compensation direct distribution requirement or Performance target-distribution handoff | Clearly separated model-owned Compensation and downstream-owned Performance values |
| Translations | Always | Header and level translations for every non-base language |
| Consumer Handoffs | Always | One structured downstream handoff per selected consumer |

For a populated tailored workbook, do not silently add a conditional sheet; the
generator derives sheets only from selected consumers and explicit flags. The
universal template-only mode is the deliberate exception and includes all
conditional sheets for completion guidance. In either mode, do not treat blank
conditional sheets as requirements.

When a conditional sheet exists, it is authoritative for its focused values:
`Review Points and Ranges` owns review points and ranges, `Rating Categories`
owns category assignments, and `Rating Distributions` owns Compensation
minimum/maximum/threshold values and Performance downstream target percentages.
The helper reads these sheets back into the normalized contract. Unknown or
duplicate level codes, unsupported distribution owners, and conflicting
Compensation thresholds are blocking workbook issues rather than silently
ignored rows.

## Validation Result

Each issue contains `source`, `worksheet`, `row`, `field`, `cell`, `issue`,
`business_impact`, `recommended_correction`, and `severity`. Blocking issues
prevent lookup, blueprint finalization, preview, and creation. Validation applies
the bundled JSON schema as well as consumer-specific business rules; schema
version, source type, dates, languages, level shapes, and handoff fields cannot
be bypassed by JSON or workbook normalization.

## Existing Customer Workbooks

Run `inspect-mapping` first. Exact normalized sheet/header matches may be
proposed. Similar or ambiguous headers remain `review_required`; the helper
never silently maps them. Record every confirmed mapping and preserve the
source workbook version. Normalize only after all required mappings are
confirmed.

## Resubmission

Keep the original source, mapping review, validation result and normalized
requirements. A material correction creates a new artifact version. Rerun all
validation and exact-model comparison; an earlier creation approval does not
carry forward.
