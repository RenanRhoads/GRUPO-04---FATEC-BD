import requests
import gzip
import shutil
import os

# TODO: Alterar o link para ser lido em um arquivo CFG, para evitar futuros problemas.

path = os.path.expanduser('~\Documents\caso_full.csv.gz')
output = os.path.expanduser('~\Documents\caso_full.csv')


def atualizar():
    print("Iniciando o download do arquivo.")
    url = 'https://data.brasil.io/dataset/covid19/caso_full.csv.gz'  # link para o arquivo fornecido pelo site Brasil.IO
    r = requests.get(url, allow_redirects=True)

    with open(path, 'wb') as f:
        f.write(r.content)
        print("Download do arquivo concluido.")
        """Após o download do arquivo, salva na pasta documentos"""

    with gzip.open(path, 'rb') as f_in:
        with open(output, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        """Extrai o arquivo da fila .GZ na pasta Documentos do usuário"""
        print("Extração concluída.")
