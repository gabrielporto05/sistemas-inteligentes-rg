import os
import glob

# Caminho da pasta
pasta = "./db/RG_Frente"

# Busca todos os arquivos .txx dentro da pasta (inclusive subpastas)
arquivos = glob.glob(os.path.join(pasta, "**", "*.txt"), recursive=True)

# Remove cada arquivo encontrado
for arquivo in arquivos:
    try:
        os.remove(arquivo)
        print(f"Apagado: {arquivo}")
    except Exception as e:
        print(f"Erro ao apagar {arquivo}: {e}")

print(f"\n{len(arquivos)} arquivos .txx foram apagados.")
