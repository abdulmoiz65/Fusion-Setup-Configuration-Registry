#!/usr/bin/env node
'use strict';

/**
 * Extract field-operation evidence from an immutable runtime evidence manifest.
 * Downloaded modules are parsed as data and are never evaluated or executed.
 */

const fs = require('node:fs');
const path = require('node:path');

class FieldContractError extends Error {
  constructor(code, message, details = null) {
    super(message);
    this.name = 'FieldContractError';
    this.code = code;
    this.details = details;
  }
}

function readOptionValue(argv, index, optionName) {
  const value = argv[index + 1];
  if (!value || value.startsWith('--')) {
    throw new FieldContractError('INVALID_ARGUMENT', `${optionName} requires a value.`);
  }
  return value;
}

function validateFieldPath(value) {
  const normalized = String(value || '').trim();
  if (!/^[A-Za-z_$][\w$-]*(?:\.[A-Za-z_$][\w$-]*)*$/.test(normalized)) {
    throw new FieldContractError('INVALID_FIELD_PATH', `Unsafe field path: ${value}`);
  }
  return normalized;
}

function parseArgs(argv) {
  const options = {
    evidenceManifest: null,
    serviceManifests: [],
    fields: [],
    all: false,
    inventory: false,
    json: false,
    help: false,
  };
  for (let index = 0; index < argv.length; index += 1) {
    const argument = argv[index];
    if (argument === '--evidence-manifest') {
      options.evidenceManifest = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--service-manifest') {
      options.serviceManifests.push(readOptionValue(argv, index, argument));
      index += 1;
    } else if (argument === '--field') {
      options.fields.push(validateFieldPath(readOptionValue(argv, index, argument)));
      index += 1;
    } else if (argument === '--all') {
      options.all = true;
    } else if (argument === '--inventory') {
      options.inventory = true;
    } else if (argument === '--json') {
      options.json = true;
    } else if (argument === '--help' || argument === '-h') {
      options.help = true;
    } else {
      throw new FieldContractError('INVALID_ARGUMENT', `Unknown argument: ${argument}`);
    }
  }
  if (!options.help && (
    !options.evidenceManifest
    || (options.fields.length === 0 && !options.all && !options.inventory)
  )) {
    throw new FieldContractError(
      'INVALID_ARGUMENT',
      '--evidence-manifest and at least one --field, --all, or --inventory are required.'
    );
  }
  options.fields = [...new Set(options.fields)].sort();
  options.serviceManifests = [...new Set(options.serviceManifests.map((item) => path.resolve(item)))];
  return options;
}

function readJson(filePath, code = 'INVALID_JSON') {
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (error) {
    throw new FieldContractError(code, `Unable to read JSON evidence: ${filePath}`);
  }
}

function readText(filePath, code = 'INVALID_TEXT_EVIDENCE') {
  // Advanced Expressions are inspected as inert source text and are never loaded as modules.
  try {
    return fs.readFileSync(filePath, 'utf8');
  } catch (error) {
    throw new FieldContractError(code, `Unable to read text evidence: ${filePath}`);
  }
}

function isWithin(root, candidate) {
  const relative = path.relative(root, candidate);
  return relative === '' || (!relative.startsWith('..') && !path.isAbsolute(relative));
}

function isJsonEvidenceItem(item) {
  // Runtime manifests may give JSON and AMD companions the same semantic role.
  return item?.mediaType === 'application/json'
    || (String(item?.moduleId || '').startsWith('text!')
      && String(item?.moduleId || '').endsWith('.json'));
}

function loadRuntimeEvidence(manifestPath) {
  const absolute = fs.realpathSync(path.resolve(manifestPath));
  const evidenceDirectory = path.dirname(absolute);
  const environmentRoot = path.dirname(evidenceDirectory);
  const manifest = readJson(absolute, 'INVALID_EVIDENCE_MANIFEST');
  if (![1, 2].includes(manifest.schemaVersion) || !Array.isArray(manifest.evidence)) {
    throw new FieldContractError('INVALID_EVIDENCE_MANIFEST', 'Unsupported runtime evidence manifest.');
  }
  const businessRules = manifest.evidence
    .filter((item) => item.role === 'business-and-validation-rules')
    .map((item) => {
      const evidencePath = fs.realpathSync(path.resolve(item.path));
      if (!isWithin(environmentRoot, evidencePath)) {
        throw new FieldContractError(
          'EVIDENCE_PATH_ESCAPE',
          'Runtime evidence path escapes its immutable environment cache.'
        );
      }
      return {
        moduleId: item.moduleId,
        sha256: item.sha256,
        path: evidencePath,
        content: readJson(evidencePath, 'INVALID_BUSINESS_RULES_EVIDENCE'),
      };
    });
  const dataDescriptions = manifest.evidence
    .filter((item) => item.role === 'data-description' && isJsonEvidenceItem(item))
    .map((item) => {
      const evidencePath = fs.realpathSync(path.resolve(item.path));
      if (!isWithin(environmentRoot, evidencePath)) {
        throw new FieldContractError(
          'EVIDENCE_PATH_ESCAPE',
          'Runtime evidence path escapes its immutable environment cache.'
        );
      }
      return {
        moduleId: item.moduleId,
        sha256: item.sha256,
        path: evidencePath,
        content: readJson(evidencePath, 'INVALID_DATA_DESCRIPTION_EVIDENCE'),
      };
    });
  const advancedExpressions = manifest.evidence
    .filter((item) => item.role === 'advanced-expression')
    .map((item) => {
      const evidencePath = fs.realpathSync(path.resolve(item.path));
      if (!isWithin(environmentRoot, evidencePath)) {
        throw new FieldContractError(
          'EVIDENCE_PATH_ESCAPE',
          'Runtime evidence path escapes its immutable environment cache.'
        );
      }
      return {
        moduleId: item.moduleId,
        sha256: item.sha256,
        path: evidencePath,
        content: readText(evidencePath),
      };
    });
  const loadLayoutEvidence = (role, parser) => manifest.evidence
    .filter((item) => item.role === role)
    .map((item) => {
      const evidencePath = fs.realpathSync(path.resolve(item.path));
      if (!isWithin(environmentRoot, evidencePath)) {
        throw new FieldContractError(
          'EVIDENCE_PATH_ESCAPE',
          'Runtime evidence path escapes its immutable environment cache.'
        );
      }
      return {
        moduleId: item.moduleId,
        sha256: item.sha256,
        path: evidencePath,
        content: parser(evidencePath),
      };
    });
  return {
    absolute,
    environmentRoot,
    manifest,
    businessRules,
    dataDescriptions,
    advancedExpressions,
    // Layout definitions and templates jointly prove how a field value is displayed.
    layoutDefinitions: loadLayoutEvidence(
      'dynamic-layout-definition',
      (evidencePath) => readJson(evidencePath, 'INVALID_LAYOUT_EVIDENCE')
    ),
    layoutTemplates: loadLayoutEvidence('layout-template-or-code', readText),
  };
}

function fieldDeclarationEvidence(metadata, fieldPath) {
  // Report literal declarations only; the model decides whether they prove a requested capability.
  const options = metadata?.['@dt']?.metadataRuleOptions;
  const overrides = options?.overrides?.fields;
  const conditions = options?.conditions;
  const fieldDefinition = overrides && !Array.isArray(overrides) ? overrides[fieldPath] : null;
  const conditionKeys = conditions && !Array.isArray(conditions) ? Object.keys(conditions) : [];
  const accessorRoot = `$fields.${fieldPath}`;
  const exactCondition = conditionKeys.includes(accessorRoot);
  const childConditions = conditionKeys.filter((candidate) => candidate.startsWith(`${accessorRoot}.`));
  const operations = fieldDefinition && !Array.isArray(fieldDefinition)
    ? Object.keys(fieldDefinition).sort()
    : [];
  const ruleOverlayOccurrences = (metadata?.metadataRules || []).flatMap((rule) => {
    const ruleField = rule?.overlay?.fields?.[fieldPath];
    if (!ruleField || Array.isArray(ruleField) || typeof ruleField !== 'object') return [];
    return [{
      ruleId: rule.id || null,
      ruleStatus: rule.status || null,
      operations: Object.keys(ruleField).sort(),
    }];
  });
  return {
    fieldOverrideDeclared: Boolean(fieldDefinition),
    declaredOverrideOperations: operations,
    listedAsSimpleCondition: exactCondition,
    listedChildSimpleConditionPaths: childConditions.sort(),
    ruleOverlayOccurrences,
  };
}

function combineDeclarationEvidence(records) {
  // Combine duplicate source declarations without assigning supported, unresolved, or unsupported states.
  return {
    fieldOverrideDeclaredIn: records
      .filter((record) => record.declaration.fieldOverrideDeclared)
      .map((record) => record.moduleId),
    declaredOverrideOperations: [
      ...new Set(records.flatMap((record) => record.declaration.declaredOverrideOperations)),
    ].sort(),
    listedAsSimpleConditionIn: records
      .filter((record) => record.declaration.listedAsSimpleCondition)
      .map((record) => record.moduleId),
    listedChildSimpleConditionPaths: [
      ...new Set(records.flatMap((record) => record.declaration.listedChildSimpleConditionPaths)),
    ].sort(),
    ruleOverlayOccurrences: records.flatMap((record) => (
      record.declaration.ruleOverlayOccurrences.map((occurrence) => ({
        moduleId: record.moduleId,
        sha256: record.sha256,
        ...occurrence,
      }))
    )),
  };
}

function escapeRegExp(value) {
  // Field paths are validated, but escaping keeps the source scanner exact and reusable.
  return String(value).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function lineAndColumnAt(source, index) {
  // Return one-based source coordinates without interpreting the downloaded expression.
  const prefix = source.slice(0, index);
  const lines = prefix.split(/\r?\n/);
  return { line: lines.length, column: lines[lines.length - 1].length + 1 };
}

function findAccessorCallSites(advancedExpressions, fieldPath) {
  // Search only literal dot-safe Business Rules accessor calls in inert Advanced Expression text.
  const pattern = new RegExp(
    `\\$fields\\.${escapeRegExp(fieldPath)}\\s*\\.\\s*\\$(value|initialValue)\\s*\\(`,
    'g'
  );
  const callSites = [];
  for (const evidence of advancedExpressions) {
    let match;
    while ((match = pattern.exec(evidence.content)) !== null) {
      callSites.push({
        accessor: `$${match[1]}`,
        moduleId: evidence.moduleId,
        sha256: evidence.sha256,
        ...lineAndColumnAt(evidence.content, match.index),
      });
    }
  }
  return callSites;
}

function inventoryFieldPaths(businessRules) {
  const paths = new Set();
  for (const item of businessRules) {
    const options = item.content?.['@dt']?.metadataRuleOptions;
    const overrides = options?.overrides?.fields;
    if (overrides && !Array.isArray(overrides)) {
      Object.keys(overrides).forEach((fieldPath) => paths.add(fieldPath));
    }
    const conditions = options?.conditions;
    if (conditions && !Array.isArray(conditions)) {
      Object.keys(conditions).forEach((accessorPath) => {
        // Inventory only dot-safe Business Rules paths; bracketed paths remain available in raw evidence.
        if (/^\$fields\.[A-Za-z_$][\w$-]*(?:\.[A-Za-z_$][\w$-]*)*$/.test(accessorPath)) {
          paths.add(accessorPath.slice('$fields.'.length));
        }
      });
    }
  }
  return [...paths].sort();
}

function normalizedFieldType(definition) {
  if (!definition || Array.isArray(definition) || typeof definition !== 'object') return null;
  const candidate = definition.type
    || definition.dataType
    || definition.valueType
    || definition.schema?.type;
  return typeof candidate === 'string' && candidate.trim() ? candidate.trim() : null;
}

function normalizedFieldLabel(definition) {
  if (!definition || Array.isArray(definition) || typeof definition !== 'object') return null;
  const candidate = definition.label
    || definition.labelHint
    || definition.title
    || definition.displayName
    || definition.description;
  return typeof candidate === 'string' && candidate.trim() ? candidate.trim() : null;
}

function collectDataDescriptionFields(dataDescriptions) {
  const records = new Map();
  const addRecord = (fieldPath, definition, evidence, pointer) => {
    try {
      validateFieldPath(fieldPath);
    } catch (error) {
      return;
    }
    const existing = records.get(fieldPath) || {
      path: fieldPath,
      labels: new Set(),
      types: new Set(),
      valueContracts: [],
      evidence: [],
    };
    const label = normalizedFieldLabel(definition);
    const type = normalizedFieldType(definition);
    if (label) existing.labels.add(label);
    if (type) existing.types.add(type);
    const valueContract = {
      // Preserve only declarative value-shape facts; never infer semantic scale from a label.
      format: typeof definition?.format === 'string' ? definition.format : null,
      scaleFactor: definition?.scaleFactor ?? null,
      percentScale: definition?.percentScale ?? null,
      minimum: definition?.minimum ?? null,
      maximum: definition?.maximum ?? null,
    };
    if (Object.values(valueContract).some((value) => value !== null)) {
      existing.valueContracts.push({ ...valueContract, moduleId: evidence.moduleId, pointer });
    }
    existing.evidence.push({
      moduleId: evidence.moduleId,
      sha256: evidence.sha256,
      pointer,
    });
    records.set(fieldPath, existing);
  };

  const visit = (value, evidence, pointer = '', ownerPath = null) => {
    if (Array.isArray(value)) {
      value.forEach((item, index) => visit(item, evidence, `${pointer}/${index}`, ownerPath));
      return;
    }
    if (!value || typeof value !== 'object') return;
    for (const [key, child] of Object.entries(value)) {
      const childPointer = `${pointer}/${key.replace(/~/g, '~0').replace(/\//g, '~1')}`;
      if ((key === 'fields' || key === 'properties')
          && child && !Array.isArray(child) && typeof child === 'object') {
        for (const [fieldName, definition] of Object.entries(child)) {
          const fieldPath = fieldName.includes('.')
            ? fieldName
            : (ownerPath ? `${ownerPath}.${fieldName}` : fieldName);
          addRecord(fieldPath, definition, evidence, `${childPointer}/${fieldName}`);
          visit(definition, evidence, `${childPointer}/${fieldName}`, fieldPath);
        }
        continue;
      }
      const nextOwner = child
        && !Array.isArray(child)
        && typeof child === 'object'
        && (child.fields || child.properties)
        && !key.startsWith('$')
        && /^[A-Za-z_$][\w$-]*$/.test(key)
        ? (ownerPath ? `${ownerPath}.${key}` : key)
        : ownerPath;
      visit(child, evidence, childPointer, nextOwner);
    }
  };

  dataDescriptions.forEach((evidence) => visit(evidence.content, evidence));
  return records;
}

function collectTemplateIds(value, fieldName, collected = new Set()) {
  if (Array.isArray(value)) {
    value.forEach((item) => collectTemplateIds(item, fieldName, collected));
    return collected;
  }
  if (!value || typeof value !== 'object') return collected;
  for (const [key, child] of Object.entries(value)) {
    if (key === 'fieldTemplateMap' && child && typeof child === 'object' && !Array.isArray(child)) {
      const templateId = child[fieldName];
      if (typeof templateId === 'string' && templateId.trim()) collected.add(templateId.trim());
    }
    collectTemplateIds(child, fieldName, collected);
  }
  return collected;
}

function dynamicLayoutIdentity(moduleId) {
  const match = String(moduleId || '').match(/\/dynamicLayouts\/([^/]+)\/([^/]+)\//);
  return match ? { owner: match[1], layout: match[2] } : null;
}

function templateBlock(source, templateId) {
  // Template IDs are sourced from parsed JSON but still escaped before text matching.
  const escaped = escapeRegExp(templateId);
  const pattern = new RegExp(
    `<template\\b[^>]*\\bid=["']${escaped}["'][^>]*>([\\s\\S]*?)<\\/template>`,
    'i'
  );
  return String(source || '').match(pattern)?.[0] || null;
}

function collectRenderedPercentageContracts(runtime, fieldPath) {
  const [owningObject, ...fieldSegments] = fieldPath.split('.');
  if (!owningObject || fieldSegments.length !== 1) return [];
  const fieldName = fieldSegments[0];
  const contracts = [];
  for (const definition of runtime.layoutDefinitions) {
    const identity = dynamicLayoutIdentity(definition.moduleId);
    if (!identity || identity.layout !== owningObject) continue;
    const templateIds = collectTemplateIds(definition.content, fieldName);
    for (const template of runtime.layoutTemplates) {
      const templateIdentity = dynamicLayoutIdentity(template.moduleId);
      if (!templateIdentity || templateIdentity.layout !== identity.layout) continue;
      for (const templateId of templateIds) {
        const block = templateBlock(template.content, templateId);
        if (!block || !/\binput-suffix\s*=\s*(?:"[^"]*%[^"]*"|'[^']*%[^']*')/i.test(block)) {
          continue;
        }
        contracts.push({
          // The field template binds the raw numeric value and appends %, so 10 is displayed as 10%.
          format: 'percentage',
          scaleFactor: 1,
          percentScale: 'whole-number-percent',
          minimum: null,
          maximum: null,
          templateId,
          moduleId: template.moduleId,
          definitionModuleId: definition.moduleId,
          pointer: null,
        });
      }
    }
  }
  return contracts;
}

function inventoryFieldRecords(runtime) {
  const described = collectDataDescriptionFields(runtime.dataDescriptions);
  const paths = new Set([
    ...inventoryFieldPaths(runtime.businessRules),
    ...described.keys(),
  ]);
  return [...paths].sort().map((fieldPath) => {
    const description = described.get(fieldPath);
    const types = description ? [...description.types].sort() : [];
    return {
      path: fieldPath,
      labels: description ? [...description.labels].sort() : [],
      types,
      valueContracts: description ? description.valueContracts : [],
      owningObject: fieldPath.includes('.') ? fieldPath.split('.')[0] : null,
      evidence: description ? description.evidence : [],
    };
  });
}

function childAtPath(schema, segments) {
  let children = schema?.children;
  let current = null;
  for (const segment of segments) {
    if (!Array.isArray(children)) return null;
    current = children.find((child) => child.name.toLowerCase() === segment.toLowerCase()) || null;
    if (!current) return null;
    children = current.children;
  }
  return current;
}

function serviceEvidenceForField(serviceManifests, fieldPath, environmentRoot = null) {
  const segments = fieldPath.split('.');
  const root = segments.shift();
  const matches = [];
  for (const filePath of serviceManifests) {
    const absolute = fs.realpathSync(path.resolve(filePath));
    if (environmentRoot && !isWithin(environmentRoot, absolute)) {
      throw new FieldContractError(
        'SERVICE_EVIDENCE_PATH_ESCAPE',
        'Service evidence must belong to the same immutable environment cache.'
      );
    }
    const manifest = readJson(absolute, 'INVALID_SERVICE_MANIFEST');
    if (![1, 2].includes(manifest.schemaVersion) || manifest.shapeDomain !== 'rest-schema') continue;
    if (String(manifest.target?.resource || '').toLowerCase() !== root.toLowerCase()) continue;
    const child = segments.length > 0 ? childAtPath(manifest.schema, segments) : null;
    const attributeName = child ? null : segments.at(-1) || null;
    const attributeParent = attributeName && segments.length > 1
      ? childAtPath(manifest.schema, segments.slice(0, -1))
      : null;
    const attributeSource = child
      ? (child.attributes || [])
      : (attributeParent?.attributes || manifest.schema?.attributes || []);
    matches.push({
      manifest: absolute,
      resource: manifest.target.resource,
      childPath: child?.path || null,
      // A missing requested child must not silently inherit root-resource attributes.
      attributes: attributeSource
        .filter((attribute) => !attributeName || attribute.name.toLowerCase() === attributeName.toLowerCase())
        .map((attribute) => ({
        name: attribute.name,
        type: attribute.type,
        updatable: attribute.updatable,
      })),
      shapeDomain: manifest.shapeDomain,
    });
  }
  return matches;
}

function buildFieldReport(options) {
  const runtime = loadRuntimeEvidence(options.evidenceManifest);
  const inventory = inventoryFieldRecords(runtime);
  if (options.inventory && !options.all) {
    // Inventory is a semantic-selection index, not a contract evaluation for every field.
    // Avoid the quadratic declarations/accessor scan that made page-wide discovery slow
    // and produced multi-megabyte repeated evidence.
    return {
      schemaVersion: 2,
      target: runtime.manifest.target,
      routeEvidence: {
        dynamicLayoutDefinitions: runtime.manifest.evidence
          .filter((item) => item.role === 'dynamic-layout-definition')
          .map((item) => ({ moduleId: item.moduleId, sha256: item.sha256 })),
        unresolvedCount: runtime.manifest.unresolved?.length || 0,
      },
      runtimeShapeVerification: runtime.manifest.runtimeShapeVerification || {
        observed: false,
        source: 'legacy-static-deployed-evidence',
      },
      fields: inventory.map((field) => ({
        path: field.path,
        labels: field.labels || [],
        types: field.types || [],
        valueContracts: field.valueContracts || [],
        owningObject: field.owningObject || null,
        evidence: field.evidence || [],
      })),
    };
  }
  const requestedFields = options.all || options.inventory
    ? inventory.map((field) => field.path)
    : options.fields;
  return {
    schemaVersion: 2,
    target: runtime.manifest.target,
    routeEvidence: {
      // Preserve graph facts so the model can decide whether route ownership affects the claim.
      dynamicLayoutDefinitions: runtime.manifest.evidence
        .filter((item) => item.role === 'dynamic-layout-definition')
        .map((item) => ({ moduleId: item.moduleId, sha256: item.sha256 })),
      unresolved: runtime.manifest.unresolved || [],
    },
    runtimeShapeVerification: runtime.manifest.runtimeShapeVerification || {
      observed: false,
      source: 'legacy-static-deployed-evidence',
    },
    fields: requestedFields.map((fieldPath) => {
      const inventoryRecord = inventory.find((field) => field.path === fieldPath);
      const renderedValueContracts = collectRenderedPercentageContracts(runtime, fieldPath);
      const declarations = runtime.businessRules.map((item) => ({
        moduleId: item.moduleId,
        sha256: item.sha256,
        declaration: fieldDeclarationEvidence(item.content, fieldPath),
      }));
      return {
        path: fieldPath,
        labels: inventoryRecord?.labels || [],
        types: inventoryRecord?.types || [],
        valueContracts: [
          ...(inventoryRecord?.valueContracts || []),
          ...renderedValueContracts,
        ],
        owningObject: inventoryRecord?.owningObject
          || (fieldPath.includes('.') ? fieldPath.split('.')[0] : null),
        businessRules: {
          declarations,
          combinedDeclarations: combineDeclarationEvidence(declarations),
          accessorCallSites: findAccessorCallSites(runtime.advancedExpressions, fieldPath),
        },
        evidence: [
          ...declarations.map(({ moduleId, sha256 }) => ({ moduleId, sha256 })),
          ...(inventoryRecord?.evidence || []),
          ...renderedValueContracts.map((contract) => ({
            moduleId: contract.moduleId,
            definitionModuleId: contract.definitionModuleId,
          })),
        ],
        restSchema: serviceEvidenceForField(
          options.serviceManifests,
          fieldPath,
          runtime.environmentRoot
        ),
      };
    }),
  };
}

function printHelp() {
  process.stdout.write([
    'Extract deployed Business Rules field-operation contracts',
    '',
    'Usage:',
    '  node scripts/extract_business_rule_contracts.js',
    '    --evidence-manifest <runtime-evidence.json>',
    '    (--field <owningObject.fieldPath> [--field <path> ...] | --all | --inventory)',
    '    [--service-manifest <service-evidence.json> ...] [--json]',
    '',
  ].join('\n'));
}

function main() {
  try {
    const options = parseArgs(process.argv.slice(2));
    if (options.help) return printHelp();
    const report = buildFieldReport(options);
    process.stdout.write(options.json
      ? `${JSON.stringify(report, null, 2)}\n`
      : `${report.fields.length} raw field evidence record(s)\n`);
  } catch (error) {
    const payload = {
      error: {
        code: error.code || 'UNEXPECTED_ERROR',
        message: error.message,
        details: error.details || null,
      },
    };
    process.stderr.write(`${JSON.stringify(payload, null, 2)}\n`);
    process.exitCode = 1;
  }
}

if (require.main === module) main();

module.exports = {
  FieldContractError,
  buildFieldReport,
  collectRenderedPercentageContracts,
  childAtPath,
  combineDeclarationEvidence,
  fieldDeclarationEvidence,
  findAccessorCallSites,
  inventoryFieldPaths,
  inventoryFieldRecords,
  collectDataDescriptionFields,
  loadRuntimeEvidence,
  parseArgs,
  serviceEvidenceForField,
  validateFieldPath,
};
