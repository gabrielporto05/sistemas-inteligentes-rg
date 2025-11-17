import colorgram
from PIL import Image, ImageDraw

def get_colors(image_file, numcolors=3):
    """Extrai até 3 cores dominantes da imagem."""
    colors = colorgram.extract(image_file, numcolors)
    return colors

def save_palette(colors, swatchsize=120, outfile="palette.png"):
    """Gera imagem com a paleta das cores dominantes."""
    num_colors = len(colors)
    palette = Image.new("RGB", (swatchsize * num_colors, swatchsize))
    draw = ImageDraw.Draw(palette)

    posx = 0
    for color in colors:
        rgb = (color.rgb.r, color.rgb.g, color.rgb.b)
        draw.rectangle([posx, 0, posx + swatchsize, swatchsize], fill=rgb)
        posx += swatchsize

    palette.save(outfile, "PNG")
    print(f"🎨 Paleta salva em: {outfile}")

# EXEMPLO DE USO
if __name__ == "__main__":
    input_img = "./utils/old_rg.jpg"      # coloque a imagem
    output_palette = "cores_old_rg.png"  # imagem de saída

    colors = get_colors(input_img, numcolors=3)
    
    for i, c in enumerate(colors):
        print(f"Cor {i+1}: ({c.rgb.r}, {c.rgb.g}, {c.rgb.b})")

    save_palette(colors, outfile=output_palette)
