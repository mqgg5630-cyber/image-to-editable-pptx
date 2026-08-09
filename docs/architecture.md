# Architecture

```mermaid
flowchart LR
    A[Flattened slide image] --> B[Visual inspection / OCR evidence]
    B --> C[PageIR in source pixels]
    C --> D[PageIR validator]
    D --> E[PptxGenJS compiler]
    E --> F[Editable PPTX]
    F --> G[LibreOffice render]
    A --> H[Source image]
    G --> I[Pixel/edge comparison]
    H --> I
    I -->|repair| C
```

PageIR separates page-specific perception and geometry decisions from the generic PowerPoint compiler. This makes it possible to correct layout, text, and representation decisions without adding special-case slide code.
