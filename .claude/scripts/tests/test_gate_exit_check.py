from __future__ import annotations

import contextlib
import importlib.util
import io
import os
import subprocess
import tempfile
import unittest
from datetime import date
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1] / "gate_exit_check.py"
)


def load_module():
    """按文件路径加载待测模块。"""
    spec = importlib.util.spec_from_file_location("gate_exit_check", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载模块: {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class GateExitCheckTest(unittest.TestCase):
    def test_extract_status_paths_parses_git_short_output(self) -> None:
        module = load_module()

        paths = module.extract_status_paths(" M tracked.txt\n?? new_file.py\nR  old.py -> new.py\n")

        self.assertEqual(paths, ["tracked.txt", "new_file.py", "old.py -> new.py"])

    def test_has_today_denied_entry_accepts_common_date_formats(self) -> None:
        module = load_module()
        target_date = date(2026, 4, 3)

        self.assertTrue(module.has_today_denied_entry("2026-04-03 denied", target_date))
        self.assertTrue(module.has_today_denied_entry("2026/04/03 denied", target_date))
        self.assertTrue(module.has_today_denied_entry("20260403 denied", target_date))
        self.assertFalse(module.has_today_denied_entry("2026-04-02 denied", target_date))

    def test_main_reports_all_three_checks(self) -> None:
        module = load_module()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            claude_dir = project_dir / ".claude"
            claude_dir.mkdir(parents=True, exist_ok=True)
            (claude_dir / ".gate-approved").write_text("{}", encoding="utf-8")
            today_text = date.today().isoformat()
            (claude_dir / ".gate-denied-log").write_text(
                f"{today_text} blocked\n",
                encoding="utf-8",
            )

            self._init_git_repo(project_dir)
            tracked_file = project_dir / "tracked.txt"
            tracked_file.write_text("updated\n", encoding="utf-8")
            (project_dir / "new_file.py").write_text("print('x')\n", encoding="utf-8")

            stderr_buffer = io.StringIO()
            old_project_dir = os.environ.get("CLAUDE_PROJECT_DIR")
            os.environ["CLAUDE_PROJECT_DIR"] = str(project_dir)
            try:
                with contextlib.redirect_stderr(stderr_buffer):
                    exit_code = module.main()
            finally:
                if old_project_dir is None:
                    os.environ.pop("CLAUDE_PROJECT_DIR", None)
                else:
                    os.environ["CLAUDE_PROJECT_DIR"] = old_project_dir

        output = stderr_buffer.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn(".gate-approved 仍存在", output)
        self.assertIn("有 2 个未提交文件", output)
        self.assertIn("tracked.txt", output)
        self.assertIn("new_file.py", output)
        self.assertIn("本次会话曾被门禁拦截", output)

    def _init_git_repo(self, project_dir: Path) -> None:
        self._run_git(project_dir, "init")
        self._run_git(project_dir, "config", "user.name", "Test User")
        self._run_git(project_dir, "config", "user.email", "test@example.com")
        (project_dir / ".gitignore").write_text(
            ".claude/.gate-approved\n.claude/.gate-denied-log\n",
            encoding="utf-8",
        )
        tracked_file = project_dir / "tracked.txt"
        tracked_file.write_text("original\n", encoding="utf-8")
        self._run_git(project_dir, "add", ".gitignore", "tracked.txt")
        self._run_git(project_dir, "commit", "-m", "initial")

    def _run_git(self, project_dir: Path, *args: str) -> None:
        result = subprocess.run(
            ["git", *args],
            cwd=str(project_dir),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if result.returncode != 0:
            self.fail(f"git {' '.join(args)} 失败: {result.stderr}")


if __name__ == "__main__":
    unittest.main()
