"""Pure comparison of API-visible receipt values; no ownership/effect certification."""
from datetime import date

import customers_package as package
from customer_api_hierarchy import collection, identifier, MISSING


def review_before(row, pages, *, response_language):
    """Surface existing periods before approval; never certify absence or replay.

    Customers derives the receipt start date from ACCOUNT_ESTABLISHED_DATE and
    supplies no receipt end date. Date-only visible overlap is a stop for review,
    not a reimplementation of Oracle DATE/MONTHS_BETWEEN or the loader's T1/T2/T3.
    Ownership, source-reference dates and actual BILL_TO binding remain separate.
    """
    observed = review(row, pages, response_language=response_language)
    records, complete = collection(pages)
    conflicts, unknown = [], []
    if not row['PAYMENT_METHOD_NAME']:
        status = 'NO_RECEIPT_INPUT'
    elif not row['PARTY_SITE_NUMBER'] or row['SITE_USE_CODE'] != 'BILL_TO':
        status = 'RECEIPT_SCOPE_REVIEW_REQUIRED'
    else:
        try:
            start = date.fromisoformat((row['ACCOUNT_ESTABLISHED_DATE'] or '1900/01/01').replace('/', '-'))
        except (ValueError, TypeError) as exc:
            raise package.InvalidInput('API_RECEIPT_INPUT_DATE') from exc
        for record in records:
            if record.get('ReceiptMethodName', MISSING) is MISSING or record.get('CustomerSiteNumber', MISSING) is MISSING:
                unknown.append(identifier(record['CustomerReceiptMethodId']))
                continue
            if (record['ReceiptMethodName'], record['CustomerSiteNumber']) != (
                    row['PAYMENT_METHOD_NAME'], row['PARTY_SITE_NUMBER']):
                continue
            end = record.get('EndDate', MISSING)
            began = record.get('StartDate', MISSING)
            if end is MISSING or began is MISSING or began is None:
                unknown.append(identifier(record['CustomerReceiptMethodId']))
            elif end is not None and date.fromisoformat(end) < date.fromisoformat(began):
                unknown.append(identifier(record['CustomerReceiptMethodId']))
            elif end is None or date.fromisoformat(end) >= start:
                conflicts.append(identifier(record['CustomerReceiptMethodId']))
        status = ('VISIBLE_RECEIPT_PERIOD_CONFLICT' if conflicts else
                  'RECEIPT_PERIOD_EVIDENCE_INCOMPLETE' if unknown or not complete else
                  'NO_VISIBLE_RECEIPT_PERIOD_CONFLICT_NOT_ELIGIBILITY')
    return {'schema_version': 'ar-customer-api-receipt-before-v1', 'status': status,
            'conflicting_assignment_ids': sorted(conflicts), 'unknown_assignment_ids': sorted(unknown),
            'pages_complete': complete, 'observed_assignment_count': observed['observed_assignment_count'],
            'execution_authorized': False, 'replay_safe': False, 'global_absence_proven': False,
            'loader_error_predicted': False,
            'limits': ['Date-only visible account/site/method periods require independent ownership review.',
                      'No account-level primary, receipt-class eligibility or unrestricted history certification.',
                      'A visible conflict must be resolved before approval; it is not loader-validation uncertainty.']}


def review(row, pages, *, response_language):
    """Compare all returned account assignments without hiding other sites/periods.

    Caller binds the candidate and central GET captures, uses the exact account
    finder without method/date/primary filters, and separately verifies ownership.
    English Yes/No is an API representation, never a replacement CSV value.
    """
    require = package.require
    require(isinstance(row, dict) and set(package.columns()) <= set(row), 'API_RECEIPT_ROW_REQUIRED')
    require(response_language == 'en', 'API_RECEIPT_LANGUAGE_UNQUALIFIED')
    account = row['ACCOUNT_NUMBER']
    require(isinstance(account, str) and bool(account), 'API_RECEIPT_ACCOUNT_NUMBER_REQUIRED')
    records, complete = collection(pages)
    ids = set()
    for record in records:
        key = identifier(record.get('CustomerReceiptMethodId'))
        require(key is not MISSING and key not in ids, 'API_RECEIPT_DUPLICATE_OR_INVALID_ID')
        ids.add(key)
        require(record.get('CustomerAccountNumber') == account, 'API_RECEIPT_ACCOUNT_SCOPE')
        for field in ('StartDate', 'EndDate'):
            if field not in record or record[field] is None:
                continue
            try:
                value = record[field]
                require(isinstance(value, str) and date.fromisoformat(value).isoformat() == value,
                        'API_RECEIPT_DATE_FORMAT')
            except (TypeError, ValueError) as exc:
                raise package.InvalidInput('API_RECEIPT_DATE_FORMAT') from exc
    method = row['PAYMENT_METHOD_NAME']
    matches = [r for r in records if r.get('ReceiptMethodName') == method
               and r.get('CustomerSiteNumber') == row['PARTY_SITE_NUMBER']]
    findings = []
    status = 'RECEIPT_API_REVIEW_REQUIRED'
    if not method:
        status = 'NO_RECEIPT_INPUT_EFFECTS_UNVERIFIED'
    elif not row['PARTY_SITE_NUMBER']:
        status = 'RECEIPT_SITE_NUMBER_NOT_SUPPLIED'
    elif len(matches) != 1:
        status = 'RECEIPT_API_NOT_FOUND' if not matches else 'RECEIPT_API_HISTORY_OR_DUPLICATE_REVIEW'
    else:
        expected = {'Primary': {'Y': 'Yes', 'N': 'No'}.get(row['PAYMENT_METHOD_PRIMARY_FLAG'] or 'N'),
                    'StartDate': (row['ACCOUNT_ESTABLISHED_DATE'] or '1900/01/01').replace('/', '-'),
                    'EndDate': None}
        require(expected['Primary'] is not None, 'API_RECEIPT_INPUT_FLAG')
        for field, value in expected.items():
            actual = matches[0].get(field, MISSING)
            findings.append({'field': field, 'status': 'NOT_RETURNED' if actual is MISSING else
                             'MATCH' if actual == value else 'MISMATCH'})
        if complete and all(f['status'] == 'MATCH' for f in findings):
            status = 'SELECTED_RECEIPT_API_VALUES_MATCH'
    return {'schema_version': 'ar-customer-api-receipt-review-v1', 'status': status,
            'findings': findings, 'pages_complete': complete, 'observed_assignment_count': len(records),
            'matching_assignment_count': len(matches), 'other_assignment_count': len(records)-len(matches),
            'observed_assignment_ids': sorted(ids), 'execution_authorized': False,
            'persisted_reconciliation_complete': False, 'assignment_delta_verified': False,
            'limits': ['Visible account/site numbers and date-only API values, not raw parent IDs or Oracle DATE seconds.',
                      'Caller must retain exact finder scope and English response context; no SQL input is needed.',
                      'No before/after change proof, receipt-class eligibility, batch marker or complete ownership certification.',
                      'Unrelated assignments remain counted; matching after-state does not authorize replay or update.']}
