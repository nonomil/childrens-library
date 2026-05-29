# Superpowers Tab Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a dedicated `superpowers.html` tab to the docs site and move superpowers explanations and installation guidance into that page.

**Architecture:** Extend the shared four-page docs navigation, keep the visual system unchanged, and redistribute content responsibilities: install page for environment setup, activation page for bat selection flow, superpowers page for framework explanation and install methods, skills page for recommended skills and AI-copy prompts.

**Tech Stack:** HTML, CSS, vanilla JavaScript, Node.js assertions

### Task 1: Update the test for a dedicated superpowers page

**Files:**
- Modify: `C:\Users\Administrator\Documents\Playground\test_docs_portal.js`

**Step 1: Write the failing test**

Add assertions for:
- `docs/superpowers.html`
- sidebar links to `./superpowers.html`
- superpowers-specific content and install commands

**Step 2: Run test to verify it fails**

Run: `node test_docs_portal.js`
Expected: FAIL because `superpowers.html` does not exist yet

**Step 3: Write minimal implementation**

Keep only expectations directly tied to the new dedicated tab.

**Step 4: Run test to verify it passes**

Run: `node test_docs_portal.js`
Expected: PASS

**Step 5: Commit**

```bash
git add C:\Users\Administrator\Documents\Playground\test_docs_portal.js
git commit -m "test: require dedicated superpowers tab"
```

### Task 2: Add the dedicated superpowers page

**Files:**
- Create: `C:\Users\Administrator\Documents\Playground\docs\superpowers.html`

**Step 1: Write the failing test**

Use assertions for:
- `What is Superpowers`
- `Layered architecture`
- `Subagent-Driven Development`
- marketplace install commands
- local bootstrap command

**Step 2: Run test to verify it fails**

Run: `node test_docs_portal.js`
Expected: FAIL until the new page exists

**Step 3: Write minimal implementation**

Add sections for:
- overview and why it matters
- layered architecture and skill system
- subagent-driven development
- common workflow and core skills
- correct installation methods

**Step 4: Run test to verify it passes**

Run: `node test_docs_portal.js`
Expected: PASS

**Step 5: Commit**

```bash
git add C:\Users\Administrator\Documents\Playground\docs\superpowers.html
git commit -m "feat: add superpowers docs page"
```

### Task 3: Rebalance the other pages

**Files:**
- Modify: `C:\Users\Administrator\Documents\Playground\docs\index.html`
- Modify: `C:\Users\Administrator\Documents\Playground\docs\activation.html`
- Modify: `C:\Users\Administrator\Documents\Playground\docs\skills.html`

**Step 1: Write the failing test**

Use assertions for:
- install page points to the dedicated superpowers tab
- all pages include the new sidebar link
- skills page no longer acts as the superpowers intro page

**Step 2: Run test to verify it fails**

Run: `node test_docs_portal.js`
Expected: FAIL until the three pages are updated

**Step 3: Write minimal implementation**

Update responsibilities:
- install page: environment setup + link to superpowers tab
- activation page: unchanged responsibility
- skills page: recommended skills + AI-copy prompts only

**Step 4: Run test to verify it passes**

Run: `node test_docs_portal.js`
Expected: PASS

**Step 5: Commit**

```bash
git add C:\Users\Administrator\Documents\Playground\docs\index.html C:\Users\Administrator\Documents\Playground\docs\activation.html C:\Users\Administrator\Documents\Playground\docs\skills.html
git commit -m "docs: separate superpowers from install and skills pages"
```
