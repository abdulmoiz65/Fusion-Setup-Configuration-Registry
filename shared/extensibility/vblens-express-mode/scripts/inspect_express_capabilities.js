#!/usr/bin/env node
'use strict';

/**
 * Inspect repository artifacts and report which Express Mode workflows have a
 * proven Extension write contract. This command never changes the repository.
 */

const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');

const CONTRACT_PATH = path.resolve(
  __dirname,
  '..',
  'references',
  'express-mode-capability-contracts.json'
);

function readOptionValue(argv, index, optionName) {
  const value = argv[index + 1];
  if (!value || value.startsWith('--')) {
    throw new Error(`${optionName} requires a value.`);
  }
  return value;
}

function parseArgs(argv) {
  const options = {
    repo: process.cwd(),
    targetFile: null,
    release: null,
    json: false,
    help: false,
  };
  for (let index = 0; index < argv.length; index += 1) {
    const argument = argv[index];
    if (argument === '--repo') {
      options.repo = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--target-file') {
      options.targetFile = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--release') {
      options.release = readOptionValue(argv, index, argument);
      index += 1;
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
  process.stdout.write([
    'Inspect Oracle Fusion Express Mode customization capabilities',
    '',
    'Usage:',
    '  node scripts/inspect_express_capabilities.js --repo <path>',
    '    [--target-file <file-or-directory>] [--release <release>] [--json]',
    '',
  ].join('\n'));
}

function resolveRepository(requestedRepo) {
  const repository = execFileSync('git', ['rev-parse', '--show-toplevel'], {
    cwd: path.resolve(requestedRepo),
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
  }).trim();
  // Canonical paths avoid macOS /var and /private/var aliases producing false escapes.
  return fs.realpathSync(repository);
}

function safeRelative(repo, requestedTarget) {
  const canonicalRepo = fs.realpathSync(repo);
  const requestedAbsolute = path.resolve(canonicalRepo, requestedTarget || '.');
  const absolute = fs.existsSync(requestedAbsolute)
    ? fs.realpathSync(requestedAbsolute)
    : requestedAbsolute;
  const relative = path.relative(canonicalRepo, absolute);
  if (relative.startsWith('..') || path.isAbsolute(relative)) {
    throw new Error('Target file must remain inside the repository.');
  }
  return { absolute, relative: relative.split(path.sep).join('/') };
}

function collectFiles(root, repo, collected = []) {
  const stat = fs.lstatSync(root);
  if (stat.isSymbolicLink()) return collected;
  if (stat.isFile()) {
    collected.push(path.relative(repo, root).split(path.sep).join('/'));
    return collected;
  }
  if (!stat.isDirectory()) return collected;
  for (const entry of fs.readdirSync(root).sort()) {
    if (entry === '.git' || entry === 'node_modules' || entry.startsWith('.vblens-')) continue;
    collectFiles(path.join(root, entry), repo, collected);
  }
  return collected;
}

function readContracts() {
  return JSON.parse(fs.readFileSync(CONTRACT_PATH, 'utf8'));
}

function findCounterparts(repo, relativePath, counterpartName) {
  const portable = relativePath.split(path.sep).join('/');
  const segments = portable.split('/');
  const dynamicLayoutsIndex = segments.indexOf('dynamicLayouts');
  if (dynamicLayoutsIndex < 0) return [];
  const layoutName = segments[dynamicLayoutsIndex + 2];
  const dynamicLayoutsRoot = path.join(repo, ...segments.slice(0, dynamicLayoutsIndex + 1));
  if (!layoutName || !fs.existsSync(dynamicLayoutsRoot)) return [];
  // Prefer the conventional self owner, then inspect every delivered owner.
  const owners = [
    'self',
    ...fs.readdirSync(dynamicLayoutsRoot).filter((owner) => owner !== 'self').sort(),
  ];
  const matches = [];
  for (const owner of owners) {
    const candidate = path.join(dynamicLayoutsRoot, owner, layoutName, counterpartName);
    if (fs.existsSync(candidate) && fs.statSync(candidate).isFile()) {
      matches.push(path.relative(repo, candidate).split(path.sep).join('/'));
    }
  }
  // A conventional self-layer match identifies the Oracle contract unambiguously.
  const selfMatch = matches.find((candidate) => candidate.includes('/dynamicLayouts/self/'));
  return selfMatch ? [selfMatch] : matches;
}

function findCounterpart(repo, relativePath, counterpartName) {
  const matches = findCounterparts(repo, relativePath, counterpartName);
  return matches.length === 1 ? matches[0] : null;
}

function readJson(filePath) {
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (error) {
    return null;
  }
}

function hasEffectiveRoot(parsed, keys) {
  if (!parsed || Array.isArray(parsed) || typeof parsed !== 'object') return false;
  return keys.some((key) => {
    const value = parsed[key];
    return Array.isArray(value)
      ? value.length > 0
      : Boolean(value && typeof value === 'object' && Object.keys(value).length > 0);
  });
}

function propertyDefinitions(parsed, requireExtendable) {
  const properties = parsed && !Array.isArray(parsed) ? parsed.properties : null;
  if (!properties || Array.isArray(properties) || typeof properties !== 'object') return [];
  return Object.entries(properties).filter(([, definition]) => (
    definition
    && typeof definition === 'object'
    && (!requireExtendable || definition.extendable === true)
    && definition.extendable !== false
  ));
}

function isGuidedJourneyProperty(name) {
  // Oracle page contracts use product-specific prefixes around Journey and Task Code suffixes.
  return /journey.*code|task.*codes?/i.test(name);
}

function findObjectKeyMatching(value, pattern) {
  if (Array.isArray(value)) return value.some((item) => findObjectKeyMatching(item, pattern));
  if (!value || typeof value !== 'object') return false;
  return Object.entries(value).some(([key, child]) => (
    pattern.test(key) || findObjectKeyMatching(child, pattern)
  ));
}

function isImportedExtensionExpression(repo, relativePath) {
  const portable = relativePath.split(path.sep).join('/');
  const marker = '/metadataRules/';
  const markerIndex = portable.indexOf(marker);
  if (markerIndex < 0) return false;
  const pageRoot = portable.slice(0, markerIndex);
  const rulesPath = path.join(repo, pageRoot, 'metadata-rules-x.json');
  const rules = readJson(rulesPath);
  const modules = rules?.imports?.modules;
  if (!modules || Array.isArray(modules) || typeof modules !== 'object') return false;
  const target = path.resolve(repo, relativePath);
  return Object.values(modules).some((definition) => {
    const modulePath = typeof definition === 'string' ? definition : definition?.path;
    if (!modulePath) return false;
    const candidate = path.resolve(
      path.dirname(rulesPath),
      modulePath.endsWith('.js') ? modulePath : `${modulePath}.js`
    );
    // Only a sibling expression imported by the same Extension overlay is writable.
    return candidate === target && candidate.startsWith(`${path.join(repo, pageRoot)}${path.sep}`);
  });
}

function inspectArtifact(repo, relativePath, contracts) {
  const baseName = path.posix.basename(relativePath);
  if (contracts.advancedModePathPrefixes.some((prefix) => relativePath.startsWith(prefix))) {
    return {
      path: relativePath,
      artifactType: 'advanced-mode-source',
      classification: 'source-visible-not-express-writable',
      workflows: [],
      counterpart: null,
      restrictions: ['Source may be inspected for explanation, but not changed by this skill.'],
    };
  }
  if (contracts.protectedOracleArtifacts.includes(baseName)) {
    return {
      path: relativePath,
      artifactType: 'oracle-delivered-evidence',
      classification: 'source-visible-not-express-writable',
      workflows: [],
      counterpart: null,
      restrictions: ['Oracle-delivered dependency artifacts are read-only.'],
    };
  }
  if (relativePath.includes('/metadataRules/') && baseName.endsWith('.js')) {
    const writable = isImportedExtensionExpression(repo, relativePath);
    // Source visibility alone never proves customer ownership of an Advanced Expression.
    return {
      path: relativePath,
      artifactType: writable ? 'express-advanced-expression' : 'advanced-expression-evidence',
      classification: writable ? 'supported-writable' : 'source-visible-not-express-writable',
      workflows: writable
        ? ['advanced-condition', 'advanced-default', 'advanced-validation']
        : [],
      counterpart: null,
      restrictions: writable
        ? ['Field accessors, imports, available context, and return semantics require validation.']
        : ['The file is not imported by a sibling Extension Business Rules overlay.'],
    };
  }
  const contract = contracts.artifacts[baseName];
  if (!contract) return null;
  const counterpartNames = contract.counterpartAlternatives
    || (contract.counterpart ? [contract.counterpart] : []);
  let counterpart = null;
  let ambiguousCounterpart = false;
  for (const counterpartName of counterpartNames) {
    const matches = findCounterparts(repo, relativePath, counterpartName);
    if (matches.length === 1) {
      counterpart = matches[0];
      break;
    }
    if (matches.length > 1) ambiguousCounterpart = true;
  }
  const restrictions = [];
  let classification = contract.classification;
  if (contract.counterpartRequired && !counterpart) {
    classification = 'unknown';
    restrictions.push(ambiguousCounterpart
      ? 'Multiple Oracle counterpart candidates make ownership ambiguous.'
      : 'No Oracle counterpart proves this overlay contract.');
  }
  if (contract.recognizedRootKeys) {
    const parsed = readJson(path.join(repo, relativePath));
    if (!parsed) {
      classification = 'unknown';
      restrictions.push('The overlay is not valid JSON.');
    } else if (!hasEffectiveRoot(parsed, contract.recognizedRootKeys)) {
      classification = 'unknown';
      restrictions.push('The overlay does not contain an effective recognized customization.');
    }
  }
  let workflows = classification === 'unknown' ? [] : [...contract.workflows];
  const unresolvedWorkflows = [];
  const counterpartJson = counterpart ? readJson(path.join(repo, counterpart)) : null;
  if (baseName === 'page-x.json' || baseName === 'page-r-x.json') {
    const definitions = propertyDefinitions(counterpartJson, baseName === 'page-r-x.json');
    if (definitions.length === 0) {
      classification = 'unknown';
      workflows = [];
      restrictions.push('No customer-configurable Page Property is proven by the Oracle contract.');
    } else if (!definitions.some(([name]) => isGuidedJourneyProperty(name))) {
      workflows = workflows.filter((workflow) => workflow !== 'guided-journey-property');
    }
  }
  if (baseName === 'layout-x.json' && !findObjectKeyMatching(counterpartJson, /sectionTemplates?|newSectionTemplate/i)) {
    workflows = workflows.filter((workflow) => workflow !== 'container-sections');
    restrictions.push('No dependency-provided section template was found.');
  }
  if (baseName === 'metadata-rules-x.json' && workflows.includes('validation-message')) {
    // Inline validation requires an exact UI consumer that dynamic-layout metadata alone cannot prove.
    workflows = workflows.filter((workflow) => workflow !== 'validation-message');
    unresolvedWorkflows.push('validation-message');
    restrictions.push('Validation messages require a proven oj-dyn-form consumer for this page.');
  }
  return {
    path: relativePath,
    artifactType: contract.artifactType,
    classification,
    workflows,
    unresolvedWorkflows,
    counterpart,
    restrictions,
  };
}

function buildCapabilityReport(options) {
  const repo = resolveRepository(options.repo || process.cwd());
  const target = safeRelative(repo, options.targetFile || '.');
  if (!fs.existsSync(target.absolute)) throw new Error(`Target does not exist: ${target.relative}`);
  const contracts = readContracts();
  const capabilities = collectFiles(target.absolute, repo)
    .map((relativePath) => inspectArtifact(repo, relativePath, contracts))
    .filter(Boolean);
  return {
    // Report the contract version so callers can distinguish stricter evidence semantics.
    schemaVersion: contracts.schemaVersion,
    repository: repo,
    target: target.relative || '.',
    release: options.release || null,
    documentationBaseline: contracts.documentationBaseline,
    capabilities,
    summary: capabilities.reduce((summary, capability) => {
      summary[capability.classification] = (summary[capability.classification] || 0) + 1;
      return summary;
    }, {}),
  };
}

function printHuman(report) {
  process.stdout.write(`Target: ${report.target}\n`);
  for (const capability of report.capabilities) {
    process.stdout.write(
      `${capability.classification}: ${capability.path} (${capability.artifactType})\n`
    );
  }
}

function main() {
  try {
    const options = parseArgs(process.argv.slice(2));
    if (options.help) return printHelp();
    const report = buildCapabilityReport(options);
    if (options.json) {
      process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
    } else {
      printHuman(report);
    }
  } catch (error) {
    process.stderr.write(`${error.message}\n`);
    process.exitCode = 1;
  }
}

if (require.main === module) main();

module.exports = {
  buildCapabilityReport,
  collectFiles,
  findCounterpart,
  findCounterparts,
  isImportedExtensionExpression,
  inspectArtifact,
  parseArgs,
  safeRelative,
};
