import cv2
import os
import csv
import numpy as np
import pytesseract
import colorgram

# --- CONFIGURAÇÕES --- #
PASTA_IMAGENS = "./db/dataset_final"
ARQUIVO_SAIDA = "./features.csv"

# Templates para detectar QR Code e digital (caso tenha)
TEMPLATE_QRCODE = "./utils/template_qr.png"
TEMPLATE_DIGITAL = "./utils/template_digital.png"


# --- FUNÇÕES DE FEATURES --- #
def detectar_template(img, template_file, limiar=0.5):
    if not os.path.exists(template_file):
        return 0  # Template não existe → pula

    template = cv2.imread(template_file, 0)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Se o template for maior que a imagem → não dá para comparar
    if img_gray.shape[0] < template.shape[0] or img_gray.shape[1] < template.shape[1]:
        return 0

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    valor = np.max(res)

    return 1 if valor >= limiar else 0



def extrair_cores(image_path, n=3):
    colors = colorgram.extract(image_path, n)
    vetor = []

    for c in colors:
        vetor.extend([c.rgb.r, c.rgb.g, c.rgb.b])

    # garante tamanho fixo
    while len(vetor) < 9:
        vetor.append(0)

    return vetor


def proporcao_cor(img, cor_alvo, tolerancia=30):
    lower = np.array([max(0, c - tolerancia) for c in cor_alvo])
    upper = np.array([min(255, c + tolerancia) for c in cor_alvo])

    mask = cv2.inRange(img, lower, upper)
    return np.sum(mask > 0) / (img.shape[0] * img.shape[1])


def extrair_texto(img):
    texto = pytesseract.image_to_string(img).upper()
    return {
        "tem_NAME": int("NAME" in texto),
        "tem_SOCIAL": int("SOCIAL" in texto),
        "tem_NACIONALIDADE": int("NACIONALIDADE" in texto)
    }


# --- PIPELINE PRINCIPAL --- #
def processar_imagens():
    imagens = os.listdir(PASTA_IMAGENS)

    with open(ARQUIVO_SAIDA, "w", newline="", encoding="utf-8") as arq:
        writer = csv.writer(arq)

        writer.writerow([
            "imagem",
            "tem_qrcode",
            "tem_digital",
            "color1_r","color1_g","color1_b",
            "color2_r","color2_g","color2_b",
            "color3_r","color3_g","color3_b",
            "prop_amarelo","prop_azul","prop_verde",
            "tem_NAME","tem_SOCIAL","tem_NACIONALIDADE",
            "classe"
        ])

        for img_name in imagens:
            caminho = os.path.join(PASTA_IMAGENS, img_name)
            img = cv2.imread(caminho)

            # QR code e digital
            tem_qr = detectar_template(img, TEMPLATE_QRCODE)
            tem_digital = detectar_template(img, TEMPLATE_DIGITAL)

            # Cores dominantes
            cores = extrair_cores(caminho)

            # Proporção de algumas cores típicas do RG
            prop_amarelo = proporcao_cor(img, (255, 255, 0))
            prop_azul = proporcao_cor(img, (0, 0, 255))
            prop_verde = proporcao_cor(img, (0, 255, 0))

            # OCR
            texto_features = extrair_texto(img)

            # Classe do arquivo (pelo nome da pasta, editável)
            classe = "novo" if "new" in PASTA_IMAGENS else "antigo"

            writer.writerow([
                img_name,
                tem_qr,
                tem_digital,
                *cores,
                prop_amarelo,
                prop_azul,
                prop_verde,
                texto_features["tem_NAME"],
                texto_features["tem_SOCIAL"],
                texto_features["tem_NACIONALIDADE"],
                classe
            ])

    print("Features extraídas com sucesso →", ARQUIVO_SAIDA)


if __name__ == "__main__":
    processar_imagens()
