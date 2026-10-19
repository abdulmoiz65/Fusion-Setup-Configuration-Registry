# Manage Cost Factors Defaulting Rules

Sources: User-provided Manage Cost Factors business-rule content from Confluence page 14988929751; user-authorized inspection of the Redwood Manage Cost Factors page on 2026-09-01.

## Redwood UI Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Pricing Basis | Per unit | A new Cost Factors inline row is created and no Pricing Basis value has been chosen | No | |
| Status | Active | A new Cost Factors inline row is created and no Status value has been chosen | No | |
| Initial Status filter | Active | The Cost Factors page is first loaded | Yes | |
| Search text | blank | The Cost Factors page is first loaded | Yes | |

These defaults apply only to the interactive Redwood page. They are not source
defaults for a Data Loader workbook.

## Data Loader Defaulting

`core.data-loader` does not inject these Redwood UI defaults into a source
workbook. Preserve the values and foreign-key columns generated from live
metadata, and let the operation-specific Data Loader validator determine
whether an omitted attribute is valid for the submitted archive.
