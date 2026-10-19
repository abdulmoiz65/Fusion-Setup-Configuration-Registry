#!/usr/bin/env node
'use strict';

/**
 * Fetch one Fusion REST resource description and publish immutable, generic
 * REST-schema evidence without retrieving business records.
 */

const fs = require('node:fs');
const path = require('node:path');
const {
  RuntimeEvidenceError,
  assertNoSymlinkBetween,
  ensureCacheRoot,
  resolveCachePaths,
  safeJoin,
  sha256,
  validateIdentifier,
} = require('./runtime_bundle');
const {
  DEFAULT_PROPERTIES,
  callFusionRest,
  parseSafeEnvironment,
} = require('./fscr_rest_client');

const DEFAULT_TIMEOUT_MS = 300000;
const MAX_DESCRIBE_BYTES = 32 * 1024 * 1024;

function readOptionValue(argv, index, optionName) {
  const value = argv[index + 1];
  if (!value || value.startsWith('--')) {
    throw new RuntimeEvidenceError('INVALID_ARGUMENT', `${optionName} requires a value.`);
  }
  return value;
}

function parseArgs(argv) {
  const options = {
    workspace: process.cwd(),
    cacheRoot: null,
    service: null,
    version: null,
    resource: null,
    fields: [],
    children: [],
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
    } else if (argument === '--cache-root') {
      options.cacheRoot = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--service') {
      options.service = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--version') {
      options.version = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--resource') {
      options.resource = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--field') {
      options.fields.push(readOptionValue(argv, index, argument));
      index += 1;
    } else if (argument === '--child') {
      options.children.push(readOptionValue(argv, index, argument));
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

function printHelp() {
  process.stdout.write([
    'Fetch deterministic Fusion REST-schema evidence',
    '',
    'Usage:',
    '  node scripts/fetch_service_evidence.js --workspace <path>',
    '    [--cache-root <shared-cache-directory>]',
    '    --service <service> --version <version> --resource <resource>',
    '    [--field <attribute>] [--child <dot-separated-child-path>] [--json]',
    '',
    'The command uses core/auth/fusionEnv.properties and the shared Fusion REST client.',
    'It retrieves only the selected resource description.',
    'It does not accept arbitrary URLs or retrieve business records.',
    '',
  ].join('\n'));
}

function normalizeChildPath(value) {
  const normalized = String(value || '').trim();
  if (!normalized) {
    throw new RuntimeEvidenceError('INVALID_TARGET', 'REST child path is required.');
  }
  // Validate every component independently so a selector cannot become a filesystem path.
  const segments = normalized.split('.');
  if (segments.some((segment) => !segment)) {
    throw new RuntimeEvidenceError('INVALID_TARGET', `REST child path is invalid: ${normalized}`);
  }
  return segments.map((segment) => validateIdentifier(segment, 'REST child')).join('.');
}

function normalizeOptions(options) {
  const service = validateIdentifier(options.service, 'Fusion REST service');
  if (!/^[A-Za-z][A-Za-z0-9]*Rest$/.test(service)) {
    throw new RuntimeEvidenceError(
      'INVALID_SERVICE',
      'Fusion REST service must be an identifier ending in Rest, such as hcmRest.'
    );
  }
  const version = validateIdentifier(options.version, 'REST resource version');
  const resource = validateIdentifier(options.resource, 'REST resource');
  const fields = [...new Set((options.fields || []).map((field) => (
    validateIdentifier(field, 'REST attribute')
  )))].sort();
  const children = [...new Set((options.children || []).map(normalizeChildPath))].sort();
  if (!Number.isSafeInteger(options.timeoutMs) || options.timeoutMs <= 0) {
    throw new RuntimeEvidenceError('INVALID_ARGUMENT', '--timeout-ms must be a positive integer.');
  }
  return {
    workspace: path.resolve(options.workspace || process.cwd()),
    cacheRoot: options.cacheRoot ? path.resolve(options.cacheRoot) : null,
    service,
    version,
    resource,
    fields,
    children,
    timeoutMs: options.timeoutMs,
    propertiesPath: options.propertiesPath || DEFAULT_PROPERTIES,
    tokenCache: options.tokenCache || null,
    json: options.json === true,
  };
}

function buildDescribeUrl(baseUrl, target) {
  const url = new URL(baseUrl);
  // Identifiers are encoded as path segments and the environment origin remains authoritative.
  url.pathname = `/${target.service}Api/resources/${encodeURIComponent(target.version)}/${encodeURIComponent(target.resource)}/describe`;
  url.search = '';
  url.hash = '';
  return url;
}

function normalizeChildren(children) {
  if (Array.isArray(children)) return children;
  if (!children || typeof children !== 'object') return [];
  // Object-shaped Oracle child metadata uses the property key as the child name.
  return Object.entries(children).map(([name, definition]) => ({
    name,
    ...(definition && typeof definition === 'object' ? definition : {}),
  }));
}

function summarizeAttributes(attributes) {
  // Preserve only stable schema facts needed for field-path assessment.
  return (Array.isArray(attributes) ? attributes : []).map((attribute) => ({
    name: attribute.name || null,
    title: attribute.title || null,
    type: attribute.type || null,
    format: attribute.format || null,
    // Numeric bounds and scale prevent callers from guessing percentage representation.
    precision: attribute.precision ?? null,
    scale: attribute.scale ?? null,
    minimum: attribute.minimum ?? null,
    maximum: attribute.maximum ?? null,
    mandatory: attribute.mandatory === true,
    inputRequired: attribute.inputRequired === true,
    queryable: attribute.queryable === true,
    updatable: attribute.updatable === true,
    allowChanges: attribute.allowChanges || null,
  }));
}

function childSummary(child, childPath, selection) {
  const summary = {
    name: child.name || null,
    title: child.title || null,
    relationship: child.relationship || null,
    type: child.type || null,
    cardinality: child.cardinality || child.collectionType || null,
  };
  if (!selection) return summary;
  // Selected branches include exact paths and attributes; unselected siblings stay compact.
  return {
    ...summary,
    path: childPath,
    attributes: summarizeAttributes(child.attributes),
    children: normalizeChildren(child.children).map((nestedChild) => {
      const nestedPath = `${childPath}.${nestedChild.name}`;
      return childSummary(nestedChild, nestedPath, selection[nestedChild.name]);
    }),
  };
}

function buildChildSelection(childPaths) {
  const selection = {};
  for (const childPath of childPaths || []) {
    let cursor = selection;
    for (const segment of childPath.split('.')) {
      if (!cursor[segment]) cursor[segment] = {};
      cursor = cursor[segment];
    }
  }
  return selection;
}

function resolveChildPath(resource, childPath) {
  let current = resource;
  for (const segment of childPath.split('.')) {
    const child = normalizeChildren(current.children).find((candidate) => candidate.name === segment);
    if (!child) {
      throw new RuntimeEvidenceError(
        'CHILD_DESCRIPTION_MISSING',
        `REST describe did not contain child path ${childPath}.`
      );
    }
    current = child;
  }
  return current;
}

function summarizeResource(payload, resourceName, childPaths = []) {
  const resource = payload && payload.Resources && payload.Resources[resourceName];
  if (!resource || typeof resource !== 'object' || Array.isArray(resource)) {
    throw new RuntimeEvidenceError(
      'RESOURCE_DESCRIPTION_MISSING',
      `REST describe did not contain resource ${resourceName}.`
    );
  }
  // Validate requested paths before returning any partial schema summary.
  for (const childPath of childPaths) resolveChildPath(resource, childPath);
  const childSelection = buildChildSelection(childPaths);
  return {
    name: resourceName,
    title: resource.title || null,
    titlePlural: resource.titlePlural || null,
    usage: resource.usage || null,
    attributes: summarizeAttributes(resource.attributes),
    children: normalizeChildren(resource.children).map((child) => (
      childSummary(child, child.name, childSelection[child.name])
    )),
  };
}

function ensureCacheDirectory(cacheRoot, directoryPath) {
  const relative = path.relative(path.resolve(cacheRoot), path.resolve(directoryPath));
  if (relative.startsWith('..') || path.isAbsolute(relative)) {
    throw new RuntimeEvidenceError('UNSAFE_CACHE_PATH', 'Service evidence path escapes its cache root.');
  }
  let current = path.resolve(cacheRoot);
  for (const segment of relative.split(path.sep).filter(Boolean)) {
    current = path.join(current, segment);
    if (fs.existsSync(current)) {
      // Refuse both symbolic links and non-directory collisions before descending.
      const stat = fs.lstatSync(current);
      if (stat.isSymbolicLink() || !stat.isDirectory()) {
        throw new RuntimeEvidenceError(
          'UNSAFE_CACHE_PATH',
          `Service evidence directory is unsafe: ${current}`
        );
      }
      continue;
    }
    try {
      fs.mkdirSync(current, { mode: 0o700 });
    } catch (error) {
      // A concurrent creator is safe only when it created a real directory.
      if (!fs.existsSync(current)) throw error;
      const stat = fs.lstatSync(current);
      if (stat.isSymbolicLink() || !stat.isDirectory()) throw error;
    }
  }
  assertNoSymlinkBetween(cacheRoot, directoryPath);
}

function publishImmutable(filePath, content, cacheRoot) {
  ensureCacheDirectory(cacheRoot, path.dirname(filePath));
  if (fs.existsSync(filePath)) {
    if (sha256(fs.readFileSync(filePath)) !== sha256(content)) {
      throw new RuntimeEvidenceError(
        'SERVICE_EVIDENCE_COLLISION',
        'Service evidence cache contains conflicting content for one identity.'
      );
    }
    return 'hit';
  }
  try {
    fs.writeFileSync(filePath, content, { mode: 0o600, flag: 'wx' });
    return 'populated';
  } catch (error) {
    // A concurrent identical writer is safe; conflicting content remains fatal.
    if (fs.existsSync(filePath) && sha256(fs.readFileSync(filePath)) === sha256(content)) {
      return 'hit';
    }
    throw error;
  }
}

function filterSchema(schema, fields) {
  if (!fields || fields.length === 0) return schema;
  const requested = new Set(fields);
  return {
    ...schema,
    attributes: schema.attributes.filter((attribute) => requested.has(attribute.name)),
  };
}

async function fetchServiceEvidence(options, dependencies = {}) {
  const target = normalizeOptions(options);
  const environmentContext = (dependencies.parseSafeEnvironment || parseSafeEnvironment)(
    target.propertiesPath
  );
  const environment = environmentContext.restBaseUrl;
  const describeUrl = buildDescribeUrl(environment, target);
  const restCall = dependencies.callFusionRest || callFusionRest;
  const response = restCall({
    endpoint: describeUrl.pathname,
    headers: ['REST-Framework-Version=9'],
    propertiesPath: target.propertiesPath,
    timeoutSeconds: Math.ceil(target.timeoutMs / 1000),
    tokenCache: target.tokenCache,
  }, dependencies.restDependencies || {});
  if (response.body.length > MAX_DESCRIBE_BYTES) {
    throw new RuntimeEvidenceError('RESPONSE_TOO_LARGE', 'REST describe response exceeded the safe size limit.');
  }
  let payload;
  try {
    payload = JSON.parse(response.body.toString('utf8'));
  } catch (error) {
    throw new RuntimeEvidenceError(
      'SERVICE_DESCRIPTION_INVALID',
      `REST describe response was not valid JSON: ${error.message}`
    );
  }
  const schema = summarizeResource(payload, target.resource, target.children);
  const cachePaths = resolveCachePaths(
    target.workspace,
    environment,
    'service-evidence',
    'v1',
    target.cacheRoot
  );
  ensureCacheRoot(cachePaths);
  const responseContent = `${JSON.stringify(payload, null, 2)}\n`;
  const responseSha256 = sha256(responseContent);
  const schemaPath = safeJoin(
    cachePaths.schemaRoot,
    'services',
    target.service,
    target.version,
    target.resource,
    `${responseSha256}.json`
  );
  const schemaCacheStatus = publishImmutable(schemaPath, responseContent, cachePaths.cacheRoot);
  const manifest = {
    schemaVersion: 2,
    environment,
    shapeDomain: 'rest-schema',
    target: {
      service: target.service,
      version: target.version,
      resource: target.resource,
      children: target.children,
    },
    request: {
      method: 'GET',
      path: describeUrl.pathname,
    },
    schema,
    evidence: {
      path: schemaPath,
      sha256: responseSha256,
      sizeBytes: Buffer.byteLength(responseContent),
      contentType: 'application/json',
    },
    trustBoundary: {
      describesSchemaOnly: true,
      businessRecordsIncluded: false,
      businessRulesExposureProven: false,
      observedRuntimeValuesIncluded: false,
    },
  };
  const manifestIdentity = sha256(JSON.stringify({
    schemaVersion: manifest.schemaVersion,
    environment,
    target: manifest.target,
    responseSha256,
  }));
  const manifestPath = safeJoin(
    cachePaths.schemaRoot,
    'evidence',
    `service-${manifestIdentity}.json`
  );
  publishImmutable(
    manifestPath,
    `${JSON.stringify(manifest, null, 2)}\n`,
    cachePaths.cacheRoot
  );
  return {
    schemaVersion: 2,
    environment,
    transport: { mode: 'core-rest-client' },
    target: manifest.target,
    shapeDomain: 'rest-schema',
    schema: filterSchema(schema, target.fields),
    evidence: {
      manifestPath,
      schemaPath,
      sha256: responseSha256,
      cacheStatus: schemaCacheStatus,
    },
    requests: {
      fusionRest: response.requestCount || 1,
    },
  };
}

function printHuman(result) {
  process.stdout.write([
    `Environment: ${result.environment}`,
    `Resource: ${result.target.service}/${result.target.version}/${result.target.resource}`,
    `Shape domain: ${result.shapeDomain}`,
    `Attributes: ${result.schema.attributes.length}`,
    `Children: ${result.schema.children.length}`,
    `Cache: ${result.evidence.cacheStatus}`,
    `Evidence manifest: ${result.evidence.manifestPath}`,
    '',
  ].join('\n'));
}

async function main() {
  try {
    const options = parseArgs(process.argv.slice(2));
    if (options.help) {
      printHelp();
      return;
    }
    const result = await fetchServiceEvidence(options);
    if (options.json) process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
    else printHuman(result);
  } catch (error) {
    process.stderr.write(`${error.message}\n`);
    process.exitCode = 1;
  }
}

if (require.main === module) main();

module.exports = {
  buildDescribeUrl,
  buildChildSelection,
  childSummary,
  ensureCacheDirectory,
  fetchServiceEvidence,
  filterSchema,
  normalizeChildren,
  normalizeChildPath,
  normalizeOptions,
  parseArgs,
  resolveChildPath,
  summarizeAttributes,
  summarizeResource,
};
