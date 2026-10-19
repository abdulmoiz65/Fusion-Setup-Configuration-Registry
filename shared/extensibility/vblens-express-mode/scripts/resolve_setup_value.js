#!/usr/bin/env node
'use strict';

/**
 * Resolve one Fusion language or lookup label through the central REST client.
 * The resolver accepts only fixed setup resources and never reads business records.
 */

const path = require('node:path');
const { RuntimeEvidenceError, validateIdentifier } = require('./runtime_bundle');
const {
  DEFAULT_PROPERTIES,
  callFusionRest,
  parseSafeEnvironment,
} = require('./fscr_rest_client');

const DEFAULT_TIMEOUT_MS = 300000;
const MAX_RESPONSE_BYTES = 8 * 1024 * 1024;
const PAGE_SIZE = 500;
const MAX_PAGES = 100;
const SUPPORTED_KINDS = new Set(['language', 'standard-lookup', 'common-lookup']);

function readOptionValue(argv, index, optionName) {
  // Reject incomplete options before they can influence a REST request.
  const value = argv[index + 1];
  if (!value || value.startsWith('--')) {
    throw new RuntimeEvidenceError('INVALID_ARGUMENT', `${optionName} requires a value.`);
  }
  return value;
}

function parseArgs(argv) {
  // Keep the CLI narrow so setup resolution cannot become a generic HTTP client.
  const options = {
    workspace: process.cwd(),
    kind: null,
    label: null,
    lookupType: null,
    languageScope: 'active',
    activeDate: null,
    currentValue: null,
    timeoutMs: DEFAULT_TIMEOUT_MS,
    propertiesPath: DEFAULT_PROPERTIES,
    tokenCache: null,
    json: false,
    help: false,
  };
  for (let index = 0; index < argv.length; index += 1) {
    const argument = argv[index];
    if (argument === '--workspace') {
      options.workspace = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--kind') {
      options.kind = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--label') {
      options.label = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--lookup-type') {
      options.lookupType = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--language-scope') {
      options.languageScope = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--active-date') {
      options.activeDate = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--current-value') {
      options.currentValue = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--timeout-ms') {
      options.timeoutMs = Number(readOptionValue(argv, index, argument));
      index += 1;
    } else if (argument === '--properties') {
      options.propertiesPath = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--token-cache') {
      options.tokenCache = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--json') {
      options.json = true;
    } else if (argument === '--help' || argument === '-h') {
      options.help = true;
    } else {
      throw new RuntimeEvidenceError('INVALID_ARGUMENT', `Unknown argument: ${argument}`);
    }
  }
  return options;
}

function normalizeOptions(options) {
  // Normalize user-controlled values once before building allowlisted queries.
  const kind = String(options.kind || '').trim();
  if (!SUPPORTED_KINDS.has(kind)) {
    throw new RuntimeEvidenceError(
      'INVALID_SETUP_KIND',
      '--kind must be language, standard-lookup, or common-lookup.'
    );
  }
  const label = String(options.label || '').normalize('NFKC').trim();
  if (!label || label.length > 200 || /[\u0000-\u001f\u007f]/.test(label)) {
    throw new RuntimeEvidenceError('INVALID_SETUP_LABEL', 'Setup label must be 1-200 text characters.');
  }
  const languageScope = String(options.languageScope || 'active').trim();
  if (!['active', 'installed'].includes(languageScope)) {
    throw new RuntimeEvidenceError(
      'INVALID_LANGUAGE_SCOPE',
      '--language-scope must be active or installed.'
    );
  }
  const lookupType = kind === 'language'
    ? null
    : validateIdentifier(options.lookupType, 'Fusion lookup type');
  const activeDate = options.activeDate ? String(options.activeDate).trim() : null;
  if (activeDate && !/^\d{4}-\d{2}-\d{2}$/.test(activeDate)) {
    throw new RuntimeEvidenceError('INVALID_ACTIVE_DATE', '--active-date must use YYYY-MM-DD.');
  }
  if (!Number.isSafeInteger(options.timeoutMs) || options.timeoutMs <= 0) {
    throw new RuntimeEvidenceError('INVALID_ARGUMENT', '--timeout-ms must be a positive integer.');
  }
  return {
    workspace: path.resolve(options.workspace || process.cwd()),
    kind,
    label,
    lookupType,
    languageScope,
    activeDate,
    currentValue: options.currentValue ? String(options.currentValue).trim() : null,
    timeoutMs: options.timeoutMs,
    propertiesPath: path.resolve(options.propertiesPath || DEFAULT_PROPERTIES),
    tokenCache: options.tokenCache ? path.resolve(options.tokenCache) : null,
    json: options.json === true,
  };
}

function buildCollectionRequest(target, offset = 0) {
  // Return only the two documented setup collections supported by this skill.
  if (target.kind === 'language') {
    return {
      endpoint: '/fscmRestApi/resources/11.13.18.05/languagesLOV',
      query: [
        'fields=LanguageCode,LanguageTag,Description,InstalledFlag,ActivationStatus',
        'onlyData=true',
        `limit=${PAGE_SIZE}`,
        `offset=${offset}`,
      ],
    };
  }
  const resource = target.kind === 'standard-lookup'
    ? 'standardLookupCodes'
    : 'commonLookupCodes';
  const query = [
    `lookupType=${target.lookupType}`,
    '$fields=lookupType,lookupCode,meaning,description',
    `$limit=${PAGE_SIZE}`,
    `$offset=${offset}`,
  ];
  if (target.activeDate) query.push(`activeDate=${target.activeDate}`);
  if (target.currentValue) query.push(`currentValue=${target.currentValue}`);
  return {
    endpoint: `/api/boss/data/objects/ora/commonAppsInfra/objects/v1/${resource}/$views/lookupLOV`,
    query,
  };
}

function normalizeSetupItem(item, kind) {
  // Normalize FND title-case fields to one stable internal shape.
  if (kind !== 'language') return item;
  return {
    languageCode: item.LanguageCode ?? item.languageCode,
    languageTag: item.LanguageTag ?? item.languageTag,
    description: item.Description ?? item.description,
    installed: item.InstalledFlag ?? item.installed,
    activationStatus: item.ActivationStatus ?? item.activationStatus,
  };
}

function languageMatchesScope(item, scope) {
  // Fusion marks base and added languages as installed with B and I.
  if (scope === 'installed') return ['B', 'I'].includes(String(item.installed || '').toUpperCase());
  return String(item.activationStatus || '').toUpperCase() === 'ACTIVE';
}

function normalizedMatchValue(value) {
  // Exact matching is case-insensitive but never fuzzy.
  return String(value == null ? '' : value).normalize('NFKC').trim().toLocaleLowerCase('en-US');
}

function candidateValues(item, kind) {
  // Compare stored and displayed values while returning only the stored code.
  return kind === 'language'
    ? [item.languageCode, item.languageTag, item.description]
    : [item.lookupCode, item.meaning];
}

function resolveExactMatch(items, target) {
  // Require one exact match so authoring never embeds a guessed setup code.
  const requested = normalizedMatchValue(target.label);
  const matches = items.filter((item) => (
    candidateValues(item, target.kind).some((value) => normalizedMatchValue(value) === requested)
  ));
  if (matches.length === 0) {
    throw new RuntimeEvidenceError(
      'SETUP_VALUE_NOT_FOUND',
      `No exact ${target.kind} match was found for ${target.label}.`
    );
  }
  const uniqueCodes = new Set(matches.map((item) => (
    target.kind === 'language' ? item.languageTag : item.lookupCode
  )));
  if (matches.length !== 1 || uniqueCodes.size !== 1) {
    throw new RuntimeEvidenceError(
      'SETUP_VALUE_AMBIGUOUS',
      `More than one exact ${target.kind} match was found for ${target.label}.`
    );
  }
  const match = matches[0];
  return target.kind === 'language'
    ? {
      code: match.languageTag,
      label: match.description,
      languageTag: match.languageTag,
      fusionLanguageCode: match.languageCode,
      installed: match.installed,
      activationStatus: match.activationStatus,
    }
    : {
      code: match.lookupCode,
      label: match.meaning,
      description: match.description,
      lookupType: match.lookupType,
    };
}

function fetchCollection(target, dependencies = {}) {
  // Follow bounded pagination through the existing central REST clients.
  const restCall = dependencies.callFusionRest || callFusionRest;
  const items = [];
  let offset = 0;
  let pageCount = 0;
  while (pageCount < MAX_PAGES) {
    const request = buildCollectionRequest(target, offset);
    const response = restCall({
      ...request,
      method: 'GET',
      propertiesPath: target.propertiesPath,
      tokenCache: target.tokenCache,
      timeoutSeconds: Math.ceil(target.timeoutMs / 1000),
    }, dependencies.restDependencies || {});
    if (response.body.length > MAX_RESPONSE_BYTES) {
      throw new RuntimeEvidenceError('SETUP_RESPONSE_TOO_LARGE', 'Fusion setup response exceeded the limit.');
    }
    let payload;
    try {
      payload = JSON.parse(response.body.toString('utf8'));
    } catch (error) {
      throw new RuntimeEvidenceError('SETUP_RESPONSE_INVALID', 'Fusion setup response was not valid JSON.');
    }
    if (!payload || !Array.isArray(payload.items)) {
      throw new RuntimeEvidenceError('SETUP_RESPONSE_INVALID', 'Fusion setup response omitted items.');
    }
    const normalizedItems = payload.items.map((item) => normalizeSetupItem(item, target.kind));
    items.push(...(
      target.kind === 'language'
        ? normalizedItems.filter((item) => languageMatchesScope(item, target.languageScope))
        : normalizedItems
    ));
    pageCount += 1;
    if (payload.hasMore !== true) return { items, pageCount };
    if (payload.items.length === 0) {
      throw new RuntimeEvidenceError('SETUP_PAGINATION_INVALID', 'Fusion setup pagination did not advance.');
    }
    offset += payload.items.length;
  }
  throw new RuntimeEvidenceError('SETUP_PAGE_LIMIT', 'Fusion setup results exceeded the page limit.');
}

function resolveSetupValue(options, dependencies = {}) {
  // Resolve environment identity separately from the selected setup record.
  const target = normalizeOptions(options);
  const environment = (dependencies.parseSafeEnvironment || parseSafeEnvironment)(target.propertiesPath);
  const collection = fetchCollection(target, dependencies);
  return {
    schemaVersion: 1,
    environment: environment.environment,
    target: {
      kind: target.kind,
      label: target.label,
      lookupType: target.lookupType,
      languageScope: target.kind === 'language' ? target.languageScope : null,
    },
    resolved: resolveExactMatch(collection.items, target),
    evidence: {
      source: target.kind === 'language' ? 'fusion-fnd-adf-languages-lov' : 'fusion-setup-service',
      matchedBy: 'exact-case-insensitive',
      pagesRead: collection.pageCount,
      recordsRead: collection.items.length,
    },
    requests: { setup: collection.pageCount },
  };
}

function printHelp() {
  // Document the properties-backed, allowlisted setup contract.
  process.stdout.write([
    'Resolve a Fusion language or lookup code',
    '',
    'Usage:',
    '  node scripts/resolve_setup_value.js --kind language --label <label-or-code>',
    '    [--language-scope active|installed] [--properties <path>] [--token-cache <path>]',
    '  node scripts/resolve_setup_value.js --kind standard-lookup|common-lookup',
    '    --lookup-type <type> --label <meaning-or-code>',
    '    [--active-date YYYY-MM-DD] [--current-value <code>] [--json]',
    '',
  ].join('\n'));
}

function main() {
  // Convert setup failures into a nonzero CLI result without exposing raw records.
  try {
    const options = parseArgs(process.argv.slice(2));
    if (options.help) return printHelp();
    const result = resolveSetupValue(options);
    process.stdout.write(`${JSON.stringify(result, null, options.json ? 2 : 0)}\n`);
  } catch (error) {
    process.stderr.write(`${error.message}\n`);
    process.exitCode = 1;
  }
}

if (require.main === module) main();

module.exports = {
  buildCollectionRequest,
  candidateValues,
  fetchCollection,
  languageMatchesScope,
  normalizeOptions,
  normalizeSetupItem,
  parseArgs,
  resolveExactMatch,
  resolveSetupValue,
};
