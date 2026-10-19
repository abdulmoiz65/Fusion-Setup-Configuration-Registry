"""Resolve an exact BU from complete, workflow-fetched finBusinessUnitsLOV pages.

Offline evaluation only. Authentication and HTTP belong to the core REST client.
"""
import argparse
import json
import re
import sys


def resolve(name, pages):
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Business-unit name is required")
    if not isinstance(pages, list) or not pages:
        raise ValueError("Complete lookup pages are required")
    matches = []
    offset = 0
    for index, page in enumerate(pages):
        if not isinstance(page, dict) or not isinstance(page.get("items"), list):
            raise ValueError("Malformed lookup page")
        items = page["items"]
        if type(page.get("hasMore")) is not bool:
            raise ValueError("Missing pagination completeness flag")
        if type(page.get("offset")) is not int or page["offset"] != offset:
            raise ValueError("Missing or noncontiguous pagination")
        if page["hasMore"] != (index < len(pages) - 1):
            raise ValueError("Incomplete or excess lookup pages")
        if page["hasMore"] and not items:
            raise ValueError("Empty nonterminal page")
        offset += len(items)
        for item in items:
            if not isinstance(item, dict) or not isinstance(item.get("BusinessUnitName"), str):
                raise ValueError("Malformed business-unit record")
            if item["BusinessUnitName"] == name.strip():
                matches.append(item)
    if len(matches) != 1:
        raise ValueError("Business-unit lookup requires exactly one exact-name match; found " + str(len(matches)))
    item = matches[0]
    identity = item.get("BusinessUnitId")
    # Fusion REST Framework 9 can serialize int64 identifiers as decimal text.
    if isinstance(identity, str) and re.fullmatch(r"[1-9][0-9]*", identity):
        identity = int(identity)
    if type(identity) is not int or not 0 < identity <= 9223372036854775807:
        raise ValueError("Missing or invalid business-unit identity")
    if item.get("ActiveFlag") is not True:
        raise ValueError("Business unit is inactive or active status is unknown")
    return {"BusinessUnitId": identity, "BuName": item["BusinessUnitName"], "ActiveFlag": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="JSON with businessUnitName and complete pages; protect customer data")
    args = parser.parse_args()
    try:
        with open(args.input, encoding="utf-8") as stream:
            data = json.load(stream)
        result = resolve(data.get("businessUnitName"), data.get("pages"))
    except (OSError, ValueError, TypeError, AttributeError):
        print(json.dumps({"status": "blocked", "failure_class": "input_validation", "message": "Lookup evidence failed validation; check exact name, uniqueness, active status and complete contiguous pages."}))
        return 1
    print(json.dumps({"status": "resolved", "result": result}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
