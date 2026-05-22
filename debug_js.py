#!/usr/bin/env python3
"""Debug JS syntax errors in generated courseware"""
import re, sys

with open(sys.argv[1]) as f:
    c = f.read()

m = re.search(r'<script>(.*?)</script>', c, re.DOTALL)
if not m:
    print("No script tag found")
    sys.exit(1)

js = m.group(1)
print(f"Script length: {len(js)}")

# Check quote balance
sq = len(re.findall(r"(?<!\\)'", js))
dq = len(re.findall(r'(?<!\\)"', js))
bt = js.count('`')
print(f"Single quotes: {sq} (even: {sq%2==0})")
print(f"Double quotes: {dq} (even: {dq%2==0})")
print(f"Backticks: {bt} (should be 0: {bt==0})")

# Find the error around line numbers  
lines = js.split('\n')
for i, line in enumerate(lines):
    # Look for unbalanced quotes
    sq_count = len(re.findall(r"(?<!\\)'", line))
    if sq_count % 2 != 0:
        print(f"  SINGLE QUOTE ISSUE line {i+1}: {line[:100]}")
    dq_count = len(re.findall(r'(?<!\\)"', line))
    if dq_count % 2 != 0:
        print(f"  DOUBLE QUOTE ISSUE line {i+1}: {line[:100]}")

# Check for common issues
check_funcs = ['renderInteractGame', 'setupInteractDrag', 'renderPage', 'speakPage', 'checkQuiz']
for func in check_funcs:
    idx = js.find(f'function {func}')
    if idx >= 0:
        line_no = js[:idx].count('\n') + 1
        print(f"  function {func} found at line {line_no}")
    else:
        print(f"  MISSING function {func}!")

# Check for specific patterns
for pat in ['\\'', "\"'", '\\"']:
    cnt = js.count(pat)
    if cnt > 0:
        print(f"  Escaped quote pattern '{pat}': {cnt}")

print("Done")
