#!/usr/bin/env node
'use strict';

/**
 * Build or inspect one VX archive, send one approved Fusion upload through the
 * core REST client, and derive deterministic Redwood snapshot URLs.
 */

const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const {
  buildVx,
  createSnapshotVersion,
  inspectArchive,
} = require('./build_vx');
const {
  buildDeploymentUrl,
  resolveChangedTargets,
  resolveExplicitRouteTargets,
} = require('./deployment_urls');
const {
  DEFAULT_PROPERTIES,
  parseSafeEnvironment,
} = require('./fscr_rest_client');
const { uploadVxOnce } = require('./upload_vx');

const RUNTIME_SELECTOR_PATTERN = /^\$vb_[A-Za-z0-9_-]+$/;

function readOptionValue(argv, index, optionName) {
  // Reject incomplete value options before any build or upload can start.
  const value = argv[index + 1];
  if (!value || value.startsWith('--')) throw new Error(`${optionName} requires a value.`);
  return value;
}

function parseArgs(argv) {
  // Keep authentication details out of this shared workflow's command surface.
  const options = {
    repo: process.cwd(),
    projectRoot: null,
    vx: null,
    targetFiles: [],
    targetRoutes: [],
    expectedHead: null,
    requireClean: false,
    propertiesPath: DEFAULT_PROPERTIES,
    tokenCache: null,
    confirmDeploy: false,
    timeoutMs: 300000,
    json: false,
    help: false,
  };
  for (let index = 0; index < argv.length; index += 1) {
    const argument = argv[index];
    if (argument === '--repo') {
      options.repo = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--project-root') {
      options.projectRoot = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--vx') {
      options.vx = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--target-file') {
      options.targetFiles.push(readOptionValue(argv, index, argument));
      index += 1;
    } else if (argument === '--target-route') {
      options.targetRoutes.push(readOptionValue(argv, index, argument));
      index += 1;
    } else if (argument === '--expected-head') {
      options.expectedHead = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--require-clean') {
      options.requireClean = true;
    } else if (argument === '--properties') {
      options.propertiesPath = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--token-cache') {
      options.tokenCache = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--timeout-ms') {
      options.timeoutMs = Number(readOptionValue(argv, index, argument));
      index += 1;
    } else if (argument === '--confirm-deploy') {
      options.confirmDeploy = true;
    } else if (argument === '--json') {
      options.json = true;
    } else if (argument === '--help' || argument === '-h') {
      options.help = true;
    } else {
      throw new Error(`Unknown argument: ${argument}`);
    }
  }
  return options;
}

function printHelp() {
  // Document the required approval marker and the absence of install behavior.
  process.stdout.write([
    'Build or deploy one Oracle Fusion Express Mode VX archive',
    '',
    'Usage:',
    '  node scripts/deploy_express_mode.js --repo <extension-workspace>',
    '    (--target-file <page-file> | --target-route <redwood-url-or-path>)',
    '    [--vx <validated-archive>] [--expected-head <commit>] [--require-clean]',
    '    [--properties core/auth/fusionEnv.properties] --token-cache <path>',
    '    --confirm-deploy [--project-root <project-artifact-directory>] [--json]',
    '',
    'Without --vx, the command builds a fresh snapshot with existing pinned dependencies.',
    'It never installs dependencies, retries the upload, polls Fusion, or opens a browser.',
    '',
  ].join('\n'));
}

function selectDeployedVersion(responseVersion, archiveVersion) {
  // Use only selectors accepted by the Redwood preview runtime.
  const responseCandidate = typeof responseVersion === 'string' ? responseVersion.trim() : '';
  if (RUNTIME_SELECTOR_PATTERN.test(responseCandidate)) {
    return { version: responseCandidate, source: 'fusion-upload-response', warning: null };
  }
  const archiveCandidate = typeof archiveVersion === 'string' ? archiveVersion.trim() : '';
  if (RUNTIME_SELECTOR_PATTERN.test(archiveCandidate)) {
    return {
      version: archiveCandidate,
      source: 'archive-manifest',
      warning: responseCandidate ? `Ignored non-runtime upload version ${responseCandidate}.` : null,
    };
  }
  return {
    version: null,
    source: 'unavailable',
    warning: 'Fusion and the archive did not provide a usable $vb_ runtime selector.',
  };
}

function resolveDeploymentTargets(repo, extensionId, targetFiles, targetRoutes) {
  // Preserve explicit URL context while attaching any matching page-file evidence.
  const changedFiles = targetFiles.map((fileName) => {
    const absolute = path.isAbsolute(fileName) ? path.resolve(fileName) : path.resolve(repo, fileName);
    return path.relative(repo, absolute).split(path.sep).join('/');
  });
  const fileTargets = resolveChangedTargets(repo, extensionId, changedFiles, {});
  const routeTargets = resolveExplicitRouteTargets(targetRoutes);
  const targets = new Map(routeTargets.targets.map((target) => [target.key, { ...target }]));
  for (const fileTarget of fileTargets.targets) {
    if (!targets.has(fileTarget.key)) targets.set(fileTarget.key, { ...fileTarget });
  }
  return {
    targets: [...targets.values()].sort((left, right) => left.key.localeCompare(right.key)),
    unresolvedTargets: [...fileTargets.unresolvedTargets, ...routeTargets.unresolvedTargets],
  };
}

function sha256File(fileName) {
  // Hash the exact immutable upload artifact shown at the approval gate.
  return crypto.createHash('sha256').update(fs.readFileSync(fileName)).digest('hex');
}

function persistDeploymentResult(projectRoot, result) {
  // Persist only sanitized output under the caller-selected project artifact directory.
  if (!projectRoot) return null;
  const root = path.resolve(projectRoot);
  fs.mkdirSync(root, { recursive: true, mode: 0o700 });
  const fileName = path.join(root, `deployment-${Date.now()}.json`);
  fs.writeFileSync(fileName, `${JSON.stringify(result, null, 2)}\n`, { mode: 0o600, flag: 'wx' });
  return fileName;
}

async function deployExpressMode(options, dependencies = {}) {
  // Fail before build or authentication when approval or target context is missing.
  if (!options.confirmDeploy) throw new Error('Deployment requires --confirm-deploy after explicit approval.');
  if (!options.tokenCache) {
    throw new Error('Deployment requires --token-cache created by the core OAuth login workflow.');
  }
  if (!Number.isSafeInteger(options.timeoutMs) || options.timeoutMs <= 0) {
    throw new Error('--timeout-ms must be a positive integer.');
  }
  if (options.targetFiles.length === 0 && options.targetRoutes.length === 0) {
    throw new Error('Deployment requires at least one approved target file or Redwood route.');
  }
  const repo = path.resolve(options.repo || process.cwd());
  let archive;
  let build;
  if (options.vx) {
    archive = await (dependencies.inspectArchive || inspectArchive)(path.resolve(options.vx), repo);
    build = { performed: false, source: 'explicit-archive', sourceState: archive.sourceState || null };
  } else {
    const version = createSnapshotVersion((dependencies.now || Date.now)());
    archive = await (dependencies.buildVx || buildVx)({
      repo,
      version,
      expectedHead: options.expectedHead || null,
      requireClean: Boolean(options.requireClean),
      excludeSources: false,
      skipOptimize: false,
    }, dependencies.buildDependencies || {});
    if (archive.extension.version !== version) {
      throw new Error(`Built archive version ${archive.extension.version || '<missing>'} does not match ${version}.`);
    }
    build = { performed: true, source: 'fresh-snapshot-build', sourceState: archive.sourceState || null };
  }
  const archivePath = path.resolve(archive.archivePath);
  const targets = resolveDeploymentTargets(
    repo,
    archive.extension.id,
    options.targetFiles,
    options.targetRoutes
  );
  if (targets.targets.length === 0) {
    throw new Error('No approved deployment target could be resolved.');
  }
  const environment = (dependencies.parseSafeEnvironment || parseSafeEnvironment)(options.propertiesPath);
  const upload = await (dependencies.uploadVxOnce || uploadVxOnce)({
    archivePath,
    restBaseUrl: environment.restBaseUrl,
    tokenCache: options.tokenCache,
    timeoutMs: options.timeoutMs,
  }, dependencies.uploadDependencies || {});
  const responseVersion = upload.response && typeof upload.response === 'object'
    ? upload.response.version
    : null;
  const versionSelection = selectDeployedVersion(responseVersion, archive.extension.version);
  const deployedTargets = upload.accepted && versionSelection.version
    ? targets.targets.map((target) => ({
        ...target,
        deploymentUrl: buildDeploymentUrl(environment.restBaseUrl, target, versionSelection.version),
      }))
    : [];
  const result = {
    status: upload.accepted ? 'accepted' : 'failed',
    environment: environment.environment,
    endpoint: '/fscmRestApi/vx/v2/extensions',
    upload,
    build,
    archive: {
      path: archivePath,
      sizeBytes: fs.statSync(archivePath).size,
      sha256: sha256File(archivePath),
      extension: archive.extension,
      warnings: archive.warnings || [],
    },
    deployedVersion: versionSelection.version,
    versionSource: versionSelection.source,
    versionWarning: versionSelection.warning,
    deployedTargets,
    unresolvedTargets: targets.unresolvedTargets,
    pollingPerformed: false,
    retryPerformed: false,
  };
  result.artifactPath = persistDeploymentResult(options.projectRoot, result);
  return result;
}

async function main() {
  try {
    const options = parseArgs(process.argv.slice(2));
    if (options.help) return printHelp();
    const result = await deployExpressMode(options);
    process.stdout.write(`${JSON.stringify(result, null, options.json ? 2 : 2)}\n`);
    if (result.status !== 'accepted') process.exitCode = 4;
  } catch (error) {
    process.stderr.write(`${error.message}\n`);
    process.exitCode = 1;
  }
}

if (require.main === module) main();

module.exports = {
  deployExpressMode,
  parseArgs,
  persistDeploymentResult,
  resolveDeploymentTargets,
  selectDeployedVersion,
  sha256File,
};
