from setuptools import setup, find_packages
from pathlib import Path

here = Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

VERSION = '1.0.0'
DESCRIPTION = 'Unstructured Document Viewer'

setup(
    name="unstructured-document-viewer",
    version=VERSION,
    author="Preprocess Team",
    author_email="support@preprocess.co",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/preprocess-co/unstructured-document-viewer",
    packages=find_packages(),
    install_requires=[
        "rag-document-viewer>=1.0.0",
    ],
    keywords=["unstructured", "document", "viewer", "rag", "pdf", "preview"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
)
