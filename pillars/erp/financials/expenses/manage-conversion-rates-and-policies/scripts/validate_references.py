"""Evaluate task-specific, core-fetched reference evidence without network IO.

The caller obtains fresh complete GET results through the selected core client.
This helper checks supplied provenance; it cannot establish that a GET occurred.
It returns evidence only, never a Task Hook approval or loader envelope.
"""
from datetime import date, datetime, timezone
import re


class ReferenceError(ValueError):
    pass


def _batch(evidence, name, environment, digest, now):
    value = evidence.get(name)
    if not isinstance(value, dict):
        raise ReferenceError('reference_unverified: missing evidence batch')
    status = value.get('http_status')
    if status in (401, 403):
        raise ReferenceError('auth_authz: core reference lookup failed')
    if status != 200:
        raise ReferenceError('transport_environment: reference lookup failed')
    if (value.get('environment') != environment or value.get('candidateSha256') != digest
            or value.get('complete') is not True):
        raise ReferenceError('reference_unverified: target, candidate or pagination mismatch')
    try:
        captured = datetime.fromisoformat(value['captured_at'].replace('Z', '+00:00'))
        if captured.tzinfo is None or not -300 <= (now - captured).total_seconds() <= 86400:
            raise ValueError('stale or unzoned evidence')
    except (KeyError, TypeError, AttributeError, ValueError) as error:
        raise ReferenceError('reference_unverified: invalid or stale capture time') from error
    items = value.get('items')
    if not isinstance(items, list) or not all(isinstance(item, dict) for item in items):
        raise ReferenceError('reference_unverified: malformed reference rows')
    return items


def _exact(items, field, wanted, identity=None):
    if any(field not in item or item[field] is None for item in items):
        raise ReferenceError('reference_unverified: response omitted a matching attribute')
    matches = [item for item in items if item.get(field) == wanted]
    if not matches:
        raise ReferenceError('reference_not_found: no exact destination match')
    if len(matches) != 1:
        raise ReferenceError('reference_ambiguous: multiple exact destination matches')
    if identity and (isinstance(matches[0].get(identity), bool)
                     or not str(matches[0].get(identity) or '').strip()):
        raise ReferenceError('reference_unverified: missing reference identity')
    return matches[0]


def validate_references(parents, children, evidence, environment, candidate_sha256, *, now=None):
    """Validate merged CSV row dicts against core-fetched, digest-bound batches.

    Batches business_units/conversion_types/currencies contain items, complete,
    http_status, environment, candidateSha256 and timezone-aware captured_at.
    For currency item GETs the caller combines verified item responses into a
    batch; a 404 is a reference_not_found outcome before invoking this helper.
    """
    now = now or datetime.now(timezone.utc)
    if (not isinstance(environment, str) or not environment.startswith('https://')
            or not isinstance(candidate_sha256, str) or not re.fullmatch('[0-9a-f]{64}', candidate_sha256)
            or not isinstance(evidence, dict) or now.tzinfo is None
            or not isinstance(parents, list) or not parents
            or not isinstance(children, list)):
        raise ReferenceError('reference_unverified: invalid target, digest or candidate rows')
    bus = _batch(evidence, 'business_units', environment, candidate_sha256, now)
    types = _batch(evidence, 'conversion_types', environment, candidate_sha256, now)
    currencies = _batch(evidence, 'currencies', environment, candidate_sha256, now) if children else []
    verified = []
    parent_names = set()
    for row in parents:
        if not isinstance(row, dict) or not row.get('BuName') or not row.get('UserConversionType'):
            raise ReferenceError('reference_unverified: missing parent reference input')
        name = row['BuName']
        if name in parent_names:
            raise ReferenceError('reference_ambiguous: duplicate candidate parent')
        parent_names.add(name)
        bu = _exact(bus, 'BusinessUnitName', name, 'BusinessUnitId')
        if bu.get('ActiveFlag') is not True:
            code = 'reference_inactive' if bu.get('ActiveFlag') is False else 'reference_unverified'
            raise ReferenceError(code + ': business unit is not verified active')
        conversion = _exact(types, 'UserConversionType', row['UserConversionType'], 'ConversionTypeId')
        verified.append({'BuName': name, 'BusinessUnitId': bu['BusinessUnitId'],
                         'UserConversionType': row['UserConversionType'],
                         'ConversionTypeId': conversion['ConversionTypeId']})
    child_keys = set()
    for row in children:
        if not isinstance(row, dict):
            raise ReferenceError('reference_unverified: malformed child')
        key = (row.get('EXM_EXCHANGE_RATE_OPTION.BuName'), row.get('CurrencyCode'))
        if key[0] not in parent_names or not key[1] or key in child_keys:
            raise ReferenceError('reference_unverified: missing parent, currency or duplicate child')
        child_keys.add(key)
        currency = _exact(currencies, 'CurrencyCode', key[1])
        for flag in ('CurrencyFlag', 'EnabledFlag'):
            if currency.get(flag) is not True:
                code = 'reference_inactive' if currency.get(flag) is False else 'reference_unverified'
                raise ReferenceError(code + ': currency is not verified enabled')
        for field, start in (('StartDateActive', True), ('EndDateActive', False)):
            if field not in currency:
                raise ReferenceError('reference_unverified: missing active-date attribute')
            if currency[field] is None:
                continue
            try:
                bound = date.fromisoformat(currency[field])
            except (TypeError, ValueError) as error:
                raise ReferenceError('reference_unverified: malformed active date') from error
            if (start and now.date() < bound) or (not start and now.date() > bound):
                raise ReferenceError('reference_inactive: currency outside active dates')
    return {'status': 'ready', 'environment': environment, 'candidateSha256': candidate_sha256,
            'parents': verified, 'child_count': len(child_keys), 'approval_granted': False}
