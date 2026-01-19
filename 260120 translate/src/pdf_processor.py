import fitz  # PyMuPDF
from PIL import Image
import io
from typing import List

def convert_pdf_to_images(pdf_file) -> List[Image.Image]:
    """
    Convert a PDF file (bytes or path) to a list of PIL Images using PyMuPDF (fitz).
    This removes the dependency on Poppler.
    """
    images = []
    try:
        # Check if it's a file-like object (Streamlit UploadedFile) or a path
        if hasattr(pdf_file, 'read'):
            pdf_file.seek(0)
            file_bytes = pdf_file.read()
            doc = fitz.open(stream=file_bytes, filetype="pdf")
        else:
            doc = fitz.open(pdf_file)

        for page in doc:
            # Render page to image (default 72 dpi, we can increase matrix for better quality if needed)
            # transform = fitz.Matrix(2, 2) # 2x zoom -> 144 dpi
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2)) 
            img_data = pix.tobytes("png")
            image = Image.open(io.BytesIO(img_data))
            images.append(image)
            
        doc.close()
        return images

    except Exception as e:
        print(f"Error converting PDF with PyMuPDF: {e}")
        raise e
