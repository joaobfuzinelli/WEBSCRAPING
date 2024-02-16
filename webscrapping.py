import requests
from bs4 import BeautifulSoup
import time

# Lista de URLs
urls = [  # 2020
    'https://dadosabertos.pgfn.gov.br/2020_trimestre_01/Dados_abertos_Nao_Previdenciario.zip',
    'https://dadosabertos.pgfn.gov.br/2020_trimestre_02/Dados_abertos_Nao_Previdenciario.zip',
    'https://dadosabertos.pgfn.gov.br/2020_trimestre_03/Dados_abertos_Nao_Previdenciario.zip',
    'https://dadosabertos.pgfn.gov.br/2020_trimestre_04/Dados_abertos_Nao_Previdenciario.zip',
    # 2021
    'https://dadosabertos.pgfn.gov.br/2021_trimestre_01/Dados_abertos_Nao_Previdenciario.zip',
    'https://dadosabertos.pgfn.gov.br/2021_trimestre_02/Dados_abertos_Nao_Previdenciario.zip',
    'https://dadosabertos.pgfn.gov.br/2021_trimestre_03/Dados_abertos_Nao_Previdenciario.zip',
    'https://dadosabertos.pgfn.gov.br/2021_trimestre_04/Dados_abertos_Nao_Previdenciario.zip',
    # 2022
    'https://dadosabertos.pgfn.gov.br/2022_trimestre_01/Dados_abertos_Nao_Previdenciario.zip',
    'https://dadosabertos.pgfn.gov.br/2022_trimestre_02/Dados_abertos_Nao_Previdenciario.zip',
    'https://dadosabertos.pgfn.gov.br/2022_trimestre_03/Dados_abertos_Nao_Previdenciario.zip',
    'https://dadosabertos.pgfn.gov.br/2022_trimestre_04/Dados_abertos_Nao_Previdenciariozip.zip',
    # 2023
    'https://dadosabertos.pgfn.gov.br/2023_trimestre_01/Dados_abertos_Nao_Previdenciario.zip',
    'https://dadosabertos.pgfn.gov.br/2023_trimestre_02/Dados_abertos_Nao_Previdenciario.zip',
    'https://dadosabertos.pgfn.gov.br/2023_trimestre_03/Dados_abertos_Nao_Previdenciario.zip',
    'https://dadosabertos.pgfn.gov.br/2023_trimestre_04/Dados_abertos_Nao_Previdenciario.zip'
]

# Headers corrigidos
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

while True:
    # Loop para baixar os arquivos .zip
    for url in urls:
        response = requests.get(url, headers=headers, stream=True)

        # Verificar se a solicitação foi bem-sucedida
        if response.status_code == 200:
            # Processar ou salvar o conteúdo, se necessário
            print(f"Download bem-sucedido para: {url}")
            with open(f"Dados_abertos_{url.split('/')[-2]}.zip", 'wb') as f:
                for chunk in response.iter_content(chunk_size=128):
                    f.write(chunk)
        else:
            print(f"Falha no download para: {url}")

    # Extrair links mais recentes
    novos_links = set()
    for url in urls:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links_atuais = set(a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.zip'))
            novos_links.update(links_atuais)

    # Comparar com os links existentes
    links_existentes = set(urls)
    links_adicionados = novos_links - links_existentes

    if links_adicionados:
        print("Novas pastas adicionadas:")
        for link_adicionado in links_adicionados:
            print(link_adicionado)

        # Atualizar a lista de URLs com os novos links
        urls.extend(links_adicionados)

    # Aguardar antes da próxima verificação (por exemplo, 1 hora)
    time.sleep(3600)
