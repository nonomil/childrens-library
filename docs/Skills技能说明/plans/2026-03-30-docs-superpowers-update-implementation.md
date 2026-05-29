# Docs Superpowers Update Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Update the docs site so superpowers installation and skills guidance are more explicit, and simplify activation instructions to a double-click flow.

**Architecture:** Keep the existing three-page static docs site, but revise the content model: `index.html` gains a dedicated superpowers overview and install section based on the local article, `activation.html` switches to a no-command walkthrough, and `skills.html` adds copyable prompts for AI-assisted skill installation instead of raw install commands.

**Tech Stack:** HTML, CSS, vanilla JavaScript, Node.js assertions

### Task 1: Tighten the docs test for the new superpowers and activation requirements

**Files:**
- Modify: `C:\Users\Administrator\Documents\Playground\test_docs_portal.js`

**Step 1: Write the failing test**

Use assertions for:
- `What is Superpowers`
- `/plugin marketplace add obra/superpowers-marketplace`
- `Double-click`
- `No command typing required`
- `Copy this to your AI`

**Step 2: Run test to verify it fails**

Run: `node test_docs_portal.js`
Expected: FAIL because the current pages do not yet include the new content model

**Step 3: Write minimal implementation**

Keep only the expectations directly tied to the requested behavior.

**Step 4: Run test to verify it passes**

Run: `node test_docs_portal.js`
Expected: PASS

**Step 5: Commit**

```bash
git add C:\Users\Administrator\Documents\Playground\test_docs_portal.js
git commit -m "test: require superpowers docs and double-click activation guidance"
```

### Task 2: Update the install page with superpowers overview and install flow

**Files:**
- Modify: `C:\Users\Administrator\Documents\Playground\docs\index.html`

**Step 1: Write the failing test**

Use assertions for:
- `What is Superpowers`
- `/plugin marketplace add obra/superpowers-marketplace`
- `/plugin install superpowers@superpowers-marketplace`

**Step 2: Run test to verify it fails**

Run: `node test_docs_portal.js`
Expected: FAIL until install page includes the new superpowers section

**Step 3: Write minimal implementation**

Add:
- a short overview of what superpowers is
- the Claude Code marketplace install flow from the local article
- a brief note about common core skills and workflow value

**Step 4: Run test to verify it passes**

Run: `node test_docs_portal.js`
Expected: PASS

**Step 5: Commit**

```bash
git add C:\Users\Administrator\Documents\Playground\docs\index.html
git commit -m "docs: add superpowers install overview"
```

### Task 3: Simplify the activation page to a pure double-click workflow

**Files:**
- Modify: `C:\Users\Administrator\Documents\Playground\docs\activation.html`

**Step 1: Write the failing test**

Use assertions for:
- `Double-click`
- `choose option 1, 2, or 3`
- `No command typing required`
- absence of `update_codex_config.bat 1/2/3`

**Step 2: Run test to verify it fails**

Run: `node test_docs_portal.js`
Expected: FAIL until activation page no longer relies on typed commands

**Step 3: Write minimal implementation**

Rewrite the activation instructions around:
- double-clicking the bat
- selecting a mode in the menu
- entering values only when prompted

**Step 4: Run test to verify it passes**

Run: `node test_docs_portal.js`
Expected: PASS

**Step 5: Commit**

```bash
git add C:\Users\Administrator\Documents\Playground\docs\activation.html
git commit -m "docs: simplify activation instructions"
```

### Task 4: Update the skills page with AI-copy install prompts

**Files:**
- Modify: `C:\Users\Administrator\Documents\Playground\docs\skills.html`

**Step 1: Write the failing test**

Use assertions for:
- `Copy this to your AI`
- `请帮我安装`
- `请使用 skill-installer`
- `subagent-driven-development`

**Step 2: Run test to verify it fails**

Run: `node test_docs_portal.js`
Expected: FAIL until the skills page presents AI-copyable install prompts

**Step 3: Write minimal implementation**

For each recommended skill:
- explain what it does
- link to its source
- add a copyable prompt intended for AI-assisted installation

**Step 4: Run test to verify it passes**

Run: `node test_docs_portal.js`
Expected: PASS

**Step 5: Commit**

```bash
git add C:\Users\Administrator\Documents\Playground\docs\skills.html
git commit -m "docs: add AI-copy skill install prompts"
```
