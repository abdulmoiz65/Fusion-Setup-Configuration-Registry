#!/usr/bin/env node
'use strict';

/**
 * Parse Oracle App UI bundles without executing JavaScript and persist an
 * immutable, content-addressed local cache for deployed runtime evidence.
 */

const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');

// Callers may place cache content in a shared project-root cache or below their workspace.
const CACHE_DIRECTORY_NAME = 'cache';
const CACHE_SCHEMA_VERSION = 1;
const CDN_ORIGIN = 'https://static.oracle.com';
const STAGE_CDN_ORIGIN = 'https://static-stage.oracle.com';
const APPROVED_CDN_ORIGINS = new Set([CDN_ORIGIN, STAGE_CDN_ORIGIN]);
const COMPLETE_FILE = 'COMPLETE';
const INDEX_FILE = 'module-index.json';
const MANIFEST_FILE = 'cache-manifest.json';

class RuntimeEvidenceError extends Error {
  constructor(code, message, details = null) {
    super(message);
    this.name = 'RuntimeEvidenceError';
    this.code = code;
    this.details = details;
  }
}

function sha256(value) {
  return crypto.createHash('sha256').update(value).digest('hex');
}

function validateIdentifier(value, label, options = {}) {
  const normalized = String(value || '').trim();
  if (!normalized) {
    throw new RuntimeEvidenceError('INVALID_TARGET', `${label} is required.`);
  }
  const segments = options.allowPath ? normalized.split('/') : [normalized];
  if (
    segments.some((segment) => (
      !segment
      || segment === '.'
      || segment === '..'
      || segment.includes('\\')
      || segment.includes('\0')
      || !/^[A-Za-z0-9._$@+-]+$/.test(segment)
    ))
  ) {
    throw new RuntimeEvidenceError(
      'INVALID_TARGET',
      `${label} contains an unsafe path segment: ${normalized}`
    );
  }
  return normalized;
}

function encodeCacheSegment(value) {
  const normalized = String(value || '');
  if (!normalized || normalized === '.' || normalized === '..' || normalized.includes('\0')) {
    throw new RuntimeEvidenceError('UNSAFE_CACHE_PATH', 'Cache path segment is unsafe.');
  }
  // URI encoding keeps the on-disk layout readable without trusting module IDs as paths.
  return encodeURIComponent(normalized).replace(/\*/g, '%2A');
}

function safeJoin(root, ...segments) {
  const resolvedRoot = path.resolve(root);
  const target = path.resolve(resolvedRoot, ...segments);
  const relative = path.relative(resolvedRoot, target);
  if (relative.startsWith('..') || path.isAbsolute(relative)) {
    throw new RuntimeEvidenceError('UNSAFE_CACHE_PATH', `Path escapes cache root: ${target}`);
  }
  return target;
}

function buildAppInfoEndpoint(applicationUrl) {
  const endpoint = new URL(applicationUrl);
  if (endpoint.protocol !== 'https:' || endpoint.username || endpoint.password) {
    throw new RuntimeEvidenceError(
      'INVALID_ENVIRONMENT_URL',
      'Fusion application URL must be an HTTPS origin without embedded credentials.'
    );
  }
  endpoint.pathname = '/fscmRestApi/vxmanifest/v2/digests/latest';
  endpoint.search = '';
  endpoint.hash = '';
  endpoint.searchParams.set('type', 'app-ui-info');
  return endpoint;
}

function resolveCdnOrigin(environmentUrl) {
  let environment;
  try {
    environment = new URL(environmentUrl);
  } catch (error) {
    throw new RuntimeEvidenceError('INVALID_ENVIRONMENT_URL', 'Fusion environment URL must be valid HTTPS.');
  }
  if (environment.protocol !== 'https:' || environment.username || environment.password) {
    throw new RuntimeEvidenceError(
      'INVALID_ENVIRONMENT_URL',
      'Fusion environment URL must use HTTPS and must not contain embedded credentials.'
    );
  }
  // Oracle oc-test environments publish App UI bundles on the stage CDN.
  return environment.hostname.endsWith('.ocs.oc-test.com') ? STAGE_CDN_ORIGIN : CDN_ORIGIN;
}

function buildBundleUrl(extensionId, version, cdnOrigin = CDN_ORIGIN) {
  const extension = validateIdentifier(extensionId, 'Extension ID');
  const deployedVersion = validateIdentifier(version, 'Extension version');
  const origin = new URL(cdnOrigin);
  if (origin.protocol !== 'https:' || origin.username || origin.password || !APPROVED_CDN_ORIGINS.has(origin.origin)) {
    throw new RuntimeEvidenceError('INVALID_CDN_ORIGIN', 'CDN origin is not an approved Oracle HTTPS origin.');
  }
  const bundleUrl = new URL(origin.origin);
  bundleUrl.pathname = [
    '',
    'cdn',
    'fa',
    encodeURIComponent(extension),
    encodeURIComponent(deployedVersion),
    'bundles',
    'base-config-bundle.js',
  ].join('/');
  return bundleUrl;
}

function normalizeRouteApplications(application) {
  // Preserve only the non-secret route metadata needed to map a Redwood URL back to its App UI.
  const routeApplications = application.metadata?.applications;
  if (!Array.isArray(routeApplications)) return [];
  return routeApplications
    .filter((entry) => entry && typeof entry === 'object' && !Array.isArray(entry))
    .map((entry) => ({
      id: typeof entry.id === 'string' ? entry.id.trim() : '',
      urlId: typeof entry.urlId === 'string' ? entry.urlId.trim() : '',
      displayName: typeof entry.displayName === 'string' ? entry.displayName.trim() : '',
      defaultFlow: typeof entry.defaultFlow === 'string' ? entry.defaultFlow.trim() : '',
      extensible: entry.extensible === true,
      navigable: Array.isArray(entry.navigable)
        ? entry.navigable.filter((value) => typeof value === 'string').map((value) => value.trim())
        : [],
      menu: Array.isArray(entry.menu)
        ? entry.menu.filter((value) => typeof value === 'string').map((value) => value.trim())
        : [],
    }))
    .filter((entry) => entry.id || entry.urlId);
}

function parseRedwoodRouteUrl(value) {
  let parsed;
  try {
    parsed = new URL(String(value || '').trim());
  } catch (error) {
    throw new RuntimeEvidenceError('INVALID_TARGET_URL', 'Target URL must be an absolute HTTPS URL.');
  }
  if (parsed.protocol !== 'https:' || parsed.username || parsed.password) {
    throw new RuntimeEvidenceError(
      'INVALID_TARGET_URL',
      'Target URL must use HTTPS and must not contain embedded credentials.'
    );
  }
  // Route parameters are evidence hints only; query values are intentionally discarded.
  const segments = parsed.pathname.split('/').filter(Boolean).map((segment) => {
    try {
      return decodeURIComponent(segment);
    } catch (error) {
      throw new RuntimeEvidenceError('INVALID_TARGET_URL', 'Target URL contains invalid path encoding.');
    }
  });
  const redwoodIndex = segments.indexOf('redwood');
  if (redwoodIndex < 1 || segments[redwoodIndex - 1] !== 'fscmUI') {
    throw new RuntimeEvidenceError(
      'INVALID_TARGET_URL',
      'Target URL must use the /fscmUI/redwood/<application>/<flow>/<page> route.'
    );
  }
  const routeSegments = segments.slice(redwoodIndex + 1);
  if (routeSegments.length < 3) {
    throw new RuntimeEvidenceError(
      'INVALID_TARGET_URL',
      'Target URL must identify an application, flow, and page.'
    );
  }
  return {
    origin: parsed.origin,
    uiShell: 'fscmUI',
    application: validateIdentifier(routeSegments[0], 'Redwood application'),
    flow: validateIdentifier(routeSegments.slice(1, -1).join('/'), 'Redwood flow', { allowPath: true }),
    page: validateIdentifier(routeSegments.at(-1), 'Redwood page'),
  };
}

function resolveApplicationFromRoute(applicationIndex, route) {
  const expectedPage = `flows/${route.flow}/pages/${route.page}-page`;
  const finalFlowSegment = route.flow.split('/').at(-1);
  const exactMatches = [];
  const flowMatches = [];

  for (const extension of applicationIndex.values()) {
    for (const application of extension.applications || []) {
      // Route ownership is established only by deployed identifiers, never a display label.
      const routeIds = [application.id, application.urlId].filter(Boolean);
      if (!routeIds.includes(route.application)) continue;
      const candidate = {
        extension: extension.id,
        version: extension.version,
        application: application.id || application.urlId,
        flow: route.flow,
        page: route.page,
      };
      if (application.navigable.includes(expectedPage)) {
        exactMatches.push({ ...candidate, matchReason: 'navigable-page' });
      } else if (
        application.defaultFlow === route.flow
        || application.defaultFlow === finalFlowSegment
        || application.menu.includes(route.flow)
        || application.menu.includes(finalFlowSegment)
      ) {
        flowMatches.push({ ...candidate, matchReason: 'flow' });
      }
    }
  }

  // Page-level navigability is stronger than a default-flow match and wins deterministically.
  const matches = exactMatches.length > 0 ? exactMatches : flowMatches;
  if (matches.length === 0) {
    throw new RuntimeEvidenceError(
      'ROUTE_NOT_FOUND',
      `App-info does not map ${route.application}/${route.flow}/${route.page} to a deployed App UI extension.`,
      { application: route.application, flow: route.flow, page: route.page }
    );
  }
  const uniqueMatches = new Map(matches.map((match) => [
    `${match.extension}\0${match.application}`,
    match,
  ]));
  if (uniqueMatches.size !== 1) {
    throw new RuntimeEvidenceError(
      'ROUTE_AMBIGUOUS',
      `App-info maps ${route.application}/${route.flow}/${route.page} to multiple App UI extensions.`,
      { matches: [...uniqueMatches.values()] }
    );
  }
  return [...uniqueMatches.values()][0];
}

function indexApplications(applications, shape) {
  const index = new Map();
  for (const application of applications) {
    if (!application || typeof application !== 'object') {
      throw new RuntimeEvidenceError(
        'MANIFEST_INVALID',
        `App-info ${shape} entries must contain JSON objects.`
      );
    }
    const id = String(application.id || '').trim();
    const version = String(application.version || '').trim();
    if (!id || !version) {
      throw new RuntimeEvidenceError(
        'MANIFEST_INVALID',
        `Every App UI entry in ${shape} must contain nonempty id and version fields.`
      );
    }
    validateIdentifier(id, 'App UI ID');
    validateIdentifier(version, `Version for ${id}`);
    if (index.has(id)) {
      throw new RuntimeEvidenceError(
        'APP_VERSION_AMBIGUOUS',
        `App-info ${shape} contains duplicate entries for ${id}.`
      );
    }
    index.set(id, {
      id,
      version,
      description: typeof application.description === 'string'
        ? application.description
        : null,
      dependencies: application.dependencies && typeof application.dependencies === 'object'
        ? application.dependencies
        : {},
      applications: normalizeRouteApplications(application),
      sourceVersion: typeof application.metadata?.['source.version'] === 'string'
        ? application.metadata['source.version']
        : null,
    });
  }
  return index;
}

function applicationIndexesAgree(left, right) {
  if (left.size !== right.size) return false;
  for (const [id, application] of left) {
    if (!right.has(id) || right.get(id).version !== application.version) return false;
  }
  return true;
}

function resolveApplicationIndex(payload) {
  if (!payload || Array.isArray(payload) || typeof payload !== 'object') {
    throw new RuntimeEvidenceError(
      'MANIFEST_INVALID',
      'App-info response must contain one JSON object.'
    );
  }
  const metadata = payload.metadata;
  const sections = Array.isArray(metadata) ? metadata : metadata ? [metadata] : [];
  const legacyApplications = [];
  for (const section of sections) {
    if (section && typeof section === 'object' && Array.isArray(section.applications)) {
      legacyApplications.push(...section.applications);
    }
  }

  const digest = payload.digest;
  let digestApplications = [];
  if (digest && typeof digest === 'object' && !Array.isArray(digest)) {
    const appUiInfo = digest['app-ui-info'];
    if (appUiInfo != null && !Array.isArray(appUiInfo)) {
      throw new RuntimeEvidenceError(
        'MANIFEST_INVALID',
        'App-info digest.app-ui-info must be an array.'
      );
    }
    digestApplications = appUiInfo || [];
  } else if (digest != null) {
    throw new RuntimeEvidenceError('MANIFEST_INVALID', 'App-info digest must be a JSON object.');
  }

  if (legacyApplications.length === 0 && digestApplications.length === 0) {
    throw new RuntimeEvidenceError(
      'MANIFEST_INVALID',
      'App-info response did not contain metadata.applications or digest.app-ui-info.'
    );
  }

  const legacyIndex = legacyApplications.length > 0
    ? indexApplications(legacyApplications, 'metadata.applications')
    : null;
  const digestIndex = digestApplications.length > 0
    ? indexApplications(digestApplications, 'digest.app-ui-info')
    : null;
  if (legacyIndex && digestIndex && !applicationIndexesAgree(legacyIndex, digestIndex)) {
    throw new RuntimeEvidenceError(
      'MANIFEST_AMBIGUOUS',
      'App-info metadata.applications and digest.app-ui-info disagree.'
    );
  }
  // Prefer the current digest representation after proving dual schemas agree.
  return digestIndex || legacyIndex;
}

function requireApplication(applicationIndex, extensionId) {
  const extension = validateIdentifier(extensionId, 'Extension ID');
  const application = applicationIndex.get(extension);
  if (!application) {
    throw new RuntimeEvidenceError(
      'APP_NOT_FOUND',
      `App-info response does not contain ${extension}.`,
      { availableExtensions: [...applicationIndex.keys()].sort().slice(0, 50) }
    );
  }
  return application;
}

function skipQuotedLiteral(source, start, quote) {
  for (let index = start + 1; index < source.length; index += 1) {
    const character = source[index];
    if (character === '\\') {
      index += 1;
    } else if (character === quote) {
      return index + 1;
    }
  }
  throw new RuntimeEvidenceError(
    'BUNDLE_FORMAT_UNSUPPORTED',
    'Bundle contains an unterminated string or template literal.'
  );
}

function skipTemplateExpression(source, start) {
  let braceDepth = 1;
  let cursor = start;
  while (cursor < source.length) {
    const character = source[cursor];
    if (character === '"' || character === "'") {
      cursor = skipQuotedLiteral(source, cursor, character);
      continue;
    }
    if (character === '`') {
      cursor = skipTemplateLiteral(source, cursor);
      continue;
    }
    if (character === '/' && source[cursor + 1] === '/') {
      cursor = skipLineComment(source, cursor);
      continue;
    }
    if (character === '/' && source[cursor + 1] === '*') {
      cursor = skipBlockComment(source, cursor);
      continue;
    }
    if (character === '/' && isRegexStart(source, cursor)) {
      cursor = skipRegexLiteral(source, cursor);
      continue;
    }
    if (character === '{') braceDepth += 1;
    if (character === '}') {
      braceDepth -= 1;
      if (braceDepth === 0) return cursor + 1;
    }
    cursor += 1;
  }
  throw new RuntimeEvidenceError(
    'BUNDLE_FORMAT_UNSUPPORTED',
    'Bundle contains an unterminated template-literal expression.'
  );
}

function skipTemplateLiteral(source, start) {
  for (let index = start + 1; index < source.length; index += 1) {
    const character = source[index];
    if (character === '\\') {
      index += 1;
    } else if (character === '`') {
      return index + 1;
    } else if (character === '$' && source[index + 1] === '{') {
      // Nested code is scanned recursively so inner templates cannot close the outer one.
      index = skipTemplateExpression(source, index + 2) - 1;
    }
  }
  throw new RuntimeEvidenceError(
    'BUNDLE_FORMAT_UNSUPPORTED',
    'Bundle contains an unterminated template literal.'
  );
}

function skipLineComment(source, start) {
  let index = start + 2;
  while (index < source.length && source[index] !== '\n' && source[index] !== '\r') {
    index += 1;
  }
  return index;
}

function skipBlockComment(source, start) {
  const end = source.indexOf('*/', start + 2);
  if (end < 0) {
    throw new RuntimeEvidenceError(
      'BUNDLE_FORMAT_UNSUPPORTED',
      'Bundle contains an unterminated block comment.'
    );
  }
  return end + 2;
}

function previousCodeToken(source, index) {
  let cursor = index - 1;
  while (cursor >= 0 && /\s/.test(source[cursor])) cursor -= 1;
  if (cursor < 0) return '';
  if (/[A-Za-z0-9_$]/.test(source[cursor])) {
    const end = cursor + 1;
    while (cursor >= 0 && /[A-Za-z0-9_$]/.test(source[cursor])) cursor -= 1;
    return source.slice(cursor + 1, end);
  }
  return source[cursor];
}

function isRegexStart(source, index) {
  const token = previousCodeToken(source, index);
  return (
    !token
    || /^[([{,:;=!?&|+*%^~<>-]$/.test(token)
    || new Set([
      'return', 'case', 'throw', 'delete', 'void', 'typeof', 'instanceof',
      'in', 'of', 'yield', 'await', 'else', 'do',
    ]).has(token)
  );
}

function skipRegexLiteral(source, start) {
  let inCharacterClass = false;
  for (let index = start + 1; index < source.length; index += 1) {
    const character = source[index];
    if (character === '\\') {
      index += 1;
    } else if (character === '[') {
      inCharacterClass = true;
    } else if (character === ']') {
      inCharacterClass = false;
    } else if (character === '/' && !inCharacterClass) {
      index += 1;
      while (index < source.length && /[A-Za-z]/.test(source[index])) index += 1;
      return index;
    } else if (character === '\n' || character === '\r') {
      break;
    }
  }
  throw new RuntimeEvidenceError(
    'BUNDLE_FORMAT_UNSUPPORTED',
    'Bundle contains an unterminated regular-expression literal.'
  );
}

function skipWhitespaceAndComments(source, start) {
  let index = start;
  while (index < source.length) {
    if (/\s/.test(source[index])) {
      index += 1;
    } else if (source[index] === '/' && source[index + 1] === '/') {
      index = skipLineComment(source, index);
    } else if (source[index] === '/' && source[index + 1] === '*') {
      index = skipBlockComment(source, index);
    } else {
      break;
    }
  }
  return index;
}

function decodeJsStringLiteral(source, start = 0) {
  const quote = source[start];
  if (quote !== '"' && quote !== "'") {
    throw new RuntimeEvidenceError(
      'BUNDLE_FORMAT_UNSUPPORTED',
      'Expected a quoted JavaScript string literal.'
    );
  }
  let value = '';
  for (let index = start + 1; index < source.length; index += 1) {
    const character = source[index];
    if (character === quote) {
      return { value, end: index + 1 };
    }
    if (character !== '\\') {
      if (character === '\n' || character === '\r') {
        throw new RuntimeEvidenceError(
          'BUNDLE_FORMAT_UNSUPPORTED',
          'JavaScript string literal contains an unescaped line break.'
        );
      }
      value += character;
      continue;
    }

    index += 1;
    const escaped = source[index];
    const simpleEscapes = {
      b: '\b',
      f: '\f',
      n: '\n',
      r: '\r',
      t: '\t',
      v: '\v',
      '0': '\0',
      '\\': '\\',
      '"': '"',
      "'": "'",
    };
    if (Object.prototype.hasOwnProperty.call(simpleEscapes, escaped)) {
      if (escaped === '0' && /[0-9]/.test(source[index + 1] || '')) {
        throw new RuntimeEvidenceError(
          'BUNDLE_FORMAT_UNSUPPORTED',
          'Legacy octal string escapes are not supported.'
        );
      }
      value += simpleEscapes[escaped];
    } else if (escaped === 'x') {
      const digits = source.slice(index + 1, index + 3);
      if (!/^[0-9A-Fa-f]{2}$/.test(digits)) {
        throw new RuntimeEvidenceError('BUNDLE_FORMAT_UNSUPPORTED', 'Invalid hex escape.');
      }
      value += String.fromCharCode(Number.parseInt(digits, 16));
      index += 2;
    } else if (escaped === 'u') {
      if (source[index + 1] === '{') {
        const close = source.indexOf('}', index + 2);
        const digits = close < 0 ? '' : source.slice(index + 2, close);
        const codePoint = /^[0-9A-Fa-f]{1,6}$/.test(digits)
          ? Number.parseInt(digits, 16)
          : Number.NaN;
        if (!Number.isFinite(codePoint) || codePoint > 0x10ffff) {
          throw new RuntimeEvidenceError('BUNDLE_FORMAT_UNSUPPORTED', 'Invalid Unicode escape.');
        }
        value += String.fromCodePoint(codePoint);
        index = close;
      } else {
        const digits = source.slice(index + 1, index + 5);
        if (!/^[0-9A-Fa-f]{4}$/.test(digits)) {
          throw new RuntimeEvidenceError('BUNDLE_FORMAT_UNSUPPORTED', 'Invalid Unicode escape.');
        }
        value += String.fromCharCode(Number.parseInt(digits, 16));
        index += 4;
      }
    } else if (escaped === '\n') {
      // JavaScript line continuations contribute no character to the decoded text.
    } else if (escaped === '\r') {
      if (source[index + 1] === '\n') index += 1;
    } else {
      // JavaScript permits escaping a non-special character as that character.
      value += escaped;
    }
  }
  throw new RuntimeEvidenceError(
    'BUNDLE_FORMAT_UNSUPPORTED',
    'Bundle contains an unterminated JavaScript string literal.'
  );
}

function parseNamedDefine(source, start) {
  const openParenthesis = skipWhitespaceAndComments(source, start + 'define'.length);
  if (source[openParenthesis] !== '(') return null;
  let cursor = skipWhitespaceAndComments(source, openParenthesis + 1);
  if (source[cursor] !== '"' && source[cursor] !== "'") return null;
  const identifier = decodeJsStringLiteral(source, cursor);

  let depth = 1;
  cursor = openParenthesis + 1;
  while (cursor < source.length) {
    const character = source[cursor];
    if (character === '"' || character === "'") {
      cursor = skipQuotedLiteral(source, cursor, character);
      continue;
    }
    if (character === '`') {
      cursor = skipTemplateLiteral(source, cursor);
      continue;
    }
    if (character === '/' && source[cursor + 1] === '/') {
      cursor = skipLineComment(source, cursor);
      continue;
    }
    if (character === '/' && source[cursor + 1] === '*') {
      cursor = skipBlockComment(source, cursor);
      continue;
    }
    if (character === '/' && isRegexStart(source, cursor)) {
      cursor = skipRegexLiteral(source, cursor);
      continue;
    }
    if (character === '(') depth += 1;
    if (character === ')') {
      depth -= 1;
      if (depth === 0) {
        return {
          id: identifier.value,
          source: source.slice(start, cursor + 1),
          start,
          end: cursor + 1,
        };
      }
    }
    cursor += 1;
  }
  throw new RuntimeEvidenceError(
    'BUNDLE_FORMAT_UNSUPPORTED',
    `Named AMD module ${identifier.value} has no closing parenthesis.`
  );
}

function scanNamedAmdModules(source) {
  const modules = [];
  let parenthesisDepth = 0;
  let braceDepth = 0;
  let bracketDepth = 0;
  let cursor = 0;
  while (cursor < source.length) {
    const character = source[cursor];
    if (character === '"' || character === "'") {
      cursor = skipQuotedLiteral(source, cursor, character);
      continue;
    }
    if (character === '`') {
      cursor = skipTemplateLiteral(source, cursor);
      continue;
    }
    if (character === '/' && source[cursor + 1] === '/') {
      cursor = skipLineComment(source, cursor);
      continue;
    }
    if (character === '/' && source[cursor + 1] === '*') {
      cursor = skipBlockComment(source, cursor);
      continue;
    }
    if (character === '/' && isRegexStart(source, cursor)) {
      cursor = skipRegexLiteral(source, cursor);
      continue;
    }

    const atTopLevel = parenthesisDepth === 0 && braceDepth === 0 && bracketDepth === 0;
    if (
      atTopLevel
      && source.startsWith('define', cursor)
      && !/[A-Za-z0-9_$]/.test(source[cursor - 1] || '')
      && !/[A-Za-z0-9_$]/.test(source[cursor + 'define'.length] || '')
    ) {
      const module = parseNamedDefine(source, cursor);
      if (module) {
        modules.push(module);
        cursor = module.end;
        continue;
      }
    }

    if (character === '(') parenthesisDepth += 1;
    if (character === ')') parenthesisDepth = Math.max(0, parenthesisDepth - 1);
    if (character === '{') braceDepth += 1;
    if (character === '}') braceDepth = Math.max(0, braceDepth - 1);
    if (character === '[') bracketDepth += 1;
    if (character === ']') bracketDepth = Math.max(0, bracketDepth - 1);
    cursor += 1;
  }
  return modules;
}

function extractTextModuleValue(moduleSource, moduleId) {
  let cursor = moduleSource.indexOf(',');
  if (cursor < 0) {
    throw new RuntimeEvidenceError(
      'BUNDLE_FORMAT_UNSUPPORTED',
      `Text module ${moduleId} has no dependency list.`
    );
  }
  const factoryMatch = moduleSource.slice(cursor).match(
    /^,\s*\[\s*\]\s*,\s*function\s*\(\s*\)\s*\{\s*return\s*/
  );
  if (!factoryMatch) {
    throw new RuntimeEvidenceError(
      'BUNDLE_FORMAT_UNSUPPORTED',
      `Text module ${moduleId} does not use the supported zero-dependency text factory.`
    );
  }
  cursor += factoryMatch[0].length;
  const decoded = decodeJsStringLiteral(moduleSource, cursor);
  const tail = moduleSource.slice(decoded.end);
  if (!/^\s*;?\s*\}\s*\)\s*$/.test(tail)) {
    throw new RuntimeEvidenceError(
      'BUNDLE_FORMAT_UNSUPPORTED',
      `Text module ${moduleId} contains executable factory content.`
    );
  }
  return decoded.value;
}

function splitModuleId(moduleId, extensionId) {
  const separator = moduleId.indexOf('!');
  const plugin = separator >= 0 ? moduleId.slice(0, separator) : null;
  const unwrappedId = separator >= 0 ? moduleId.slice(separator + 1) : moduleId;
  const prefix = `vx/${extensionId}/`;
  if (!unwrappedId.startsWith(prefix)) return null;
  const logicalPath = unwrappedId.slice(prefix.length);
  if (!logicalPath) return null;
  const segments = logicalPath.split('/');
  if (segments.some((segment) => (
    !segment
    || segment === '.'
    || segment === '..'
    || segment.includes('\\')
    || segment.includes('\0')
  ))) {
    throw new RuntimeEvidenceError(
      'UNSAFE_MODULE_PATH',
      `Module ${moduleId} contains an unsafe logical path.`
    );
  }
  return { plugin, logicalPath, segments };
}

function detectMediaType(logicalPath) {
  if (logicalPath.endsWith('.json')) return 'application/json';
  if (logicalPath.endsWith('.html')) return 'text/html';
  if (logicalPath.endsWith('.css')) return 'text/css';
  if (logicalPath.endsWith('.js')) return 'text/javascript';
  return 'text/plain';
}

function buildModuleStoragePath(parts, kind) {
  const encodedSegments = parts.segments.map(encodeCacheSegment);
  if (kind === 'text') return path.join('modules', 'text', ...encodedSegments);
  const last = `${encodedSegments.pop()}.amd.js`;
  return path.join('modules', 'amd', ...encodedSegments, last);
}

function parseBundle(source, extensionId) {
  const extension = validateIdentifier(extensionId, 'Extension ID');
  const seenIds = new Set();
  const seenStoragePaths = new Set();
  const parsedModules = [];
  for (const scanned of scanNamedAmdModules(source)) {
    const parts = splitModuleId(scanned.id, extension);
    if (!parts) continue;
    if (seenIds.has(scanned.id)) {
      throw new RuntimeEvidenceError(
        'DUPLICATE_MODULE',
        `Bundle contains duplicate module ID ${scanned.id}.`
      );
    }
    seenIds.add(scanned.id);

    const kind = parts.plugin === 'text' ? 'text' : 'amd';
    const content = kind === 'text'
      ? extractTextModuleValue(scanned.source, scanned.id)
      : `${scanned.source};\n`;
    if (kind === 'text' && parts.logicalPath.endsWith('.json')) {
      try {
        JSON.parse(content);
      } catch (error) {
        throw new RuntimeEvidenceError(
          'MODULE_JSON_INVALID',
          `Text module ${scanned.id} is not valid JSON: ${error.message}`
        );
      }
    }
    const relativePath = buildModuleStoragePath(parts, kind).split(path.sep).join('/');
    if (seenStoragePaths.has(relativePath)) {
      throw new RuntimeEvidenceError(
        'DUPLICATE_MODULE_PATH',
        `Bundle modules collide at cache path ${relativePath}.`
      );
    }
    seenStoragePaths.add(relativePath);
    parsedModules.push({
      id: scanned.id,
      plugin: parts.plugin,
      logicalPath: parts.logicalPath,
      kind,
      mediaType: detectMediaType(parts.logicalPath),
      relativePath,
      sha256: sha256(content),
      sizeBytes: Buffer.byteLength(content),
      sourceOffset: scanned.start,
      content,
    });
  }
  if (parsedModules.length === 0) {
    throw new RuntimeEvidenceError(
      'BUNDLE_FORMAT_UNSUPPORTED',
      `Bundle contains no named modules for ${extension}.`
    );
  }
  return parsedModules.sort((left, right) => left.id.localeCompare(right.id));
}

function resolveCachePaths(workspace, applicationUrl, extensionId, version, cacheRootOverride = null) {
  const resolvedWorkspace = path.resolve(workspace || process.cwd());
  const environment = new URL(applicationUrl);
  if (environment.protocol !== 'https:' || environment.username || environment.password) {
    throw new RuntimeEvidenceError(
      'INVALID_ENVIRONMENT_URL',
      'Cache environment identity must be an HTTPS URL without embedded credentials.'
    );
  }
  const extension = validateIdentifier(extensionId, 'Extension ID');
  const deployedVersion = validateIdentifier(version, 'Extension version');
  const hostLabel = environment.host.toLowerCase().replace(/[^a-z0-9.-]+/g, '-');
  const environmentKey = `${hostLabel}-${sha256(environment.origin).slice(0, 12)}`;
  // An explicit root lets all implementation projects reuse one validated cache.
  const cacheRoot = cacheRootOverride
    ? path.resolve(cacheRootOverride)
    : path.join(resolvedWorkspace, CACHE_DIRECTORY_NAME);
  const cacheParent = cacheRootOverride ? path.dirname(cacheRoot) : resolvedWorkspace;
  const schemaRoot = safeJoin(cacheRoot, `v${CACHE_SCHEMA_VERSION}`, environmentKey);
  const versionDirectory = safeJoin(
    schemaRoot,
    'extensions',
    encodeCacheSegment(extension),
    encodeCacheSegment(deployedVersion)
  );
  return {
    workspace: resolvedWorkspace,
    cacheParent,
    cacheRoot,
    schemaRoot,
    environmentKey,
    versionDirectory,
    manifestPath: path.join(versionDirectory, MANIFEST_FILE),
    indexPath: path.join(versionDirectory, INDEX_FILE),
    completePath: path.join(versionDirectory, COMPLETE_FILE),
    lockPath: `${versionDirectory}.lock`,
  };
}

function assertNoSymlinkBetween(root, target) {
  const resolvedRoot = path.resolve(root);
  const resolvedTarget = path.resolve(target);
  const relative = path.relative(resolvedRoot, resolvedTarget);
  if (relative.startsWith('..') || path.isAbsolute(relative)) {
    throw new RuntimeEvidenceError('UNSAFE_CACHE_PATH', 'Cache target escapes its root.');
  }
  let current = resolvedRoot;
  for (const segment of relative.split(path.sep).filter(Boolean)) {
    current = path.join(current, segment);
    if (fs.existsSync(current) && fs.lstatSync(current).isSymbolicLink()) {
      throw new RuntimeEvidenceError(
        'UNSAFE_CACHE_PATH',
        `Cache path must not traverse a symbolic link: ${current}`
      );
    }
  }
}

function ensureCacheRoot(paths) {
  if (fs.existsSync(paths.cacheRoot) && fs.lstatSync(paths.cacheRoot).isSymbolicLink()) {
    throw new RuntimeEvidenceError('UNSAFE_CACHE_PATH', 'Evidence cache root is a symlink.');
  }
  fs.mkdirSync(paths.cacheRoot, { recursive: true, mode: 0o700 });
  // Validate from the cache parent because a shared cache may sit outside the report workspace.
  assertNoSymlinkBetween(paths.cacheParent || paths.workspace, paths.cacheRoot);
  const ignorePath = path.join(paths.cacheRoot, '.gitignore');
  if (!fs.existsSync(ignorePath)) {
    // The cache owns its ignore marker and never changes the repository's tracked ignore file.
    fs.writeFileSync(ignorePath, '*\n', { mode: 0o600, flag: 'wx' });
  }
}

function readJsonFile(filePath, code, label) {
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (error) {
    throw new RuntimeEvidenceError(code, `${label}: ${error.message}`);
  }
}

function loadBundleCache(paths, expected = {}) {
  if (!fs.existsSync(paths.completePath)) return null;
  assertNoSymlinkBetween(paths.cacheRoot, paths.versionDirectory);
  const manifest = readJsonFile(paths.manifestPath, 'CACHE_CORRUPT', 'Invalid cache manifest');
  let indexText;
  let index;
  try {
    indexText = fs.readFileSync(paths.indexPath, 'utf8');
    index = JSON.parse(indexText);
  } catch (error) {
    throw new RuntimeEvidenceError('CACHE_CORRUPT', `Invalid module index: ${error.message}`);
  }
  if (
    manifest.schemaVersion !== CACHE_SCHEMA_VERSION
    || !manifest.extension
    || manifest.extension.id !== expected.extensionId
    || manifest.extension.version !== expected.version
    || !manifest.cdn
    || !/^[a-f0-9]{64}$/.test(manifest.cdn.sha256 || '')
    || !/^[a-f0-9]{64}$/.test(manifest.indexSha256 || '')
    || sha256(indexText) !== manifest.indexSha256
    || index.schemaVersion !== CACHE_SCHEMA_VERSION
    || index.extension?.id !== expected.extensionId
    || index.extension?.version !== expected.version
    || !Array.isArray(index.modules)
  ) {
    throw new RuntimeEvidenceError(
      'CACHE_CORRUPT',
      `Cached bundle metadata does not match ${expected.extensionId}@${expected.version}.`
    );
  }
  let completeHash;
  let bundleContent;
  const bundlePath = path.join(paths.versionDirectory, 'base-config-bundle.js');
  try {
    completeHash = fs.readFileSync(paths.completePath, 'utf8').trim();
    bundleContent = fs.readFileSync(bundlePath);
  } catch (error) {
    throw new RuntimeEvidenceError(
      'CACHE_CORRUPT',
      `Cached bundle files are incomplete for ${expected.extensionId}@${expected.version}: ${error.message}`
    );
  }
  if (
    completeHash !== manifest.cdn.sha256
    || sha256(bundleContent) !== manifest.cdn.sha256
  ) {
    throw new RuntimeEvidenceError(
      'CACHE_CORRUPT',
      `Cached bundle hash does not match ${expected.extensionId}@${expected.version}.`
    );
  }

  const seenIds = new Set();
  const seenPaths = new Set();
  for (const module of index.modules) {
    if (
      !module
      || typeof module.id !== 'string'
      || seenIds.has(module.id)
      || (module.kind !== 'text' && module.kind !== 'amd')
      || typeof module.relativePath !== 'string'
      || seenPaths.has(module.relativePath)
      || !/^[a-f0-9]{64}$/.test(module.sha256 || '')
      || !Number.isSafeInteger(module.sizeBytes)
      || module.sizeBytes < 0
    ) {
      throw new RuntimeEvidenceError(
        'CACHE_CORRUPT',
        `Cached module index is invalid for ${expected.extensionId}@${expected.version}.`
      );
    }
    // Resolving every indexed path detects traversal before any selected evidence is read.
    const modulePath = safeJoin(paths.versionDirectory, ...module.relativePath.split('/'));
    try {
      assertNoSymlinkBetween(paths.versionDirectory, modulePath);
      const content = fs.readFileSync(modulePath);
      if (sha256(content) !== module.sha256 || content.length !== module.sizeBytes) {
        throw new Error('content hash or size does not match the module index');
      }
    } catch (error) {
      throw new RuntimeEvidenceError(
        'CACHE_CORRUPT',
        `Cached module ${module.id} is invalid: ${error.message}`
      );
    }
    seenIds.add(module.id);
    seenPaths.add(module.relativePath);
  }
  return {
    paths,
    manifest,
    index,
    moduleMap: new Map(index.modules.map((module) => [module.id, module])),
  };
}

function writeJson(filePath, value) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true, mode: 0o700 });
  fs.writeFileSync(filePath, serializeJson(value), { mode: 0o600 });
}

function serializeJson(value) {
  return `${JSON.stringify(value, null, 2)}\n`;
}

function publishBundleCache(paths, bundleText, metadata) {
  const expectedBundleUrl = buildBundleUrl(
    metadata.extension?.id,
    metadata.extension?.version,
    resolveCdnOrigin(metadata.environment)
  ).toString();
  if (metadata.bundleUrl !== expectedBundleUrl) {
    throw new RuntimeEvidenceError(
      'UNSAFE_REQUEST_URL',
      `Cache publication requires the fixed Oracle CDN URL for ${metadata.extension?.id}.`
    );
  }
  ensureCacheRoot(paths);
  fs.mkdirSync(path.dirname(paths.versionDirectory), { recursive: true, mode: 0o700 });
  assertNoSymlinkBetween(paths.cacheRoot, path.dirname(paths.versionDirectory));
  const suffix = `${process.pid}-${Date.now()}-${crypto.randomBytes(6).toString('hex')}`;
  const stagingDirectory = safeJoin(
    path.dirname(paths.versionDirectory),
    `.staging-${path.basename(paths.versionDirectory)}-${suffix}`
  );
  fs.mkdirSync(stagingDirectory, { recursive: false, mode: 0o700 });
  try {
    const modules = parseBundle(bundleText, metadata.extension.id);
    const indexModules = [];
    for (const module of modules) {
      const destination = safeJoin(stagingDirectory, ...module.relativePath.split('/'));
      fs.mkdirSync(path.dirname(destination), { recursive: true, mode: 0o700 });
      fs.writeFileSync(destination, module.content, { mode: 0o600 });
      const { content, ...record } = module;
      indexModules.push(record);
    }

    const bundlePath = path.join(stagingDirectory, 'base-config-bundle.js');
    fs.writeFileSync(bundlePath, bundleText, { mode: 0o600 });
    const bundleHash = sha256(bundleText);
    const index = {
      schemaVersion: CACHE_SCHEMA_VERSION,
      extension: metadata.extension,
      modules: indexModules,
    };
    const indexText = serializeJson(index);
    const manifest = {
      schemaVersion: CACHE_SCHEMA_VERSION,
      environment: metadata.environment,
      extension: metadata.extension,
      cdn: {
        url: metadata.bundleUrl,
        sha256: bundleHash,
        sizeBytes: Buffer.byteLength(bundleText),
        etag: metadata.headers?.etag || null,
        lastModified: metadata.headers?.lastModified || null,
        contentType: metadata.headers?.contentType || null,
        fetchedAt: metadata.fetchedAt || new Date().toISOString(),
      },
      // Bind extracted-module metadata to the completed cache publication.
      indexSha256: sha256(indexText),
      moduleCount: indexModules.length,
    };
    writeJson(path.join(stagingDirectory, MANIFEST_FILE), manifest);
    fs.writeFileSync(path.join(stagingDirectory, INDEX_FILE), indexText, { mode: 0o600 });
    fs.writeFileSync(path.join(stagingDirectory, COMPLETE_FILE), `${bundleHash}\n`, {
      mode: 0o600,
    });

    if (fs.existsSync(paths.versionDirectory)) {
      const corruptPath = `${paths.versionDirectory}.corrupt-${suffix}`;
      fs.renameSync(paths.versionDirectory, corruptPath);
    }
    fs.renameSync(stagingDirectory, paths.versionDirectory);
    return loadBundleCache(paths, {
      extensionId: metadata.extension.id,
      version: metadata.extension.version,
    });
  } catch (error) {
    fs.rmSync(stagingDirectory, { recursive: true, force: true });
    throw error;
  }
}

function isProcessAlive(pid) {
  if (!Number.isInteger(pid) || pid <= 0) return false;
  try {
    process.kill(pid, 0);
    return true;
  } catch (error) {
    return error.code === 'EPERM';
  }
}

function wait(delayMs) {
  return new Promise((resolve) => setTimeout(resolve, delayMs));
}

async function acquireCacheLock(paths, options = {}) {
  const timeoutMs = options.timeoutMs || 300000;
  const pollMs = options.pollMs || 100;
  const startedAt = Date.now();
  ensureCacheRoot(paths);
  fs.mkdirSync(path.dirname(paths.lockPath), { recursive: true, mode: 0o700 });
  assertNoSymlinkBetween(paths.cacheRoot, path.dirname(paths.lockPath));
  while (true) {
    try {
      fs.mkdirSync(paths.lockPath, { mode: 0o700 });
      writeJson(path.join(paths.lockPath, 'owner.json'), {
        pid: process.pid,
        createdAt: new Date().toISOString(),
      });
      let released = false;
      return {
        release() {
          if (released) return;
          released = true;
          // The lock directory is owned by this process and contains no user data.
          fs.rmSync(paths.lockPath, { recursive: true, force: true });
        },
      };
    } catch (error) {
      if (error.code !== 'EEXIST') throw error;
      const ownerPath = path.join(paths.lockPath, 'owner.json');
      let owner = null;
      try {
        owner = JSON.parse(fs.readFileSync(ownerPath, 'utf8'));
      } catch {
        // A writer can briefly exist before owner.json is visible; bounded waiting handles it.
      }
      const lockAge = fs.existsSync(paths.lockPath)
        ? Date.now() - fs.statSync(paths.lockPath).mtimeMs
        : 0;
      if (owner && lockAge > timeoutMs * 2 && !isProcessAlive(Number(owner.pid))) {
        const stalePath = `${paths.lockPath}.stale-${Date.now()}`;
        try {
          fs.renameSync(paths.lockPath, stalePath);
          continue;
        } catch (renameError) {
          if (renameError.code !== 'ENOENT') throw renameError;
        }
      }
      if (Date.now() - startedAt >= timeoutMs) {
        throw new RuntimeEvidenceError(
          'CACHE_LOCK_TIMEOUT',
          `Timed out waiting for cache lock ${paths.lockPath}.`
        );
      }
      await wait(pollMs);
    }
  }
}

function readCachedModule(cache, moduleOrId) {
  const record = typeof moduleOrId === 'string'
    ? cache.moduleMap.get(moduleOrId)
    : moduleOrId;
  if (!record) {
    throw new RuntimeEvidenceError('MODULE_NOT_FOUND', `Cached module was not found.`);
  }
  const filePath = safeJoin(cache.paths.versionDirectory, ...record.relativePath.split('/'));
  assertNoSymlinkBetween(cache.paths.versionDirectory, filePath);
  const content = fs.readFileSync(filePath, 'utf8');
  if (sha256(content) !== record.sha256) {
    throw new RuntimeEvidenceError(
      'CACHE_CORRUPT',
      `Cached module hash does not match ${record.id}.`
    );
  }
  return { record, content, filePath };
}

module.exports = {
  CACHE_DIRECTORY_NAME,
  CACHE_SCHEMA_VERSION,
  CDN_ORIGIN,
  RuntimeEvidenceError,
  acquireCacheLock,
  assertNoSymlinkBetween,
  buildAppInfoEndpoint,
  buildBundleUrl,
  resolveCdnOrigin,
  decodeJsStringLiteral,
  ensureCacheRoot,
  extractTextModuleValue,
  applicationIndexesAgree,
  indexApplications,
  loadBundleCache,
  parseBundle,
  parseRedwoodRouteUrl,
  publishBundleCache,
  readCachedModule,
  requireApplication,
  resolveApplicationIndex,
  resolveApplicationFromRoute,
  resolveCachePaths,
  safeJoin,
  scanNamedAmdModules,
  skipTemplateLiteral,
  sha256,
  validateIdentifier,
};
