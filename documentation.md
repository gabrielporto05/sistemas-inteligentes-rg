# Criando ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
pip install faker albumentations opencv-python numpy pytesseract
python seu_script.py
```

# RG antigo VS RG novo

## Se não tiver DIGITAL e tiver QRcode

- novo
- nomes dos campos possuindo a versao so nome do mesmo em ingles (nome/name)
- nome social
- nacionalidade
- cores dominantes sendo amarelo e azul

## Se tiver DIGITAL

- antigo

script de suzana para identificar as cores dominantes :

https://suzana-svm.medium.com/extraindo-cores-dominantes-de-uma-imagem-com-python-b277ee948213
