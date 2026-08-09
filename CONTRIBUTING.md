# Contributing

Contributions are welcome when they improve editability, fidelity, portability, or test coverage without introducing a full-slide raster shortcut.

## Development flow

1. Fork the repository and create a focused branch.
2. Keep page-specific geometry in PageIR rather than hardcoding a sample slide in the compiler.
3. Add or update tests for behavior changes.
4. Run the local validation and smoke compile commands in `RELEASE_CHECKLIST.md`.
5. Open a pull request describing the source case, failure mode, repair, and validation evidence.

Do not include confidential slides, private customer data, proprietary fonts, or assets that you do not have permission to redistribute.
