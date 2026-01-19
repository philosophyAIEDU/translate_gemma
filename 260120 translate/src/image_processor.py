from PIL import Image

def resize_image_for_model(image: Image.Image, target_size: int = 896) -> Image.Image:
    """
    Resize image to the target size (square) as required by TranslateGemma.
    The requirement says 896x896 normalization.
    """
    return image.resize((target_size, target_size), Image.Resampling.LANCZOS)
