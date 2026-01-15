#!/bin/bash

# Unstructured Document Viewer - Installation Script (PDF-only)
# Usage: Run with sudo for system-wide installation
# Example: sudo ./install.sh

set -e  # Exit on error

echo "Starting installation process..."

# Update package lists
echo "Updating package lists..."
apt update

# Upgrade existing packages
echo "Upgrading existing packages..."
apt upgrade -y

# Install pdf2htmlEX dependencies
echo "Installing pdf2htmlEX dependencies..."
apt install -y \
    libglib2.0-0 \
    libfreetype6 \
    libfontconfig1 \
    libcairo2 \
    libpng16-16 \
    libjpeg-turbo8 \
    libxml2 \
    wget

# Download pdf2htmlEX package
echo "Downloading pdf2htmlEX package..."
wget https://github.com/pdf2htmlEX/pdf2htmlEX/releases/download/v0.18.8.rc1/pdf2htmlEX-0.18.8.rc1-master-20200630-Ubuntu-bionic-x86_64.deb -O /var/tmp/pdf2htmlEX.deb

# Install pdf2htmlEX
echo "Installing pdf2htmlEX..."
apt install -y /var/tmp/pdf2htmlEX.deb

# Clean up downloaded file
echo "Cleaning up temporary files..."
rm -f /var/tmp/pdf2htmlEX.deb

echo "Installation completed successfully!"
echo "You can now use pdf2htmlEX to convert PDF files to HTML."
echo ""
echo "Verify installation:"
echo "  pdf2htmlEX --version"
