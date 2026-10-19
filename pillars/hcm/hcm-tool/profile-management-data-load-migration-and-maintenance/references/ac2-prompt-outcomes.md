# GROW-8164 AC2 prompt outcomes

The AC2 resolver accepts natural-language intake requests. It is local only:
every outcome reports `execution: not-authorized`, `fusion_activity: none`, and
`load_status: no load initiated`.

| User intent or example phrasing | Mode | Required outcome |
| --- | --- | --- |
| "I want to enter a synthetic model profile directly." | Direct entry | Return a prefilled form containing only stated values, retain the Talent Profile root, list missing target, operation, root, identifier, and target-check values as applicable. |
| "Create a profile file for model profile." | Direct entry | Return the form and ask for missing data; do not interpret "create" as a load approval. |
| "Give me an Excel/spreadsheet/workbook template." | Template and guidance | Attach the default XLSX intake workbook and explain the Request and Records sheets. |
| "Export a CSV intake template." | CSV export | Return the documented CSV columns and local-interchange warning. |
| "Validate/import/map this CSV." | CSV import and mapping review | Require an attached CSV, or parse it locally, preserve optional source evidence, show mappings and uncertainties, and report validation errors. |
| "Please proceed with profile work." | Clarification required | Ask the user to select direct entry, spreadsheet, CSV export, or CSV import. |
| A request includes Content Item, relationships, extra information, flexfields, or attachments | Any mode | Capture only as intake when supplied, identify the dependency or provider-blocked route, and never invent fields or enable HDL generation. |

## Default spreadsheet guidance

- Complete target environment, requested operation, root record type, and exact target-check status on **Request**.
- Put every parent and child record on **Records**. Repeat rows for translations and relationships, with the parent identifier retained.
- Supply Language only for translation records; validate it against the target installed-language list before any artifact work.
- Leave optional flexfield and attachment fields blank until their owner has provided exact target evidence. The workbook is not an HDL payload and never approves a load.
