# Multi-Page Docs Portal Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace the single-page docs portal with a three-page documentation site that separates installation, activation, and skills guidance.

**Architecture:** Keep the site fully static under `docs/` so it works over `file://` without any build step. Use one shared stylesheet and one shared JavaScript file for sidebar navigation, active-page highlighting, copy buttons, and light interaction. Split content into `index.html`, `activation.html`, and `skills.html` so each page stays focused and easier to scan.

**Tech Stack:** HTML, CSS, vanilla JavaScript, Node.js assertions

### Task 1: Rewrite the failing portal test for the new multi-page structure

**Files:**
- Modify: `C:\Users\Administrator\Documents\Playground\test_docs_portal.js`

**Step 1: Write the failing test**

```javascript
expect_file_exists(path.join(docs_dir, 'activation.html'));
expect_file_exists(path.join(docs_dir, 'skills.html'));
assert.match(install_text, /Codex CLI/);
assert.match(activation_text, /Claude Code Activation/);
assert.match(skills_text, /How to install/);
```

**Step 2: Run test to verify it fails**

Run: `node test_docs_portal.js`
Expected: FAIL because `activation.html` and `skills.html` do not exist yet

**Step 3: Write minimal implementation**

Keep only the expectations needed for the requested three-page structure and page content.

**Step 4: Run test to verify it passes**

Run: `node test_docs_portal.js`
Expected: PASS after the three pages exist and contain the tested sections

**Step 5: Commit**

```bash
git add C:\Users\Administrator\Documents\Playground\test_docs_portal.js
git commit -m "test: require multi-page docs portal"
```

### Task 2: Build the shared layout and styling for a sidebar-driven docs site

**Files:**
- Modify: `C:\Users\Administrator\Documents\Playground\docs\assets\site.css`
- Modify: `C:\Users\Administrator\Documents\Playground\docs\assets\site.js`

**Step 1: Write the failing test**

Use the new `test_docs_portal.js` expectations for the shared sidebar markup and asset files.

**Step 2: Run test to verify it fails**

Run: `node test_docs_portal.js`
Expected: FAIL because the new pages and sidebar structure are missing

**Step 3: Write minimal implementation**

Add shared support for:
- sidebar navigation across three pages
- active page highlighting
- copy buttons
- responsive layout for desktop and mobile

**Step 4: Run test to verify it passes**

Run: `node test_docs_portal.js`
Expected: PASS when the new pages use the shared assets and tested sidebar hooks

**Step 5: Commit**

```bash
git add C:\Users\Administrator\Documents\Playground\docs\assets\site.css C:\Users\Administrator\Documents\Playground\docs\assets\site.js
git commit -m "feat: add shared multi-page docs site layout"
```

### Task 3: Create the installation page with Codex and Claude Code split apart

**Files:**
- Modify: `C:\Users\Administrator\Documents\Playground\docs\index.html`

**Step 1: Write the failing test**

Use assertions for:
- `Install Only What You Need`
- `Codex CLI`
- `Claude Code CLI`
- `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`
- superpowers bootstrap command

**Step 2: Run test to verify it fails**

Run: `node test_docs_portal.js`
Expected: FAIL until install page includes separated install flows and detailed setup

**Step 3: Write minimal implementation**

Build the install page with:
- common prerequisites
- optional install path for Codex only
- optional install path for Claude Code only
- optional install path for both
- superpowers bootstrap section
- links back to local docs

**Step 4: Run test to verify it passes**

Run: `node test_docs_portal.js`
Expected: PASS

**Step 5: Commit**

```bash
git add C:\Users\Administrator\Documents\Playground\docs\index.html
git commit -m "feat: split install docs by tool"
```

### Task 4: Create the activation page focused only on configuration switching

**Files:**
- Create: `C:\Users\Administrator\Documents\Playground\docs\activation.html`

**Step 1: Write the failing test**

Use assertions for:
- `Codex Activation`
- `Claude Code Activation`
- `update_codex_config.bat 1`
- `update_codex_config.bat 2`
- `update_codex_config.bat 3`

**Step 2: Run test to verify it fails**

Run: `node test_docs_portal.js`
Expected: FAIL because the activation page does not exist yet

**Step 3: Write minimal implementation**

Explain:
- which file each mode writes
- when to use each mode
- example commands
- what happens after activation

**Step 4: Run test to verify it passes**

Run: `node test_docs_portal.js`
Expected: PASS

**Step 5: Commit**

```bash
git add C:\Users\Administrator\Documents\Playground\docs\activation.html
git commit -m "feat: add activation docs page"
```

### Task 5: Create the skills page with introductions and install routes

**Files:**
- Create: `C:\Users\Administrator\Documents\Playground\docs\skills.html`

**Step 1: Write the failing test**

Use assertions for:
- six skill names from the markdown article
- `How to install`
- `skill-installer`
- `node C:/Users/Administrator/.codex/superpowers/.codex/superpowers-codex use-skill`

**Step 2: Run test to verify it fails**

Run: `node test_docs_portal.js`
Expected: FAIL because the skills page does not exist yet

**Step 3: Write minimal implementation**

For each listed skill:
- summarize what it solves
- link to the referenced repo or source
- explain installation route:
  - curated install when applicable
  - GitHub repo install route for third-party skills
  - how to invoke a skill once installed

**Step 4: Run test to verify it passes**

Run: `node test_docs_portal.js`
Expected: PASS

**Step 5: Commit**

```bash
git add C:\Users\Administrator\Documents\Playground\docs\skills.html
git commit -m "feat: add skills guide page"
```
