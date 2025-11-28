import cv2
import os
import csv
import numpy as np
import pytesseract
import colorgram
import re

PASTA_IMAGENS = "./db/dataset_final_classificados"
ARQUIVO_SAIDA = "./features.csv"

TEMPLATE_QRCODE = "./utils/template_qr.png"
TEMPLATE_DIGITAL = "./utils/template_digital.png"

def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])

def detectar_template(img, template_file, limiar=0.5):
    if not os.path.exists(template_file):
        return 0

    template = cv2.imread(template_file, 0)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if img_gray.shape[0] < template.shape[0] or img_gray.shape[1] < template.shape[1]:
        return 0

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    return 1 if np.max(res) >= limiar else 0

def extrair_cores_hex(image_path, n=3):
    try:
        colors = colorgram.extract(image_path, n)
    except:
        return ["#000000", "#000000", "#000000"]

    hex_colors = []
    for c in colors:
        hex_color = rgb_to_hex((c.rgb.r, c.rgb.g, c.rgb.b))
        hex_colors.append(hex_color)

    while len(hex_colors) < 3:
        hex_colors.append("#000000")

    return hex_colors

def extrair_texto_features(img):
    texto = pytesseract.image_to_string(img).upper()

    return {
        "tem_nome": int(bool(re.search(r"\bNOME\b|\bNAME\b", texto))),
        "tem_nome_social": int(bool(re.search(r"NOME SOCIAL|SOCIAL NAME", texto))),
        "tem_nacionalidade": int(bool(re.search(r"NACIONALIDADE|PLACE OF BIRTH", texto)))
    }

def obter_classe(img_name: str):
    nome = img_name.lower()

    if "old_rg" in nome:
        return "old"
    if "new_rg" in nome:
        return "new"

    return "ilegivel"  # fallback

def processar_imagens():
    imagens = os.listdir(PASTA_IMAGENS)

    with open(ARQUIVO_SAIDA, "w", newline="", encoding="utf-8") as arq:
        writer = csv.writer(arq)

        writer.writerow([
            "imagem",
            "classe",           # <-- nova coluna
            "tem_qrcode",
            "tem_digital",
            "color1_hex",
            "color2_hex",
            "color3_hex",
            "tem_nome",
            "tem_nome_social",
            "tem_nacionalidade"
        ])

        for img_name in imagens:
            caminho = os.path.join(PASTA_IMAGENS, img_name)
            img = cv2.imread(caminho)

            if img is None:
                print("Erro ao carregar imagem:", img_name)
                continue

            # Detectar classe baseada no nome do arquivo
            classe = obter_classe(img_name)

            # Features
            tem_qr = detectar_template(img, TEMPLATE_QRCODE)
            tem_digital = detectar_template(img, TEMPLATE_DIGITAL)

            cores_hex = extrair_cores_hex(caminho)
            texto_features = extrair_texto_features(img)

            writer.writerow([
                img_name,
                classe,  # <-- classe incluída aqui
                tem_qr,
                tem_digital,
                *cores_hex,
                texto_features["tem_nome"],
                texto_features["tem_nome_social"],
                texto_features["tem_nacionalidade"],
            ])

    print("\nFeatures extraídas com sucesso →", ARQUIVO_SAIDA)

if __name__ == "__main__":
    processar_imagens()
