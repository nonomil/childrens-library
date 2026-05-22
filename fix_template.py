#!/usr/bin/env python3
"""Final fix - remove all inline on* handlers from tiles"""
import os, re

BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "template_nursery_v3_fixed.html"), "r") as f:
    tpl = f.read()

# Fix the tiles line - remove all inline on* handlers, use pure data-attrs
old = 'const tiles=letters.map(function(l){return \'<div class="letter-tile" draggable="true" data-idx="\'+idx+\'" data-letter="\'+l+\'" onclick="pickTile(this)" ondragstart="onDragStart(event,\'+idx+\',\'"+l+"\')\" ondragend="onDragEnd(event)">\'+l+\'</div>\';}).join(\'\');'
new = 'const tiles=letters.map(function(l){return \'<div class="letter-tile" draggable="true" data-idx="\'+idx+\'" data-letter="\'+l+\'">\'+l+\'</div>\';}).join(\'\');'

if old in tpl:
    tpl = tpl.replace(old, new)
    print("Fixed tiles line")
else:
    print("Tiles line NOT FOUND, looking...")
    idx = tpl.find("data-letter")
    print(f"Found data-letter at {idx}")
    print(tpl[max(0,idx-50):idx+150])

# Add event delegation for drag - listen for dragstart on .letter-tile
old_del = '''// Event delegation for tile clicks
document.addEventListener('click',function(e){'''
new_del = '''// Event delegation for drag and tile clicks
document.addEventListener('dragstart',function(e){var tile=e.target.closest('.letter-tile');if(tile&&tile.dataset.idx!==undefined){var idx=parseInt(tile.dataset.idx);var letter=tile.dataset.letter;dragData={idx,letter,el:tile};tile.classList.add('dragging');e.dataTransfer.effectAllowed='move';e.dataTransfer.setData('text/plain',idx+':'+letter);}});
document.addEventListener('dragend',function(e){var tile=e.target.closest('.letter-tile');if(tile){tile.classList.remove('dragging');}document.querySelectorAll('.word-slot.drag-over').forEach(function(s){s.classList.remove('drag-over');});dragData=null;});
document.addEventListener('click',function(e){'''

if old_del in tpl:
    tpl = tpl.replace(old_del, new_del)
    print("Added drag event delegation")
else:
    print("Event delegation section not found")

with open(os.path.join(BASE, "template_nursery_v3_fixed.html"), "w") as f:
    f.write(tpl)

print("Template saved. Verifying...")
# Verify no more inline on* in tiles lines
if 'ondragstart' in tpl.split("data-letter")[-1].split("</div>'")[0]:
    print("WARNING: ondragstart still present!")
else:
    print("OK: No inline ondragstart in tiles")
