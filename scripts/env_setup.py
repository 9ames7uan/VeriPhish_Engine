import os
import subprocess

def cleanup_and_install():
    # Cleanup previous instances
    print("🧹 Cleaning up old processes...")
    subprocess.run(["pkill", "-f", "uvicorn"], capture_output=True)

    # Install dependencies
    print("📦 Installing requirements...")
    subprocess.run(["pip", "install", "-q", "fastapi", "uvicorn", "pydantic"], check=True)

    print("✅ Environment ready")

cleanup_and_install()
