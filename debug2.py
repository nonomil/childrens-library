with open('/home/deploy/childrens-library/docs/courseware/wheels-on-bus.html') as f:
    content = f.read()

idx = content.find('pickLetter(')
snippet = content[idx:idx+150]
# Show repr
print(repr(snippet))
print()
# Count backslashes
for i, c in enumerate(snippet):
    if c == '\\':
        print(f'  pos {i} in snippet: backslash')
