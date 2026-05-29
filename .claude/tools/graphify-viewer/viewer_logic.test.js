const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const {
  normalizeCommunityKey,
  getCommunityClusterId,
  buildCommunityClusterOptions,
  buildCommunityDisplayName,
  buildTreeModel,
  buildEditorTarget,
  resolveNodeIdFromDomPoint,
} = require('./viewer_logic.js');

const viewer_template = fs.readFileSync(path.join(__dirname, 'viewer_template.html'), 'utf8');

test('normalizeCommunityKey keeps community ids stable across number and string inputs', function() {
  assert.equal(normalizeCommunityKey(7), '7');
  assert.equal(normalizeCommunityKey('7'), '7');
  assert.equal(getCommunityClusterId(7), 'cluster_7');
  assert.equal(getCommunityClusterId('7'), 'cluster_7');
});

test('buildCommunityClusterOptions preserves custom cluster id and label', function() {
  const info = {
    color: '#89b4fa',
    node_ids: ['alpha', 'beta'],
  };
  const options = buildCommunityClusterOptions(3, info, 'utils (2)');

  assert.equal(options.clusterNodeProperties.id, 'cluster_3');
  assert.equal(options.clusterNodeProperties.label, 'utils (2)');
  assert.equal(options.clusterNodeProperties.title, 'utils (2)');
  assert.ok(!Object.prototype.hasOwnProperty.call(options, 'processProperties'));
  assert.equal(options.joinCondition({ id: 'alpha' }), true);
  assert.equal(options.joinCondition({ id: 'gamma' }), false);
});

test('buildCommunityDisplayName prefers directory file and representative symbol over generic community names', function() {
  const info = {
    count: 64,
    node_ids: ['main_window_mainwindow', 'main_window_mainwindow_build_ui']
  };
  const rels = {
    main_window_mainwindow: 'prj/检测软件工程/gui/main_window.py',
    main_window_mainwindow_build_ui: 'prj/检测软件工程/gui/main_window.py'
  };
  const nodes = {
    main_window_mainwindow: { label: 'main_window_mainwindow' },
    main_window_mainwindow_build_ui: { label: 'main_window_mainwindow_build_ui' }
  };
  const outgoing = {
    main_window_mainwindow: [{}, {}, {}],
    main_window_mainwindow_build_ui: [{}]
  };
  const incoming = {
    main_window_mainwindow: [{}, {}],
    main_window_mainwindow_build_ui: []
  };

  assert.equal(
    buildCommunityDisplayName('0', info, rels, nodes, incoming, outgoing),
    'gui/main_window.py · mainwindow (64)'
  );
});

test('buildTreeModel returns depth-based hierarchy for IDE-like indentation', function() {
  const tree = {
    _children: {
      src: {
        _children: {
          utils: {
            _children: {},
            _files: {
              'helper.js': ['helper_fn']
            }
          }
        },
        _files: {}
      }
    },
    _files: {}
  };
  const nodes = {
    helper_fn: {
      label: 'build_helper',
      file_type: 'code',
      source_location: 'L18',
    }
  };

  const model = buildTreeModel(tree, nodes, '', 0);

  assert.equal(model.length, 1);
  assert.equal(model[0].type, 'dir');
  assert.equal(model[0].depth, 0);
  assert.equal(model[0].children[0].type, 'dir');
  assert.equal(model[0].children[0].depth, 1);
  assert.equal(model[0].children[0].children[0].type, 'file');
  assert.equal(model[0].children[0].children[0].depth, 2);
  assert.equal(model[0].children[0].children[0].children[0].type, 'node');
  assert.equal(model[0].children[0].children[0].children[0].depth, 3);
});

test('buildTreeModel prunes unmatched branches when filtering', function() {
  const tree = {
    _children: {
      src: {
        _children: {},
        _files: {
          'alpha.js': ['alpha_fn']
        }
      },
      docs: {
        _children: {},
        _files: {
          'guide.md': ['guide_doc']
        }
      }
    },
    _files: {}
  };
  const nodes = {
    alpha_fn: {
      label: 'AlphaRunner',
      file_type: 'code',
      source_location: 'L10',
    },
    guide_doc: {
      label: 'Overview',
      file_type: 'doc',
      source_location: 'L2',
    }
  };

  const model = buildTreeModel(tree, nodes, 'alpha', 0);

  assert.equal(model.length, 1);
  assert.equal(model[0].label, 'src');
  assert.equal(model[0].children.length, 1);
  assert.equal(model[0].children[0].label, 'alpha.js');
});

test('resolveNodeIdFromDomPoint falls back to nearest visible node when direct hit misses', function() {
  const network = {
    getNodeAt() {
      return null;
    },
    canvasToDOM(point) {
      return point;
    },
    body: {
      nodes: {
        cluster_0: { x: 100, y: 100 },
        alpha: { x: 260, y: 240 },
      }
    }
  };

  assert.equal(resolveNodeIdFromDomPoint(network, { x: 112, y: 108 }, 24), 'cluster_0');
  assert.equal(resolveNodeIdFromDomPoint(network, { x: 240, y: 230 }, 24), 'alpha');
});

test('resolveNodeIdFromDomPoint returns null when no node is close enough', function() {
  const network = {
    getNodeAt() {
      return null;
    },
    canvasToDOM(point) {
      return point;
    },
    body: {
      nodes: {
        cluster_0: { x: 100, y: 100 },
      }
    }
  };

  assert.equal(resolveNodeIdFromDomPoint(network, { x: 200, y: 200 }, 24), null);
});

test('buildEditorTarget encodes unicode paths and local open endpoint consistently', function() {
  const target = buildEditorTarget(
    {
      source_file: 'D:\\Workplace\\项目 空间\\src\\main window.py',
      source_location: 'L42',
    },
    'src/main window.py',
    'http://localhost:3335'
  );

  assert.deepEqual(target.path, 'D:/Workplace/项目 空间/src/main window.py');
  assert.equal(target.line, 42);
  assert.equal(target.relPath, 'src/main window.py');
  assert.equal(
    target.vscodeUri,
    'vscode://file/D:/Workplace/%E9%A1%B9%E7%9B%AE%20%E7%A9%BA%E9%97%B4/src/main%20window.py:42'
  );
  assert.equal(
    target.openUrl,
    'http://localhost:3335/__open_in_editor?path=D%3A%2FWorkplace%2F%E9%A1%B9%E7%9B%AE%20%E7%A9%BA%E9%97%B4%2Fsrc%2Fmain%20window.py&line=42'
  );
});

test('viewer_template consumes shared viewer logic and removes unsafe cluster overrides', function() {
  assert.match(viewer_template, /<script src="viewer_logic\.js"><\/script>/);
  assert.match(viewer_template, /\.tree-entry\s*\{/);
  assert.match(viewer_template, /resolveNodeIdFromDomPoint/);
  assert.match(viewer_template, /buildEditorTarget/);
  assert.match(viewer_template, /openEditorTarget/);
  assert.match(viewer_template, /__open_in_editor/);
  assert.doesNotMatch(
    viewer_template,
    /processProperties:\s*function\s*\(\)\s*\{\s*return\s*\{\};\s*\}/
  );
});
