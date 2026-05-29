# Codebase Map: full-project-scan

> Generated at: 2026-04-02T19:29
> Scope: .claude/workflows, .claude/rules, .claude/scripts, .claude/skills, docs

## 模块概览

| 模块 | 文件数 | LOC | 入口点 | 公开函数 | 内部依赖 |
|------|--------|-----|--------|----------|----------|
| `.claude` | 8 | 1576 | ✓ | 59 | - |

## .claude

路径: `.claude`

**入口点**: 包含 `__main__` 或默认导出

### 公开函数

- `run_command(command_args, workdir)` — .claude/scripts/append_changelog_draft.py:13
- `get_project_dir()` — .claude/scripts/append_changelog_draft.py:26
- `get_last_commit(project_dir)` — .claude/scripts/append_changelog_draft.py:34
- `build_draft_line(commit_hash, commit_subject)` — .claude/scripts/append_changelog_draft.py:47
- `main()` — .claude/scripts/append_changelog_draft.py:53
- `run_git()` — .claude/scripts/auto_checkpoint_commit.py:29
- `get_project_dir()` — .claude/scripts/auto_checkpoint_commit.py:41
- `is_git_repo(d)` — .claude/scripts/auto_checkpoint_commit.py:48
- `detect_worktree(d)` — .claude/scripts/auto_checkpoint_commit.py:53
- `get_current_branch(d)` — .claude/scripts/auto_checkpoint_commit.py:85
- `get_changed_files(d)` — .claude/scripts/auto_checkpoint_commit.py:90
- `get_recent_commits_authors(d, count)` — .claude/scripts/auto_checkpoint_commit.py:103
- `get_oldest_unstaged_age_minutes(d)` — .claude/scripts/auto_checkpoint_commit.py:110
- `analyze_workspace(d, wt_info)` — .claude/scripts/auto_checkpoint_commit.py:128
- `create_backup_branch(d)` — .claude/scripts/auto_checkpoint_commit.py:177
- `create_zip_backup(d, changed_files)` — .claude/scripts/auto_checkpoint_commit.py:184
- `do_commit(d, message)` — .claude/scripts/auto_checkpoint_commit.py:231
- `main()` — .claude/scripts/auto_checkpoint_commit.py:251
- `run_git()` — .claude/scripts/git_safety_check.py:23
- `is_git_write_op(tool_input)` — .claude/scripts/git_safety_check.py:39
- ... 共 59 个公开函数

### 依赖

外部: __future__, argparse, datetime, fnmatch, glob, json, os, pathlib, re, runpy, shlex, subprocess, sys, verify_parallel_scope, zipfile

---
