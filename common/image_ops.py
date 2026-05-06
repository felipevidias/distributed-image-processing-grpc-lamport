from PIL import Image, ImageOps, ImageFilter


def apply_operation(image: Image.Image, operation: str) -> Image.Image:
    """Aplica uma operação simples em um bloco de imagem.

    Operações suportadas:
    - grayscale: converte para tons de cinza.
    - invert: inverte as cores.
    - edges: aplica filtro simples de bordas.
    - blur: aplica desfoque simples.
    """
    operation = (operation or "grayscale").lower().strip()
    image = image.convert("RGB")

    if operation == "grayscale":
        return ImageOps.grayscale(image).convert("RGB")
    if operation == "invert":
        return ImageOps.invert(image)
    if operation == "edges":
        return image.filter(ImageFilter.FIND_EDGES)
    if operation == "blur":
        return image.filter(ImageFilter.BLUR)

    raise ValueError(
        f"Operação inválida: {operation}. Use: grayscale, invert, edges ou blur."
    )
