"""
自动修复脚本：为缺少 celebrate() 调用的课件文件添加调用
同时为缺少 480px 响应式断点的文件添加断点
"""
import os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

COURSEWARE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Prj", "childrens-library", "courseware")

def add_celebrate_to_file(filepath, content):
    """Add celebrate() call to a file that doesn't have one"""
    filename = os.path.basename(filepath)

    # Strategy: find the last </script> before </body> and add celebrate logic before it
    # Look for common completion patterns

    # Pattern 1: File has quiz with checkQuiz function
    if 'function checkQuiz' in content:
        # Find the quiz completion logic - look for "quizScore.total >= N" or similar
        # Add celebrate call after the quiz completion block

        # Find the closing of the checkQuiz function or the last quiz-related code
        # Look for patterns like "quizScore.total >= " or "allCorrect" or "quiz-complete"

        # Simple approach: add a wrapper that calls celebrate when all quizzes are done
        celebrate_code = """
// === AUTO-ADDED: village completion reporting ===
(function() {
  var _origCheckQuiz = window.checkQuiz;
  if (_origCheckQuiz) {
    window.checkQuiz = function() {
      _origCheckQuiz.apply(this, arguments);
      // Check if all quizzes are answered
      setTimeout(function() {
        var totalQ = document.querySelectorAll('.quiz-question').length || document.querySelectorAll('[data-q]').length;
        var answered = Object.keys(window.quizAnswered || {}).length;
        if (totalQ > 0 && answered >= totalQ) {
          if (window.celebrate) window.celebrate();
        }
      }, 500);
    };
  }
})();
"""

        # Insert before the last </script>
        last_script_end = content.rfind('</script>')
        if last_script_end > 0:
            content = content[:last_script_end] + celebrate_code + content[last_script_end:]
            return content, "added quiz wrapper"

    # Pattern 2: File has turn.js book with last page
    if 'turn' in content.lower() and ('.turn(' in content or 'pages' in content.lower()):
        celebrate_code = """
// === AUTO-ADDED: village completion reporting ===
(function() {
  var _book = document.getElementById('book') || document.querySelector('.book');
  if (_book && _book.turn) {
    $(_book).bind('turned', function(e, page, pages) {
      if (page >= pages) {
        setTimeout(function() { if (window.celebrate) window.celebrate(); }, 500);
      }
    });
  }
})();
"""
        last_script_end = content.rfind('</script>')
        if last_script_end > 0:
            content = content[:last_script_end] + celebrate_code + content[last_script_end:]
            return content, "added turn.js wrapper"

    # Pattern 3: File has pages array with goToPage (like story files)
    if 'pages' in content and 'goToPage' in content:
        # Already handled by story structure
        return content, "skipped (story pattern)"

    # Pattern 4: File has a "complete" or "finish" section
    if 'complete' in content.lower() or 'finish' in content.lower():
        celebrate_code = """
// === AUTO-ADDED: village completion reporting ===
document.addEventListener('click', function(e) {
  if (e.target && (e.target.classList.contains('complete-btn') || e.target.classList.contains('finish-btn'))) {
    setTimeout(function() { if (window.celebrate) window.celebrate(); }, 500);
  }
});
"""
        last_script_end = content.rfind('</script>')
        if last_script_end > 0:
            content = content[:last_script_end] + celebrate_code + content[last_script_end:]
            return content, "added click listener"

    # Pattern 5: Generic fallback - add celebrate on reaching last section
    celebrate_code = """
// === AUTO-ADDED: village completion reporting ===
(function() {
  var celebrationDone = false;
  function tryCelebrate() {
    if (celebrationDone) return;
    celebrationDone = true;
    setTimeout(function() { if (window.celebrate) window.celebrate(); }, 300);
  }
  // Trigger on scroll to bottom
  window.addEventListener('scroll', function() {
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 100) {
      tryCelebrate();
    }
  });
  // Trigger on last nav button click
  document.addEventListener('click', function(e) {
    if (e.target && (e.target.id === 'nextBtn' || e.target.classList.contains('next-btn'))) {
      var btn = e.target;
      if (btn.disabled || btn.classList.contains('disabled')) {
        tryCelebrate();
      }
    }
  });
})();
"""
    last_script_end = content.rfind('</script>')
    if last_script_end > 0:
        content = content[:last_script_end] + celebrate_code + content[last_script_end:]
        return content, "added fallback scroll/nav listener"

    return content, "no suitable insertion point"


def add_responsive_480(content):
    """Add 480px responsive breakpoint if missing"""
    if '480px' in content:
        return content, False

    # Find the 768px breakpoint and add a 480px one after it
    if '768px' in content:
        responsive_480 = """
@media (max-width: 480px) {
  body { padding: 8px; }
  h1 { font-size: 24px; }
  h2 { font-size: 18px; }
  .quiz-btn { padding: 10px 14px; font-size: 14px; }
  .nav-btn { width: 36px; height: 36px; font-size: 16px; }
}
"""
        # Insert after the 768px media query
        idx = content.rfind('768px')
        if idx > 0:
            # Find the end of this media query
            brace_count = 0
            in_media = False
            i = idx
            while i < len(content):
                if content[i] == '{':
                    brace_count += 1
                    in_media = True
                elif content[i] == '}':
                    brace_count -= 1
                    if in_media and brace_count == 0:
                        # Insert after this closing brace
                        content = content[:i+1] + '\n' + responsive_480 + content[i+1:]
                        return content, True
                i += 1

    return content, False


def main():
    html_files = sorted([f for f in os.listdir(COURSEWARE_DIR) if f.endswith('.html')])

    celebrate_fixed = 0
    responsive_fixed = 0
    skipped = 0
    errors = []

    for filename in html_files:
        filepath = os.path.join(COURSEWARE_DIR, filename)

        # Skip index files and shared files
        if filename in ['stories-index.html']:
            continue

        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        except Exception as e:
            errors.append(f"{filename}: read error - {e}")
            continue

        modified = False

        # Fix celebrate()
        if 'celebrate' not in content:
            content, method = add_celebrate_to_file(filepath, content)
            if 'added' in method:
                celebrate_fixed += 1
                modified = True
                print(f"  CELEBRATE | {filename}: {method}")
            elif 'skipped' in method:
                skipped += 1
            else:
                print(f"  SKIP | {filename}: {method}")

        # Fix 480px responsive
        content_res, was_fixed = add_responsive_480(content)
        if was_fixed:
            content = content_res
            responsive_fixed += 1
            modified = True
            print(f"  RESPONSIVE | {filename}: added 480px breakpoint")

        # Save if modified
        if modified:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
            except Exception as e:
                errors.append(f"{filename}: write error - {e}")

    print(f"\n=== 修复总结 ===")
    print(f"  celebrate() 修复: {celebrate_fixed} 个文件")
    print(f"  480px 响应式修复: {responsive_fixed} 个文件")
    print(f"  跳过: {skipped} 个文件")
    if errors:
        print(f"  错误: {len(errors)} 个")
        for e in errors:
            print(f"    - {e}")


if __name__ == "__main__":
    main()
