import os
import platform
import tempfile
from PIL import Image
import subprocess

def print_jpg(jpg_path):
    system = platform.system()

    # Convert to temporary PDF (some systems require this for printing)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        pdf_path = temp_pdf.name
        image = Image.open(jpg_path)
        # Convert RGB to avoid mode errors
        if image.mode != "RGB":
            image = image.convert("RGB")
        image.save(pdf_path, "PDF")
        print(f"Converted to PDF: {pdf_path}")

    try:
        if system == "Windows":
            os.startfile(pdf_path, "print")
        elif system in ["Linux", "Darwin"]:  # Darwin = macOS
            subprocess.run(["lp", pdf_path], check=True)
        else:
            raise RuntimeError(f"Unsupported OS: {system}")
        print("Print command sent successfully.")
    except Exception as e:
        print(f"Error printing: {e}")
    finally:
        os.remove(pdf_path)

if __name__ == "__main__":
    print_jpg("../person-face-dataset.jpg")
