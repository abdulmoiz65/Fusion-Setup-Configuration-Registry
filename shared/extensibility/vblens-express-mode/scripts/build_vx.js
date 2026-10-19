#!/usr/bin/env node
'use strict';

/**
 * Build and validate a Visual Builder extension archive using the target
 * repository's pinned Oracle Grunt tooling. Generated with vblens-engineer.
 */

const fs = require('node:fs');
const path = require('node:path');
const { createRequire } = require('node:module');
const { execFileSync, spawnSync } = require('node:child_process');

function readOptionValue(argv, index, optionName) {
  const value = argv[index + 1];
  if (!value || value.startsWith('--')) {
    throw new Error(`${optionName} requires a value.`);
  }
  return value;
}

function createSnapshotVersion(now = Date.now()) {
  if (!Number.isInteger(now) || now <= 0) {
    throw new Error('Snapshot version requires a positive integer timestamp.');
  }
  // Match the unique preview-version convention used by VBLens Engineer.
  return `$vb_snapshot_${now}`;
}

function parseArgs(argv) {
  const options = {
    repo: process.cwd(),
    version: null,
    expectedHead: null,
    requireClean: false,
    excludeSources: false,
    skipOptimize: false,
    json: false,
    help: false,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index];
    if (value === '--repo') {
      options.repo = readOptionValue(argv, index, value);
      index += 1;
    } else if (value === '--version') {
      options.version = readOptionValue(argv, index, value);
      index += 1;
    } else if (value === '--expected-head') {
      options.expectedHead = readOptionValue(argv, index, value);
      index += 1;
    } else if (value === '--require-clean') {
      options.requireClean = true;
    } else if (value === '--exclude-sources') {
      options.excludeSources = true;
    } else if (value === '--skip-optimize') {
      options.skipOptimize = true;
    } else if (value === '--json') {
      options.json = true;
    } else if (value === '--help' || value === '-h') {
      options.help = true;
    } else {
      throw new Error(`Unknown argument: ${value}`);
    }
  }

  return options;
}

function printHelp() {
  process.stdout.write(
    [
      'Build a local Visual Builder .vx archive',
      '',
      'Usage:',
      '  node scripts/build_vx.js [--repo <path>] [--version <version>]',
      '    [--expected-head <commit>] [--require-clean]',
      '    [--exclude-sources] [--skip-optimize] [--json]',
      '',
      'The target repository must already contain its pinned Visual Builder dependencies.',
      'This command never installs packages.',
      'The script never deploys the archive.',
      '',
    ].join('\n')
  );
}

function inspectGitSourceState(repo, options = {}) {
  let root;
  try {
    root = execFileSync('git', ['rev-parse', '--show-toplevel'], {
      cwd: repo,
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
    }).trim();
  } catch (error) {
    if (options.expectedHead || options.requireClean) {
      throw new Error('Reviewed-state build gates require a Git repository.');
    }
    return {
      available: false,
      head: null,
      worktreeClean: null,
      expectedHead: options.expectedHead || null,
    };
  }

  const head = execFileSync('git', ['rev-parse', 'HEAD'], {
    cwd: root,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
  }).trim();
  const status = execFileSync('git', ['status', '--porcelain'], {
    cwd: root,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
  }).trim();
  if (options.expectedHead) {
    let expectedHead;
    try {
      expectedHead = execFileSync('git', ['rev-parse', '--verify', options.expectedHead], {
        cwd: root,
        encoding: 'utf8',
        stdio: ['ignore', 'pipe', 'pipe'],
      }).trim();
    } catch (error) {
      throw new Error(`Unable to resolve reviewed commit: ${options.expectedHead}`);
    }
    if (head !== expectedHead) {
      throw new Error(`Current HEAD ${head} does not match reviewed commit ${expectedHead}.`);
    }
  }
  if (options.requireClean && status) {
    throw new Error('Fresh build requires a clean worktree.');
  }

  return {
    available: true,
    head,
    worktreeClean: status.length === 0,
    expectedHead: options.expectedHead || null,
  };
}

function readJson(filePath) {
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (error) {
    throw new Error(`Unable to parse JSON file ${filePath}: ${error.message}`);
  }
}

function resolveExtensionMetadata(repo) {
  const candidates = [
    {
      filePath: path.join(repo, 'extension1', 'sources', 'extension.json'),
      topology: 'multi-product-fusion-extension',
    },
    {
      filePath: path.join(repo, 'extension1', 'sources', 'vb-extension.json'),
      topology: 'appui-extension',
    },
  ];
  const selected = candidates.find((candidate) => fs.existsSync(candidate.filePath));
  if (!selected) {
    throw new Error(
      'Unable to find extension1/sources/extension.json or extension1/sources/vb-extension.json.'
    );
  }

  const metadata = readJson(selected.filePath);
  if (!metadata.id || typeof metadata.id !== 'string') {
    throw new Error(`Extension metadata is missing a string id: ${selected.filePath}`);
  }

  return {
    id: metadata.id,
    name: typeof metadata.name === 'string' ? metadata.name : metadata.id,
    version: metadata.version || null,
    metadataPath: selected.filePath,
    topology: selected.topology,
  };
}

function resolveBuildTooling(repo) {
  const builderPackage = path.join(
    repo,
    'node_modules',
    '@oracle',
    'grunt-vb-build',
    'package.json'
  );
  const gruntName = process.platform === 'win32' ? 'grunt.cmd' : 'grunt';
  const gruntPath = path.join(repo, 'node_modules', '.bin', gruntName);

  if (!fs.existsSync(builderPackage) || !fs.existsSync(gruntPath)) {
    throw new Error(
      'Visual Builder dependencies are not installed in the target repository.'
    );
  }

  return {
    builderPackage,
    gruntPath,
  };
}

function runGrunt(gruntPath, args, repo, runner = spawnSync) {
  const result = runner(gruntPath, args, {
    cwd: repo,
    encoding: 'utf8',
    stdio: 'inherit',
  });
  if (result.error) {
    throw new Error(`Unable to run ${path.basename(gruntPath)}: ${result.error.message}`);
  }
  if (result.status !== 0) {
    throw new Error(`Visual Builder command failed: ${path.basename(gruntPath)} ${args.join(' ')}`);
  }
}

function inspectGeneratedBuildOutput(repo) {
  const buildRoot = path.join(repo, 'build');
  let buildStat;
  try {
    // lstat detects dangling links that existsSync would treat as an absent path.
    buildStat = fs.lstatSync(buildRoot);
  } catch (error) {
    if (error.code !== 'ENOENT') {
      throw error;
    }
    return {
      buildRoot,
      generatedEntries: [],
    };
  }

  if (buildStat.isSymbolicLink() || !buildStat.isDirectory()) {
    throw new Error(`Refusing to clean unsafe Visual Builder output path: ${buildRoot}`);
  }

  const generatedEntries = fs.readdirSync(buildRoot).sort();
  const pendingPaths = generatedEntries.map((entry) => path.join(buildRoot, entry));
  while (pendingPaths.length > 0) {
    const candidate = pendingPaths.pop();
    const candidateStat = fs.lstatSync(candidate);
    if (candidateStat.isSymbolicLink()) {
      throw new Error(`Refusing to clean symlinked Visual Builder output: ${candidate}`);
    }
    if (candidateStat.isDirectory()) {
      // Inspect descendants without following links before delegating cleanup to Oracle tooling.
      for (const child of fs.readdirSync(candidate)) {
        pendingPaths.push(path.join(candidate, child));
      }
    }
  }

  return {
    buildRoot,
    generatedEntries,
  };
}

function cleanGeneratedBuildOutput(repo, tooling, runner = spawnSync) {
  const generatedOutput = inspectGeneratedBuildOutput(repo);
  if (generatedOutput.generatedEntries.length === 0) {
    return {
      performed: false,
      generatedEntries: [],
    };
  }

  // Fresh builds own build/ and use the repository's pinned cleanup task instead of direct deletion.
  runGrunt(tooling.gruntPath, ['vb-clean'], repo, runner);
  return {
    performed: true,
    generatedEntries: generatedOutput.generatedEntries,
  };
}

function loadJsZip(repo) {
  const builderPackage = path.join(
    repo,
    'node_modules',
    '@oracle',
    'grunt-vb-build',
    'package.json'
  );
  const builderRequire = createRequire(builderPackage);
  return builderRequire('jszip');
}

async function readZipJson(zip, entryName) {
  const entry = zip.file(entryName);
  if (!entry) {
    throw new Error(`Archive is missing required root entry: ${entryName}`);
  }
  const content = await entry.async('string');
  try {
    return JSON.parse(content);
  } catch (error) {
    throw new Error(`Archive entry ${entryName} is not valid JSON: ${error.message}`);
  }
}

async function inspectArchive(archivePath, repo, jsZipOverride = null) {
  if (!fs.existsSync(archivePath)) {
    throw new Error(`Built .vx archive does not exist: ${archivePath}`);
  }

  const archiveBuffer = fs.readFileSync(archivePath);
  if (archiveBuffer.length < 4 || archiveBuffer.subarray(0, 2).toString('binary') !== 'PK') {
    throw new Error(`Built artifact is not a ZIP-based .vx archive: ${archivePath}`);
  }

  const JSZip = jsZipOverride || loadJsZip(repo);
  const zip = await JSZip.loadAsync(archiveBuffer);
  const entries = Object.values(zip.files)
    .filter((entry) => !entry.dir)
    .map((entry) => entry.name)
    .sort();
  const entrySet = new Set(entries);
  const manifest = await readZipJson(zip, 'manifest.json');
  const buildInfo = await readZipJson(zip, 'build-info.json');
  const metadata = resolveExtensionMetadata(repo);
  const errors = [];
  const warnings = [];

  if (manifest.id && manifest.id !== metadata.id) {
    errors.push(`Manifest id ${manifest.id} does not match extension id ${metadata.id}.`);
  }
  if (!manifest.version || typeof manifest.version !== 'string') {
    errors.push('Manifest does not contain a string version.');
  }

  const manifestFiles = Array.isArray(manifest.files) ? manifest.files : [];
  const missingManifestFiles = manifestFiles.filter((entry) => !entrySet.has(entry));
  if (missingManifestFiles.length > 0) {
    errors.push(`Manifest references ${missingManifestFiles.length} missing archive file(s).`);
  }

  const buildResources = Array.isArray(buildInfo.resources) ? buildInfo.resources : [];
  const missingBuildResources = buildResources.filter((entry) => !entrySet.has(entry));
  if (missingBuildResources.length > 0) {
    errors.push(`Build information references ${missingBuildResources.length} missing file(s).`);
  }

  const testArtifacts = entries.filter(
    (entry) => entry.endsWith('-tests.js') || entry.endsWith('-tests.json')
  );
  if (testArtifacts.length > 0) {
    warnings.push(`Archive contains ${testArtifacts.length} test artifact(s).`);
  }
  if (errors.length > 0) {
    throw new Error(`Archive validation failed:\n- ${errors.join('\n- ')}`);
  }

  return {
    archivePath,
    sizeBytes: archiveBuffer.length,
    entriesCount: entries.length,
    extension: {
      id: metadata.id,
      name: metadata.name,
      version: manifest.version,
      topology: metadata.topology,
    },
    warnings,
  };
}

function findArchive(repo, extensionId, buildStartedAt) {
  const archivePath = path.join(repo, 'build', `${extensionId}.vx`);
  if (!fs.existsSync(archivePath)) {
    throw new Error(
      `The Oracle vb-package task completed but did not create build/${extensionId}.vx.`
    );
  }

  const modifiedAt = fs.statSync(archivePath).mtimeMs;
  if (modifiedAt < buildStartedAt - 2000) {
    throw new Error(`The discovered .vx archive predates this build: ${archivePath}`);
  }
  return archivePath;
}

async function buildVx(options, dependencies = {}) {
  const repo = path.resolve(options.repo || process.cwd());
  const inspectSourceState = dependencies.inspectGitSourceState || inspectGitSourceState;
  // Capture source identity before generated-output cleanup.
  const sourceState = inspectSourceState(repo, {
    expectedHead: options.expectedHead || null,
    requireClean: Boolean(options.requireClean),
  });
  const metadata = resolveExtensionMetadata(repo);
  const runner = dependencies.runner || spawnSync;
  const tooling = dependencies.tooling || resolveBuildTooling(repo);
  const inspect = dependencies.inspectArchive || inspectArchive;
  const clean = dependencies.cleanGeneratedBuildOutput || cleanGeneratedBuildOutput;
  const cleanup = clean(repo, tooling, runner);
  const buildStartedAt = Date.now();
  const processArgs = ['vb-process-local'];
  const packageArgs = ['vb-package'];

  if (options.version) {
    processArgs.push(`--vx-version=${options.version}`);
  }
  if (options.excludeSources) {
    packageArgs.push('--vx-include-sources=false');
  }
  if (options.skipOptimize) {
    packageArgs.push('--skip-optimize');
  }

  runGrunt(tooling.gruntPath, processArgs, repo, runner);
  runGrunt(tooling.gruntPath, packageArgs, repo, runner);

  const archivePath = findArchive(repo, metadata.id, buildStartedAt);
  const archive = await inspect(archivePath, repo);
  const finalSourceState = inspectSourceState(repo, {
    expectedHead: options.expectedHead || null,
    requireClean: Boolean(options.requireClean),
  });
  if (
    sourceState.available
    && finalSourceState.available
    && sourceState.head !== finalSourceState.head
  ) {
    throw new Error('Repository HEAD changed while the .vx archive was being built.');
  }
  if (
    sourceState.available
    && sourceState.worktreeClean
    && !finalSourceState.worktreeClean
  ) {
    throw new Error('Repository source changed while the .vx archive was being built.');
  }
  return {
    ...archive,
    cleanup,
    sourceState: {
      ...finalSourceState,
      stableDuringBuild: true,
    },
  };
}

async function main() {
  try {
    const options = parseArgs(process.argv.slice(2));
    if (options.help) {
      printHelp();
      return;
    }

    const result = await buildVx(options);
    if (options.json) {
      process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
      return;
    }

    process.stdout.write(
      [
        `Built .vx: ${result.archivePath}`,
        `Extension: ${result.extension.id}`,
        `Version: ${result.extension.version}`,
        `Source HEAD: ${result.sourceState.head || '<unavailable>'}`,
        `Generated output cleanup: ${result.cleanup.performed ? 'performed' : 'not-needed'}`,
        `Archive entries: ${result.entriesCount}`,
        `Archive warnings: ${result.warnings.length}`,
        '',
      ].join('\n')
    );
  } catch (error) {
    process.stderr.write(`${error.message}\n`);
    process.exitCode = 1;
  }
}

if (require.main === module) {
  main();
}

module.exports = {
  buildVx,
  cleanGeneratedBuildOutput,
  createSnapshotVersion,
  inspectGeneratedBuildOutput,
  inspectGitSourceState,
  findArchive,
  inspectArchive,
  parseArgs,
  resolveBuildTooling,
  resolveExtensionMetadata,
  runGrunt,
};
