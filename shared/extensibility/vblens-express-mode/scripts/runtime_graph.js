#!/usr/bin/env node
'use strict';

/**
 * Resolve the smallest static evidence closure connecting an App UI page to
 * reachable fragments, dynamic components, layouts, rules, and service data.
 */

const path = require('node:path');
const {
  RuntimeEvidenceError,
  readCachedModule,
  validateIdentifier,
} = require('./runtime_bundle');

const DEFAULT_LIMITS = Object.freeze({
  maxBundles: 10,
  maxDepth: 12,
  maxNodes: 5000,
});

function portableBasename(value) {
  const segments = String(value || '').split('/');
  return segments[segments.length - 1] || '';
}

function derivePageId(fileName) {
  const suffixes = [
    '-page-rules.json',
    '-page-r.json',
    '-page.json',
    '-page.html',
    '-page.js',
    '-page',
  ];
  const suffix = suffixes.find((candidate) => fileName.endsWith(candidate));
  return suffix ? fileName.slice(0, -suffix.length) || null : null;
}

function parseUiPageIdentity(logicalPath) {
  const segments = String(logicalPath || '').split('/');
  const applicationsIndex = segments.indexOf('applications');
  const pagesIndex = segments.lastIndexOf('pages');
  if (
    segments[0] !== 'ui'
    || applicationsIndex < 0
    || pagesIndex <= applicationsIndex + 1
    || !segments[applicationsIndex + 1]
    || !segments[pagesIndex + 1]
  ) {
    return null;
  }
  const flowSegments = [];
  for (let index = applicationsIndex + 2; index < pagesIndex; index += 1) {
    if (segments[index] === 'flows' && segments[index + 1]) {
      flowSegments.push(segments[index + 1]);
      index += 1;
    }
  }
  const page = derivePageId(segments[pagesIndex + 1]);
  if (!page) return null;
  return {
    producer: segments[1],
    application: segments[applicationsIndex + 1],
    flow: flowSegments.join('/'),
    page,
    pageDirectory: segments.slice(0, pagesIndex + 1).join('/'),
  };
}

function parseAttributes(source) {
  const attributes = {};
  const pattern = /([:@A-Za-z_][:@A-Za-z0-9_.-]*)\s*=\s*("[^"]*"|'[^']*')/g;
  for (const match of source.matchAll(pattern)) {
    attributes[match[1]] = match[2].slice(1, -1);
  }
  return attributes;
}

function scanHtmlStartTags(html) {
  const tags = [];
  let cursor = 0;
  while (cursor < html.length) {
    const open = html.indexOf('<', cursor);
    if (open < 0) break;
    if (html.startsWith('<!--', open)) {
      const commentEnd = html.indexOf('-->', open + 4);
      cursor = commentEnd < 0 ? html.length : commentEnd + 3;
      continue;
    }
    const nameMatch = html.slice(open + 1).match(/^([A-Za-z][A-Za-z0-9_.:-]*)\b/);
    if (!nameMatch) {
      cursor = open + 1;
      continue;
    }
    let end = open + 1 + nameMatch[0].length;
    let quote = null;
    for (; end < html.length; end += 1) {
      const character = html[end];
      if (quote) {
        if (character === quote) quote = null;
      } else if (character === '"' || character === "'") {
        quote = character;
      } else if (character === '>') {
        break;
      }
    }
    if (end >= html.length) break;
    tags.push({
      name: nameMatch[1],
      attributesSource: html.slice(open + 1 + nameMatch[0].length, end),
      offset: open,
    });
    cursor = end + 1;
  }
  return tags;
}

function extractFragmentReferences(html) {
  const references = [];
  for (const tag of scanHtmlStartTags(html)) {
    if (tag.name.toLowerCase() !== 'oj-vb-fragment') continue;
    const attributes = parseAttributes(tag.attributesSource);
    if (!attributes.name) continue;
    const dynamic = /\[\[|\{\{/.test(attributes.name);
    references.push({
      name: attributes.name,
      dynamic,
      offset: tag.offset,
    });
  }
  return references;
}

function extractLiteralGuidedStepFragments(source) {
  // Read only bounded, flat object-literal text emitted by the VB page controller.
  // Downloaded JavaScript is never evaluated, and nested or computed values are ignored.
  const fragments = [];
  const objectPattern = /\{[^{}]{0,8192}\}/g;
  for (const objectMatch of String(source || '').matchAll(objectPattern)) {
    const objectSource = objectMatch[0];
    const idMatch = objectSource.match(/\bid\s*:\s*(["'])([A-Za-z_$][\w$-]*)\1/);
    const fragmentMatch = objectSource.match(
      /\bfragmentName\s*:\s*(["'])([A-Za-z0-9_$-]+(?::[A-Za-z0-9_$-]+)?)\1/
    );
    if (!idMatch || !fragmentMatch) continue;
    const sectionMatch = objectSource.match(
      /\bsectionFieldId\s*:\s*(["'])([A-Za-z0-9_.$-]+)\1/
    );
    fragments.push({
      id: idMatch[2],
      fragmentName: fragmentMatch[2],
      sectionFieldId: sectionMatch ? sectionMatch[2] : null,
      offset: objectMatch.index,
    });
  }
  return fragments;
}

function isGuidedStepMapReference(referenceName) {
  // Resolve only the known HCM Guided Process selector backed by page-local step literals.
  return /^\[\[\s*\$variables\.stepMap\[\$variables\.currentFragment\]\.fragmentName\s*\]\]$/
    .test(String(referenceName || ''));
}

function extractDynamicComponents(html) {
  const components = [];
  for (const tag of scanHtmlStartTags(html)) {
    if (!/^oj-(?:dyn|dynamic)-(?:form|table|container)$/i.test(tag.name)) continue;
    const attributes = parseAttributes(tag.attributesSource);
    const metadataExpression = attributes.metadata
      || attributes['metadata-provider']
      || attributes['layout-provider']
      || null;
    const providerMatch = metadataExpression
      ? metadataExpression.match(
        /\$metadata(?:\.([A-Za-z0-9_$-]+)|\[['"]([^'"]+)['"]\])(?:\.provider|\[['"]provider['"]\])/
      )
      : null;
    const layoutExpression = attributes.layout || attributes['layout-name'] || null;
    const literalLayouts = [];
    if (layoutExpression) {
      // Conditional layout expressions may expose safe literal alternatives without evaluation.
      for (const match of layoutExpression.matchAll(/(["'])([A-Za-z_$][\w$-]*)\1/g)) {
        if (!literalLayouts.includes(match[2])) literalLayouts.push(match[2]);
      }
    }
    components.push({
      tag: tag.name,
      attributes,
      metadataExpression,
      metadataName: providerMatch ? providerMatch[1] || providerMatch[2] : null,
      layoutExpression,
      literalLayout: layoutExpression && !/\[\[|\{\{/.test(layoutExpression)
        ? layoutExpression
        : null,
      literalLayouts,
      offset: tag.offset,
    });
  }
  return components;
}

function parseJsonModule(cache, record) {
  const cached = readCachedModule(cache, record);
  try {
    return { ...cached, value: JSON.parse(cached.content) };
  } catch (error) {
    throw new RuntimeEvidenceError(
      'MODULE_JSON_INVALID',
      `Cached JSON module ${record.id} is invalid: ${error.message}`
    );
  }
}

function moduleFamilyRecords(cache, prefix) {
  return cache.index.modules.filter((record) => (
    record.logicalPath === prefix
    || record.logicalPath.startsWith(`${prefix}.`)
    || record.logicalPath.startsWith(`${prefix}-`)
    || record.logicalPath.startsWith(`${prefix}/`)
  ));
}

function findUiPage(cache, target) {
  const candidates = new Map();
  for (const record of cache.index.modules) {
    const identity = parseUiPageIdentity(record.logicalPath);
    if (!identity || identity.flow !== target.flow || identity.page !== target.page) continue;
    if (target.application && identity.application !== target.application) continue;
    const key = [identity.producer, identity.application, identity.flow, identity.page].join('|');
    candidates.set(key, identity);
  }
  if (candidates.size === 0) {
    throw new RuntimeEvidenceError(
      'PAGE_NOT_FOUND',
      `No deployed UI page matches flow ${target.flow} and page ${target.page}.`
    );
  }
  if (candidates.size > 1) {
    throw new RuntimeEvidenceError(
      'PAGE_AMBIGUOUS',
      `Multiple deployed pages match flow ${target.flow} and page ${target.page}.`,
      { candidates: [...candidates.values()] }
    );
  }
  const identity = [...candidates.values()][0];
  const familyPrefix = `${identity.pageDirectory}/${identity.page}-page`;
  const records = moduleFamilyRecords(cache, familyPrefix);
  if (records.length === 0) {
    throw new RuntimeEvidenceError('PAGE_NOT_FOUND', `Page module family ${familyPrefix} is empty.`);
  }
  return {
    identity,
    familyPrefix,
    scopeDirectory: identity.pageDirectory,
    records,
  };
}

function extractActionChainIds(value, collected = new Set()) {
  if (Array.isArray(value)) {
    for (const item of value) extractActionChainIds(item, collected);
    return collected;
  }
  if (!value || typeof value !== 'object') return collected;
  for (const [key, child] of Object.entries(value)) {
    if (key === 'chainId' && typeof child === 'string' && child.trim()) {
      collected.add(child.trim());
    } else {
      extractActionChainIds(child, collected);
    }
  }
  return collected;
}

function findActionChainFamily(cache, familyPrefix, scopeDirectory, chainId) {
  // Current VB output places chains beside the owning page/fragment family;
  // older output uses a shared chains directory under the containing scope.
  const candidatePrefixes = [...new Set([
    familyPrefix ? `${familyPrefix}-chains/${chainId}` : null,
    scopeDirectory ? `${scopeDirectory}/chains/${chainId}` : null,
  ].filter(Boolean))];
  const matches = candidatePrefixes.map((prefix) => ({
    prefix,
    records: moduleFamilyRecords(cache, prefix),
  })).filter((candidate) => candidate.records.length > 0);
  if (matches.length === 0) return null;
  if (matches.length > 1) {
    return {
      ambiguous: true,
      candidates: matches.map((candidate) => candidate.prefix).sort(),
    };
  }
  return matches[0];
}

function splitFragmentName(referenceName, currentExtension) {
  const separator = referenceName.indexOf(':');
  if (separator < 0) return { extension: currentExtension, fragment: referenceName };
  return {
    extension: referenceName.slice(0, separator),
    fragment: referenceName.slice(separator + 1),
  };
}

function findFragmentFamily(cache, fragmentName) {
  const fragment = validateIdentifier(fragmentName, 'Fragment name');
  const marker = `/fragments/${fragment}/`;
  const records = cache.index.modules.filter((record) => record.logicalPath.includes(marker));
  if (records.length === 0) return null;
  const scopeDirectories = new Set(records.map((record) => {
    const markerIndex = record.logicalPath.indexOf(marker);
    return `${record.logicalPath.slice(0, markerIndex)}${marker.slice(0, -1)}`;
  }));
  if (scopeDirectories.size > 1) {
    return {
      ambiguous: true,
      candidates: [...scopeDirectories].sort(),
      roots: [],
      scopeDirectory: null,
      records: [],
    };
  }
  const scopeDirectory = [...scopeDirectories][0];
  const familyRoot = `${scopeDirectory}/${fragment}-fragment`;
  const matchingRecords = moduleFamilyRecords(cache, familyRoot);
  if (matchingRecords.length === 0) return null;
  return {
    roots: [familyRoot],
    scopeDirectory,
    records: matchingRecords,
  };
}

function escapeJsonPointerSegment(value) {
  return String(value).replace(/~/g, '~0').replace(/\//g, '~1');
}

function serviceIdentityFromEndpoint(endpoint) {
  const normalized = String(endpoint || '').trim();
  if (!normalized) return null;
  return normalized.split('/')[0] || null;
}

function extensionFromServiceId(serviceId, fallbackExtension) {
  const separator = String(serviceId || '').indexOf(':');
  return separator > 0 ? serviceId.slice(0, separator) : fallbackExtension;
}

function findLayoutCandidates(cache, serviceId, literalLayout) {
  const candidates = [];
  for (const record of cache.index.modules) {
    if (
      record.kind !== 'text'
      || !record.logicalPath.startsWith('dynamicLayouts/')
      || !record.logicalPath.endsWith('/layout.json')
    ) {
      continue;
    }
    const parsed = parseJsonModule(cache, record);
    const layoutTypes = parsed.value.layoutTypes && typeof parsed.value.layoutTypes === 'object'
      ? Object.values(parsed.value.layoutTypes)
      : [];
    const serviceMatches = !serviceId || layoutTypes.some((type) => type?.serviceId === serviceId);
    const layoutMatches = !literalLayout || Boolean(parsed.value.layouts?.[literalLayout]);
    if (!serviceMatches || !layoutMatches) continue;
    const layoutRoot = record.logicalPath.slice(0, -'/layout.json'.length);
    candidates.push({
      cache,
      record,
      value: parsed.value,
      layoutRoot,
      selectedLayout: literalLayout || null,
    });
  }
  return candidates;
}

function evidenceRole(record) {
  const baseName = portableBasename(record.logicalPath);
  if (baseName === 'layout.json') return 'dynamic-layout-definition';
  if (baseName === 'metadata-rules.json') return 'business-and-validation-rules';
  if (baseName.startsWith('data-description')) return 'data-description';
  if (baseName.includes('page-r')) return 'page-property-rules';
  if (record.logicalPath.includes('/metadataRules/')) return 'advanced-expression';
  if (record.logicalPath.includes('/chains/')) return 'action-chain';
  if (record.logicalPath.includes('/services/')) return 'service-metadata';
  if (record.logicalPath.includes('/pages/')) return 'page-source';
  if (record.logicalPath.includes('/fragments/')) return 'fragment-source';
  if (baseName.startsWith('layout.')) return 'layout-template-or-code';
  return 'supporting-runtime-module';
}

function evidenceRoleOrder(role) {
  const order = [
    'page-source',
    'page-property-rules',
    'fragment-source',
    'dynamic-layout-definition',
    'business-and-validation-rules',
    'advanced-expression',
    'data-description',
    'layout-template-or-code',
    'action-chain',
    'service-metadata',
    'supporting-runtime-module',
  ];
  const index = order.indexOf(role);
  return index < 0 ? order.length : index;
}

function artifactLayer(record) {
  const baseName = portableBasename(record.logicalPath);
  if (baseName === 'data-description.json') return 'data-description-base';
  if (baseName === 'data-description-overlay.json') return 'data-description-overlay';
  if (baseName === 'metadata-rules.json') return 'business-rules-base';
  if (baseName.includes('page-r')) return 'page-properties-base';
  return 'oracle-base-bundle';
}

function evidenceShapeDomain(record, role = evidenceRole(record)) {
  // Classify what a static module can prove without promoting it to observed runtime evidence.
  if (role === 'business-and-validation-rules' || role === 'advanced-expression') {
    return 'business-rules';
  }
  if (role === 'service-metadata') return 'rest-schema';
  if (role === 'data-description') return 'business-rules';
  return 'page-state';
}

class EvidenceGraphBuilder {
  constructor(options) {
    this.applicationIndex = options.applicationIndex;
    this.loadBundle = options.loadBundle;
    this.limits = { ...DEFAULT_LIMITS, ...(options.limits || {}) };
    this.bundleCaches = new Map();
    this.nodes = new Map();
    this.edges = [];
    this.edgeKeys = new Set();
    this.evidence = new Map();
    this.unresolved = [];
    this.visitedFragments = new Set();
    this.visitedLayouts = new Set();
    this.visitedActionChains = new Set();
    this.guidedStepFragments = new Map();
    this.guidedStepConflicts = new Set();
    this.pageMetadataLayoutTargets = new Map();
  }

  addNode(node) {
    if (!this.nodes.has(node.id) && this.nodes.size >= this.limits.maxNodes) {
      throw new RuntimeEvidenceError(
        'GRAPH_LIMIT_EXCEEDED',
        `Evidence graph exceeded ${this.limits.maxNodes} nodes.`
      );
    }
    this.nodes.set(node.id, { ...this.nodes.get(node.id), ...node });
    return node.id;
  }

  addEdge(from, to, type) {
    const key = `${from}\0${to}\0${type}`;
    if (this.edgeKeys.has(key)) return;
    this.edgeKeys.add(key);
    this.edges.push({ from, to, type });
  }

  addUnresolved(code, source, reference, message, candidates = []) {
    this.unresolved.push({
      code,
      source,
      reference,
      message,
      candidates: candidates.slice(0, 25),
    });
  }

  addEvidence(cache, record, reason, role = evidenceRole(record)) {
    const cached = readCachedModule(cache, record);
    if (!this.evidence.has(record.id)) {
      this.evidence.set(record.id, {
        role,
        moduleId: record.id,
        path: cached.filePath,
        sha256: record.sha256,
        sizeBytes: record.sizeBytes,
        mediaType: record.mediaType,
        sourceLayer: 'oracle-delivered',
        artifactLayer: artifactLayer(record),
        shapeDomain: evidenceShapeDomain(record, role),
        reasons: [],
      });
    }
    const evidence = this.evidence.get(record.id);
    if (!evidence.reasons.includes(reason)) evidence.reasons.push(reason);
    const moduleNode = this.addNode({
      id: `module:${record.id}`,
      type: 'module',
      extension: cache.manifest.extension.id,
      version: cache.manifest.extension.version,
      moduleId: record.id,
      role,
    });
    return { evidence, moduleNode, content: cached.content };
  }

  async ensureBundle(extensionId) {
    if (this.bundleCaches.has(extensionId)) return this.bundleCaches.get(extensionId);
    if (this.bundleCaches.size >= this.limits.maxBundles) {
      throw new RuntimeEvidenceError(
        'GRAPH_LIMIT_EXCEEDED',
        `Evidence graph exceeded ${this.limits.maxBundles} extension bundles.`
      );
    }
    if (!this.applicationIndex.has(extensionId)) {
      this.addUnresolved(
        'REFERENCED_APP_NOT_DEPLOYED',
        'app-info',
        extensionId,
        `Referenced extension ${extensionId} is absent from app-ui-info.`
      );
      return null;
    }
    const cache = await this.loadBundle(extensionId);
    this.bundleCaches.set(extensionId, cache);
    this.addNode({
      id: `bundle:${extensionId}@${cache.manifest.extension.version}`,
      type: 'bundle',
      extension: extensionId,
      version: cache.manifest.extension.version,
    });
    return cache;
  }

  async includeModuleFamily(cache, records, parentNode, reason) {
    const artifacts = [];
    for (const record of records) {
      const added = this.addEvidence(cache, record, reason);
      this.addEdge(parentNode, added.moduleNode, 'supported-by');
      artifacts.push({ record, content: added.content });
    }
    return artifacts;
  }

  async visitUiFamily(cache, family, nodeId, depth) {
    if (depth > this.limits.maxDepth) {
      this.addUnresolved(
        'GRAPH_DEPTH_EXCEEDED',
        nodeId,
        family.familyPrefix || nodeId,
        `Dependency traversal exceeded depth ${this.limits.maxDepth}.`
      );
      return;
    }
    const artifacts = await this.includeModuleFamily(
      cache,
      family.records,
      nodeId,
      `Reachable UI source for ${nodeId}`
    );
    const jsonValues = [];
    for (const artifact of artifacts) {
      if (artifact.record.kind === 'text' && artifact.record.logicalPath.endsWith('.json')) {
        jsonValues.push(JSON.parse(artifact.content));
      }
    }
    const descriptorMetadata = Object.assign(
      {},
      ...jsonValues.map((value) => (
        value.metadata && typeof value.metadata === 'object' ? value.metadata : {}
      ))
    );
    for (const artifact of artifacts) {
      if (artifact.record.kind !== 'amd') continue;
      for (const step of extractLiteralGuidedStepFragments(artifact.content)) {
        // A duplicate step must agree exactly; conflicting literals stay unresolved.
        if (this.guidedStepConflicts.has(step.id)) continue;
        const existing = this.guidedStepFragments.get(step.id);
        if (existing && existing.fragmentName !== step.fragmentName) {
          this.addUnresolved(
            'GUIDED_STEP_FRAGMENT_AMBIGUOUS',
            artifact.record.id,
            step.id,
            `Guided Process step ${step.id} has conflicting literal fragment names.`,
            [existing.fragmentName, step.fragmentName]
          );
          this.guidedStepFragments.delete(step.id);
          this.guidedStepConflicts.add(step.id);
          continue;
        }
        this.guidedStepFragments.set(step.id, {
          ...step,
          source: artifact.record.id,
        });
      }
    }

    await this.includeStaticMetadataLayouts(
      cache,
      descriptorMetadata,
      nodeId,
      depth + 1
    );

    const chainIds = new Set();
    for (const value of jsonValues) extractActionChainIds(value, chainIds);
    for (const chainId of chainIds) {
      await this.visitActionChain(
        cache,
        family,
        chainId,
        nodeId,
        depth + 1
      );
    }

    for (const artifact of artifacts) {
      if (artifact.record.kind !== 'text' || artifact.record.mediaType !== 'text/html') continue;
      for (const reference of extractFragmentReferences(artifact.content)) {
        if (reference.dynamic) {
          if (isGuidedStepMapReference(reference.name) && this.guidedStepFragments.size > 0) {
            for (const step of this.guidedStepFragments.values()) {
              await this.visitFragment(
                cache.manifest.extension.id,
                step.fragmentName,
                nodeId,
                depth + 1,
                'resolves-guided-step-fragment'
              );
            }
            continue;
          }
          this.addUnresolved(
            'DYNAMIC_FRAGMENT_REFERENCE',
            artifact.record.id,
            reference.name,
            'Fragment name is computed at runtime and cannot be followed statically.'
          );
          continue;
        }
        await this.visitFragment(cache.manifest.extension.id, reference.name, nodeId, depth + 1);
      }

      const components = extractDynamicComponents(artifact.content);
      for (let index = 0; index < components.length; index += 1) {
        await this.visitDynamicComponent(
          cache,
          components[index],
          descriptorMetadata,
          nodeId,
          `${artifact.record.id}#component-${index + 1}`,
          depth + 1
        );
      }
    }
  }

  async visitActionChain(cache, family, chainId, parentNode, depth) {
    if (!family || (!family.familyPrefix && !family.scopeDirectory)) return;
    if (depth > this.limits.maxDepth) {
      this.addUnresolved(
        'GRAPH_DEPTH_EXCEEDED',
        parentNode,
        chainId,
        `Dependency traversal exceeded depth ${this.limits.maxDepth}.`
      );
      return;
    }
    let chain;
    try {
      chain = validateIdentifier(chainId, 'Action-chain ID', { allowPath: true });
    } catch (error) {
      this.addUnresolved('ACTION_CHAIN_REFERENCE_INVALID', parentNode, chainId, error.message);
      return;
    }
    const chainFamily = findActionChainFamily(
      cache,
      family.familyPrefix,
      family.scopeDirectory,
      chain
    );
    if (!chainFamily) {
      this.addUnresolved(
        'ACTION_CHAIN_NOT_FOUND',
        parentNode,
        chain,
        `Referenced action chain ${chain} is absent from the deployed bundle.`
      );
      return;
    }
    if (chainFamily.ambiguous) {
      this.addUnresolved(
        'ACTION_CHAIN_AMBIGUOUS',
        parentNode,
        chain,
        `Referenced action chain ${chain} has multiple deployed module families.`,
        chainFamily.candidates
      );
      return;
    }
    const { prefix, records } = chainFamily;
    const visitKey = `${cache.manifest.extension.id}:${prefix}`;
    const chainNode = this.addNode({
      id: `action-chain:${visitKey}`,
      type: 'action-chain',
      extension: cache.manifest.extension.id,
      chainId: chain,
      scopeDirectory: family.scopeDirectory,
      familyPrefix: family.familyPrefix,
    });
    this.addEdge(parentNode, chainNode, 'invokes-action-chain');
    if (this.visitedActionChains.has(visitKey)) return;
    this.visitedActionChains.add(visitKey);
    const artifacts = await this.includeModuleFamily(
      cache,
      records,
      chainNode,
      `Statically referenced action chain ${chain}`
    );
    for (const artifact of artifacts) {
      if (artifact.record.kind !== 'text' || artifact.record.mediaType !== 'application/json') {
        continue;
      }
      let value;
      try {
        value = JSON.parse(artifact.content);
      } catch {
        continue;
      }
      for (const nestedId of extractActionChainIds(value)) {
        if (nestedId !== chain) {
          await this.visitActionChain(cache, family, nestedId, chainNode, depth + 1);
        }
      }
    }
  }

  async includeStaticMetadataLayouts(cache, metadata, parentNode, depth) {
    for (const [metadataName, descriptor] of Object.entries(metadata || {})) {
      if (descriptor?.type !== 'vb/DynamicLayoutMetadataProviderDescriptor') continue;
      const descriptorPath = descriptor.defaultValue?.path;
      if (typeof descriptorPath !== 'string' || !descriptorPath.trim()) continue;
      const segments = descriptorPath.split('/');
      if (segments.length !== 3 || segments[0] !== 'dynamicLayouts') {
        this.addUnresolved(
          'DYNAMIC_LAYOUT_DESCRIPTOR_PATH_INVALID',
          parentNode,
          descriptorPath,
          `Metadata descriptor ${metadataName} has an unsupported dynamic-layout path.`
        );
        continue;
      }
      try {
        validateIdentifier(segments[1], 'Dynamic-layout owner');
        validateIdentifier(segments[2], 'Dynamic-layout ID');
      } catch (error) {
        this.addUnresolved(
          'DYNAMIC_LAYOUT_DESCRIPTOR_PATH_INVALID',
          parentNode,
          descriptorPath,
          error.message
        );
        continue;
      }
      if (String(parentNode).startsWith('page:')) {
        // Page-provided metadata can flow through a Guided Process into child fragments.
        const targetKey = `${cache.manifest.extension.id}:${segments[1]}/${segments[2]}`;
        this.pageMetadataLayoutTargets.set(targetKey, {
          extension: cache.manifest.extension.id,
          owner: segments[1],
          layout: segments[2],
        });
      }
      await this.includeDirectLayoutTarget({
        extension: cache.manifest.extension.id,
        owner: segments[1],
        layout: segments[2],
      }, parentNode, depth, 'uses-metadata-descriptor-layout');
    }
  }

  async visitFragment(
    currentExtension,
    referenceName,
    parentNode,
    depth,
    edgeType = 'references-fragment'
  ) {
    const parsed = splitFragmentName(referenceName, currentExtension);
    try {
      validateIdentifier(parsed.extension, 'Fragment extension');
      validateIdentifier(parsed.fragment, 'Fragment name');
    } catch (error) {
      this.addUnresolved('FRAGMENT_REFERENCE_INVALID', parentNode, referenceName, error.message);
      return;
    }
    const visitKey = `${parsed.extension}:${parsed.fragment}`;
    const fragmentNode = this.addNode({
      id: `fragment:${visitKey}`,
      type: 'fragment',
      extension: parsed.extension,
      fragment: parsed.fragment,
    });
    this.addEdge(parentNode, fragmentNode, edgeType);
    if (this.visitedFragments.has(visitKey)) return;
    this.visitedFragments.add(visitKey);
    const cache = await this.ensureBundle(parsed.extension);
    if (!cache) return;
    const family = findFragmentFamily(cache, parsed.fragment);
    if (!family) {
      this.addUnresolved(
        'FRAGMENT_NOT_FOUND',
        parentNode,
        referenceName,
        `Referenced fragment ${referenceName} is absent from its deployed bundle.`
      );
      return;
    }
    if (family.ambiguous) {
      this.addUnresolved(
        'FRAGMENT_AMBIGUOUS',
        parentNode,
        referenceName,
        `Referenced fragment ${referenceName} has multiple deployed module families.`,
        family.candidates
      );
      return;
    }
    await this.visitUiFamily(cache, {
      familyPrefix: family.roots.join(', '),
      scopeDirectory: family.scopeDirectory,
      records: family.records,
    }, fragmentNode, depth);
  }

  async visitDynamicComponent(cache, component, metadata, parentNode, source, depth) {
    const normalizedTag = String(component.tag || '').toLowerCase();
    const componentNode = this.addNode({
      id: `component:${source}`,
      type: 'dynamic-component',
      extension: cache.manifest.extension.id,
      tag: component.tag,
      // Publish the consumer contract so readiness checks do not infer it from filenames.
      consumerKind: normalizedTag.endsWith('-form') ? 'dynamic-form'
        : normalizedTag.endsWith('-table') ? 'dynamic-table'
          : 'dynamic-container',
      validationMessageConsumer: normalizedTag.endsWith('-form'),
      metadataName: component.metadataName,
      layout: component.literalLayout,
      literalLayouts: component.literalLayouts,
      attributes: component.attributes,
    });
    this.addEdge(parentNode, componentNode, 'contains-component');

    const layoutNames = component.literalLayout
      ? [component.literalLayout]
      : component.literalLayouts;
    let inheritedLayoutsResolved = 0;
    if (/\$variables\.metadataProvider\b/.test(component.metadataExpression || '')) {
      for (const target of this.pageMetadataLayoutTargets.values()) {
        const targetCache = await this.ensureBundle(target.extension);
        if (!targetCache) continue;
        const layoutRoot = `dynamicLayouts/${target.owner}/${target.layout}`;
        const layoutRecord = targetCache.index.modules.find((record) => (
          record.logicalPath === `${layoutRoot}/layout.json`
        ));
        if (!layoutRecord) continue;
        const parsedLayout = parseJsonModule(targetCache, layoutRecord);
        for (const layoutName of layoutNames) {
          if (!parsedLayout.value.layouts?.[layoutName]) continue;
          await this.includeDynamicLayout({
            cache: targetCache,
            record: layoutRecord,
            value: parsedLayout.value,
            layoutRoot,
            selectedLayout: layoutName,
          }, componentNode, depth, null, 'uses-inherited-metadata-layout');
          inheritedLayoutsResolved += 1;
        }
      }
    }

    if (!component.metadataName) {
      if (inheritedLayoutsResolved > 0) return;
      this.addUnresolved(
        'DYNAMIC_METADATA_BINDING',
        source,
        component.metadataExpression || '<missing>',
        'Dynamic component metadata is missing or computed outside $metadata.'
      );
      return;
    }
    const descriptor = metadata[component.metadataName];
    if (!descriptor || descriptor.type !== 'vb/DynamicLayoutMetadataProviderDescriptor') {
      this.addUnresolved(
        'METADATA_DESCRIPTOR_NOT_FOUND',
        source,
        component.metadataName,
        'Referenced DynamicLayoutMetadataProviderDescriptor was not found in the UI JSON.'
      );
      return;
    }
    const endpoint = descriptor.defaultValue?.endpoint || descriptor.defaultValue?.serviceId || null;
    if (typeof endpoint !== 'string' || !endpoint.trim()) {
      this.addUnresolved(
        'DYNAMIC_SERVICE_BINDING',
        source,
        JSON.stringify(descriptor.defaultValue || {}),
        'Metadata provider service is missing or is not a static string.'
      );
      return;
    }
    if (/\[\[|\{\{/.test(endpoint)) {
      this.addUnresolved(
        'DYNAMIC_SERVICE_BINDING',
        source,
        endpoint,
        'Metadata provider service is computed at runtime and cannot be followed statically.'
      );
      return;
    }
    const serviceId = serviceIdentityFromEndpoint(endpoint);

    const ownerExtension = extensionFromServiceId(serviceId, cache.manifest.extension.id);
    const ownerCache = await this.ensureBundle(ownerExtension);
    if (!ownerCache) return;
    const candidateGroups = (layoutNames.length > 0 ? layoutNames : [null]).map((layoutName) => ({
      layoutName,
      candidates: findLayoutCandidates(ownerCache, serviceId, layoutName),
    }));
    const ambiguousGroup = candidateGroups.find((group) => group.candidates.length > 1);
    const candidates = candidateGroups.flatMap((group) => group.candidates);
    if (candidates.length === 0) {
      if (inheritedLayoutsResolved > 0) return;
      this.addUnresolved(
        'DYNAMIC_LAYOUT_NOT_FOUND',
        source,
        `${serviceId}:${component.literalLayout || '<computed>'}`,
        'No deployed dynamic layout matches the component provider and layout.'
      );
      return;
    }
    if (ambiguousGroup) {
      this.addUnresolved(
        'DYNAMIC_LAYOUT_AMBIGUOUS',
        source,
        `${serviceId}:${ambiguousGroup.layoutName || '<computed>'}`,
        'Multiple deployed dynamic layouts match the component provider.',
        ambiguousGroup.candidates.map((candidate) => candidate.layoutRoot)
      );
      return;
    }
    if (component.layoutExpression && !component.literalLayout && layoutNames.length === 0) {
      this.addUnresolved(
        'DYNAMIC_LAYOUT_EXPRESSION',
        source,
        component.layoutExpression,
        'Layout name is computed at runtime; the owning layout is included without selecting a rule set.'
      );
    }
    for (const candidate of candidates) {
      await this.includeDynamicLayout(candidate, componentNode, depth, serviceId);
    }
  }

  async includeDynamicLayout(candidate, parentNode, depth, serviceId = null, edgeType = 'uses-dynamic-layout') {
    if (depth > this.limits.maxDepth) {
      this.addUnresolved(
        'GRAPH_DEPTH_EXCEEDED',
        parentNode,
        candidate.layoutRoot,
        `Dependency traversal exceeded depth ${this.limits.maxDepth}.`
      );
      return;
    }
    const extension = candidate.cache.manifest.extension.id;
    const visitKey = `${extension}:${candidate.layoutRoot}:${candidate.selectedLayout || '*'}`;
    const layoutNode = this.addNode({
      id: `layout:${visitKey}`,
      type: 'dynamic-layout',
      extension,
      version: candidate.cache.manifest.extension.version,
      layoutRoot: candidate.layoutRoot,
      selectedLayout: candidate.selectedLayout,
      serviceId,
    });
    this.addEdge(parentNode, layoutNode, edgeType);
    if (this.visitedLayouts.has(visitKey)) return;
    this.visitedLayouts.add(visitKey);

    const allLayouts = candidate.value.layouts && typeof candidate.value.layouts === 'object'
      ? candidate.value.layouts
      : {};
    const namedLayoutEntries = candidate.selectedLayout
      ? [[candidate.selectedLayout, allLayouts[candidate.selectedLayout]]]
      : Object.entries(allLayouts).filter(([, definition]) => (
        definition
        && typeof definition === 'object'
        && (
          Array.isArray(definition.rules)
          || definition.layout
          || definition.layouts
          || definition.layoutType
        )
      ));
    for (const [namedLayout, selectedDefinition] of namedLayoutEntries) {
      if (!selectedDefinition || typeof selectedDefinition !== 'object') continue;
      const selectedNode = this.addNode({
        id: `named-layout:${extension}:${candidate.layoutRoot}:${namedLayout}`,
        type: 'named-layout',
        extension,
        layoutRoot: candidate.layoutRoot,
        name: namedLayout,
        selectedByComponent: candidate.selectedLayout === namedLayout,
        jsonPointer: `/layouts/${escapeJsonPointerSegment(namedLayout)}`,
        ruleOrder: Array.isArray(selectedDefinition.rules) ? selectedDefinition.rules : [],
      });
      this.addEdge(
        layoutNode,
        selectedNode,
        candidate.selectedLayout ? 'selects-named-layout' : 'declares-named-layout'
      );
      for (const [index, ruleName] of (selectedDefinition.rules || []).entries()) {
        if (typeof ruleName !== 'string') continue;
        const definition = allLayouts[ruleName] || null;
        const ruleNode = this.addNode({
          id: `rule-set-rule:${extension}:${candidate.layoutRoot}:${namedLayout}:${ruleName}`,
          type: 'rule-set-rule',
          extension,
          layoutRoot: candidate.layoutRoot,
          ruleSet: namedLayout,
          name: ruleName,
          order: index,
          evaluation: 'top-down-first-match',
          expression: definition?.expression || null,
          jsonPointer: `/layouts/${escapeJsonPointerSegment(ruleName)}`,
        });
        this.addEdge(selectedNode, ruleNode, 'evaluates-rule');
      }
      const variants = selectedDefinition.layouts && typeof selectedDefinition.layouts === 'object'
        ? selectedDefinition.layouts
        : {};
      for (const [variantName, variant] of Object.entries(variants)) {
        const variantNode = this.addNode({
          id: `layout-variant:${extension}:${candidate.layoutRoot}:${namedLayout}:${variantName}`,
          type: 'layout-variant',
          extension,
          layoutRoot: candidate.layoutRoot,
          selectedLayout: namedLayout,
          name: variantName,
          usedIn: Array.isArray(variant?.usedIn) ? variant.usedIn : [],
          jsonPointer: `/layouts/${escapeJsonPointerSegment(namedLayout)}`
            + `/layouts/${escapeJsonPointerSegment(variantName)}`,
        });
        this.addEdge(selectedNode, variantNode, 'contains-layout-variant');
      }
    }

    const records = candidate.cache.index.modules.filter((record) => (
      record.logicalPath === candidate.layoutRoot
      || record.logicalPath.startsWith(`${candidate.layoutRoot}/`)
    ));
    await this.includeModuleFamily(
      candidate.cache,
      records,
      layoutNode,
      candidate.selectedLayout
        ? `Supports selected layout ${candidate.selectedLayout}`
        : `Supports dynamic layout ${candidate.layoutRoot}`
    );

    if (serviceId) {
      const serviceName = serviceId.includes(':') ? serviceId.split(':').slice(1).join(':') : serviceId;
      for (const record of candidate.cache.index.modules) {
        if (
          record.kind !== 'text'
          || !record.logicalPath.startsWith('services/')
          || record.mediaType !== 'application/json'
        ) {
          continue;
        }
        const cached = readCachedModule(candidate.cache, record);
        if (!cached.content.includes(serviceName)) continue;
        const added = this.addEvidence(
          candidate.cache,
          record,
          `Describes dynamic-layout service ${serviceId}`,
          'service-metadata'
        );
        this.addEdge(layoutNode, added.moduleNode, 'uses-service-metadata');
      }
    }
  }

  async includeDirectLayoutTarget(target, parentNode, depth, edgeType = 'uses-dynamic-layout') {
    const cache = await this.ensureBundle(target.extension);
    const layoutRoot = `dynamicLayouts/${target.owner}/${target.layout}`;
    const layoutRecord = cache.index.modules.find((record) => (
      record.logicalPath === `${layoutRoot}/layout.json`
    ));
    if (!layoutRecord) {
      const candidates = cache.index.modules
        .filter((record) => (
          record.logicalPath.startsWith(`dynamicLayouts/${target.owner}/`)
          && record.logicalPath.endsWith('/layout.json')
        ))
        .map((record) => record.logicalPath)
        .slice(0, 25);
      throw new RuntimeEvidenceError(
        'DYNAMIC_LAYOUT_NOT_FOUND',
        `Dynamic layout ${target.owner}/${target.layout} is absent from ${target.extension}.`,
        { candidates }
      );
    }
    const parsed = parseJsonModule(cache, layoutRecord);
    const candidate = {
      cache,
      record: layoutRecord,
      value: parsed.value,
      layoutRoot,
      selectedLayout: null,
    };
    await this.includeDynamicLayout(candidate, parentNode, depth, null, edgeType);
  }

  async resolveUiPage(target) {
    const cache = await this.ensureBundle(target.extension);
    const page = findUiPage(cache, target);
    const pageNode = this.addNode({
      id: `page:${target.extension}:${page.identity.application}:${page.identity.flow}:${page.identity.page}`,
      type: 'ui-page',
      extension: target.extension,
      version: cache.manifest.extension.version,
      ...page.identity,
    });
    // Persist the exact application selected when the CLI target omitted it.
    this.resolvedTarget = {
      ...target,
      application: page.identity.application,
    };
    await this.visitUiFamily(cache, page, pageNode, 0);
    if (target.fallbackDynamicLayout) {
      // Direct-layout fallback verifies source presence without proving this UI route selects it.
      this.addUnresolved(
        'DIRECT_LAYOUT_NOT_BOUND_TO_PAGE',
        pageNode,
        `${target.fallbackDynamicLayout.owner}/${target.fallbackDynamicLayout.layout}`,
        'Fallback dynamic-layout evidence was included directly; no static UI binding proved route selection.'
      );
      await this.includeDirectLayoutTarget({
        kind: 'dynamic-layout',
        extension: target.extension,
        owner: target.fallbackDynamicLayout.owner,
        layout: target.fallbackDynamicLayout.layout,
      }, pageNode, 1, 'includes-direct-layout-evidence');
    }
    return pageNode;
  }

  async resolveDirectLayout(target) {
    const targetNode = this.addNode({
      id: `direct-layout:${target.extension}:${target.owner}/${target.layout}`,
      type: 'direct-dynamic-layout-target',
      extension: target.extension,
      owner: target.owner,
      layout: target.layout,
    });
    this.resolvedTarget = target;
    await this.includeDirectLayoutTarget(target, targetNode, 0);
    return targetNode;
  }

  async resolve(target) {
    const rootNode = target.kind === 'ui-page'
      ? await this.resolveUiPage(target)
      : await this.resolveDirectLayout(target);
    return {
      schemaVersion: 1,
      target: this.resolvedTarget || target,
      rootNode,
      complete: this.unresolved.length === 0,
      nodes: [...this.nodes.values()].sort((left, right) => left.id.localeCompare(right.id)),
      edges: this.edges.sort((left, right) => (
        `${left.from}|${left.to}|${left.type}`.localeCompare(`${right.from}|${right.to}|${right.type}`)
      )),
      evidence: [...this.evidence.values()]
        .map((entry) => ({ ...entry, reasons: [...entry.reasons].sort() }))
        .sort((left, right) => (
          evidenceRoleOrder(left.role) - evidenceRoleOrder(right.role)
          || left.moduleId.localeCompare(right.moduleId)
        )),
      unresolved: this.unresolved,
      bundles: [...this.bundleCaches.values()]
        .map((cache) => ({
          extension: cache.manifest.extension.id,
          version: cache.manifest.extension.version,
          description: cache.manifest.extension.description || null,
          bundleSha256: cache.manifest.cdn.sha256,
          cacheStatus: cache.cacheStatus || 'hit',
        }))
        .sort((left, right) => left.extension.localeCompare(right.extension)),
    };
  }
}

async function resolveEvidenceGraph(options) {
  const builder = new EvidenceGraphBuilder(options);
  return builder.resolve(options.target);
}

module.exports = {
  DEFAULT_LIMITS,
  EvidenceGraphBuilder,
  derivePageId,
  evidenceShapeDomain,
  extractActionChainIds,
  extractDynamicComponents,
  extractFragmentReferences,
  extractLiteralGuidedStepFragments,
  findActionChainFamily,
  findFragmentFamily,
  findLayoutCandidates,
  findUiPage,
  parseAttributes,
  parseUiPageIdentity,
  resolveEvidenceGraph,
  serviceIdentityFromEndpoint,
  scanHtmlStartTags,
  splitFragmentName,
};
