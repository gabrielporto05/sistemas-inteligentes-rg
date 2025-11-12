import cv2
import csv
import json
import os
import sys

qtd_imgs = 55

image_base = 'img_teste1.png'
csv_arquivo = 'dados_fakes.csv'
json_arquivo = 'posicoes.json'

pasta_saida = 'imgs_geradas'

def gerar_imgs(qtd_imgs, image_base, csv_arquivo, json_arquivo, pasta_saida):
  tamanho_fonte = 1
  cor_fonte = (0, 0, 0)
  font = cv2.FONT_HERSHEY_SIMPLEX

  dados_csv = []
  with open(csv_arquivo, newline='', encoding='utf-8') as f:
    leitor = csv.DictReader(f)
    for linha in leitor:
      print(linha)
      dados_csv.append(linha)

  with open(json_arquivo, 'r') as f:
    dados_json = json.load(f)
    print(dados_json)

  qtd_imgs = min(qtd_imgs, len(dados_json))

  # insere dados na imagem

  for id_item, dado in enumerate(dados_csv[:qtd_imgs], start = 1):
    img = cv2.imread(image_base)
    print(dado)
    cv2.putText(img, dado['Nome Completo'], tuple(dados_json['nome_completo']),
                font, tamanho_fonte, cor_fonte, 2, cv2.LINE_AA)

    pasta_saida = '/content/imgs_geradas'

    nome_saida = os.path.join(pasta_saida, f'img_{id_item}.jpg')
    cv2.imwrite(nome_saida, img)