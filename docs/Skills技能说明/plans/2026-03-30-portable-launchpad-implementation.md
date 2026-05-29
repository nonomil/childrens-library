# Portable Launchpad Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make the project easier to copy to another computer by keeping a stable root entrypoint, adding Chinese activation prompts, and letting the batch launcher open the local docs site directly.

**Architecture:** Preserve the current root-level entry files so existing links and tests keep working, then improve portability through relative-path launching, Chinese menu text, and docs that explain which files should travel together. The PowerShell helper remains the source of truth for config writes, while the batch file becomes the friendlier launcher.

**Tech Stack:** Windows batch, PowerShell, static HTML/CSS/JS, Node.js assertions

### Task 1: Lock in the new launcher behavior with failing tests

**Files:**
- Modify: `C:\Users\Administrator\Documents\Playground\test_update_codex_config.js`
- Modify: `C:\Users\Administrator\Documents\Playground\test_docs_portal.js`

**Step 1: Write the failing test**

Add assertions for:
- Chinese launcher menu text
- a docs-open option exposed by the batch flow
- activation docs describing the new docs-open action and portable copy usage

**Step 2: Run test to verify it fails**

Run: `node test_update_codex_config.js`
Expected: FAIL because the launcher still prints English prompts and cannot open local docs

Run: `node test_docs_portal.js`
Expected: FAIL because the activation docs do not yet describe the updated launcher behavior

**Step 3: Write minimal implementation**

Keep the new assertions focused on user-visible behavior only.

**Step 4: Run test to verify it passes**

Run: `node test_update_codex_config.js`
Expected: PASS

Run: `node test_docs_portal.js`
Expected: PASS

**Step 5: Commit**

```bash
git add C:\Users\Administrator\Documents\Playground\test_update_codex_config.js C:\Users\Administrator\Documents\Playground\test_docs_portal.js
git commit -m "test: cover chinese launcher and docs shortcut"
```

### Task 2: Update the launcher scripts for Chinese prompts and local docs opening

**Files:**
- Modify: `C:\Users\Administrator\Documents\Playground\update_codex_config.bat`
- Modify: `C:\Users\Administrator\Documents\Playground\update_codex_config.ps1`

**Step 1: Write the failing test**

Use assertions for:
- menu options `1/2/3`
- a new menu option for opening local docs
- Chinese error and completion messages
- non-interactive mode continuing to support direct arguments

**Step 2: Run test to verify it fails**

Run: `node test_update_codex_config.js`
Expected: FAIL until the batch and PowerShell scripts expose the new interactive menu behavior

**Step 3: Write minimal implementation**

Add:
- a Chinese interactive menu
- a docs-open branch that resolves `docs/index.html` relative to the script directory
- portable relative-path handling so the copied folder keeps working under different usernames and locations

**Step 4: Run test to verify it passes**

Run: `node test_update_codex_config.js`
Expected: PASS

**Step 5: Commit**

```bash
git add C:\Users\Administrator\Documents\Playground\update_codex_config.bat C:\Users\Administrator\Documents\Playground\update_codex_config.ps1
git commit -m "feat: localize launcher and add docs shortcut"
```

### Task 3: Sync docs for copy-friendly distribution

**Files:**
- Modify: `C:\Users\Administrator\Documents\Playground\docs\index.html`
- Modify: `C:\Users\Administrator\Documents\Playground\docs\activation.html`
- Modify: `C:\Users\Administrator\Documents\Playground\INSTALL.md`

**Step 1: Write the failing test**

Add assertions for:
- portable copy guidance
- the new docs-open action in the launcher
- Chinese guidance aligned with the updated script behavior

**Step 2: Run test to verify it fails**

Run: `node test_docs_portal.js`
Expected: FAIL until the docs match the new launcher behavior

**Step 3: Write minimal implementation**

Update the docs to explain:
- which top-level files to keep together when copying
- that users can double-click the batch file and choose an activation mode or open the docs
- that all paths are discovered automatically from the copied folder and current user profile

**Step 4: Run test to verify it passes**

Run: `node test_docs_portal.js`
Expected: PASS

**Step 5: Commit**

```bash
git add C:\Users\Administrator\Documents\Playground\docs\index.html C:\Users\Administrator\Documents\Playground\docs\activation.html C:\Users\Administrator\Documents\Playground\INSTALL.md
git commit -m "docs: explain portable copy flow and launcher shortcut"
```
