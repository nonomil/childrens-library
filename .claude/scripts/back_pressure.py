#!/usr/bin/env python3
"""PostToolUse hook：在代码文件修改后执行轻量语法检查。"""

from __future__ import annotations

import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

CPP_SUFFIXES = {".c", ".cc", ".cpp", ".cxx", ".h", ".hpp"}
EDIT_TOOLS = {"Edit", "Write", "MultiEdit"}

def get_project_dir() -> Path:
    project_dir_text = os.getenv("CLAUDE_PROJECT_DIR", "").strip()
    return Path(project_dir_text).resolve() if project_dir_text else Path.cwd().resolve()

def emit(status: str, message: str) -> None:
    print(f"[back_pressure] {status}: {message}", file=sys.stderr)

def load_preferences(project_dir: Path) -> dict[str, object]:
    prefs_path = project_dir / ".claude" / "preferences.json"
    try:
        return json.loads(prefs_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}

def load_payload() -> dict:
    """读取 hook 输入。"""
    raw_text = ""
    try:
        raw_text = sys.stdin.read()
    except OSError:
        raw_text = ""
    if not raw_text.strip():
        raw_text = os.getenv("CLAUDE_TOOL_INPUT", "").strip()
    if not raw_text:
        return {}
    try:
        payload = json.loads(raw_text)
        return payload if isinstance(payload, dict) else {}
    except (json.JSONDecodeError, TypeError):
        return {}

def extract_path(value: object) -> str:
    """递归提取目标文件路径。"""
    if isinstance(value, dict):
        for key_name in ("file_path", "path", "target_file"):
            target_value = value.get(key_name)
            if isinstance(target_value, str) and target_value.strip():
                return target_value.strip()
        for child_value in value.values():
            path_text = extract_path(child_value)
            if path_text:
                return path_text
    elif isinstance(value, list):
        for item in value:
            path_text = extract_path(item)
            if path_text:
                return path_text
    return ""

def resolve_target(project_dir: Path) -> Path | None:
    payload = load_payload()
    if payload.get("tool_name") not in EDIT_TOOLS:
        return None
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        return None
    file_path = extract_path(tool_input)
    if not file_path:
        return None
    target_path = Path(file_path)
    return target_path.resolve() if target_path.is_absolute() else (project_dir / target_path).resolve()

def run_command(args: list[str], project_dir: Path) -> tuple[int, str]:
    result = subprocess.run(
        args,
        cwd=project_dir,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    output = "\n".join(part.strip() for part in (result.stdout, result.stderr) if part.strip())
    return result.returncode, output

def check_python(target_path: Path, project_dir: Path) -> int:
    emit("Checking", f"{target_path.name} (python)")
    return_code, output = run_command([sys.executable, "-m", "py_compile", str(target_path)], project_dir)
    if return_code != 0:
        emit("BLOCKED", f"syntax error in {target_path.name}")
        if output:
            print(output, file=sys.stderr)
        return 2
    emit("OK", "py_compile passed")
    if importlib.util.find_spec("ruff") is None:
        emit("SKIP", "ruff not found")
        return 0
    return_code, output = run_command([sys.executable, "-m", "ruff", "check", str(target_path)], project_dir)
    if return_code != 0:
        match = re.search(r"Found\s+(\d+)\s+", output)
        emit("WARNING", f"ruff found {match.group(1)} issues" if match else "ruff reported issues")
        if output:
            print(output, file=sys.stderr)
    return 0

def check_cpp(target_path: Path, project_dir: Path) -> int:
    emit("Checking", f"{target_path.name} ({'c' if target_path.suffix.lower() == '.c' else 'c++'})")
    compiler_path = shutil.which("g++")
    if not compiler_path:
        emit("SKIP", "g++ not found")
        return 0
    standard_name = "c11" if target_path.suffix.lower() == ".c" else "c++17"
    return_code, output = run_command(
        [compiler_path, "-fsyntax-only", f"-std={standard_name}", str(target_path)],
        project_dir,
    )
    if return_code != 0 or output:
        emit("WARNING", f"g++ reported issues in {target_path.name}")
        if output:
            print(output, file=sys.stderr)
    else:
        emit("OK", "g++ syntax check passed")
    return 0

def main() -> int:
    project_dir = get_project_dir()
    target_path = resolve_target(project_dir)
    if target_path is None:
        return 0
    suffix = target_path.suffix.lower()
    if suffix != ".py" and suffix not in CPP_SUFFIXES:
        return 0
    preferences = load_preferences(project_dir)
    if preferences.get("profile") == "minimal":
        emit("SKIP", "profile=minimal")
        return 0
    if preferences.get("project_lang") == "none":
        return 0
    if suffix == ".py":
        return check_python(target_path, project_dir)
    return check_cpp(target_path, project_dir)

if __name__ == "__main__":
    raise SystemExit(main())
