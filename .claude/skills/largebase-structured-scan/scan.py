"""兼容入口。

外部命令继续调用 skill 根目录下的 scan.py，
实际实现统一收敛在 scripts/scan.py。
"""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


SKILL_ROOT = Path(__file__).resolve().parent
SCRIPTS_DIR = SKILL_ROOT / "scripts"
IMPL_PATH = SCRIPTS_DIR / "scan.py"
IMPL_MODULE_NAME = "largebase_structured_scan_impl"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

impl_spec = spec_from_file_location(IMPL_MODULE_NAME, IMPL_PATH)
if impl_spec is None or impl_spec.loader is None:
    raise RuntimeError(f"无法加载扫描器实现: {IMPL_PATH}")

impl_module = module_from_spec(impl_spec)
sys.modules[IMPL_MODULE_NAME] = impl_module
impl_spec.loader.exec_module(impl_module)

# 透传实现模块的公开符号，兼容现有测试和调用方。
for name in dir(impl_module):
    if not name.startswith("__"):
        globals()[name] = getattr(impl_module, name)


if __name__ == "__main__":
    main()
