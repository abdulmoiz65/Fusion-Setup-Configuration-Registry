# Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| verify_time_slots_api_access | Before direct execution preflight | none | GET /api/field-service/configuration/v1/timeSlots/ | HTTP status | Accept a successful implementation collection response | API access result | Stop and report the authorization or transport failure |
| list_time_slots | User asks to list or search time slots | limit, offset, label, name | GET /rest/ofscMetadata/v1/timeSlots (public discovery) or GET /api/field-service/configuration/v1/timeSlots/ (implementation search) | items, totalResults, hasMore, limit, offset | Retrieve the collection; filter returned items by exact label or exact name only when supplied | label, name, active, isAllDay, timeStart, timeEnd, links | Return no-match or multiple-match result and request a more specific label or name |
| find_time_slot_by_label | User asks to read, update, enable, disable, or confirm create absence | label as itemId | GET /api/field-service/configuration/v1/timeSlots/{itemId} | label, name, active, isAllDay, timeStart, timeEnd | Exact item path lookup by label | Current record or not-found state | Return not found for update, enable, or disable; return conflict for create when found |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Collection has no items | Return an empty collection; the public endpoint may omit items when empty. |
| Collection has more pages | Follow the next offset only when a complete search is required. |
| Item lookup returns 404 for create | Treat the label as available, subject to the remaining validation and design gates. |
| Item lookup returns 404 for update, enable, or disable | Stop and report that the requested time slot is not found. |
| Item lookup returns extra fields | Preserve them as read-only context; do not write association APIs. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TS.LOOKUP | step | 4 | reference_lookup | ready->TS.DESIGN_BUSINESS_PURPOSE;not_found->TS.DESIGN_BLOCKED;error->TS.DESIGN_BLOCKED | TS.DEFAULTS | stop | Time Slots input needs API access, collection lookup, item lookup, or create-absence confirmation. |
