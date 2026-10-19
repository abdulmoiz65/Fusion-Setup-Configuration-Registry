#!/usr/bin/env node
'use strict';

/**
 * Convert changed Express Mode page artifacts into deterministic Fusion URLs.
 * This module is intentionally pure: it does not read Git, persist sidecars,
 * send credentials, or make network requests.
 */

const crypto = require('node:crypto');
const path = require('node:path');

// Fusion page verification uses one runtime shell for every supported extension family.
const DEFAULT_UI_PREFIX = 'fscmUI';
const BASE_EXTENSION_ROUTES = new Map([
  ['hcm_extension', DEFAULT_UI_PREFIX],
  ['fscm_extension', DEFAULT_UI_PREFIX],
  ['scm_extension', DEFAULT_UI_PREFIX],
  ['prc_extension', DEFAULT_UI_PREFIX],
  ['cx_extension', DEFAULT_UI_PREFIX],
]);

function normalizeBaseExtension(value) {
  const normalized = String(value || '').trim().toLowerCase();
  for (const baseExtension of BASE_EXTENSION_ROUTES.keys()) {
    if (normalized === baseExtension || normalized.endsWith(`_${baseExtension}`)) {
      return baseExtension;
    }
  }
  return null;
}

function resolveBaseExtension(repo, extensionId) {
  const repositoryEvidence = normalizeBaseExtension(path.basename(path.resolve(repo)));
  const metadataEvidence = normalizeBaseExtension(extensionId);
  if (
    repositoryEvidence
    && metadataEvidence
    && repositoryEvidence !== metadataEvidence
  ) {
    return {
      baseExtension: null,
      uiPrefix: DEFAULT_UI_PREFIX,
      source: 'conflict',
      reason: (
        `Repository implies ${repositoryEvidence}, but extension metadata implies `
        + `${metadataEvidence}.`
      ),
    };
  }

  const baseExtension = repositoryEvidence || metadataEvidence;
  return {
    baseExtension,
    uiPrefix: DEFAULT_UI_PREFIX,
    source: repositoryEvidence ? 'repository-name' : metadataEvidence ? 'extension-id' : null,
    reason: baseExtension
      ? null
      : (
        'Extension family is unknown, but deployed page URLs still use fscmUI.'
      ),
  };
}

function derivePageId(pageArtifact) {
  const suffixes = [
    '-page-rules-x.json',
    '-page-rules-x.js',
    '-page-x.json',
    '-page-x.js',
    '-page-x.html',
    '-page-chains',
    '-page.json',
    '-page.js',
    '-page.html',
  ];
  const suffix = suffixes.find((candidate) => pageArtifact.endsWith(candidate));
  return suffix ? pageArtifact.slice(0, -suffix.length) || null : null;
}

function deriveRouteTarget(relativePath, pillar) {
  // Git paths use forward slashes, while injected test paths may use platform separators.
  const portablePath = String(relativePath || '').split(path.sep).join('/');
  const segments = portablePath.split('/');
  const applicationsIndex = segments.indexOf('applications');
  if (
    applicationsIndex < 0
    || applicationsIndex < 4
    || segments[0] !== 'extension1'
    || segments[1] !== 'sources'
    || segments[2] !== 'ui'
  ) {
    return {
      file: portablePath,
      reason: 'Changed file is not under a supported UI application path.',
    };
  }

  const producer = segments[3];
  const application = segments[applicationsIndex + 1];
  if (!producer || !application) {
    return {
      file: portablePath,
      reason: 'Changed UI path does not identify both producer and application.',
    };
  }

  const flows = [];
  let page = null;
  let pageArtifact = null;
  for (let index = applicationsIndex + 2; index < segments.length; index += 1) {
    if (segments[index] === 'flows' && segments[index + 1]) {
      flows.push(segments[index + 1]);
      index += 1;
    } else if (segments[index] === 'pages' && segments[index + 1]) {
      pageArtifact = segments[index + 1];
      page = derivePageId(pageArtifact);
      break;
    }
  }
  if (pageArtifact && !page) {
    return {
      file: portablePath,
      producer,
      application,
      flows,
      reason: `Unable to derive a logical page id from ${pageArtifact}.`,
    };
  }

  const routeSegments = [application, ...flows];
  if (page) {
    routeSegments.push(page);
  }
  if (!pillar.uiPrefix) {
    return {
      file: portablePath,
      producer,
      application,
      flows,
      page,
      reason: pillar.reason,
    };
  }

  return {
    key: `${pillar.uiPrefix}/${routeSegments.join('/')}`,
    producer,
    application,
    flows,
    flow: flows.length > 0 ? flows[flows.length - 1] : null,
    page,
    routeSegments,
    uiPrefix: pillar.uiPrefix,
    baseExtension: pillar.baseExtension,
    changedFiles: [portablePath],
  };
}

function resolveChangedTargets(repo, extensionId, changedFiles, options = {}) {
  if (options.uiTarget && options.uiTarget !== DEFAULT_UI_PREFIX) {
    throw new Error(`UI target must be ${DEFAULT_UI_PREFIX}.`);
  }
  const detectedPillar = resolveBaseExtension(repo, extensionId);
  const pillar = options.uiTarget
    ? {
        ...detectedPillar,
        uiPrefix: DEFAULT_UI_PREFIX,
        source: 'user-selected-target',
      }
    : detectedPillar;
  const targetMap = new Map();
  const unresolvedTargets = [];

  for (const relativePath of changedFiles) {
    const candidate = deriveRouteTarget(relativePath, pillar);
    if (!candidate.key) {
      unresolvedTargets.push(candidate);
      continue;
    }

    const existing = targetMap.get(candidate.key);
    if (existing) {
      // Multiple changed artifacts belonging to one page produce one URL.
      existing.changedFiles.push(...candidate.changedFiles);
    } else {
      targetMap.set(candidate.key, candidate);
    }
  }

  return {
    pillar,
    targets: [...targetMap.values()]
      .map((target) => ({
        ...target,
        changedFiles: [...new Set(target.changedFiles)].sort(),
      }))
      .sort((left, right) => left.key.localeCompare(right.key)),
    unresolvedTargets,
  };
}

/** Convert a user-supplied Redwood URL into a route plus its exact page context. */
function deriveExplicitRouteTarget(route) {
  let parsed;
  try {
    parsed = new URL(String(route || ''), 'https://route.invalid');
  } catch (error) {
    return {
      route: String(route || ''),
      reason: `Unable to parse the supplied Redwood route: ${error.message}`,
    };
  }

  let pathSegments;
  try {
    pathSegments = parsed.pathname
      .split('/')
      .filter(Boolean)
      .map((segment) => decodeURIComponent(segment));
  } catch (error) {
    return {
      route: parsed.pathname,
      reason: `Unable to decode the supplied Redwood route: ${error.message}`,
    };
  }
  if (
    pathSegments[0] !== DEFAULT_UI_PREFIX
    || pathSegments[1] !== 'redwood'
    || pathSegments.length < 3
  ) {
    return {
      route: parsed.pathname,
      reason: `Deployment routes must begin with /${DEFAULT_UI_PREFIX}/redwood/.`,
    };
  }

  const routeSegments = pathSegments.slice(2);
  const routeKey = `${DEFAULT_UI_PREFIX}/${routeSegments.join('/')}`;
  const suppliedSearch = parsed.search;
  const suppliedHash = parsed.hash;
  // Hash the context for internal deduplication so target keys do not expose PII.
  const contextDigest = suppliedSearch || suppliedHash
    ? crypto.createHash('sha256')
      .update(`${suppliedSearch}\u0000${suppliedHash}`)
      .digest('hex')
      .slice(0, 16)
    : null;
  return {
    key: contextDigest ? `${routeKey}#context-${contextDigest}` : routeKey,
    routeKey,
    producer: null,
    application: routeSegments[0],
    flows: routeSegments.slice(1, -1),
    flow: routeSegments.length > 1 ? routeSegments.at(-2) : null,
    page: routeSegments.at(-1),
    routeSegments,
    uiPrefix: DEFAULT_UI_PREFIX,
    baseExtension: null,
    changedFiles: [],
    // Retain the user-provided transaction context for the returned deployment URL.
    suppliedRoute: `${parsed.pathname}${suppliedSearch}${suppliedHash}`,
    suppliedSearch,
    suppliedHash,
  };
}

/** Resolve and deduplicate explicit Redwood routes without reading Git state. */
function resolveExplicitRouteTargets(routes) {
  const targets = new Map();
  const unresolvedTargets = [];
  for (const route of routes || []) {
    const candidate = deriveExplicitRouteTarget(route);
    if (!candidate.key) {
      unresolvedTargets.push(candidate);
    } else if (!targets.has(candidate.key)) {
      targets.set(candidate.key, candidate);
    }
  }
  return {
    targets: [...targets.values()].sort((left, right) => left.key.localeCompare(right.key)),
    unresolvedTargets,
  };
}

function decodeQueryKey(rawKey) {
  try {
    return decodeURIComponent(rawKey.replace(/\+/g, ' '));
  } catch (error) {
    // An invalid encoded key cannot equal the well-formed snapshot selector.
    return null;
  }
}

function buildDeploymentSearch(suppliedSearch, version) {
  const rawQuery = String(suppliedSearch || '').replace(/^\?/, '');
  const retainedPairs = rawQuery
    ? rawQuery.split('&').filter((pair) => {
        const separatorIndex = pair.indexOf('=');
        const rawKey = separatorIndex < 0 ? pair : pair.slice(0, separatorIndex);
        return decodeQueryKey(rawKey) !== 'vbdt:preferExtensionVersion';
      })
    : [];
  // Preserve all other raw query pairs and replace only the preview selector.
  retainedPairs.push(
    `${encodeURIComponent('vbdt:preferExtensionVersion')}=${encodeURIComponent(version)}`
  );
  return `?${retainedPairs.join('&')}`;
}

function buildDeploymentUrl(baseUrl, target, version) {
  const deploymentUrl = new URL(baseUrl);
  deploymentUrl.pathname = [
    '',
    // Do not trust a legacy caller-provided pillar; verification URLs always use fscmUI.
    DEFAULT_UI_PREFIX,
    'redwood',
    ...target.routeSegments.map((segment) => encodeURIComponent(segment)),
  ].join('/');
  deploymentUrl.search = buildDeploymentSearch(target.suppliedSearch, version);
  deploymentUrl.hash = target.suppliedHash || '';
  return deploymentUrl.toString();
}

module.exports = {
  BASE_EXTENSION_ROUTES,
  DEFAULT_UI_PREFIX,
  buildDeploymentSearch,
  buildDeploymentUrl,
  deriveExplicitRouteTarget,
  derivePageId,
  deriveRouteTarget,
  normalizeBaseExtension,
  resolveBaseExtension,
  resolveChangedTargets,
  resolveExplicitRouteTargets,
};
