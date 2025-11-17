import os
import shutil
import random
import unicodedata
from faker import Faker

# Pastas de origem
pasta_new = "./db/new_rgs_transformadas"
pasta_old = "./db/old_rgs"

# Pasta final (saída)
pasta_final = "./db/dataset_final"

# Criar pasta final
os.makedirs(pasta_final, exist_ok=True)

# Função para remover acentos dos nomes
def remover_acentos(txt):
    return unicodedata.normalize("NFKD", txt).encode("ASCII", "ignore").decode("utf-8")

# Gerador de nomes fake
fake = Faker("pt_BR")

# Função para gerar nome aleatório
def gerar_nome():
    return remover_acentos(fake.first_name() + fake.last_name()).replace(" ", "_")

# Coletar todos os arquivos das duas pastas
arquivos = []

for pasta in [pasta_new, pasta_old]:
    for arquivo in os.listdir(pasta):
        caminho = os.path.join(pasta, arquivo)
        if os.path.isfile(caminho):
            arquivos.append(caminho)

# Embaralhar
random.shuffle(arquivos)

print(f"Total de imagens encontradas: {len(arquivos)}")

# Copiar e renomear
for idx, img_path in enumerate(arquivos, start=1):
    nome_aleatorio = gerar_nome()
    novo_nome = f"{nome_aleatorio}_rg.jpg"
    destino = os.path.join(pasta_final, novo_nome)

    shutil.copy(img_path, destino)

    print(f"✔ {img_path} → {destino}")

print("\n🎉 Dataset final criado em ./db/dataset_final")
