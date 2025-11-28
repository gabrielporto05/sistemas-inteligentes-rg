import colorgram
from PIL import Image, ImageDraw, ImageFont

def rgb_to_hex(rgb):
    """Converte (R, G, B) para HEX."""
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])


def get_colors(image_file, numcolors=3):
    """Extrai até 3 cores dominantes da imagem."""
    return colorgram.extract(image_file, numcolors)


def save_palette(colors, swatchsize=120, outfile="palette.png"):
    """
    Gera imagem com a paleta das cores dominantes + texto HEX (compatível com Pillow 10+)
    """
    num_colors = len(colors)
    height = swatchsize + 40  # espaço extra para o hex

    palette = Image.new("RGB", (swatchsize * num_colors, height), "white")
    draw = ImageDraw.Draw(palette)

    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()

    posx = 0
    for color in colors:
        rgb = (color.rgb.r, color.rgb.g, color.rgb.b)
        hex_code = rgb_to_hex(rgb)

        # bloco de cor
        draw.rectangle([posx, 0, posx + swatchsize, swatchsize], fill=rgb)

        # calcular tamanho do texto usando textbbox()
        bbox = draw.textbbox((0, 0), hex_code, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        # centralizar texto
        text_x = posx + (swatchsize - text_w) // 2
        text_y = swatchsize + 10

        draw.text((text_x, text_y), hex_code, fill="black", font=font)

        posx += swatchsize

    palette.save(outfile, "PNG")
    print(f"🎨 Paleta salva em: {outfile}")

# EXEMPLO DE USO
if __name__ == "__main__":
    input_img = "./utils/new_rg.jpg"
    output_palette = "cores_new_rg.png"

    colors = get_colors(input_img, numcolors=3)

    print("\n=== CORES DOMINANTES ===")
    for i, c in enumerate(colors):
        rgb = (c.rgb.r, c.rgb.g, c.rgb.b)
        hex_code = rgb_to_hex(rgb)

        print(f"Cor {i+1}: RGB={rgb} | HEX={hex_code} | Proporção={c.proportion:.2%}")

    save_palette(colors, outfile=output_palette)
