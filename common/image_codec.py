from io import BytesIO
from PIL import Image


def image_to_png_bytes(image: Image.Image) -> bytes:
    """Serializa uma imagem PIL em bytes PNG."""
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def png_bytes_to_image(data: bytes) -> Image.Image:
    """Desserializa bytes PNG para imagem PIL no modo RGB."""
    return Image.open(BytesIO(data)).convert("RGB")
