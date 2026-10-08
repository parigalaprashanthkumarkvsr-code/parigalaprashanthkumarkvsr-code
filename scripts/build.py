#!/usr/bin/env python3
"""Build standalone GitHub-renderable SVG panels from the original vector source."""
from pathlib import Path
from copy import deepcopy
import re
from lxml import etree

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'assets/source/original.svg'
OUT = ROOT / 'assets/svg'
NS = 'http://www.w3.org/2000/svg'
Q = lambda name: '{%s}%s' % (NS, name)

PANELS = [
    ('featured-handle', 16, 575, 176),
    ('builder-index', 17, 315, 322),
    ('visual-identity', 18, 482, 510),
    ('about-me', 19, 423, 245),
    ('current-focus', 20, 423, 249),
    ('featured-projects', 21, 597, 327),
    ('tech-stack', 22, 299, 535),
    ('learning-log', 23, 597, 197),
    ('mission', 24, 908, 140),
]

def clean(element):
    """Make static SVG reliable in GitHub's image sanitizer; preserve visual content."""
    for node in list(element.iter()):
        local = etree.QName(node).localname
        if local in {'animate','animateTransform','animateMotion','set','script','foreignObject'}:
            if node.getparent() is not None:
                node.getparent().remove(node)
        elif node.get('opacity') == '0':
            del node.attrib['opacity']
    return element

def document(width, height, defs):
    root = etree.Element(Q('svg'), nsmap={None:NS})
    root.set('viewBox', f'0 0 {width} {height}')
    root.set('width', str(width)); root.set('height', str(height))
    root.set('role', 'img')
    root.append(deepcopy(defs))
    bg = etree.SubElement(root, Q('rect'), width=str(width), height=str(height), fill='#050b1c')
    return root

def dump(root, path):
    path.write_bytes(etree.tostring(root, encoding='utf-8', xml_declaration=True, pretty_print=True))
    etree.parse(str(path))

original = etree.parse(str(SOURCE)).getroot()
defs = original.find(Q('defs'))
OUT.mkdir(exist_ok=True,parents=True)

# Header uses real original heading and introductory text, with a dedicated safe viewBox.
header = document(940, 185, defs)
header.append(etree.Element(Q('rect'), x='0',y='0',width='940',height='3',fill='#5b73ff'))
for index in [11,12,13,14,15]:
    header.append(deepcopy(original[index]))
for t in header.iter(Q('text')):
    if t.get('class') == 'name':
        t.set('font-size','37')
        t.attrib.pop('textLength',None)
        t.attrib.pop('lengthAdjust',None)
# Parent art was positioned against a 941px canvas; header keeps original x positions.
clean(header)
dump(header, OUT / 'header.svg')

for filename, index, width, height in PANELS:
    svg = document(width + 24, height + 24, defs)
    layer = etree.SubElement(svg, Q('g'), transform='translate(12,12)')
    # Top-level panel container includes an outer animation wrapper.
    outer = deepcopy(original[index])
    panel = outer[0]
    panel_copy = deepcopy(panel)
    panel_copy.set("transform", "translate(0,0)")
    layer.append(panel_copy)
    clean(svg)
    # Correct source's handle spelling, matching the visible @username.
    if filename == 'featured-handle':
        for t in svg.iter(Q('text')):
            if t.text and '#parigalaprashanthkumkvsr-code' in t.text:
                t.text = '#parigalaprashanthkumarkvsr-code'
                # Keep within the original 548px terminal strip.
                t.set('font-size','20')
                t.attrib.pop('textLength',None)
                t.attrib.pop('lengthAdjust',None)
    if filename == 'builder-index':
        # Omit self-awarded score and fake progress bar; radar is decorative, not measured.
        for t in list(svg.iter(Q('text'))):
            val=''.join(t.itertext()).strip()
            if val in {'94.8','/100','LEARNER INDEX'}:
                t.getparent().remove(t)
        for n in list(svg.iter(Q('rect'))):
            if n.get('y')=='285' and n.get('width') in {'98','92.9'}:
                n.getparent().remove(n)
        label=etree.SubElement(svg.find(Q('g')).find(Q('g')),Q('text'),x='159',y='290',**{'text-anchor':'middle','font-size':'12','class':'mut'})
        label.text='FOCUS MAP / ILLUSTRATIVE'
    if filename == 'featured-projects':
        # Display no speculative GitHub stars. README hyperlinks are explicit and editable.
        for t in svg.iter(Q('text')):
            if (t.text or '').strip() in {'128','86','64','102','45','38'}:
                t.text='—'
        # Avoid representing numerical stars as verified counts.
    dump(svg, OUT / f'{filename}.svg')

# Combined portrait-like image for users who prefer one image (individual panels are primary).
full = deepcopy(original)
for n in list(full):
    if etree.QName(n).localname == 'metadata': full.remove(n)
clean(full)
for t in full.iter(Q('text')):
    if t.text and '#parigalaprashanthkumkvsr-code' in t.text:
        t.text=t.text.replace('#parigalaprashanthkumkvsr-code','#parigalaprashanthkumarkvsr-code')
    if (t.text or '').strip() in {'128','86','64','102','45','38'}: t.text='—'
    if (t.text or '').strip() in {'94.8','/100','LEARNER INDEX'}: t.text=''
dump(full,OUT/'full-profile.svg')
print('Generated',len(PANELS)+2,'standalone SVG files')
