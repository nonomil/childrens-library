"""
差异修复验收脚本 — 统一验证128课件与规范的对齐状态
用法：python verify_gap_fix.py [--check all|css-theme|onerror|unlock|pet-food]
"""
import os, re, sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

COURSEWARE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "Prj", "childrens-library", "courseware")
VILLAGE_JS = os.path.join(COURSEWARE_DIR, "shared", "village.js")
COURSEWARE_CSS = os.path.join(COURSEWARE_DIR, "shared", "courseware.css")


def get_all_html_files():
    """获取所有HTML课件文件"""
    return sorted([f for f in os.listdir(COURSEWARE_DIR)
                   if f.endswith('.html') and f != 'stories-index.html'])


def check_css_theme():
    """检查CSS主题变量是否定义并被引用"""
    results = {'total': 0, 'defined': 0, 'used': 0, 'details': []}

    # 检查 courseware.css 是否定义了 [data-type] 变量
    css_path = COURSEWARE_CSS
    if os.path.exists(css_path):
        with open(css_path, 'r', encoding='utf-8', errors='replace') as f:
            css_content = f.read()
        for dt in ['nursery', 'story', 'science', 'courseware']:
            if f'data-type="{dt}"' in css_content or f"data-type='{dt}'" in css_content:
                results['defined'] += 1
                results['details'].append(f"CSS定义: [{dt}] ✓")
            else:
                results['details'].append(f"CSS定义: [{dt}] ✗ 缺失")

    # 检查各文件是否引用了 var(--bg)
    html_files = get_all_html_files()
    results['total'] = len(html_files)
    for fname in html_files:
        fpath = os.path.join(COURSEWARE_DIR, fname)
        try:
            with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            if 'var(--bg)' in content or 'var(--primary)' in content:
                results['used'] += 1
        except Exception:
            pass

    return results


def check_onerror():
    """检查所有img标签是否有onerror降级"""
    results = {'total': 0, 'with_onerror': 0, 'without_onerror': 0, 'no_images': 0, 'details': []}
    html_files = get_all_html_files()
    results['total'] = len(html_files)

    for fname in html_files:
        fpath = os.path.join(COURSEWARE_DIR, fname)
        try:
            with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            img_tags = re.findall(r'<img[^>]*>', content)
            if not img_tags:
                results['no_images'] += 1
                continue
            has_onerror = all('onerror' in tag for tag in img_tags)
            if has_onerror:
                results['with_onerror'] += 1
            else:
                results['without_onerror'] += 1
                results['details'].append(f"{fname}: {len(img_tags)} imgs, missing onerror")
        except Exception:
            pass

    return results


def check_unlock():
    """检查解锁逻辑：数学需英语>=3，科学需总完成>=5"""
    results = {'pass': False, 'details': []}
    if not os.path.exists(VILLAGE_JS):
        results['details'].append("village.js 不存在")
        return results

    with open(VILLAGE_JS, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # 检查 ZONE_CONFIG 中 math 的 unlockRequirement
    math_req = re.search(r"math:\s*\{[^}]*unlockRequirement:\s*(\d+)", content, re.DOTALL)
    science_req = re.search(r"science:\s*\{[^}]*unlockRequirement:\s*(\d+)", content, re.DOTALL)

    if math_req:
        val = int(math_req.group(1))
        results['details'].append(f"math unlockRequirement: {val} (期望: 3)")
    if science_req:
        val = int(science_req.group(1))
        results['details'].append(f"science unlockRequirement: {val} (期望: 5)")

    # 检查是否有 requiredZone 字段
    has_required_zone = 'requiredZone' in content
    results['details'].append(f"requiredZone 字段: {'存在' if has_required_zone else '缺失'}")

    # 检查解锁逻辑是否支持特定zone检查
    if has_required_zone and math_req and int(math_req.group(1)) == 3:
        results['pass'] = True
    elif not has_required_zone:
        results['details'].append("当前使用总完成数检查，需改为特定zone检查")

    return results


def check_pet_food():
    """检查宠物是否有偏好食物字段"""
    results = {'pass': False, 'total_pets': 0, 'with_preference': 0, 'details': []}
    if not os.path.exists(VILLAGE_JS):
        results['details'].append("village.js 不存在")
        return results

    with open(VILLAGE_JS, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # 检查 PET_TYPES 是否有 preferredFood
    pet_types_match = re.search(r'var PET_TYPES\s*=\s*\[(.*?)\];', content, re.DOTALL)
    if pet_types_match:
        pets_str = pet_types_match.group(1)
        pets = re.findall(r"\{[^}]+\}", pets_str)
        results['total_pets'] = len(pets)
        for pet in pets:
            if 'preferredFood' in pet:
                results['with_preference'] += 1
                name = re.search(r"name:\s*'([^']+)'", pet)
                food = re.search(r"preferredFood:\s*'([^']+)'", pet)
                if name and food:
                    results['details'].append(f"{name.group(1)}: {food.group(1)} ✓")
            else:
                name = re.search(r"name:\s*'([^']+)'", pet)
                if name:
                    results['details'].append(f"{name.group(1)}: 无偏好食物 ✗")

    results['pass'] = (results['with_preference'] == results['total_pets'] and results['total_pets'] > 0)
    return results


def main():
    checks = ['all']
    if len(sys.argv) > 2 and sys.argv[1] == '--check':
        checks = [sys.argv[2]]

    print("=" * 60)
    print("  差异修复验收脚本 (verify_gap_fix.py)")
    print("=" * 60)

    if 'all' in checks or 'css-theme' in checks:
        print("\n[CSS-THEME] CSS主题变量检查")
        r = check_css_theme()
        print(f"  定义: {r['defined']}/4 类型")
        print(f"  引用: {r['used']}/{r['total']} 文件使用 var(--bg)")
        for d in r['details']:
            print(f"    {d}")

    if 'all' in checks or 'onerror' in checks:
        print("\n[ONERROR] 图片降级检查")
        r = check_onerror()
        print(f"  有onerror: {r['with_onerror']}/{r['total']}")
        print(f"  缺onerror: {r['without_onerror']}/{r['total']}")
        print(f"  无图片: {r['no_images']}/{r['total']}")
        for d in r['details'][:10]:
            print(f"    {d}")

    if 'all' in checks or 'unlock' in checks:
        print("\n[UNLOCK] 解锁逻辑检查")
        r = check_unlock()
        print(f"  结果: {'PASS' if r['pass'] else 'NEEDS_FIX'}")
        for d in r['details']:
            print(f"    {d}")

    if 'all' in checks or 'pet-food' in checks:
        print("\n[PET-FOOD] 宠物偏好食物检查")
        r = check_pet_food()
        print(f"  结果: {'PASS' if r['pass'] else 'NEEDS_FIX'}")
        print(f"  有偏好: {r['with_preference']}/{r['total_pets']}")
        for d in r['details']:
            print(f"    {d}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
