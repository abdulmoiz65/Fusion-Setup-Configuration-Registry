"""Validate Benefits-only business intent. No network, payloads, or execution."""
import argparse
import json
import sys


ALLOWED_ALERT_CODES = (
    "BEN_BILL_CHARGES",
    "BEN_BILL_PAYMENT",
    "BEN_PENDING_ACTIONS_NOTIFICATION",
    "BEN_SELF_REPORTED_LIFE_EVENT_APPROVED",
    "BEN_COURT_ORDER_DEPENDENT_CREATED",
    "BEN_REPORT_LIFE_EVENT",
    "BEN_COURT_ORDER_DEPENDENT_ENDDATED",
    "BEN_DOCUMENT_APPROVAL",
    "BEN_OPEN_NOTIFICATION",
    "BEN_OPEN_REMINDER",
    "BEN_SELF_REPORTED_LIFE_EVENT_REJECTED",
    "BEN_SELF_REPORTED_LIFE_EVENT_INFO_REQD",
    "BEN_SELF_REPORTED_LIFE_EVENT_SUBMIT",
    "BEN_ELECTIONS_SUMMARY",
)


def validate_intent(value):
    if not isinstance(value, dict) or set(value) != {"operation", "alert_codes"}:
        raise ValueError("Supply only operation and alert_codes.")
    operation = value["operation"]
    if not isinstance(operation, str) or operation not in ("enable", "disable"):
        raise ValueError("operation must be enable or disable.")
    codes = value["alert_codes"]
    if not isinstance(codes, list) or not codes:
        raise ValueError("alert_codes must be a nonempty list.")
    for index, code in enumerate(codes, 1):
        if not isinstance(code, str) or code not in ALLOWED_ALERT_CODES:
            raise ValueError("alert_codes entry %d is not an exact allowed Benefits code." % index)
    if len(set(codes)) != len(codes):
        raise ValueError("alert_codes contains duplicates.")
    return {
        "consumer_skill_id": "hcm.benefits-configuration.benefits-alerts",
        "status": "validated_business_intent",
        "intents": [
            {"alert_code": code,
             "requested_intent": "update" if operation == "enable" else "disable",
             "enabled": operation == "enable"}
            for code in codes
        ],
    }


def unique_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError("Duplicate JSON property.")
        value[key] = item
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-stdin", required=True, action="store_true")
    parser.parse_args()
    try:
        result = validate_intent(json.load(sys.stdin, object_pairs_hook=unique_object))
    except (ValueError, UnicodeError):
        # Do not echo arbitrary source values, which may contain secrets.
        print(json.dumps({"status": "validation_failed", "failure_class": "input_validation",
                          "message": "Invalid JSON or scope. Supply enable/disable and unique exact allowlisted alert_codes only."}))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
