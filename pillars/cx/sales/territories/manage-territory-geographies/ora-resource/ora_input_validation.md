# Input Validation

Validate the user-supplied rows and the exact normalized CSV before any
staged-file or Fusion side effect. Do not infer row kind solely from `ZoneCode`
or compare Territory Geography import values directly with the `geoZones`
resource.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Source | input_csv or records_json | Stop before artifact creation | Provide exactly one CSV file or JSON records source | Every run | |
| Row identity | GeographyOrZoneName, LanguageCode, SourceId, GeographyOrZoneType | Reject the affected file | Supply every required value as text | Every row | |
| Hierarchy | ParentSourceId | Reject the affected file | Place the parent earlier in the file; leave blank only for the one root | Every non-root row | |
| Execution context | project_id, fusion_environment_context, task_context | Stop before preview | Supply the project, exact target environment, and native Data Loader task context | Import execution is requested | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Headers differ from the eleven-column base contract, optionally followed by GeoParentName5, or their order differs | Blocked | Correct the source headers; do not map them heuristically | |
| SourceId or ParentSourceId is not an unsigned Oracle Long value | Blocked | Supply numeric identifiers without signs, decimals, or letters | |
| SourceId repeats, references itself, or ParentSourceId does not identify an earlier row | Blocked | Correct the submitted hierarchy | |
| Exactly one first-row root is present | Satisfied | Continue with local validation and checksum generation | |
| A row populates ZoneCode together with CountryName or GeoParentName fields | Satisfied | Preserve the values; Oracle's published Territory Geography example uses this combination | |
| Numeric postal code contains fewer than five characters | Warning | Preserve it exactly and ask the user to confirm whether leading zeroes were lost upstream | |
| Local validation and checksum generation succeed | Ready | Run core Data Loader CX preflight, then Task Hook for its final immutable archive | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| CSV header contract | Require GeographyOrZoneName, LanguageCode, SourceId, ParentSourceId, GeographyOrZoneType, ZoneCode, CountryName, GeoParentName1, GeoParentName2, GeoParentName3, GeoParentName4 in that order; accept optional GeoParentName5 only as the final column | CSV input | |
| Unknown JSON property | Reject the record; never copy an unknown property into the CSV | JSON records input | |
| Identifier type and preservation | Require SourceId and populated ParentSourceId to be unsigned integers within the Oracle Long range; preserve their CSV text representation plus geography names and postal codes | Every row | |
| Whitespace and control characters | Reject surrounding whitespace, embedded NUL, carriage return, or line feed rather than silently changing the value | Every populated value | |
| Root count | Require exactly one root and require it to be the first row | Every file | |
| Parent ordering | Require every non-root ParentSourceId to match an earlier SourceId in the same file | Every non-root row | |
| Zone and geography-path coexistence | Preserve ZoneCode, CountryName, and GeoParentName1 through GeoParentName5 combinations without inferring an invalid row kind | Every row | |

Validate the CSV member from the final core archive against these same rules.
Local source preparation is not approval. Require its contents to match the
prepared source, and bind Task Hook to the final archive digest.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TG.INPUT | step | 1 | validate_input | valid->TG.CSV;invalid->TG.ERROR | none | stop | Validate task source identity against the final core CX archive. |
| TG.CSV | step | 2 | validate_input | valid->TG.DEPENDENCIES;invalid->TG.ERROR | TG.INPUT | stop | Validate final archive CSV headers, hierarchy and preserved values. |
