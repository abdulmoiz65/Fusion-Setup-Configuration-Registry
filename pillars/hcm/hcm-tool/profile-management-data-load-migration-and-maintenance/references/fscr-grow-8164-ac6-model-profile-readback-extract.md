# FSCR GROW-8164 AC6 model-profile readback extract

Create this definition only in the approved non-production tenancy:
`FSCR_GROW_8164_AC6_MODEL_PROFILE_READBACK`.

## Contract

- The extract is read-only and accepts one mandatory exact-match `ProfileCode` parameter.
- Its Talent Profile user entity must be validated before publication. It must expose every populated `TalentProfile` DAT field in the approved AC6 artifact. A field that is unavailable is an AC6 blocker, not an opportunity to omit it.
- Use a single CSV delivery with a stable, unique header. Header names must exactly equal their DAT field names; no aliases are permitted.
- Emit exactly one row for the supplied `ProfileCode`. Do not include child records, person-profile data, or unrelated model profiles.
- Add at least these conventional model-profile columns when populated by the artifact: `ProfileCode`, `ProfileTypeCode`, `ProfileTypeId`, `ProfileStatusCode`, `ProfileUsageCode`, `Description`, and `Summary`.
- The release owner records the definition version, parameter value, extract run ID, output SHA-256, and approved DAT SHA-256. Output retention must be redacted and limited to AC6 evidence.

## Approval gates

1. Obtain approval before creating or publishing the extract definition.
2. Confirm the synthetic `ProfileCode` is absent and create the immutable HDL archive and execution preview.
3. Obtain fresh, explicit approval immediately before submitting the HCM Data Loader request.
4. After terminal success, run:

   ```text
   python scripts/profile_root_extract_readback_comparison.py --approved-dat path/to/TalentProfile.dat --extract-csv path/to/FSCR_GROW_8164_AC6_MODEL_PROFILE_READBACK.csv
   ```

Only a `verified` result closes AC6. Do not use REST, UI inspection, or direct database access as a substitute for a missing extract field.
