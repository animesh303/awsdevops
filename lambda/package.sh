#!/bin/bash
set -e

# Lambda deployment package creation script
# This script packages the Lambda function code and dependencies into a ZIP file

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="${SCRIPT_DIR}/build"
PACKAGE_DIR="${BUILD_DIR}/package"
OUTPUT_FILE="${SCRIPT_DIR}/lambda_deployment.zip"

echo "Creating Lambda deployment package..."

# Clean up previous build
if [ -d "$BUILD_DIR" ]; then
    echo "Cleaning up previous build directory..."
    rm -rf "$BUILD_DIR"
fi

# Create build directory structure
echo "Creating build directory..."
mkdir -p "$PACKAGE_DIR"

# Copy Lambda function code (exclude test files, cache, and virtual environments)
echo "Copying Lambda function code..."
cp "${SCRIPT_DIR}/lambda_function.py" "$PACKAGE_DIR/"
cp "${SCRIPT_DIR}/iam_scanner.py" "$PACKAGE_DIR/"
cp "${SCRIPT_DIR}/dynamodb_writer.py" "$PACKAGE_DIR/"
cp "${SCRIPT_DIR}/metrics_emitter.py" "$PACKAGE_DIR/"
cp "${SCRIPT_DIR}/logger_config.py" "$PACKAGE_DIR/"
cp "${SCRIPT_DIR}/concurrency_lock.py" "$PACKAGE_DIR/"

# Install dependencies
echo "Installing dependencies..."
pip install -r "${SCRIPT_DIR}/requirements.txt" -t "$PACKAGE_DIR" --upgrade --quiet

# Remove unnecessary files to reduce package size
echo "Cleaning up unnecessary files..."
find "$PACKAGE_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$PACKAGE_DIR" -type d -name "*.dist-info" -exec rm -rf {} + 2>/dev/null || true
find "$PACKAGE_DIR" -type d -name "tests" -exec rm -rf {} + 2>/dev/null || true
find "$PACKAGE_DIR" -type f -name "*.pyc" -delete 2>/dev/null || true
find "$PACKAGE_DIR" -type f -name "*.pyo" -delete 2>/dev/null || true

# Remove test-only dependencies (hypothesis and moto are not needed in production)
echo "Removing test-only dependencies..."
rm -rf "${PACKAGE_DIR}/hypothesis" 2>/dev/null || true
rm -rf "${PACKAGE_DIR}/moto" 2>/dev/null || true
rm -rf "${PACKAGE_DIR}/_hypothesis_ftz_detector.py" 2>/dev/null || true

# Create ZIP file
echo "Creating ZIP file..."
cd "$PACKAGE_DIR"
zip -r "$OUTPUT_FILE" . -q

# Set proper permissions on the ZIP file
chmod 644 "$OUTPUT_FILE"

# Display package information
PACKAGE_SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
echo ""
echo "✓ Lambda deployment package created successfully!"
echo "  Location: $OUTPUT_FILE"
echo "  Size: $PACKAGE_SIZE"
echo ""
echo "Package contents:"
unzip -l "$OUTPUT_FILE" | head -20

# Clean up build directory
echo ""
echo "Cleaning up build directory..."
rm -rf "$BUILD_DIR"

echo "Done!"
