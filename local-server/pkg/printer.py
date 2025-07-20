import os
import platform
import tempfile
from PIL import Image
import subprocess

def print_jpg(jpg_path):
    system = platform.system()

    try:
        if system == "Windows":
            os.startfile(jpg_path, "print")
        elif system in ["Linux", "Darwin"]:  # Darwin = macOS
            subprocess.run(["lp", jpg_path], check=True)
        else:
            raise RuntimeError(f"Unsupported OS: {system}")
        print("Print command sent successfully.")
    except Exception as e:
        print(f"Error printing: {e}")

if __name__ == "__main__":
    print_jpg("../person-face-dataset.jpg")
