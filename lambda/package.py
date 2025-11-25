#!/usr/bin/env python3
"""
Lambda deployment package creation script.
This script packages the Lambda function code and dependencies into a ZIP file.
"""

import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path


def main():
    """Create Lambda deployment package."""
    script_dir = Path(__file__).parent.absolute()
    build_dir = script_dir / "build"
    package_dir = build_dir / "package"
    output_file = script_dir / "lambda_deployment.zip"
    
    print("Creating Lambda deployment package...")
    
    # Clean up previous build
    if build_dir.exists():
        print("Cleaning up previous build directory...")
        shutil.rmtree(build_dir)
    
    # Create build directory structure
    print("Creating build directory...")
    package_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy Lambda function code (exclude test files)
    print("Copying Lambda function code...")
    lambda_modules = [
        "lambda_function.py",
        "iam_scanner.py",
        "dynamodb_writer.py",
        "metrics_emitter.py",
        "logger_config.py",
        "concurrency_lock.py",
    ]
    
    for module in lambda_modules:
        src = script_dir / module
        dst = package_dir / module
        if src.exists():
            shutil.copy2(src, dst)
            print(f"  ✓ Copied {module}")
        else:
            print(f"  ✗ Warning: {module} not found", file=sys.stderr)
    
    # Install dependencies
    print("Installing dependencies...")
    requirements_file = script_dir / "requirements.txt"
    if requirements_file.exists():
        try:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "-r",
                    str(requirements_file),
                    "-t",
                    str(package_dir),
                    "--upgrade",
                    "--quiet",
                ],
                check=True,
                capture_output=True,
            )
            print("  ✓ Dependencies installed")
        except subprocess.CalledProcessError as e:
            print(f"  ✗ Error installing dependencies: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("  ✗ requirements.txt not found", file=sys.stderr)
        sys.exit(1)
    
    # Remove unnecessary files to reduce package size
    print("Cleaning up unnecessary files...")
    
    # Remove __pycache__ directories
    for pycache_dir in package_dir.rglob("__pycache__"):
        if pycache_dir.is_dir():
            shutil.rmtree(pycache_dir, ignore_errors=True)
    
    # Remove .dist-info directories
    for dist_info_dir in package_dir.rglob("*.dist-info"):
        if dist_info_dir.is_dir():
            shutil.rmtree(dist_info_dir, ignore_errors=True)
    
    # Remove tests directories
    for tests_dir in package_dir.rglob("tests"):
        if tests_dir.is_dir():
            shutil.rmtree(tests_dir, ignore_errors=True)
    
    # Remove .pyc and .pyo files
    for pyc_file in package_dir.rglob("*.pyc"):
        if pyc_file.is_file():
            pyc_file.unlink()
    
    for pyo_file in package_dir.rglob("*.pyo"):
        if pyo_file.is_file():
            pyo_file.unlink()
    
    # Remove test-only dependencies
    print("Removing test-only dependencies...")
    test_deps = ["hypothesis", "moto", "_hypothesis_ftz_detector.py"]
    for dep in test_deps:
        dep_path = package_dir / dep
        if dep_path.exists():
            if dep_path.is_dir():
                shutil.rmtree(dep_path, ignore_errors=True)
            else:
                dep_path.unlink()
    
    # Create ZIP file
    print("Creating ZIP file...")
    if output_file.exists():
        output_file.unlink()
    
    with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_path in package_dir.rglob("*"):
            if file_path.is_file():
                arcname = file_path.relative_to(package_dir)
                zipf.write(file_path, arcname)
    
    # Set proper permissions
    output_file.chmod(0o644)
    
    # Display package information
    package_size = output_file.stat().st_size / (1024 * 1024)  # Convert to MB
    print()
    print("✓ Lambda deployment package created successfully!")
    print(f"  Location: {output_file}")
    print(f"  Size: {package_size:.1f} MB")
    print()
    
    # Show package contents (first 20 files)
    print("Package contents (first 20 files):")
    with zipfile.ZipFile(output_file, "r") as zipf:
        file_list = zipf.namelist()[:20]
        for filename in file_list:
            print(f"  - {filename}")
        if len(zipf.namelist()) > 20:
            print(f"  ... and {len(zipf.namelist()) - 20} more files")
    
    # Clean up build directory
    print()
    print("Cleaning up build directory...")
    shutil.rmtree(build_dir)
    
    print("Done!")


if __name__ == "__main__":
    main()
