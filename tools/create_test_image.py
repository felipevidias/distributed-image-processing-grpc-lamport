from pathlib import Path
from PIL import Image, ImageDraw


def main():
    output = Path("images/entrada.png")
    output.parent.mkdir(parents=True, exist_ok=True)

    width, height = 900, 500
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    # Desenha formas simples para a saída ficar visualmente perceptível.
    for x in range(0, width, 50):
        color = (x % 255, 100, 255 - (x % 255))
        draw.rectangle([x, 0, x + 40, height], fill=color)

    draw.ellipse([120, 80, 380, 340], fill=(255, 210, 50), outline=(20, 20, 20), width=5)
    draw.rectangle([500, 120, 780, 370], fill=(50, 180, 120), outline=(20, 20, 20), width=5)
    draw.text((40, 430), "Teste - Processamento Distribuido com gRPC + Lamport", fill=(0, 0, 0))

    img.save(output)
    print(f"Imagem de teste criada em: {output}")


if __name__ == "__main__":
    main()
