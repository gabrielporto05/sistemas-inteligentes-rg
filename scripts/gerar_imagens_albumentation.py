import cv2
import albumentations as A
import os

# Pasta de saída (onde as imagens transformadas serão salvas)
pasta_saida = "./db/new_rgs_transformadas"

# Cria a pasta de saída se não existir
os.makedirs(pasta_saida, exist_ok=True)

# Define uma transformação do Albumentation
transformacao = A.Compose([
    A.RandomBrightnessContrast(brightness_limit=0.15, contrast_limit=0.15, p=0.4),
    A.Rotate(limit=10, border_mode=cv2.BORDER_CONSTANT, value=(255,255,255), p=0.4),
    A.GaussianBlur(blur_limit=(3, 5), p=0.2),
    A.GaussNoise(var_limit=(1.0, 15.0), p=0.2),
    A.HorizontalFlip(p=0.1),
])

# Pasta de entrada (onde você colocou suas imagens)
pasta_entrada = "./db/new_rgs"

# Lista todas as imagens da pasta de entrada
arquivos = os.listdir(pasta_entrada)


# Itera sobre cada imagem da pasta
for arquivo in arquivos:
    caminho_arquivo = os.path.join(pasta_entrada, arquivo)
    imagem = cv2.imread(caminho_arquivo)
    
    # Aplica a transformação
    imagem_aumentada = transformacao(image=imagem)["image"]
    
    # Salva a imagem transformada
    caminho_saida = os.path.join(pasta_saida, "aug_" + arquivo)
    cv2.imwrite(caminho_saida, imagem_aumentada)
    