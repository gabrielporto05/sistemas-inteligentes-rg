import csv
import random
from faker import Faker
from datetime import datetime, timedelta

def gerar_csv(qtd_itens, nome_arquivo="dados_fakes.csv"):
    fake = Faker("pt_BR")  
    sexos = ["M", "F"]
    cidades = [
        "Almenara", "Belo Horizonte", "Rugim", "Arinos",
        "São Paulo", "Pedra Grande", "Porto Seguro"
    ]

    with open(nome_arquivo, mode="w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow([
            "nome",
            "nome_social",
            "cpf",
            "data_nascimento",
            "naturalidade",
            "sexo",
            "nacionalidade",
            "data_validade"
        ])

        for _ in range(qtd_itens):
            nome = fake.name()
            nome_social = nome  
            cpf = fake.cpf()
            data_nascimento = fake.date_of_birth(minimum_age=18, maximum_age=80).strftime("%d/%m/%Y")
            naturalidade = random.choice(cidades)
            sexo = random.choice(sexos)
            nacionalidade = "Brasileiro(a)"
            
            data_validade = (datetime.now() + timedelta(days=random.randint(365, 3650))).strftime("%d/%m/%Y")

            escritor.writerow([
                nome,
                nome_social,
                cpf,
                data_nascimento,
                naturalidade,
                sexo,
                nacionalidade,
                data_validade
            ])

    print(f"{qtd_itens} registros salvos em '{nome_arquivo}'")

if __name__ == "__main__":
    gerar_csv(1000)
