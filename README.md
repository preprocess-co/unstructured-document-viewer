# Unstructured Document Viewer ![V1.0.0](https://img.shields.io/badge/Version-1.0.0-333.svg?labelColor=eee) ![MIT License](https://img.shields.io/badge/License-MIT-333.svg?labelColor=eee)

**Unstructured Document Viewer** is an open-source library that provides interactive answer references and source grounding for RAG applications that use [Unstructured](https://unstructured.io/) for file preprocessing.

It converts PDF files into a high-fidelity, HTML-based viewer. Using element coordinates provided by Unstructured, it delivers desktop-like document viewing capabilities:
- Preserves the exact look and feel of the original document, similar to a native file viewer
- Highlights and lets users navigate text chunks to support citations and references in your RAG application

The library generates an HTML component that can be easily embedded into web applications, desktop apps, or any system that supports HTML rendering.

*Developed by [Preprocess Team](https://preprocess.co)*

**Unstructured Document Viewer** is an extension of [RAG Document Viewer](https://github.com/preprocess-co/rag-document-viewer) that provides native support for [Unstructured.io](https://unstructured.io/) element format.

## How it works
-   Pass in a PDF file, Unstructured element and a destination path.
-   An HTML bundle is created.
-   You can now embed the viewer in your application, as simple as using an `<iframe>`. Files are served directly from *your* backend under *your* auth logic, no external servers.

**Viewer features:**


![RAG Document Viewer Demo](previewer.png)

1.  **Chunks Highlighting** - Visual emphasis of the important content part you want to highlight.
2.  **Chunk Navigator**: Navigate between highlighted chunks with next/previous controls.
3.  **Zoom Controls**: Renders the document at the optimal zoom level, and users can zoom in/out as needed.
4.  **Scrollbar Navigator**: Visual indicators on the scrollbar show highlighted chunk positions; click to jump to a specific chunk.

---

## Quick Start

**1. Install Dependencies**

Follow the [RAG Document Viewer prerequisites](https://github.com/preprocess-co/rag-document-viewer#prerequisites) first.

**2. Install the Library**
```bash
pip install unstructured-document-viewer
```

**3. Generate a Viewer**
```python
from unstructured.partition.auto import partition
from unstructured_document_viewer import Unstructured_DV

# Partition a PDF file
elements = partition("document.pdf", strategy="hi_res")

# Generate an HTML viewer - pass partition output directly
Unstructured_DV(
    file_path="document.pdf",
    store_path="/path/to/output",
    elements=elements
)
```

Or if you already have elements as dictionaries:
```python
# From API response or pre-converted data
elements_data = [el.to_dict() for el in elements]

Unstructured_DV(
    file_path="document.pdf",
    store_path="/path/to/output",
    elements=elements_data
)
```

**4. Serve in your application**
```html
<iframe
  src="/path/to/output/"
  width="100%"
  height="800"
  style="border:0"
></iframe>
```

---

## Usage

### Basic Chunking Highlight (element level)

Each element with valid coordinates becomes its own chunk. You can pass either `partition()` output directly or a list of element dictionaries:

```python
from unstructured.partition.auto import partition
from unstructured_document_viewer import Unstructured_DV

elements = partition("document.pdf", strategy="hi_res")

Unstructured_DV(
    file_path="document.pdf",
    store_path="/path/to/output",
    elements=elements  # or [el.to_dict() for el in elements]
)
```

### Advanced Chunking Highlight (group elements into chunks)

Group multiple elements into single chunks using element IDs:

```python
from unstructured_document_viewer import Unstructured_DV

# Group elements by their element_ids
chunks = [
    ["33e49c0bd64d7e833d8564d8ca782e7d", "d931f460bc31732a0838a5b0b42db122"],  # Chunk 0
    ["e2acbe7602ede36bbec85ff1de7c3fae"],  # Chunk 1
]

Unstructured_DV(
    file_path="document.pdf",
    store_path="/path/to/output",
    elements=elements_data,
    chunks=chunks
)
```

---

## Parameters

### Unstructured_DV Function

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `file_path` | `str` | Required | Path to the input document file |
| `store_path` | `str` | `None` | Output directory path (auto-generated if not provided) |
| `elements` | `list` | Required | Unstructured elements - either `partition()` output directly or list of element dicts |
| `chunks` | `list` | `None` | Element ID groupings; if not provided, each element becomes its own chunk |
| `**kwargs` | | | Additional styling/configuration options (see RAG Document Viewer docs) |

### Styling Options

All styling options from RAG Document Viewer are supported:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `main_color` | `str` | `#ff8000` | Primary colour for interactive elements |
| `background_color` | `str` | `#dddddd` | Viewer background colour |
| `chunks_navigator` | `bool` | `True` | Show chunk navigation controls |
| `scrollbar_navigator` | `bool` | `True` | Display chunk indicators on scrollbar |
| `page_number` | `bool` | `True` | Display page numbers |

See [RAG Document Viewer documentation](https://github.com/preprocess-co/rag-document-viewer#viewer-options) for all options.

---

## Requirements

- Python >= 3.8
- [RAG Document Viewer](https://github.com/preprocess-co/rag-document-viewer) >= 1.0.0
- System dependencies: LibreOffice, pdf2htmlEX (see RAG Document Viewer docs)

---

## Support

Contact the Preprocess team at `support@preprocess.co` or join our [Discord channel](https://discord.gg/7G5xqsZmGu).

## License

This project is licensed under the MIT License.
