import cv2
import os
import csv
import numpy as np
import pytesseract
import colorgram
import re

PASTA_IMAGENS = "./db/dataset_final_classificados"
ARQUIVO_SAIDA = "./features_v3.csv"

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
    return int(np.max(res) >= limiar)


def extrair_cores_hex(image_path, n=3):
    try:
        colors = colorgram.extract(image_path, n)
        hex_colors = [rgb_to_hex((c.rgb.r, c.rgb.g, c.rgb.b)) for c in colors]
    except:
        return ["#000000"] * 3

    while len(hex_colors) < 3:
        hex_colors.append("#000000")

    return hex_colors


def extrair_texto_avancado(img):
    texto = pytesseract.image_to_string(img).upper()

    palavras = texto.split()
    qtd_palavras = len(palavras)
    qtd_numeros = len(re.findall(r"\d", texto))

    return {
        "tem_nome": int("NOME" in texto or "NAME" in texto),
        "tem_nome_social": int("NOME SOCIAL" in texto),
        "tem_nacionalidade": int("NACIONALIDADE" in texto or "BIRTH" in texto),
        "qtd_palavras": qtd_palavras,
        "qtd_numeros": qtd_numeros,
    }


def features_brilho_contraste(img_gray):
    return np.mean(img_gray), np.std(img_gray)


def extrair_bordas_normalizado(img_gray):
    edges = cv2.Canny(img_gray, 80, 200)
    qtd_bordas = np.sum(edges > 0)
    total_pixels = img_gray.shape[0] * img_gray.shape[1]

    return qtd_bordas / total_pixels


def detectar_area_foto_corrigido(img):
    h, w = img.shape[:2]
    area_img = h * w

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(img_gray, (15, 15), 0)

    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    contornos, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    maior_area_foto = 0

    for c in contornos:
        x, y, w_box, h_box = cv2.boundingRect(c)
        area = w_box * h_box

        if area > area_img * 0.90:
            continue

        ratio = h_box / max(w_box, 1)

        if 0.65 < ratio < 0.85:
            if area > maior_area_foto:
                maior_area_foto = area

    return maior_area_foto / area_img


def obter_classe(img_name: str):
    nome = img_name.lower()

    if "old_rg" in nome:
        return "old"
    if "new_rg" in nome:
        return "new"

    return "ilegivel"


def processar_imagens():
    imagens = os.listdir(PASTA_IMAGENS)

    if len(imagens) == 0:
        print(" Nenhuma imagem encontrada na pasta:", PASTA_IMAGENS)
        return

    print(f"🔍 Processando {len(imagens)} imagens...\n")

    with open(ARQUIVO_SAIDA, "w", newline="", encoding="utf-8") as arq:
        writer = csv.writer(arq)

        
        header = [
            "imagem",
            "classe",
            "tem_qrcode",
            "tem_digital",
            "color1_hex",
            "color2_hex",
            "color3_hex",
            "tem_nome",
            "tem_nome_social",
            "tem_nacionalidade",
            "qtd_palavras",
            "qtd_numeros",
            "brilho_medio",
            "contraste",
            "bordas_normalizado",
            "area_foto_normalizada",
        ]

        writer.writerow(header)

        processadas = 0

        for img_name in imagens:
            caminho = os.path.join(PASTA_IMAGENS, img_name)

            img = cv2.imread(caminho)
            if img is None:
                print(" Erro ao carregar:", img_name)
                continue

            print("→ Extraindo:", img_name)

            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            classe = obter_classe(img_name)
            tem_qr = detectar_template(img, TEMPLATE_QRCODE)
            tem_digital = detectar_template(img, TEMPLATE_DIGITAL)
            cores_hex = extrair_cores_hex(caminho)
            texto = extrair_texto_avancado(img)
            brilho, contraste = features_brilho_contraste(img_gray)
            bordas_norm = extrair_bordas_normalizado(img_gray)
            area_foto = detectar_area_foto_corrigido(img)

            writer.writerow([
                img_name,
                classe,
                tem_qr,
                tem_digital,
                *cores_hex,
                texto["tem_nome"],
                texto["tem_nome_social"],
                texto["tem_nacionalidade"],
                texto["qtd_palavras"],
                texto["qtd_numeros"],
                brilho,
                contraste,
                bordas_norm,
                area_foto,
            ])

            processadas += 1

    print(f"\n Features extraídas com sucesso ({processadas} imagens).")
    print("📁 Arquivo salvo em:", ARQUIVO_SAIDA)


if __name__ == "__main__":
    processar_imagens()
