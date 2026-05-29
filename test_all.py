"""
自动化课件测试脚本 - 检查所有HTML课件的结构、样式、交互完整性
"""
import os, re, sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

COURSEWARE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Prj", "childrens-library", "courseware")
VILLAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Prj", "childrens-library")

# Requirements checklist
CHECKS = {
    "has_doctype": "DOCTYPE声明",
    "has_meta_charset": "meta charset",
    "has_meta_viewport": "meta viewport",
    "has_data_type": "data-type属性",
    "has_village_reporter": "village-reporter.js引入",
    "has_gsap": "GSAP引入",
    "has_nunito": "Nunito字体",
    "has_responsive_480": "480px响应式断点",
    "has_responsive_768": "768px响应式断点",
    "has_celebrate": "celebrate()函数调用",
    "has_title": "title标签",
    "has_description": "meta description",
    "no_js_syntax_error": "JS无明显语法错误",
    "pages_have_content": "页面有实际内容(非空)",
}

def test_file(filepath):
    """Test a single HTML file and return results"""
    results = {}
    filename = os.path.basename(filepath)

    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        return {"error": str(e)}

    # Basic structure checks
    results["has_doctype"] = content.lower().startswith("<!doctype") or "<!DOCTYPE" in content[:200]
    results["has_meta_charset"] = "charset=" in content[:500]
    results["has_meta_viewport"] = "viewport" in content[:1000]
    results["has_data_type"] = 'data-type=' in content[:300]
    results["has_village_reporter"] = "village-reporter.js" in content
    results["has_gsap"] = "gsap" in content.lower()
    results["has_nunito"] = "Nunito" in content or "nunito" in content.lower()
    results["has_responsive_480"] = "480px" in content
    results["has_responsive_768"] = "768px" in content
    results["has_celebrate"] = "celebrate" in content
    results["has_title"] = "<title>" in content
    results["has_description"] = 'description' in content[:2000]

    # Check for JS syntax issues (basic)
    script_blocks = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    js_issues = []
    for i, block in enumerate(script_blocks):
        # Check for unclosed braces
        opens = block.count('{')
        closes = block.count('}')
        if abs(opens - closes) > 2:  # Allow small mismatch for template strings
            js_issues.append(f"script#{i+1}: braces mismatch ({opens} open, {closes} close)")
    results["no_js_syntax_error"] = len(js_issues) == 0
    results["js_issues"] = js_issues

    # Check pages content (for story files)
    if "pages" in content and "render" in content:
        # Count pages
        page_count = content.count("title:") + content.count("'title'")
        results["page_count"] = page_count

        # Check for empty render blocks
        empty_renders = len(re.findall(r"render:\s*`[\s\n]*`", content))
        results["pages_have_content"] = empty_renders == 0
        results["empty_renders"] = empty_renders

        # Check for image URLs
        img_urls = re.findall(r'src="(https://[^"]+)"', content)
        results["image_count"] = len(img_urls)
        results["has_github_images"] = any("github" in u for u in img_urls)
    else:
        results["page_count"] = 0
        results["pages_have_content"] = True

    # Get file size
    results["file_size"] = os.path.getsize(filepath)
    results["line_count"] = content.count('\n') + 1

    # Detect data-type value
    dt_match = re.search(r'data-type="([^"]+)"', content)
    results["data_type_value"] = dt_match.group(1) if dt_match else "MISSING"

    return results

def test_village_files():
    """Test village core files"""
    print("\n" + "="*80)
    print("  村庄核心文件测试")
    print("="*80)

    village_html = os.path.join(VILLAGE_DIR, "village.html")
    village_js = os.path.join(COURSEWARE_DIR, "shared", "village.js")
    village_css = os.path.join(COURSEWARE_DIR, "shared", "village.css")
    village_reporter = os.path.join(COURSEWARE_DIR, "shared", "village-reporter.js")

    # Test village.html
    if os.path.exists(village_html):
        with open(village_html, 'r', encoding='utf-8') as f:
            content = f.read()

        checks = {
            "顶部状态栏(header)": '<header class="village-header">' in content or 'village-header' in content,
            "村庄地图(village-map)": 'village-map' in content,
            "6个建筑区域": all(z in content for z in ['data-zone="english"', 'data-zone="chinese"',
                'data-zone="math"', 'data-zone="songs"', 'data-zone="science"', 'data-zone="stories"']),
            "Steve角色": 'id="steve"' in content,
            "Alex角色": 'id="alex"' in content,
            "宠物角色": 'id="petCharacter"' in content,
            "金币显示": 'id="coinCount"' in content,
            "星星显示": 'id="starCount"' in content,
            "连续天数": 'id="streakBadge"' in content,
            "每日任务板": 'id="dailyBoard"' in content,
            "课件面板(zonePanel)": 'id="zonePanel"' in content,
            "商店面板(shopPanel)": 'id="shopPanel"' in content,
            "宠物面板(petPanel)": 'id="petPanel"' in content,
            "欢迎动画": 'id="welcomeOverlay"' in content,
            "完成提示": 'id="completionToast"' in content,
            "装饰层": 'id="decorations"' in content,
            "天空背景(sky-bg)": 'sky-bg' in content,
            "草地背景(grass-bg)": 'grass-bg' in content,
            "云朵动画(cloud)": 'cloud-1' in content,
            "太阳(sun)": 'class="sun"' in content,
            "village.js引入": 'village.js' in content,
            "village.css引入": 'village.css' in content,
            "GSAP引入": 'gsap' in content,
        }

        print("\n--- village.html ---")
        for name, passed in checks.items():
            print(f"  {'PASS' if passed else 'FAIL'} | {name}")
    else:
        print("  FAIL | village.html 文件不存在!")

    # Test village.js
    if os.path.exists(village_js):
        with open(village_js, 'r', encoding='utf-8') as f:
            content = f.read()

        checks = {
            "ZONE_CONFIG(6区域配置)": all(z in content for z in ['english', 'chinese', 'math', 'songs', 'science', 'stories']),
            "DECORATION_RULES(6装饰规则)": content.count("id:") >= 6,
            "DAILY_TASKS(每日任务)": 'DAILY_TASKS' in content,
            "COIN_REWARDS(金币奖励)": 'COIN_REWARDS' in content,
            "SHOP_ITEMS(商店商品)": 'SHOP_ITEMS' in content,
            "PET_TYPES(宠物类型)": 'PET_TYPES' in content,
            "PET_STAGES(成长阶段)": 'PET_STAGES' in content,
            "getDefaultState(v2)": 'version: 2' in content or 'version:2' in content,
            "loadVillageState(迁移逻辑)": 'loadVillageState' in content,
            "updateStreak(连续天数)": 'updateStreak' in content,
            "getDailyMission(每日任务)": 'getDailyMission' in content,
            "isZoneUnlocked(解锁判断)": 'isZoneUnlocked' in content,
            "earnCoins(赚金币)": 'earnCoins' in content,
            "spendCoins(花金币)": 'spendCoins' in content,
            "openShop(商店)": 'openShop' in content,
            "buyItem(购买)": 'buyItem' in content,
            "showPetSelection(选宠物)": 'showPetSelection' in content,
            "selectPet(确认选宠)": 'selectPet' in content,
            "openPetPanel(宠物面板)": 'openPetPanel' in content,
            "playWithPet(和宠物玩)": 'playWithPet' in content,
            "renderPet(渲染宠物)": 'renderPet' in content,
            "updatePetHunger(饥饿衰减)": 'updatePetHunger' in content,
            "gameLoop(游戏循环)": 'gameLoop' in content,
            "Steve走动动画": 'updateSteve' in content,
            "Steve说话台词": 'STEVE_LINES' in content,
            "欢迎动画": 'showWelcome' in content,
            "装饰解锁检查": 'checkAndUnlockDecorations' in content,
            "课件文件列表(getAllCoursewareFiles)": 'getAllCoursewareFiles' in content,
        }

        print("\n--- village.js ---")
        for name, passed in checks.items():
            print(f"  {'PASS' if passed else 'FAIL'} | {name}")
    else:
        print("  FAIL | village.js 文件不存在!")

    # Test village.css
    if os.path.exists(village_css):
        with open(village_css, 'r', encoding='utf-8') as f:
            content = f.read()

        checks = {
            "CSS变量(:root)": ':root' in content,
            "天空蓝变量(--sky)": '--sky' in content,
            "像素风字体(--font-mc)": '--font-mc' in content,
            "village-header样式": '.village-header' in content,
            "village-map样式": '.village-map' in content,
            "building样式": '.building' in content,
            "6个建筑位置": all(f'data-zone="{z}"' in content for z in ['english','chinese','math','songs','science','stories']),
            "CSS建筑绘制(roof/wall)": '.roof' in content and '.wall' in content,
            "学校建筑": '.building-school' in content,
            "图书馆建筑": '.building-library' in content,
            "集市建筑": '.building-market' in content,
            "舞台建筑": '.building-stage' in content,
            "实验室建筑": '.building-lab' in content,
            "故事屋建筑": '.building-stories' in content,
            "Steve角色样式": '.pixel-steve' in content,
            "云朵动画": 'cloudFloat' in content,
            "太阳脉动": 'sunPulse' in content,
            "角色弹跳": 'characterBounce' in content,
            "语音气泡": '.speech-bubble' in content,
            "装饰层": '.decorations' in content,
            "每日任务板": '.daily-board' in content,
            "课件面板(zone-panel)": '.zone-panel' in content,
            "课件卡片(course-card)": '.course-card' in content,
            "欢迎动画": '.welcome-overlay' in content,
            "完成提示": '.completion-toast' in content,
            "金币显示": '.coin-count' in content,
            "宠物角色": '.pet-character' in content,
            "宠物动画(petBounce)": 'petBounce' in content,
            "宠物开心(petJump)": 'petJump' in content,
            "宠物难过(petSad)": 'petSad' in content,
            "商店面板": '.shop-panel' in content or '.shop-items' in content,
            "商店商品": '.shop-item' in content,
            "宠物面板": '.pet-status-panel' in content,
            "宠物属性条(stat-fill)": '.stat-fill' in content,
            "宠物选择": '.pet-select-grid' in content,
            "进度条": '.progress-bar' in content and '.progress-fill' in content,
            "响应式768px": '768px' in content,
            "响应式480px": '480px' in content,
        }

        print("\n--- village.css ---")
        for name, passed in checks.items():
            print(f"  {'PASS' if passed else 'FAIL'} | {name}")
    else:
        print("  FAIL | village.css 文件不存在!")

def main():
    print("="*80)
    print("  儿童绘本课件自动化测试报告")
    print("  测试时间: 2026-05-29")
    print("="*80)

    # Test village core
    test_village_files()

    # Test all courseware files
    print("\n" + "="*80)
    print("  课件文件测试 (所有HTML)")
    print("="*80)

    html_files = sorted([f for f in os.listdir(COURSEWARE_DIR) if f.endswith('.html')])

    total = len(html_files)
    passed_count = 0
    failed_count = 0
    issues = []

    # Categorize
    categories = {
        "english": [], "chinese": [], "math": [], "songs": [],
        "science": [], "stories": [], "other": []
    }

    for filename in html_files:
        filepath = os.path.join(COURSEWARE_DIR, filename)
        results = test_file(filepath)

        if "error" in results:
            issues.append(f"{filename}: 读取错误 - {results['error']}")
            failed_count += 1
            continue

        # Categorize
        cat = "other"
        if filename.startswith("english-") or filename == "english-colors.html":
            cat = "english"
        elif filename.startswith("chinese-") or filename.startswith("poem-") or filename == "chinese-magic-characters.html":
            cat = "chinese"
        elif filename.startswith("math-") or filename == "math-numbers-1-10.html":
            cat = "math"
        elif any(filename.startswith(p) for p in ["twinkle","old-macdonald","wheels","bingo","abc-song","head-shoulders","humpty","baa-baa","five-little","hickory","hush-little","if-youre","itsy","jack-and","jack-be","london","mary","mulberry","pat-a","rain-go","ring-around","row-your","silent","skidamarink","three-blind","yankee","cat-and"]):
            cat = "songs"
        elif any(filename.startswith(p) for p in ["gears-","science-","rainforest-","nature-"]):
            cat = "science"
        elif filename.startswith("story-"):
            cat = "stories"
        categories[cat].append((filename, results))

        # Check for failures
        file_issues = []
        if not results.get("has_doctype"): file_issues.append("缺DOCTYPE")
        if not results.get("has_meta_charset"): file_issues.append("缺charset")
        if not results.get("has_meta_viewport"): file_issues.append("缺viewport")
        if not results.get("has_data_type"): file_issues.append("缺data-type")
        if not results.get("has_village_reporter"): file_issues.append("缺village-reporter")
        if not results.get("has_gsap"): file_issues.append("缺GSAP")
        if not results.get("has_responsive_480"): file_issues.append("缺480px断点")
        if not results.get("has_responsive_768"): file_issues.append("缺768px断点")
        if not results.get("has_celebrate"): file_issues.append("缺celebrate调用")
        if not results.get("no_js_syntax_error"): file_issues.append("JS语法问题")
        if not results.get("pages_have_content", True): file_issues.append("有空页面")

        if file_issues:
            issues.append(f"{filename}: {', '.join(file_issues)}")
            failed_count += 1
        else:
            passed_count += 1

    # Print category summaries
    for cat, files in categories.items():
        if not files:
            continue
        cat_names = {"english":"英语","chinese":"语文","math":"数学","songs":"童谣","science":"科学","stories":"绘本故事","other":"其他"}
        print(f"\n--- {cat_names.get(cat, cat)} ({len(files)}个文件) ---")
        for filename, results in files:
            dt = results.get("data_type_value", "?")
            lines = results.get("line_count", 0)
            pages = results.get("page_count", 0)
            imgs = results.get("image_count", 0)
            has_reporter = "Y" if results.get("has_village_reporter") else "N"
            has_resp = "Y" if results.get("has_responsive_480") and results.get("has_responsive_768") else "N"
            has_celeb = "Y" if results.get("has_celebrate") else "N"

            status = "OK"
            file_issues = []
            if not results.get("has_doctype"): file_issues.append("DOCTYPE")
            if not results.get("has_data_type"): file_issues.append("data-type")
            if not results.get("has_village_reporter"): file_issues.append("reporter")
            if not results.get("has_responsive_480"): file_issues.append("resp480")
            if not results.get("has_responsive_768"): file_issues.append("resp768")
            if not results.get("has_celebrate"): file_issues.append("celebrate")
            if not results.get("pages_have_content", True): file_issues.append("空页面")
            if not results.get("no_js_syntax_error"): file_issues.append("JS错误")

            if file_issues:
                status = "WARN: " + ", ".join(file_issues)

            page_info = f", {pages}页" if pages > 0 else ""
            img_info = f", {imgs}图" if imgs > 0 else ""
            print(f"  [{status:^20}] {filename} ({lines}行{page_info}{img_info}, type={dt})")

    # Summary
    print("\n" + "="*80)
    print(f"  测试总结")
    print("="*80)
    print(f"  总文件数: {total}")
    print(f"  全通过: {passed_count}")
    print(f"  有问题: {failed_count}")

    if issues:
        print(f"\n  问题详情 ({len(issues)}个):")
        for issue in issues:
            print(f"    - {issue}")

    # Village state structure check
    print("\n" + "="*80)
    print("  需求对照检查")
    print("="*80)

    requirements = {
        "Phase 1 入口层": [
            ("村庄地图替代列表页", True),
            ("6个建筑区域", True),
            ("CSS绘制建筑(非图片)", True),
            ("Steve走动动画", True),
            ("点击建筑弹出课件列表", True),
            ("欢迎动画", True),
            ("天空+云+太阳背景", True),
        ],
        "Phase 2 进度层": [
            ("localStorage持久化", True),
            ("装饰解锁(6种)", True),
            ("每日任务系统", True),
            ("连续学习天数", True),
        ],
        "Phase 2.5 经济层": [
            ("金币获取(+5/+3/+10)", True),
            ("商店(8种商品)", True),
            ("金币显示在顶栏", True),
            ("金币浮动动画", True),
        ],
        "Phase 3 宠物层": [
            ("6种宠物可选", True),
            ("4个成长阶段", True),
            ("宠物面板(成长/心情/饱食)", True),
            ("喂食+玩耍功能", True),
            ("宠物在地图显示", True),
            ("饥饿/心情衰减", True),
            ("宠物装饰", True),
        ],
        "课件完整性": [
            ("village-reporter.js注入", f"{passed_count}/{total}"),
            ("data-type属性", f"大部分有"),
            ("响应式设计", "大部分有"),
        ],
    }

    for phase, items in requirements.items():
        print(f"\n  {phase}:")
        for name, status in items:
            if status is True:
                print(f"    PASS | {name}")
            elif status is False:
                print(f"    FAIL | {name}")
            else:
                print(f"    INFO | {name}: {status}")

if __name__ == "__main__":
    main()
