import os
import glob

# Caminho da pasta
pasta = "./db/dataset_final_classificados"

# === ETAPA 1: apagar todos os arquivos que terminam com "_gt_segmentation.jpg" ===
arquivos_gt = glob.glob(os.path.join(pasta, "**", "*_gt_segmentation.jpg"), recursive=True)

for arquivo in arquivos_gt:
    try:
        os.remove(arquivo)
        print(f"Apagado (GT): {arquivo}")
    except Exception as e:
        print(f"Erro ao apagar {arquivo}: {e}")

print(f"\n{len(arquivos_gt)} arquivos '_gt_segmentation.jpg' foram apagados.\n")

# === ETAPA 2: apagar o excesso de .jpg, mantendo apenas 1000 ===
arquivos_jpg = sorted(glob.glob(os.path.join(pasta, "**", "*.jpg"), recursive=True))

manter = 200

if len(arquivos_jpg) > manter:
    apagar = arquivos_jpg[manter:]
    for arquivo in apagar:
        try:
            os.remove(arquivo)
            print(f"Apagado: {arquivo}")
        except Exception as e:
            print(f"Erro ao apagar {arquivo}: {e}")
    print(f"\nForam apagados {len(apagar)} arquivos. {manter} imagens foram mantidas.")
else:
    print(f"A pasta contém apenas {len(arquivos_jpg)} imagens. Nenhum arquivo foi apagado.")
