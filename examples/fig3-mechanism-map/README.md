# Example: Fig 3 mechanism map → editable PPTX + SVG

Source: a flattened 1024×1536 hand-drawn mechanism figure
(`source_fig3_mechanism_map.png`, *Porphyromonas gingivalis* → Alzheimer's
disease mechanism map), rebuilt into fully editable office formats with the
`image-to-editable-pptx` skill.

## Files

| File | Description |
| --- | --- |
| `source_fig3_mechanism_map.png` | Original flattened source image (visual source of truth) |
| `fig3_mechanism_map.pptx` | Editable single-slide deck (227 native objects: 85 text boxes with 1,139 editable characters + native shapes/lines, no full-slide raster) |
| `fig3_mechanism_map.svg` | Same geometry as an editable vector SVG |
| `fig3_page_ir.json` | Intermediate PageIR representation (source-pixel coordinates) |
| `fig3_compare_preview.png` | Side-by-side source vs. reconstruction preview |
| `build_fig3.py` | Generator script — single object model emits both PageIR and SVG |

## Reproduce

```bash
# 1. regenerate PageIR + SVG
python3 build_fig3.py          # writes ./generated/

# 2. validate the PageIR
python3 ../../scripts/validate_page_ir.py generated/fig3_page_ir.json

# 3. compile the editable PPTX
node ../../scripts/compile_page_ir.js generated/fig3_page_ir.json generated/fig3_mechanism_map.pptx

# 4. inspect the deck (bounds / full-slide-raster checks)
python3 ../../scripts/inspect_pptx.py generated/fig3_mechanism_map.pptx
```

## Reconstruction notes

- Geometry is authored in source pixels (1024×1536); the slide keeps the
  2:3 page ratio (13.33 × 20 in).
- Colors were sampled from the source: rust red `#A02D14` (pathogen
  factors), teal `#0C646D` (host proteins/genes), purple `#381F61` /
  `#2B1459` (pathology/outcomes), lavender `#F6F3F8` box fills.
- Hand-drawn marker strokes are rebuilt as clean native geometry (solid /
  dashed / dotted lines with arrowheads); hand-drawn pictorial icons
  (bacterium, LPS comb, OMVs, tangles, plaques, microglia, brain) are
  approximated with native ellipses/rects/chevrons.
- Font: Comic Sans MS (closest widely-available match to the source's
  hand-lettered style). All 1,139 characters are editable text.
