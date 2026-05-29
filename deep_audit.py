"""
深度课件审查脚本 - 逐文件逐页审查每个HTML课件的元素、内容、图片、交互
"""
import os, re, sys, io, json, html
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

COURSEWARE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Prj", "childrens-library", "courseware")

def extract_pages_from_js(content):
    """Extract page data from JS pages array in story/quiz files"""
    pages = []
    # Find the pages array
    pages_match = re.search(r'const\s+pages\s*=\s*\[(.*?)\];', content, re.DOTALL)
    if not pages_match:
        return pages

    pages_str = pages_match.group(1)

    # Split by page objects - look for { title: pattern
    # Each page is: { title: '...', render: `...` }
    page_pattern = re.finditer(r"\{\s*title:\s*'([^']*)',\s*render:\s*`([\s\S]*?)`\s*\}", pages_str)

    for m in page_pattern:
        title = m.group(1)
        render = m.group(2)
        pages.append({'title': title, 'render': render})

    return pages


def analyze_page_render(render_html, page_idx, filename):
    """Analyze a single page's render HTML for issues"""
    issues = []
    info = {}

    # Check for images
    img_tags = re.findall(r'<img[^>]+>', render_html)
    img_srcs = re.findall(r'src="([^"]+)"', render_html)
    info['images'] = len(img_tags)
    info['image_srcs'] = img_srcs

    # Check for broken image patterns
    for src in img_srcs:
        if 'github' in src and 'raw.githubusercontent' not in src:
            issues.append(f"图片URL非raw格式: {src[:60]}")
        if src.startswith('http') and '//' in src[8:]:
            pass  # OK
        elif not src.startswith('http') and not src.startswith('data:'):
            issues.append(f"图片URL可能无效: {src[:60]}")

    # Check for onerror handler on images
    for tag in img_tags:
        if 'onerror' not in tag:
            issues.append(f"图片缺少onerror降级处理")

    # Check for text content
    text_content = re.sub(r'<[^>]+>', '', render_html).strip()
    text_content = re.sub(r'\s+', ' ', text_content)
    info['text_length'] = len(text_content)
    info['text_preview'] = text_content[:100]

    if len(text_content) < 5 and page_idx > 0:
        issues.append("页面文字内容过少(<5字符)")

    # Check for empty render
    if len(render_html.strip()) < 20:
        issues.append("页面render内容为空或极短")

    # Check for broken template literals (unclosed ${})
    if render_html.count('${') != render_html.count('}'):
        # This is approximate
        pass

    # Check for Chinese text presence (for bilingual content)
    has_chinese = bool(re.search(r'[一-鿿]', text_content))
    has_english = bool(re.search(r'[a-zA-Z]{3,}', text_content))
    info['has_chinese'] = has_chinese
    info['has_english'] = has_english

    # Check for buttons
    buttons = re.findall(r'<button[^>]*>(.*?)</button>', render_html, re.DOTALL)
    info['buttons'] = len(buttons)

    # Check for quiz elements
    quiz_items = re.findall(r'quiz|question|answer|选择|答案|题目', render_html, re.IGNORECASE)
    info['has_quiz'] = len(quiz_items) > 0

    # Check for speak/朗读 button
    info['has_speak'] = 'speak' in render_html.lower() or '朗读' in render_html

    return info, issues


def audit_story_file(filepath, content):
    """Audit a story-type file page by page"""
    filename = os.path.basename(filepath)
    results = {
        'filename': filename,
        'type': 'story',
        'total_pages': 0,
        'pages': [],
        'global_issues': [],
        'total_images': 0,
        'broken_images': 0,
        'empty_pages': 0,
    }

    pages = extract_pages_from_js(content)
    results['total_pages'] = len(pages)

    if len(pages) == 0:
        results['global_issues'].append("无法解析pages数组")
        return results

    for idx, page in enumerate(pages):
        page_result = {
            'index': idx,
            'title': page['title'],
            'issues': [],
            'info': {},
        }

        info, issues = analyze_page_render(page['render'], idx, filename)
        page_result['info'] = info
        page_result['issues'] = issues

        # Track stats
        results['total_images'] += info.get('images', 0)
        if info.get('text_length', 0) < 5:
            results['empty_pages'] += 1

        # Check image URLs reachability (just check format, not actual HTTP)
        for src in info.get('image_srcs', []):
            if 'raw.githubusercontent.com' in src:
                # Check URL format
                parts = src.split('/')
                if 'stories' in parts and 'images' in parts:
                    pass  # Good format
                else:
                    page_result['issues'].append(f"GitHub图片路径格式异常: {src[:80]}")

        # Verify last page has celebration
        if idx == len(pages) - 1:
            if 'celebrate' not in content.lower() and 'celebration' not in page['render'].lower():
                page_result['issues'].append("最后一页缺少庆祝/完成元素")

        results['pages'].append(page_result)

    return results


def audit_quiz_file(filepath, content):
    """Audit a quiz-type file"""
    filename = os.path.basename(filepath)
    results = {
        'filename': filename,
        'type': 'quiz',
        'total_pages': 0,
        'pages': [],
        'global_issues': [],
        'total_images': 0,
        'empty_pages': 0,
    }

    pages = extract_pages_from_js(content)
    results['total_pages'] = len(pages)

    if len(pages) == 0:
        # Maybe it uses a different structure - check for slide/section divs
        slides = re.findall(r'<div[^>]*class="[^"]*slide[^"]*"[^>]*>(.*?)</div>\s*(?=<div[^>]*class="[^"]*slide|$)', content, re.DOTALL)
        if slides:
            results['total_pages'] = len(slides)
            results['global_issues'].append(f"使用slide结构而非pages数组, {len(slides)}个slide")
        else:
            results['global_issues'].append("无法解析页面结构")
        return results

    for idx, page in enumerate(pages):
        page_result = {
            'index': idx,
            'title': page['title'],
            'issues': [],
            'info': {},
        }

        info, issues = analyze_page_render(page['render'], idx, filename)
        page_result['info'] = info
        page_result['issues'] = issues

        results['total_images'] += info.get('images', 0)
        if info.get('text_length', 0) < 5:
            results['empty_pages'] += 1

        results['pages'].append(page_result)

    return results


def audit_slide_file(filepath, content):
    """Audit files using slide-based structure (not pages array)"""
    filename = os.path.basename(filepath)
    results = {
        'filename': filename,
        'type': 'slide',
        'total_pages': 0,
        'pages': [],
        'global_issues': [],
        'total_images': 0,
        'empty_pages': 0,
    }

    # Extract slides from HTML
    slides = re.findall(r'<div[^>]*class="[^"]*slide[^"]*"[^>]*>(.*?)</div>', content, re.DOTALL)
    if not slides:
        # Try sections
        slides = re.findall(r'<section[^>]*>(.*?)</section>', content, re.DOTALL)

    results['total_pages'] = len(slides)

    for idx, slide in enumerate(slides):
        page_result = {
            'index': idx,
            'title': f'slide-{idx}',
            'issues': [],
            'info': {},
        }

        info, issues = analyze_page_render(slide, idx, filename)
        page_result['info'] = info
        page_result['issues'] = issues

        results['total_images'] += info.get('images', 0)
        if info.get('text_length', 0) < 5:
            results['empty_pages'] += 1

        results['pages'].append(page_result)

    return results


def audit_file(filepath):
    """Audit a single HTML file"""
    filename = os.path.basename(filepath)

    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        return {'filename': filename, 'error': str(e)}

    # Detect file type
    data_type_match = re.search(r'data-type="([^"]+)"', content)
    data_type = data_type_match.group(1) if data_type_match else 'unknown'

    # Choose audit method based on type
    if data_type == 'story' or 'pages' in content and 'render' in content:
        return audit_story_file(filepath, content)
    elif data_type in ('quiz', 'lesson', 'phonics', 'song', 'nursery'):
        # Check if it has pages array or slides
        if 'const pages' in content:
            return audit_quiz_file(filepath, content)
        else:
            return audit_slide_file(filepath, content)
    else:
        # Generic: try pages first, then slides
        if 'const pages' in content:
            return audit_quiz_file(filepath, content)
        else:
            return audit_slide_file(filepath, content)


def main():
    print("=" * 80)
    print("  深度课件审查 - 逐页元素检查")
    print("=" * 80)

    html_files = sorted([f for f in os.listdir(COURSEWARE_DIR) if f.endswith('.html')])

    total_files = len(html_files)
    total_pages = 0
    total_issues = 0
    total_images = 0
    total_empty = 0

    all_results = []
    files_with_issues = []

    for filename in html_files:
        filepath = os.path.join(COURSEWARE_DIR, filename)
        result = audit_file(filepath)
        all_results.append(result)

        if 'error' in result:
            print(f"\n  ERROR | {filename}: {result['error']}")
            files_with_issues.append((filename, [result['error']]))
            total_issues += 1
            continue

        pages_count = result.get('total_pages', 0)
        total_pages += pages_count
        total_images += result.get('total_images', 0)
        total_empty += result.get('empty_pages', 0)

        # Collect issues
        file_issues = list(result.get('global_issues', []))
        for page in result.get('pages', []):
            for issue in page.get('issues', []):
                file_issues.append(f"Page {page['index']}({page.get('title','?')}): {issue}")

        if file_issues:
            total_issues += len(file_issues)
            files_with_issues.append((filename, file_issues))

        # Print per-file summary
        dt = result.get('type', '?')
        imgs = result.get('total_images', 0)
        empty = result.get('empty_pages', 0)
        status = "OK" if not file_issues else f"WARN({len(file_issues)})"
        print(f"  [{status:^12}] {filename} — {pages_count}页, {imgs}图, type={dt}" +
              (f", {empty}空页" if empty else ""))

    # Summary
    print("\n" + "=" * 80)
    print(f"  审查总结")
    print("=" * 80)
    print(f"  总文件数: {total_files}")
    print(f"  总页面数: {total_pages}")
    print(f"  总图片数: {total_images}")
    print(f"  空页面数: {total_empty}")
    print(f"  问题文件: {len(files_with_issues)}")
    print(f"  问题总数: {total_issues}")

    if files_with_issues:
        print(f"\n  问题详情:")
        for fname, issues in files_with_issues:
            print(f"\n  --- {fname} ---")
            for issue in issues:
                print(f"    - {issue}")

    # Check image URL reachability (batch check with HEAD requests)
    print("\n" + "=" * 80)
    print("  图片链接抽查")
    print("=" * 80)

    all_image_urls = set()
    for result in all_results:
        if 'error' in result:
            continue
        for page in result.get('pages', []):
            for src in page.get('info', {}).get('image_srcs', []):
                if src.startswith('http'):
                    all_image_urls.add(src)

    print(f"  总共 {len(all_image_urls)} 个唯一图片URL")

    # Sample check a few
    import urllib.request
    checked = 0
    broken = 0
    for url in sorted(all_image_urls)[:20]:
        try:
            req = urllib.request.Request(url, method='HEAD')
            with urllib.request.urlopen(req, timeout=5) as r:
                status = r.status
            checked += 1
            if status != 200:
                broken += 1
                print(f"    BROKEN {status}: {url[:80]}")
        except Exception as e:
            checked += 1
            broken += 1
            print(f"    ERROR: {url[:80]} -> {e}")

    print(f"  抽查 {checked} 个URL, {broken} 个不可达")


if __name__ == "__main__":
    main()
