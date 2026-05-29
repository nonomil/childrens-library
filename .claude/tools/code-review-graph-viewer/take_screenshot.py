# -*- coding: utf-8 -*-
"""Take screenshot of the viewer in browser."""
import os
from playwright.sync_api import sync_playwright

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "扫描代码库知识图谱Graphify", "screenshots")
os.makedirs(OUT, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.goto("http://localhost:3334")
    page.wait_for_timeout(5000)  # wait for graph to render

    path = os.path.join(OUT, "08-code-graph-viewer.png")
    page.screenshot(path=path, full_page=False)
    print(f"OK: {os.path.basename(path)} ({os.path.getsize(path)//1024}KB)")

    # Click a node in the tree
    tree_nodes = page.query_selector_all(".tree-node")
    if tree_nodes:
        tree_nodes[5].click()
        page.wait_for_timeout(1000)
        path2 = os.path.join(OUT, "09-code-graph-viewer-detail.png")
        page.screenshot(path=path2, full_page=False)
        print(f"OK: {os.path.basename(path2)} ({os.path.getsize(path2)//1024}KB)")

    browser.close()
print("Done")
