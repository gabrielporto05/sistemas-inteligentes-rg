import cv2
import csv
import json
import os

qtd_imgs = 1000

image_base = './imgs/rg_new_exemple_borrada.jpg'
csv_arquivo = './utils/dados_fakes.csv'
json_arquivo = './utils/posicoes.json'

pasta_saida = './db/NEW_RG_FRENTE'

def gerar_imgs(qtd_imgs, image_base, csv_arquivo, json_arquivo, pasta_saida):
    # Fonte e estilo
    tamanho_fonte = 0.7
    cor_fonte = (0, 0, 0)  # preto
    espessura = 1
    fonte = cv2.FONT_HERSHEY_SIMPLEX

    # Cria a pasta de saída se não existir
    os.makedirs(pasta_saida, exist_ok=True)

    # Lê os dados do CSV
    dados_csv = []
    with open(csv_arquivo, newline='', encoding='utf-8') as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            dados_csv.append(linha)

    # Lê as posições do JSON
    with open(json_arquivo, 'r', encoding='utf-8') as f:
        posicoes = json.load(f)

    # Garante que não gere mais imagens do que existem dados
    qtd_imgs = min(qtd_imgs, len(dados_csv))

    # Loop para gerar imagens
    for i, dado in enumerate(dados_csv[:qtd_imgs], start=1):
        img = cv2.imread(image_base)

        if img is None:
            print(f"❌ Erro ao carregar a imagem base: {image_base}")
            break

        # Escreve cada campo na posição certa
        for campo, pos in posicoes.items():
            valor = dado.get(campo, "")
            if valor:
                cv2.putText(img, str(valor), tuple(pos), fonte, tamanho_fonte, cor_fonte, espessura, cv2.LINE_AA)

        # Salva a imagem
        nome_saida = os.path.join(pasta_saida, f"rg_{i:04d}.jpg")
        cv2.imwrite(nome_saida, img)
        print(f"✅ Imagem gerada: {nome_saida}")

    print(f"\n{qtd_imgs} imagens geradas com sucesso em '{pasta_saida}'.")

if __name__ == "__main__":
    gerar_imgs(qtd_imgs, image_base, csv_arquivo, json_arquivo, pasta_saida)
