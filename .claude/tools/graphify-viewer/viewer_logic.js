(function(root, factory) {
  const api = factory();

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
  }

  if (root) {
    root.viewerLogic = api;
  }
})(typeof globalThis !== 'undefined' ? globalThis : this, function() {
  function normalize_file_path(filePath) {
    if (!filePath) {
      return '';
    }

    return String(filePath).replace(/\\/g, '/');
  }

  function parse_line_number(sourceLocation) {
    if (typeof sourceLocation === 'number' && Number.isFinite(sourceLocation)) {
      return Math.max(1, Math.floor(sourceLocation));
    }

    if (!sourceLocation) {
      return 1;
    }

    const match = String(sourceLocation).match(/(\d+)/);
    if (!match) {
      return 1;
    }

    const parsed = Number.parseInt(match[1], 10);
    return Number.isFinite(parsed) && parsed > 0 ? parsed : 1;
  }

  function encode_editor_path(filePath) {
    return encodeURI(normalize_file_path(filePath)).replace(/[?#]/g, encodeURIComponent);
  }

  function normalize_origin(origin) {
    if (!origin) {
      return '';
    }

    const normalized = String(origin).replace(/\/+$/, '');
    if (normalized === 'null' || normalized === 'file://' || normalized === 'file:') {
      return '';
    }

    return normalized;
  }

  function buildEditorTarget(node, relPath, origin) {
    const path = normalize_file_path(
      (node && (node.path || node.source_file || node.file_path)) || ''
    );
    const line = parse_line_number(
      node && Object.prototype.hasOwnProperty.call(node, 'line')
        ? node.line
        : (node && (node.source_location || node.line_number))
    );
    const normalizedRelPath = normalize_file_path(
      relPath || (node && (node.relPath || node.rel_path)) || ''
    );
    const normalizedOrigin = normalize_origin(origin);
    const query = 'path=' + encodeURIComponent(path) + '&line=' + encodeURIComponent(String(line));
    const openPath = '/__open_in_editor?' + query;

    return {
      path: path,
      line: line,
      relPath: normalizedRelPath,
      vscodeUri: path ? ('vscode://file/' + encode_editor_path(path) + ':' + line) : '',
      openUrl: path ? ((normalizedOrigin || '') + openPath) : '',
    };
  }

  function openEditorTarget(target) {
    if (!target || !target.path) {
      return Promise.resolve(false);
    }

    const openUrl = target.openUrl || '';
    if (openUrl && typeof fetch === 'function') {
      const requestUrl = openUrl + (openUrl.includes('?') ? '&' : '?') + '_ts=' + Date.now();
      return fetch(requestUrl, {
        method: 'GET',
        cache: 'no-store',
        credentials: 'same-origin',
      }).then(function(response) {
        if (response && response.ok) {
          return true;
        }

        if (typeof window !== 'undefined' && typeof window.open === 'function' && target.vscodeUri) {
          window.open(target.vscodeUri, '_blank');
          return true;
        }

        return false;
      }).catch(function() {
        if (typeof window !== 'undefined' && typeof window.open === 'function' && target.vscodeUri) {
          window.open(target.vscodeUri, '_blank');
          return true;
        }

        return false;
      });
    }

    if (typeof window !== 'undefined' && typeof window.open === 'function' && target.vscodeUri) {
      window.open(target.vscodeUri, '_blank');
      return Promise.resolve(true);
    }

    return Promise.resolve(false);
  }

  function normalizeCommunityKey(communityId) {
    return String(communityId);
  }

  function getCommunityClusterId(communityId) {
    return 'cluster_' + normalizeCommunityKey(communityId);
  }

  function buildCommunityClusterOptions(communityId, info, label) {
    const communityKey = normalizeCommunityKey(communityId);

    return {
      joinCondition: function(node) {
        return info.node_ids.includes(node.id);
      },
      clusterNodeProperties: {
        id: getCommunityClusterId(communityKey),
        label: label,
        title: label,
        shape: 'dot',
        size: 25,
        color: {
          background: info.color,
          border: info.color,
          highlight: { background: '#fff', border: '#fff' },
          hover: { background: info.color, border: '#fff' }
        },
        font: { color: '#cdd6f4', size: 12 },
        borderWidth: 2,
      }
    };
  }

  function getPathFileName(relPath) {
    if (!relPath) {
      return '';
    }

    const parts = relPath.split('/');
    return parts[parts.length - 1] || '';
  }

  function getPathDirName(relPath) {
    if (!relPath) {
      return '';
    }

    const parts = relPath.split('/').filter(Boolean);
    if (parts.length <= 1) {
      return '';
    }

    return parts[parts.length - 2] || '';
  }

  function getFileStem(fileName) {
    return fileName.replace(/\.[^.]+$/, '');
  }

  function getRepresentativeCommunityNodeId(info, incoming, outgoing) {
    let bestId = info.node_ids[0] || '';
    let bestScore = -1;

    info.node_ids.forEach(function(nodeId) {
      const score = ((incoming[nodeId] || []).length + (outgoing[nodeId] || []).length);
      if (score > bestScore) {
        bestId = nodeId;
        bestScore = score;
      }
    });

    return bestId;
  }

  function shortenRepresentativeLabel(label, relPath) {
    const fileStem = getFileStem(getPathFileName(relPath));
    if (!label) {
      return fileStem;
    }

    let output = label;
    const repeatedPrefix = fileStem ? (fileStem + '_') : '';

    if (repeatedPrefix && output.startsWith(repeatedPrefix)) {
      output = output.slice(repeatedPrefix.length);
    }

    return output || label;
  }

  function buildCommunityDisplayName(communityId, info, rels, nodes, incoming, outgoing) {
    const representativeId = getRepresentativeCommunityNodeId(info, incoming, outgoing);
    const relPath = rels[representativeId] || '';
    const fileName = getPathFileName(relPath);
    const dirName = getPathDirName(relPath);
    const rawLabel = (nodes[representativeId] && nodes[representativeId].label) || representativeId || ('community_' + communityId);
    const shortLabel = shortenRepresentativeLabel(rawLabel, relPath);
    const parts = [];

    if (fileName && dirName) {
      parts.push(dirName + '/' + fileName);
    } else if (fileName) {
      parts.push(fileName);
    }

    if (shortLabel && shortLabel !== fileName && shortLabel !== getFileStem(fileName)) {
      parts.push(shortLabel);
    }

    if (parts.length === 0) {
      parts.push('社区 ' + communityId);
      if (shortLabel) {
        parts.push(shortLabel);
      }
    }

    return parts.join(' · ') + ' (' + info.count + ')';
  }

  function buildTreeModel(data, nodes, filter, depth) {
    const currentDepth = depth || 0;
    const entries = [];
    const dirEntries = Object.entries(data._children || {}).sort(function(a, b) {
      return a[0].localeCompare(b[0]);
    });

    for (const [name, child] of dirEntries) {
      const children = buildTreeModel(child, nodes, filter, currentDepth + 1);

      if (filter && children.length === 0) {
        continue;
      }

      entries.push({
        type: 'dir',
        label: name,
        icon: '📁',
        depth: currentDepth,
        children: children,
      });
    }

    const fileEntries = Object.entries(data._files || {}).sort(function(a, b) {
      return a[0].localeCompare(b[0]);
    });

    for (const [name, nodeIds] of fileEntries) {
      let visibleIds = nodeIds;

      if (filter) {
        visibleIds = nodeIds.filter(function(id) {
          const node = nodes[id] || {};
          return (node.label || '').toLowerCase().includes(filter) || name.toLowerCase().includes(filter);
        });

        if (!visibleIds.length && !name.toLowerCase().includes(filter)) {
          continue;
        }
      }

      const children = visibleIds.map(function(id) {
        const node = nodes[id] || {};
        const kind = node.file_type === 'code' ? 'code' : 'doc';

        return {
          type: 'node',
          label: node.label || id,
          icon: node.file_type === 'code' ? '⚡' : '📝',
          depth: currentDepth + 1,
          nodeId: id,
          badge: node.source_location || '',
          kind: kind,
        };
      });

      entries.push({
        type: 'file',
        label: name,
        icon: '📄',
        depth: currentDepth,
        children: children,
      });
    }

    return entries;
  }

  function resolveNodeIdFromDomPoint(network, domPoint, threshold) {
    const maxDistance = typeof threshold === 'number' ? threshold : 32;
    const directHit = network.getNodeAt(domPoint);
    if (directHit) {
      return directHit;
    }

    let bestId = null;
    let bestDistance = Number.POSITIVE_INFINITY;
    const bodyNodes = (network.body && network.body.nodes) || {};

    Object.entries(bodyNodes).forEach(function([nodeId, node]) {
      if (typeof node.x !== 'number' || typeof node.y !== 'number') {
        return;
      }

      const domPosition = network.canvasToDOM({ x: node.x, y: node.y });
      const dx = domPosition.x - domPoint.x;
      const dy = domPosition.y - domPoint.y;
      const distance = Math.sqrt((dx * dx) + (dy * dy));

      if (distance <= maxDistance && distance < bestDistance) {
        bestId = nodeId;
        bestDistance = distance;
      }
    });

    return bestId;
  }

  return {
    normalize_file_path: normalize_file_path,
    parse_line_number: parse_line_number,
    buildEditorTarget: buildEditorTarget,
    openEditorTarget: openEditorTarget,
    normalizeCommunityKey: normalizeCommunityKey,
    getCommunityClusterId: getCommunityClusterId,
    buildCommunityClusterOptions: buildCommunityClusterOptions,
    buildCommunityDisplayName: buildCommunityDisplayName,
    buildTreeModel: buildTreeModel,
    resolveNodeIdFromDomPoint: resolveNodeIdFromDomPoint,
  };
});
