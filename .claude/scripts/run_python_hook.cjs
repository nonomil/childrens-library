/**
 * Smart Python Hook Launcher
 *
 * 自动检测 Python 路径，启动目标 Python hook 脚本。
 * 检测顺序：缓存文件 → PATH → uv → 常见安装路径
 * 找不到时输出错误提示，不静默失败。
 *
 * 用法: node .claude/scripts/run_python_hook.cjs .claude/scripts/xxx.py
 * stdin 会透传给 Python 脚本。
 */

const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

const PROJECT_DIR = (
  process.env.CLAUDE_PROJECT_DIR || process.cwd()
).replace(/\\/g, "/");
const CACHE_FILE = path.join(PROJECT_DIR, ".claude", "python_path.txt");
const PROJECT_VENV_PYTHON = path.join(PROJECT_DIR, ".venv", "Scripts", "python.exe");

// ── Python 候选路径（按优先级排列）────────────────────────
function getCandidates() {
  const home = process.env.USERPROFILE || process.env.HOME || "C:/Users/KLD";
  const candidates = [];

  // 1. ???? .venv?????? Python?
  if (fs.existsSync(PROJECT_VENV_PYTHON)) {
    candidates.push(PROJECT_VENV_PYTHON);
  }


  // 1. uv 管理的 Python（按版本号排序，优先高版本）
  const uvDir = path.join(home, "AppData", "Roaming", "uv", "python");
  if (fs.existsSync(uvDir)) {
    try {
      const entries = fs
        .readdirSync(uvDir)
        .filter((e) => e.startsWith("cpython-"))
        .sort()
        .reverse(); // 高版本优先
      for (const e of entries) {
        const p = path.join(uvDir, e, "python.exe");
        if (fs.existsSync(p)) candidates.push(p);
      }
    } catch {}
  }

  // 2. 标准 PATH 位置
  candidates.push("python");
  candidates.push("python3");

  // 3. 常见安装路径
  const commonDirs = [
    path.join(home, "AppData", "Local", "Programs", "Python"),
    "C:/Python310",
    "C:/Python311",
    "C:/Python312",
    "C:/Python313",
    "C:/Program Files/Python310",
    "C:/Program Files/Python311",
    "C:/Program Files/Python312",
    "C:/Program Files/Python313",
    "C:/ProgramData/Anaconda3",
    "C:/ProgramData/miniconda3",
    path.join(home, "Anaconda3"),
    path.join(home, "Miniconda3"),
    path.join(home, "anaconda3"),
    path.join(home, "miniconda3"),
    path.join(home, "scoop", "apps", "python", "current"),
  ];
  for (const d of commonDirs) {
    candidates.push(path.join(d, "python.exe"));
  }

  return candidates;
}

// ── 验证 Python 可用 ──────────────────────────────────────
function verifyPython(pythonPath) {
  try {
    const r = spawnSync(
      pythonPath,
      ["-c", "import sys; print(sys.executable)"],
      {
        encoding: "utf-8",
        timeout: 5000,
        windowsHide: true,
      }
    );
    if (r.status === 0 && ((r.stdout || "").trim().length > 0 || (r.stderr || "").trim().length > 0)) {
      return true;
    }
  } catch {}
  return false;
}

// ── 查找 Python ──────────────────────────────────────────
function findPython() {
  // 1. 读缓存
  if (fs.existsSync(CACHE_FILE)) {
    try {
      const cached = fs.readFileSync(CACHE_FILE, "utf-8").trim();
      if (cached && verifyPython(cached)) {
        return cached;
      }
    } catch {}
    // 缓存失效，删除
    try { fs.unlinkSync(CACHE_FILE); } catch {}
  }

  // 2. 逐个尝试候选路径
  for (const candidate of getCandidates()) {
    if (verifyPython(candidate)) {
      // 缓存结果
      try {
        fs.mkdirSync(path.dirname(CACHE_FILE), { recursive: true });
        fs.writeFileSync(CACHE_FILE, candidate, "utf-8");
      } catch {}
      return candidate;
    }
  }

  return null;
}

// ── 主逻辑 ────────────────────────────────────────────────
function main() {
  const scriptPath = process.argv[2];
  if (!scriptPath) {
    process.stderr.write(
      "[run_python_hook] Usage: node run_python_hook.cjs <script.py>\n"
    );
    process.exit(2);
  }

  const pythonPath = findPython();
  if (!pythonPath) {
    process.stderr.write(
      "[run_python_hook] Python not found!\n" +
        "  Searched: PATH, uv, common install paths\n" +
        "  Fix: run `echo <python_exe_path> > .claude/python_path.txt`\n" +
        "  Example: echo E:\\Project_LM\\SPC_Floor\\.venv\\Scripts\\python.exe > .claude/python_path.txt\n"
    );
    process.exit(2);
  }

  // 解析脚本绝对路径
  const absScript = path.isAbsolute(scriptPath)
    ? scriptPath
    : path.resolve(PROJECT_DIR, scriptPath);

  if (!fs.existsSync(absScript)) {
    process.stderr.write(`[run_python_hook] Script not found: ${absScript}\n`);
    process.exit(2);
  }

  // 透传 stdin，执行 Python 脚本
  const result = spawnSync(
    pythonPath,
    [absScript, ...process.argv.slice(3)],
    {
      stdio: ["inherit", "inherit", "inherit"],
      timeout: 30000,
      windowsHide: true,
      env: { ...process.env, CLAUDE_PROJECT_DIR: PROJECT_DIR },
    }
  );

  if (result.error) {
    process.stderr.write(`[run_python_hook] Spawn error: ${result.error.message}\n`);
    process.exit(2);
  }

  process.exit(result.status || 0);
}

main();