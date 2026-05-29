# Docs Portal Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a static docs portal in `docs/` that explains setup, activation modes, superpowers installation, and project documentation in one local web page.

**Architecture:** Create a self-contained static site with `docs/index.html` as the entry point, a dedicated stylesheet for the visual system, and a lightweight script for copy buttons and mode switching. Reuse the existing installation scripts and local markdown docs as the content source, summarized into navigable sections that work under `file://`.

**Tech Stack:** HTML, CSS, vanilla JavaScript, Node.js assertions

### Task 1: Define portal coverage with a failing test

**Files:**
- Create: `test_docs_portal.js`

**Step 1: Write the failing test**

```javascript
assert.equal(fs.existsSync(html_path), true, '缺少 docs/index.html');
assert.match(html_text, /Quick Setup/);
assert.match(html_text, /Install Superpowers Skills/);
```

**Step 2: Run test to verify it fails**

Run: `node test_docs_portal.js`
Expected: FAIL because `docs/index.html` does not exist yet

**Step 3: Write minimal implementation**

Create the missing files and add the tested sections.

**Step 4: Run test to verify it passes**

Run: `node test_docs_portal.js`
Expected: PASS

**Step 5: Commit**

```bash
git add test_docs_portal.js docs/index.html docs/assets/site.css docs/assets/site.js
git commit -m "feat: add docs portal landing page"
```

### Task 2: Build the static docs portal

**Files:**
- Create: `docs/index.html`
- Create: `docs/assets/site.css`
- Create: `docs/assets/site.js`

**Step 1: Write the failing test**

Use `test_docs_portal.js` assertions as the specification.

**Step 2: Run test to verify it fails**

Run: `node test_docs_portal.js`
Expected: FAIL until the portal files exist and include all required content

**Step 3: Write minimal implementation**

Build a single-page portal with:
- quick setup commands
- activation mode cards tied to `update_codex_config.bat`
- superpowers install instructions
- docs overview cards for the two markdown files
- recommended skills summary

**Step 4: Run test to verify it passes**

Run: `node test_docs_portal.js`
Expected: PASS

**Step 5: Commit**

```bash
git add docs/index.html docs/assets/site.css docs/assets/site.js
git commit -m "feat: add static docs portal"
```

### Task 3: Verify the existing script docs still match the portal

**Files:**
- Modify: `INSTALL.md`

**Step 1: Write the failing test**

Add assertions only if the docs page needs a new referenced install file.

**Step 2: Run test to verify it fails**

Run: `node test_docs_portal.js`
Expected: FAIL only if the portal references missing install guidance

**Step 3: Write minimal implementation**

Keep `INSTALL.md` aligned with the portal language and commands, if needed.

**Step 4: Run test to verify it passes**

Run: `node test_docs_portal.js`
Expected: PASS

**Step 5: Commit**

```bash
git add INSTALL.md docs/index.html
git commit -m "docs: align install guide with docs portal"
```
