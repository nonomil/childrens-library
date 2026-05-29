from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path


HOOK_ROOT = Path(__file__).resolve().parents[1]
if str(HOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(HOOK_ROOT))

from runtime.contracts import HookEvent, HookPlatform
from runtime.platform_adapter import detect_platform, event_is_supported, normalize_event_name


class CompatibilityTest(unittest.TestCase):
    def test_detect_platform_prefers_explicit_override(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            env_map = dict(os.environ)
            env_map["HOOK_RUNTIME_PLATFORM"] = "claude"
            self.assertEqual(detect_platform(project_dir, env_map), HookPlatform.CLAUDE)

    def test_detect_platform_falls_back_to_codex_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            (project_dir / ".codex" / "hooks").mkdir(parents=True, exist_ok=True)
            self.assertEqual(detect_platform(project_dir, {}), HookPlatform.CODEX)

    def test_normalize_event_name_supports_common_formats(self) -> None:
        self.assertEqual(normalize_event_name("post_tool_use"), HookEvent.POST_TOOL_USE)
        self.assertEqual(normalize_event_name("SessionStart"), HookEvent.SESSION_START)

    def test_codex_does_not_claim_user_prompt_submit_support(self) -> None:
        self.assertFalse(event_is_supported(HookPlatform.CODEX, HookEvent.USER_PROMPT_SUBMIT))
        self.assertTrue(event_is_supported(HookPlatform.CLAUDE, HookEvent.USER_PROMPT_SUBMIT))


if __name__ == "__main__":
    unittest.main()
