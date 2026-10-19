"""Review full party-scoped supporting inventories; changes are observations, not approval."""
from datetime import datetime

import customers_package as package
import customer_identity_review as identity
import customer_ownership_review as ownership

require = package.require
FIELDS = {
    'organization_profiles': ('party_id', 'organization_profile_id', 'effective_start_date',
        'effective_end_date', 'effective_sequence', 'effective_latest_change',
        'duns_number_c', 'jgzz_fiscal_code', 'gsa_indicator_flag'),
    'party_site_uses': ('party_id', 'party_site_id', 'party_site_use_id', 'site_use_type',
        'primary_per_type', 'status', 'begin_date', 'end_date'),
}
KEYS = {'organization_profiles': ('organization_profile_id', 'effective_start_date', 'effective_sequence'),
        'party_site_uses': ('party_site_use_id',)}
PARTY_VALUES = {'DUNS_NUMBER': 'duns_number_c', 'TAXPAYER_ID_NUM': 'jgzz_fiscal_code',
                'GSA_INDICATOR_FLAG': 'gsa_indicator_flag'}


def snapshot(candidate, operation, environment, identities, owners, evidence):
    reviewed = ownership.analyze(candidate, operation, environment, identities, owners)
    require(isinstance(evidence, dict) and set(evidence) == {
        'schema_version', 'candidate_sha256', 'environment_url', 'operation_intent',
        'ownership_evidence_sha256', 'phase', 'captured_at', 'database_as_of',
        'evidence_reference', 'queries'}, 'SUPPORTING_SCHEMA')
    require(evidence['schema_version'] == 'ar-customer-supporting-evidence-v1', 'SUPPORTING_VERSION')
    require(evidence['candidate_sha256'] == reviewed['candidate_sha256']
        and evidence['environment_url'] == environment and evidence['operation_intent'] == operation
        and evidence['ownership_evidence_sha256'] == package.fingerprint(owners)
        and evidence['phase'] == owners['phase'], 'SUPPORTING_BINDING')
    require(identity.text(evidence['evidence_reference']), 'SUPPORTING_PROVENANCE')
    database_time = identity.oracle_date(evidence['database_as_of'])
    try:
        captured = datetime.fromisoformat(evidence['captured_at'].replace('Z', '+00:00'))
        owner_time = datetime.fromisoformat(owners['captured_at'].replace('Z', '+00:00'))
        require(captured.tzinfo is not None and captured >= owner_time, 'SUPPORTING_CAPTURE_TIME')
    except (ValueError, TypeError, AttributeError) as exc:
        raise package.InvalidInput('SUPPORTING_CAPTURE_TIME') from exc
    allowed = {q['owner_table_id'] for q in owners['queries'] if q['entity'] == 'party'}
    require(isinstance(evidence['queries'], list), 'SUPPORTING_QUERIES')
    queries = {}
    for query in evidence['queries']:
        require(isinstance(query, dict) and set(query) == {'kind', 'party_id', 'complete', 'records'}, 'SUPPORTING_QUERY_SCHEMA')
        require(isinstance(query['kind'], str) and query['kind'] in FIELDS
                and isinstance(query['party_id'], str) and query['party_id'] in allowed, 'SUPPORTING_QUERY_SCOPE')
        key = query['kind'], query['party_id']
        require(key not in queries, 'SUPPORTING_DUPLICATE_QUERY')
        require(type(query['complete']) is bool and isinstance(query['records'], list), 'SUPPORTING_QUERY_TYPE')
        for record in query['records']:
            require(isinstance(record, dict) and set(record) == set(FIELDS[key[0]]), 'SUPPORTING_COMPLETE_PROJECTION')
            require(all(v is None or isinstance(v, str) for v in record.values()), 'SUPPORTING_RECORD_TYPE')
            require(record['party_id'] == key[1], 'SUPPORTING_PARENT_SCOPE')
            ids = ('party_site_id', 'party_site_use_id') if key[0] == 'party_site_uses' else ('organization_profile_id',)
            require(all(ownership.identifier(record[f]) for f in ids), 'SUPPORTING_RECORD_ID')
            if key[0] == 'organization_profiles':
                require(record['effective_sequence'] == '0' or ownership.identifier(record['effective_sequence']), 'SUPPORTING_SEQUENCE')
            start, end = ('begin_date', 'end_date') if key[0] == 'party_site_uses' else ('effective_start_date', 'effective_end_date')
            for f in (start, end):
                if record[f] is not None:
                    identity.oracle_date(record[f])
            require(record[start] is None or record[end] is None or
                    identity.oracle_date(record[start]) <= identity.oracle_date(record[end]), 'SUPPORTING_DATE_ORDER')
        queries[key] = query
    return reviewed, queries, captured, database_time


def query_status(query):
    if query is None or not query['complete']:
        return 'QUERY_MISSING_OR_INCOMPLETE'
    keys = [tuple(r[f] for f in KEYS[query['kind']]) for r in query['records']]
    return 'DUPLICATE_INVENTORY_ROWS' if len(keys) != len(set(keys)) else 'COMPLETE_SUPPLIED_INVENTORY'


def inventory_status(query, owners):
    status = query_status(query)
    if status != 'COMPLETE_SUPPLIED_INVENTORY' or query['kind'] != 'party_site_uses':
        return status
    sites = {r['party_site_id']: r['party_id'] for q in owners['queries'] if q['entity'] == 'party_site'
             for r in q['records']}
    actual = {r['party_site_use_id']: r for r in query['records']}
    for q in owners['queries']:
        if q['entity'] != 'party_site_use':
            continue
        for record in q['records']:
            if sites.get(record['party_site_id']) != query['party_id']:
                continue
            match = actual.get(record['party_site_use_id'])
            if match is None:
                return 'INVENTORY_MISSING_BOUND_SITE_USE'
            if any(match[f] != record[f] for f in ('party_site_id', 'site_use_type')):
                return 'INVENTORY_OWNERSHIP_MISMATCH'
    return status


def analyze(candidate, operation, environment, before_identity, before_owners, after_identity,
            after_owners, before_evidence, after_evidence):
    br, bq, bt, bd = snapshot(candidate, operation, environment, before_identity, before_owners, before_evidence)
    ar, aq, at, ad = snapshot(candidate, operation, environment, after_identity, after_owners, after_evidence)
    require(before_owners['phase'] == 'before' and after_owners['phase'] == 'after', 'SUPPORTING_PHASES')
    require(at > bt and ad >= bd and
            datetime.fromisoformat(after_identity['captured_at'].replace('Z', '+00:00')) > bt, 'SUPPORTING_CAPTURE_ORDER')
    # Require both inventories for every party observed in either phase. A new
    # after-state party has no before inventory; do not manufacture an empty one.
    parties = {q['owner_table_id'] for owners in (before_owners, after_owners)
               for q in owners['queries'] if q['entity'] == 'party'}
    effects = []
    for index, party_id in enumerate(sorted(parties, key=int), 1):
        for kind in FIELDS:
            before, after = bq.get((kind, party_id)), aq.get((kind, party_id))
            detail = {'party_observation': index, 'kind': kind,
                      'before_status': inventory_status(before, before_owners),
                      'after_status': inventory_status(after, after_owners)}
            if detail['before_status'] != 'COMPLETE_SUPPLIED_INVENTORY' or detail['after_status'] != 'COMPLETE_SUPPLIED_INVENTORY':
                effects.append({**detail, 'status': 'EFFECT_EVIDENCE_INCOMPLETE', 'counts': None})
                continue
            if br['status'] != 'SUPPLIED_OWNERSHIP_CONSISTENT' or ar['status'] != 'SUPPLIED_OWNERSHIP_CONSISTENT':
                effects.append({**detail, 'status': 'OWNERSHIP_NOT_VERIFIED', 'counts': None})
                continue
            def keyed(q):
                return {tuple(r[f] for f in KEYS[kind]): r for r in q['records']}
            left, right = keyed(before), keyed(after)
            common = left.keys() & right.keys()
            changed = [key for key in common if left[key] != right[key]]
            columns = sorted({f for key in changed for f in FIELDS[kind] if left[key][f] != right[key][f]})
            counts = {'added': len(right.keys() - left.keys()), 'removed': len(left.keys() - right.keys()),
                      'changed': len(changed), 'unchanged': len(common) - len(changed)}
            effects.append({**detail, 'status': 'CHANGES_REQUIRE_EFFECT_REVIEW' if any(counts[k] for k in ('added', 'removed', 'changed'))
                            else 'NO_SELECTED_INVENTORY_CHANGE', 'counts': counts, 'changed_columns': columns})
    rows = [dict(zip(package.columns(), raw)) for raw in package.inspect_zip(candidate)]
    sources = {q['source_name']: q for q in after_identity['source_system_queries']}
    refs = {(q['orig_system'], q['owner_table_name'], q['reference']): q for q in after_identity['reference_queries']}
    profile_findings = []
    for number, row in enumerate(rows, 1):
        selected = {field: column for field, column in PARTY_VALUES.items() if row[field]}
        if not selected:
            continue
        if ar['status'] != 'SUPPLIED_OWNERSHIP_CONSISTENT':
            profile_findings.append({'row': number, 'status': 'OWNERSHIP_NOT_VERIFIED'})
            continue
        code = sources[row['ORIG_SOURCE_SYSTEM_NAME']]['records'][0]['orig_system']
        key = identity.reference_candidates(row)['party']
        party_id = refs[code, key['owner'], key['reference']]['records'][0]['owner_table_id']
        query = aq.get(('organization_profiles', party_id))
        status = query_status(query)
        if status != 'COMPLETE_SUPPLIED_INVENTORY':
            profile_findings.append({'row': number, 'status': status})
            continue
        if any(r[f] is None for r in query['records'] for f in ('effective_start_date', 'effective_end_date', 'effective_latest_change')):
            profile_findings.append({'row': number, 'status': 'PROFILE_TIME_EVIDENCE_MISSING'})
            continue
        current = [r for r in query['records'] if r['effective_latest_change'] == 'Y'
                   and identity.oracle_date(r['effective_start_date']) <= ad <= identity.oracle_date(r['effective_end_date'])]
        if len(current) != 1:
            profile_findings.append({'row': number, 'status': 'CURRENT_PROFILE_NOT_FOUND' if not current else 'AMBIGUOUS_CURRENT_PROFILES'})
            continue
        profile_findings.extend({'row': number, 'field': field,
            'status': 'MATCH' if current[0][column] == row[field] else 'PROFILE_VALUE_MISMATCH'} for field, column in selected.items())
    return {'schema_version': 'ar-customer-supporting-review-v1', 'status': 'SUPPORTING_OBSERVATIONS_ONLY',
        'candidate_sha256': ar['candidate_sha256'], 'before_evidence_sha256': package.fingerprint(before_evidence),
        'after_evidence_sha256': package.fingerprint(after_evidence), 'effects': effects,
        'organization_profile_findings': profile_findings, 'effect_acceptance_verified': False,
        'party_site_use_identity_verified': False, 'attempt_causality_verified': False,
        'persisted_reconciliation_complete': False, 'execution_authorized': False, 'journey_complete': False,
        'limits': ['Party-scoped inventories must include all sibling sites and history, without candidate-only filtering.',
                   'Selected profile values use the supplied database-as-of instant, not inferred loader execution time.',
                   'Changes, new rows and absent inventories do not establish approved effects, physical creation or attempt causality.']}
