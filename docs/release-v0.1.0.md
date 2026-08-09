# v0.1.0 - Initial public release

First public clean-room release of **Image to Editable PPTX**.

## Highlights

- ChatGPT Skill entrypoint for flattened-slide reconstruction.
- Editable text and native PowerPoint shape reconstruction through PageIR.
- Portable PptxGenJS compiler.
- PageIR and Skill validators.
- OCR candidate line extraction for English and Chinese language packs.
- PPTX inspection that flags out-of-bounds shapes and full-slide picture shortcuts.
- LibreOffice/Poppler render-comparison workflow.
- CI validation and tag-driven GitHub Release automation.
- Bilingual README showcase with downloadable Chinese and English editable PPTX outputs produced with this skill.

## Release assets

Recommended assets to upload to the first GitHub Release:

1. `skill.zip`
2. `image-to-editable-pptx-v0.1.0-repo.zip`
3. `SHA256SUMS.txt`
4. `docs/showcase/image-to-editable-pptx-demo-en-editable.pptx`
5. `docs/showcase/image-to-editable-pptx-demo-zh-editable.pptx`

The project reconstructs visible slide content; it does not recover hidden source vectors, chart data, animations, masters, or inaccessible metadata.
