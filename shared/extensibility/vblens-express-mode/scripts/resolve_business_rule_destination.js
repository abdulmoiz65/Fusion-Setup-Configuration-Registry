#!/usr/bin/env node
'use strict';

/**
 * Resolve the customer-owned Business Rules overlay and sibling Advanced
 * Expression destination from repository topology and exact Oracle evidence.
 * This helper reports paths only; it never creates or changes an artifact.
 */

const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');

function readOptionValue(argv, index, optionName) {
  const value = argv[index + 1];
  if (!value || value.startsWith('--')) throw new Error(`${optionName} requires a value.`);
  return value;
}

function validateIdentifier(value, label) {
  const normalized = String(value || '').trim();
  if (!/^[A-Za-z][A-Za-z0-9_-]*$/.test(normalized)) {
    throw new Error(`${label} must be a safe Express identifier.`);
  }
  return normalized;
}

function parseArgs(argv) {
  const options = {
    repo: process.cwd(),
    owner: null,
    layout: null,
    moduleName: 'validateBusinessRule',
    evidenceManifest: null,
    json: false,
    help: false,
  };
  for (let index = 0; index < argv.length; index += 1) {
    const argument = argv[index];
    if (argument === '--repo') {
      options.repo = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--owner') {
      options.owner = validateIdentifier(readOptionValue(argv, index, argument), 'Owner');
      index += 1;
    } else if (argument === '--layout') {
      options.layout = validateIdentifier(readOptionValue(argv, index, argument), 'Layout');
      index += 1;
    } else if (argument === '--module-name') {
      options.moduleName = validateIdentifier(
        readOptionValue(argv, index, argument),
        'Module name'
      );
      index += 1;
    } else if (argument === '--evidence-manifest') {
      options.evidenceManifest = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--json') {
      options.json = true;
    } else if (argument === '--help' || argument === '-h') {
      options.help = true;
    } else {
      throw new Error(`Unknown argument: ${argument}`);
    }
  }
  if (!options.help && (!options.owner || !options.layout)) {
    throw new Error('--owner and --layout are required.');
  }
  return options;
}

function resolveRepository(requestedRepo) {
  return fs.realpathSync(execFileSync('git', ['rev-parse', '--show-toplevel'], {
    cwd: path.resolve(requestedRepo),
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
  }).trim());
}

function discoverExtensionRoots(repo) {
  return fs.readdirSync(repo, { withFileTypes: true })
    .filter((entry) => entry.isDirectory() && /^extension\w*$/i.test(entry.name))
    .map((entry) => {
      const sourcesRoot = path.join(repo, entry.name, 'sources');
      const extensionMetadata = path.join(sourcesRoot, 'extension.json');
      // A valid Extension source root can own a new dynamicLayouts directory.
      return fs.existsSync(extensionMetadata) && fs.statSync(extensionMetadata).isFile()
        ? path.join(sourcesRoot, 'dynamicLayouts')
        : null;
    })
    .filter(Boolean)
    .sort();
}

function readEvidenceManifest(filePath) {
  if (!filePath) return null;
  const parsed = JSON.parse(fs.readFileSync(path.resolve(filePath), 'utf8'));
  if (![1, 2].includes(parsed.schemaVersion) || !Array.isArray(parsed.evidence)) {
    throw new Error('Unsupported runtime evidence manifest.');
  }
  return parsed;
}

function cacheCounterpart(manifest, owner, layout) {
  if (!manifest) return null;
  const suffix = `/dynamicLayouts/self/${layout}/metadata-rules.json`;
  const matches = manifest.evidence.filter((item) => (
    item.role === 'business-and-validation-rules'
    && String(item.moduleId || '').includes(`vx/${owner}/`)
    && String(item.moduleId || '').endsWith(suffix)
  ));
  return matches.length === 1 ? {
    kind: 'deployed-cache',
    moduleId: matches[0].moduleId,
    sha256: matches[0].sha256 || null,
    manifest: path.resolve(manifest.__path || ''),
  } : null;
}

function localCounterpart(dynamicLayoutsRoot, layout) {
  const candidate = path.join(dynamicLayoutsRoot, 'self', layout, 'metadata-rules.json');
  return fs.existsSync(candidate) && fs.statSync(candidate).isFile()
    ? { kind: 'repository', path: candidate }
    : null;
}

function buildDestinationReport(options) {
  const repo = resolveRepository(options.repo || process.cwd());
  const owner = validateIdentifier(options.owner, 'Owner');
  const layout = validateIdentifier(options.layout, 'Layout');
  const moduleName = validateIdentifier(options.moduleName || 'validateBusinessRule', 'Module name');
  const roots = discoverExtensionRoots(repo);
  if (roots.length !== 1) {
    return {
      schemaVersion: 1,
      repository: repo,
      owner,
      layout,
      decision: 'ambiguous-extension-root',
      candidates: roots.map((root) => path.relative(repo, root).split(path.sep).join('/')),
      destinations: null,
    };
  }

  const dynamicLayoutsRoot = roots[0];
  const manifest = readEvidenceManifest(options.evidenceManifest);
  if (manifest) manifest.__path = options.evidenceManifest;
  const counterpart = localCounterpart(dynamicLayoutsRoot, layout)
    || cacheCounterpart(manifest, owner, layout);
  const pageRoot = path.join(dynamicLayoutsRoot, owner, layout);
  const overlayPath = path.join(pageRoot, 'metadata-rules-x.json');
  const modulePath = path.join(
    pageRoot,
    'metadataRules',
    `site_hcm_extension_${moduleName}.js`
  );
  const relative = (filePath) => path.relative(repo, filePath).split(path.sep).join('/');
  let decision = 'counterpart-required';
  if (counterpart) decision = fs.existsSync(overlayPath) ? 'extend-overlay' : 'create-minimum-overlay';
  return {
    schemaVersion: 1,
    repository: repo,
    owner,
    layout,
    decision,
    counterpart,
    overlayExists: fs.existsSync(overlayPath),
    destinations: {
      rule: relative(overlayPath),
      module: relative(modulePath),
      moduleImportPath: `./metadataRules/site_hcm_extension_${moduleName}`,
    },
  };
}

function printHelp() {
  process.stdout.write([
    'Resolve an Express Mode Business Rules write destination',
    '',
    'Usage:',
    '  node scripts/resolve_business_rule_destination.js --repo <path>',
    '    --owner <application-owner> --layout <layout-name>',
    '    [--module-name <name>] [--evidence-manifest <runtime-evidence.json>] [--json]',
    '',
  ].join('\n'));
}

function main() {
  try {
    const options = parseArgs(process.argv.slice(2));
    if (options.help) return printHelp();
    const report = buildDestinationReport(options);
    process.stdout.write(options.json
      ? `${JSON.stringify(report, null, 2)}\n`
      : `${report.decision}: ${report.destinations?.rule || 'no unique destination'}\n`);
  } catch (error) {
    process.stderr.write(`${error.message}\n`);
    process.exitCode = 1;
  }
}

if (require.main === module) main();

module.exports = {
  buildDestinationReport,
  cacheCounterpart,
  discoverExtensionRoots,
  parseArgs,
  validateIdentifier,
};
