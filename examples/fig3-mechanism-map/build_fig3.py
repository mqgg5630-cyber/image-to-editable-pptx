#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build a source-faithful editable reconstruction of fig3_mechanism_map.png
(1024x1536) as:
  1. PageIR JSON  -> compiled to PPTX with the image-to-editable-pptx skill
  2. SVG          -> same geometry, fully editable vector
One object model, two emitters.
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))

W, H = 1024, 1536

# ---------------- palette (sampled from source) ----------------
RED      = '#A02D14'   # pathogen factor text / icons
RED_ICON = '#9B3521'   # rods, block arrows
TEAL     = '#0C646D'   # host protein text
TEAL_AR  = '#0D5961'   # host arrows
TEAL_LT  = '#6E9BA6'   # membrane mesh
TEAL_FILL= '#D5E7E8'   # AChE oval fill
PURPLE   = '#381F61'   # box title / pathology text
PURPLE_D = '#2B1459'   # pathology outcome text
PURPLE_BR= '#492D6B'   # lavender box borders
PURPLE_AR= '#83669B'   # big box-to-box arrow
INK      = '#1C1C1C'   # black text
GRAY     = '#3E4A4A'   # legend text
LAVENDER = '#F6F3F8'   # box fill
AD_FILL  = '#F3F1F6'
DOTGRAY  = '#3A3A3A'   # dotted connectors
FONT     = 'Comic Sans MS'

# ---------------- helpers ----------------
objects = []   # PageIR objects
sid = [0]
def oid(p):
    sid[0] += 1
    return f'{p}-{sid[0]:03d}'

def text(x, y, w, h, t, color=INK, size=13, bold=False, align='left', valign='top', z=30):
    objects.append(dict(id=oid('t'), type='text', bbox=[x, y, w, h], text=t, z=z,
        style=dict(font_face=FONT, font_size_pt=size, bold=bold, color=color,
                   align=align, valign=valign, margin_pt=0)))

def shape(kind, x, y, w, h, fill=None, line=None, lw=1.5, dash=None, z=10, trans=None):
    st = dict(fill=fill, line=line, line_width_pt=lw)
    if dash: st['dash'] = dash
    if trans is not None: st['fill_transparency'] = trans
    objects.append(dict(id=oid('s'), type=kind, bbox=[x, y, w, h], z=z, style=st))

def arrow(x1, y1, x2, y2, color=INK, w=2.0, dash=None, head=True, tail=False, z=15):
    st = dict(color=color, width_pt=w,
              start_arrow='triangle' if tail else 'none',
              end_arrow='triangle' if head else 'none')
    if dash: st['dash'] = dash
    objects.append(dict(id=oid('a'), type='line', points=[x1, y1, x2, y2], z=z, style=st))

# =========================================================================
# TITLE + big bacterium ellipse
# =========================================================================
text(302, 6, 462, 42, 'Porphyromonas gingivalis', RED, 23, align='center')
shape('ellipse', 302, 56, 462, 119, fill=None, line=RED, lw=3.0)   # sketchy outer ring
shape('ellipse', 322, 74, 348, 86, fill='#BF5D4A', line=RED, lw=2.5)  # solid body
for sx, sy in ((400, 130), (460, 150), (520, 142), (580, 155)):  # interior speckles
    shape('ellipse', sx, sy, 13, 9, fill=RED, line=None)

# dashed arrows ellipse -> three factor clusters
arrow(247, 180, 247, 212, DOTGRAY, 2.0, 'dash')
arrow(494, 178, 494, 218, DOTGRAY, 2.0, 'dash')
arrow(769, 180, 769, 212, DOTGRAY, 2.0, 'dash')

# ---------------- LPS cluster (left) ----------------
shape('round_rect', 198, 206, 15, 92, fill=RED_ICON, line=None)          # membrane rod
shape('rect', 221, 231, 82, 9, fill=RED_ICON, line=None)                 # lipid-A bar
for lx in (222, 240, 258, 273, 288, 300):                                # acyl tails
    arrow(lx, 240, lx, 296, RED_ICON, 1.75, head=False)
text(196, 304, 62, 26, 'LPS', RED, 15, align='center')
text(148, 332, 172, 24, '(lipopolysaccharide)', INK, 11.5, align='center')

# ---------------- Gingipains cluster (center) ----------------
text(436, 218, 104, 28, 'Gingipains', RED, 15, align='center')
for rx, rw in ((418, 46), (482, 48), (546, 42)):
    shape('round_rect', rx, 266, rw, 47, fill=RED_ICON, line=None)
text(410, 320, 46, 24, 'Kgp', INK, 11.5, align='center')
text(470, 320, 52, 24, 'RgpA', INK, 11.5, align='center')
text(524, 320, 52, 24, 'RgpB', INK, 11.5, align='center')

# ---------------- OMVs cluster (right) ----------------
shape('ellipse', 685, 234, 60, 60, fill=None, line=RED_ICON, lw=3.0)
shape('ellipse', 748, 207, 50, 50, fill=None, line=RED_ICON, lw=3.0)
shape('ellipse', 781, 258, 47, 48, fill=None, line=RED_ICON, lw=3.0)
for dx, dy in ((700, 250), (716, 264), (704, 276), (720, 244), (710, 258)):
    shape('ellipse', dx, dy, 6, 6, fill=RED_ICON, line=None)
text(721, 306, 62, 26, 'OMVs', RED, 15, align='center')
text(654, 332, 186, 26, '(outer membrane vesicles)', INK, 11.5, align='center')

# =========================================================================
# Bus under clusters -> three lavender effect boxes
# =========================================================================
for bx in (245, 500, 793):
    arrow(bx, 352, bx, 376, DOTGRAY, 1.75, 'dot', head=False)            # cluster -> bus
arrow(165, 378, 840, 378, DOTGRAY, 1.75, 'dot', head=False)              # bus
for bx in (165, 512, 795):
    arrow(bx, 380, bx, 408, DOTGRAY, 1.75, 'dot')                        # bus -> boxes

# ---------------- three effect boxes ----------------
shape('round_rect', 48, 412, 243, 82, fill=LAVENDER, line=PURPLE_BR, lw=2.0, dash='dot')
shape('round_rect', 372, 412, 259, 82, fill=LAVENDER, line=PURPLE_BR, lw=2.0, dash='dot')
shape('round_rect', 680, 412, 311, 81, fill=LAVENDER, line=PURPLE_BR, lw=2.0, dash='dot')
for ix in (56, 383, 687):                                                # spiral icons
    shape('ellipse', ix, 424, 27, 27, fill=None, line='#4A2F6F', lw=2.25)
text(96, 421, 180, 26, 'Tau proteolysis', PURPLE, 15)
text(92, 447, 190, 26, 'and NFT formation', PURPLE, 15)
text(420, 421, 180, 26, 'APP processing', PURPLE, 15)
text(416, 447, 190, 26, 'and Aβ deposition', PURPLE, 15)
text(716, 419, 240, 26, 'AChE-PAS nucleation of Aβ', PURPLE, 15)
text(712, 445, 250, 26, 'and increased AChE activity', PURPLE, 15)

# =========================================================================
# Row of red mechanism labels + red block arrows + dashed drops
# =========================================================================
text(60, 488, 246, 26, 'Gingipains (Kgp, RgpA, RgpB)', RED, 13)
text(378, 488, 250, 26, 'Gingipains (Kgp, RgpA, RgpB)', RED, 13)
text(700, 488, 110, 26, 'LPS/OMVs', RED, 13)

for ax in (124, 166, 208):                                               # left blocks
    arrow(ax, 519, ax, 548, RED_ICON, 6.0)
for ax in (462, 494, 526):                                               # center blocks
    arrow(ax, 519, ax, 548, RED_ICON, 6.0)
arrow(140, 551, 140, 582, DOTGRAY, 2.0, 'dash')                          # left drops
arrow(183, 551, 183, 582, DOTGRAY, 2.0, 'dash')
arrow(463, 551, 463, 574, DOTGRAY, 2.0, 'dash')                          # center drops
arrow(505, 551, 505, 574, DOTGRAY, 2.0, 'dash')

# =========================================================================
# LEFT COLUMN - tau axis
# =========================================================================
text(22, 583, 60, 26, 'Tau', TEAL, 14)
text(356, 581, 60, 26, 'APP', TEAL, 14)
arrow(78, 594, 300, 594, TEAL_AR, 3.5)                                   # Tau -> APP axis
arrow(163, 608, 163, 646, DOTGRAY, 2.0, 'dash')                          # -> Tau fragments
arrow(62, 658, 116, 670, TEAL_AR, 3.0)                                   # fan out
arrow(186, 658, 240, 670, TEAL_AR, 3.0)
text(18, 664, 60, 24, 'Tau', TEAL, 14)
text(16, 685, 100, 24, 'fragments', TEAL, 14)
arrow(155, 700, 155, 720, DOTGRAY, 2.0, 'dash')                          # -> hyperphos box

shape('rect', 78, 718, 208, 44, fill=None, line=INK, lw=1.5, dash='dot')
text(84, 719, 200, 22, 'Hyperphosphorylation', INK, 12.5)
text(82, 740, 196, 22, '(dysregulated kinases)', INK, 11.5)
arrow(155, 762, 155, 784, DOTGRAY, 2.0, 'dash')                          # -> PLK2
text(132, 785, 60, 24, 'PLK2', TEAL, 13)
arrow(155, 818, 155, 856, DOTGRAY, 2.0, 'dash')                          # -> PHF
text(34, 858, 210, 24, 'Paired helical filaments', PURPLE_D, 12.5)
text(84, 880, 70, 24, '(PHF)', PURPLE_D, 12.5)
text(248, 839, 66, 24, 'CALD1', TEAL, 13)
text(353, 839, 56, 24, 'HES1', TEAL, 13)
arrow(155, 906, 155, 952, DOTGRAY, 2.0, 'dash')                          # -> NFT

# tangle icon + NFT box
shape('ellipse', 78, 960, 96, 76, fill='#8B6FAD', line='#684988', lw=3.5, trans=55)
shape('ellipse', 96, 976, 60, 44, fill=None, line='#684988', lw=2.5)
shape('rect', 166, 1000, 132, 48, fill=None, line=PURPLE_BR, lw=1.75, dash='dot')
text(170, 1000, 150, 22, 'Neurofibrillary', PURPLE_D, 12.5)
text(170, 1023, 150, 22, 'tangles (NFTs)', PURPLE_D, 12.5)
arrow(215, 1052, 215, 1084, DOTGRAY, 1.75, 'dot')                        # -> bus

# =========================================================================
# CENTER COLUMN - APP / Abeta axis
# =========================================================================
# membrane drawing: two wavy teal lines + ticks + embedded protein bar
arrow(410, 624, 560, 624, TEAL_LT, 2.5, head=False)
arrow(410, 658, 560, 658, TEAL_LT, 2.5, head=False)
for tx in (420, 434, 448, 462, 492, 506, 520, 534, 548):
    arrow(tx, 627, tx, 655, TEAL_LT, 1.5, head=False)
shape('round_rect', 468, 576, 22, 112, fill='#1B6A72', line=None)
text(536, 570, 100, 24, 'β-secretase', TEAL, 12.5)
text(538, 592, 90, 22, '(BACE1)', TEAL, 11.5)
text(540, 658, 100, 24, 'γ-secretase', TEAL, 12.5)
text(536, 680, 115, 22, '(presenilin 1)', TEAL, 11.5)
arrow(470, 696, 470, 716, DOTGRAY, 2.5)                                  # -> Abeta box

shape('rect', 408, 717, 164, 36, fill=None, line=INK, lw=1.5, dash='dot')
text(402, 720, 180, 24, 'Aβ peptides (Aβ40/42)', INK, 12.5)
arrow(470, 762, 492, 800, TEAL_AR, 2.5, 'dash')                          # -> oligomers
text(450, 802, 90, 24, 'Oligomers', INK, 12.5)
arrow(492, 830, 492, 876, TEAL_AR, 2.5)                                  # -> fibrils
text(466, 879, 80, 24, 'Fibrils', INK, 12.5)
shape('ellipse', 354, 830, 54, 36, fill=None, line=TEAL_AR, lw=2.25)     # fibril scribble icon
arrow(448, 918, 528, 918, TEAL_AR, 8.0, head=False)                      # thick shaft
arrow(528, 916, 528, 950, TEAL_AR, 4.0)                                  # -> plaque box

# plaque drawing + box
shape('ellipse', 449, 961, 78, 52, fill='#684988', line=None, trans=15, z=5)
shape('ellipse', 462, 972, 46, 30, fill='#8B6FAD', line=None, trans=5, z=6)
shape('round_rect', 431, 958, 124, 113, fill=LAVENDER, line=PURPLE_BR, lw=1.75, dash='dot', z=4)
text(426, 1022, 124, 24, 'Aβ deposition', PURPLE_D, 12.5, z=30)
text(422, 1044, 140, 22, '(amyloid plaques)', PURPLE_D, 11.5, z=30)
arrow(505, 1073, 505, 1084, DOTGRAY, 1.75, 'dot')                        # -> bus

# dotted divider between tau and APP columns
arrow(338, 575, 338, 730, DOTGRAY, 1.25, 'dot', head=False, z=3)

# =========================================================================
# RIGHT COLUMN - AChE axis
# =========================================================================
# small LPS/OMV icons under label
shape('round_rect', 691, 519, 14, 55, fill=RED_ICON, line=None)
for lx in (716, 731, 746):
    arrow(lx, 524, lx, 556, RED_ICON, 1.5, head=False)
shape('ellipse', 752, 538, 32, 32, fill=None, line=RED_ICON, lw=2.5)
shape('ellipse', 784, 521, 30, 30, fill=None, line=RED_ICON, lw=2.5)
arrow(748, 560, 748, 606, DOTGRAY, 2.5, 'dash')                          # -> AChE oval

# AChE oval + PAS band + label
shape('ellipse', 714, 617, 68, 84, fill='#B9D6D8', line='#58387A', lw=2.25)
text(722, 642, 70, 26, 'AChE', '#0A525E', 13, align='center')
arrow(660, 671, 795, 671, '#58387A', 2.25, head=False)
arrow(660, 685, 795, 685, '#58387A', 2.25, head=False)
text(818, 660, 50, 24, 'PAS', PURPLE, 12.5)

shape('rect', 672, 704, 150, 28, fill=None, line=INK, lw=1.5, dash='dot')
text(676, 705, 145, 22, 'AChE-PAS complex', INK, 12)
shape('rect', 656, 728, 200, 28, fill=None, line=INK, lw=1.5, dash='dot')
text(660, 729, 192, 22, 'nucleates Aβ aggregation', INK, 12)
arrow(757, 755, 757, 784, DOTGRAY, 2.0, 'dash')
shape('rect', 648, 786, 212, 50, fill=None, line=INK, lw=1.5, dash='dot')
text(649, 788, 178, 22, 'Enhanced Aβ aggregation', INK, 12)
text(678, 810, 145, 22, '(oligomers/fibrils)', INK, 11)
# effect-3 box -> enhanced aggregation (long dotted drop at x=648)
arrow(648, 500, 648, 784, DOTGRAY, 1.75, 'dot')

shape('rect', 866, 770, 146, 52, fill=None, line=INK, lw=1.5, dash='dot')
text(888, 772, 100, 22, 'Increased', TEAL, 12.5)
text(872, 794, 130, 22, 'AChE activity', TEAL, 12.5)
# OMVs -> increased AChE activity (elbow dotted)
arrow(860, 563, 930, 563, DOTGRAY, 1.75, 'dot', head=False)
arrow(930, 563, 930, 766, DOTGRAY, 1.75, 'dot')
arrow(930, 833, 930, 874, DOTGRAY, 1.75, 'dot')                          # -> AChE
text(894, 876, 70, 24, 'AChE', TEAL, 13)
text(838, 894, 50, 24, 'ACh', INK, 12.5)
arrow(882, 906, 948, 906, DOTGRAY, 1.75, 'dot')                          # -> products
text(950, 893, 74, 24, 'Choline', INK, 12.5)
text(968, 914, 24, 24, '+', INK, 12.5, align='center')
text(952, 929, 72, 24, 'Acetate', INK, 12.5)
arrow(940, 926, 940, 998, TEAL_AR, 2.0, 'dash')                          # -> UCHL1
text(910, 999, 75, 24, 'UCHL1', TEAL, 12.5)

# reduced synaptic ACh box
arrow(753, 846, 753, 884, TEAL_AR, 10.0)                                 # enhanced -> (big teal arrow)
arrow(690, 856, 746, 882, TEAL_AR, 6.5, head=False)                     # wide arrow wings
arrow(812, 858, 762, 882, TEAL_AR, 6.5, head=False)
arrow(770, 894, 770, 958, DOTGRAY, 2.0, 'dash')                          # -> reduced box
shape('round_rect', 674, 962, 218, 62, fill=LAVENDER, line=PURPLE_BR, lw=2.0, dash='dot')
text(698, 968, 175, 24, 'Reduced synaptic ACh', PURPLE_D, 12.5)
text(692, 991, 190, 22, '(cholinergic dysfunction)', PURPLE_D, 11)

# =========================================================================
# BOTTOM: bus -> three outcome boxes -> collector -> AD bar
# =========================================================================
arrow(150, 1088, 850, 1088, DOTGRAY, 1.75, 'dot', head=False)
for bx in (152, 512, 852):
    arrow(bx, 1090, bx, 1117, DOTGRAY, 1.75, 'dot')

shape('round_rect', 22, 1122, 302, 231, fill=LAVENDER, line=PURPLE_BR, lw=2.0, dash='dot')
shape('round_rect', 360, 1123, 291, 232, fill=LAVENDER, line=PURPLE_BR, lw=2.0, dash='dot')
shape('round_rect', 683, 1121, 298, 232, fill=LAVENDER, line=PURPLE_BR, lw=2.0, dash='dot')

# --- box 1: neuroinflammation
text(86, 1128, 210, 26, 'Neuroinflammation', PURPLE, 15.5)
text(82, 1152, 200, 24, '(microglial activation)', PURPLE, 11.5)
text(165, 1178, 100, 24, 'LPS/OMVs', RED, 12)
for lx in (196, 214, 232, 250):                                          # mini LPS marks
    arrow(lx, 1206, lx, 1234, RED_ICON, 1.5, head=False)
# box1: purple microglia drawing + TLR4/NLRP3 axis
shape('ellipse', 62, 1212, 56, 66, fill='#B398C4', line='#8A6F9E', lw=2.0, trans=42)
shape('ellipse', 50, 1240, 24, 18, fill='#B398C4', line='#8A6F9E', lw=1.5, trans=30)
text(128, 1253, 60, 24, 'TLR4', TEAL, 12.5)
text(258, 1251, 70, 24, 'IL-1β ↑', INK, 11.5)
text(166, 1283, 70, 24, 'NLRP3', TEAL, 12.5)
text(256, 1273, 70, 24, 'IL-18 ↑', INK, 11.5)
text(162, 1299, 105, 24, 'inflammasome', TEAL, 12.5)
text(256, 1295, 75, 24, 'TNF-α ↑', INK, 11.5)
text(165, 1320, 95, 24, 'activation', TEAL, 12.5)
text(259, 1316, 65, 24, 'ROS ↑', INK, 11.5)

# big light-teal arrows box1 -> box2
shape('chevron', 390, 1150, 92, 98, fill='#95BEC2', line=None)
shape('chevron', 378, 1288, 108, 42, fill='#A5C9CB', line=None, trans=28)

# --- box 2: cholinergic deficit
text(410, 1130, 198, 26, 'Cholinergic deficit', PURPLE, 15.5)
text(522, 1185, 120, 24, '↓ACh synthesis', INK, 11.5)
text(522, 1209, 115, 24, '↓ACh release', INK, 11.5)
text(470, 1231, 50, 24, 'ACh', INK, 11.5)
text(520, 1233, 130, 24, '↑ AChE activity', INK, 11.5)
text(522, 1259, 115, 24, '↓Cholinergic', INK, 11.5)
text(522, 1283, 135, 24, 'receptor signaling', INK, 11.5)

# big purple arrow box2 -> box3
shape('chevron', 698, 1195, 128, 95, fill='#C2A8D1', line=None, trans=20)

# box3: brain sketch (light purple) + bullets
shape('ellipse', 731, 1164, 96, 54, fill='#C9B2D6', line='#8A6F9E', lw=2.0, trans=15)
shape('ellipse', 800, 1178, 34, 30, fill='#C9B2D6', line='#8A6F9E', lw=1.75, trans=15)
text(750, 1132, 186, 26, 'Cognitive decline', PURPLE, 15.5)
text(826, 1191, 150, 24, '• Memory impairment', INK, 11.5)
text(826, 1215, 145, 24, '• Learning deficits', INK, 11.5)
text(824, 1242, 175, 24, '• Executive dysfunction', INK, 11.5)
text(822, 1264, 160, 24, '• Behavioral changes', INK, 11.5)

# collector under boxes -> AD bar
for bx in (150, 515, 836):
    arrow(bx, 1355, bx, 1369, DOTGRAY, 1.75, 'dot', head=False)
arrow(150, 1370, 840, 1370, DOTGRAY, 1.75, 'dot', head=False)
arrow(515, 1372, 515, 1384, DOTGRAY, 1.75, 'dot')

shape('round_rect', 277, 1385, 432, 74, fill=AD_FILL, line='#5F497E', lw=2.0, dash='dot')
text(322, 1408, 342, 30, 'Alzheimer disease progression', '#3B1E62', 15.5, align='center')

# =========================================================================
# LEGEND
# =========================================================================
shape('rect', 37, 1474, 678, 52, fill=None, line='#79617F', lw=1.5, dash='dot')
shape('rect', 47, 1487, 24, 24, fill='#94210B', line=None)
text(77, 1487, 245, 26, 'Pathogen factors (P. gingivalis)', GRAY, 11.5)
shape('rect', 323, 1488, 23, 23, fill='#106670', line=None)
text(352, 1487, 155, 26, 'Host proteins/genes', GRAY, 11.5)
shape('rect', 538, 1488, 23, 23, fill='#503074', line=None)
text(567, 1487, 145, 26, 'Pathology/outcomes', GRAY, 11.5)
text(788, 1474, 190, 24, '→ Activation/promotion', '#4A4A4A', 11.5)
text(778, 1502, 195, 24, '-- Inhibition/reduction', '#4A4A4A', 11.5)

# =========================================================================
# emit PageIR
# =========================================================================
page_ir = {
    'schema_version': '1.0',
    'pages': [{
        'id': 'fig3-mechanism-map',
        'width_px': W, 'height_px': H,
        'background': '#FEFEFE',
        'objects': objects,
    }],
}
os.makedirs(os.path.join(HERE, 'generated'), exist_ok=True)
with open(os.path.join(HERE, 'generated', 'fig3_page_ir.json'), 'w') as f:
    json.dump(page_ir, f, ensure_ascii=False, indent=1)
print('PageIR objects:', len(objects))

# =========================================================================
# emit SVG from the same model
# =========================================================================
def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))

pt2px = 1.0 / 0.938  # pt -> source px  (1 px = 0.938 pt)
svg = []
svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Comic Sans MS, Segoe Print, Bradley Hand, cursive">')
svg.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#FEFEFE"/>')
svg.append('<defs>')
for c, tag in ((DOTGRAY, 'ad'), (RED_ICON, 'ar'), (TEAL_AR, 'at'), ('#58387A', 'ap')):
    svg.append(f'<marker id="{tag}" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="4.5" markerHeight="4.5" orient="auto-start-reverse">'
               f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{c}"/></marker>')
svg.append('</defs>')

def dash_attr(dash, w):
    if dash == 'dash': return f'stroke-dasharray="{6+w*2:.0f} {4+w:.0f}" '
    if dash == 'dot':  return f'stroke-dasharray="{max(1.5,w*0.8):.1f} {3+w:.0f}" '
    return ''

for o in objects:
    st = o.get('style', {})
    if o['type'] == 'text':
        x, y, w, h = o['bbox']
        anchor = {'left': 'start', 'center': 'middle', 'right': 'end'}[st.get('align', 'left')]
        size = st.get('font_size_pt', 18) * pt2px
        weight = '700' if st.get('bold') else '400'
        # dominant baseline ~ text top + ascent
        ty = y + h / 2 + size * 0.36
        tx = x + w / 2 if anchor == 'middle' else x
        svg.append(f'<text x="{tx:.0f}" y="{ty:.0f}" font-size="{size:.1f}" font-weight="{weight}" '
                   f'fill="{st.get("color", "#111")}" text-anchor="{anchor}">{esc(o["text"])}</text>')
    elif o['type'] == 'line':
        x1, y1, x2, y2 = o['points']
        c = st.get('color', '#111'); w = st.get('width_pt', 1) * pt2px
        head = st.get('end_arrow') == 'triangle'
        tag = {DOTGRAY: 'ad', RED_ICON: 'ar', TEAL_AR: 'at', '#58387A': 'ap'}.get(c, 'ad')
        m = f'marker-end="url(#{tag})"' if head else ''
        svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w:.1f}" '
                   f'stroke-linecap="round" {dash_attr(st.get("dash"), w)}{m}/>')
    else:
        x, y, w, h = o['bbox']
        fill = st.get('fill')
        fill_a = ''
        if fill and st.get('fill_transparency'):
            fill_a = f' fill-opacity="{1 - st["fill_transparency"] / 100}"'
        stroke = st.get('line')
        sw = st.get('line_width_pt', 1) * pt2px if stroke else 0
        common = (f'fill="{fill or "none"}"{fill_a} stroke="{stroke or "none"}" '
                  f'stroke-width="{sw:.1f}" stroke-linejoin="round" stroke-linecap="round" {dash_attr(st.get("dash"), sw)}')
        if o['type'] == 'rect':
            svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" {common}/>')
        elif o['type'] == 'round_rect':
            svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{min(w, h) * 0.28:.0f}" {common}/>')
        elif o['type'] == 'ellipse':
            svg.append(f'<ellipse cx="{x + w / 2:.0f}" cy="{y + h / 2:.0f}" rx="{w / 2:.0f}" ry="{h / 2:.0f}" {common}/>')
        elif o['type'] == 'chevron':
            k = h * 0.5
            pts = f'{x},{y} {x + w - k},{y} {x + w},{y + h / 2} {x + w - k},{y + h} {x},{y + h} {x + k},{y + h / 2}'
            svg.append(f'<polygon points="{pts}" fill="{fill or "none"}" fill-opacity="{1 - (st.get("fill_transparency") or 0) / 100}"/>')
        elif o['type'] == 'triangle':
            svg.append(f'<polygon points="{x + w / 2},{y} {x + w},{y + h} {x},{y + h}" fill="{fill or "none"}"/>')

svg.append('</svg>')
with open(os.path.join(HERE, 'generated', 'fig3_mechanism_map.svg'), 'w') as f:
    f.write('\n'.join(svg))
print('SVG written, lines:', len(svg))
