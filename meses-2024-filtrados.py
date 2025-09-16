import requests
import pandas as pd

meses = [
    "202401", "202402", "202403", "202404", "202405", "202406",
    "202407", "202408", "202409", "202410", "202411", "202412"
]

for mes in meses:
    print(f"Baixando e processando dados para o mês: {mes}...")

    url = f"https://olinda.bcb.gov.br/olinda/servico/Pix_DadosAbertos/versao/v1/odata/EstatisticasTransacoesPix(Database=@Database)?@Database='{mes}'"
    params = {
        "$format": "json"
    }

    response = requests.get(url, params=params)
    print("Status code:", response.status_code)
    print("URL final:", response.url)

    if response.status_code == 200:
        try:
            data = response.json()["value"]
            df = pd.DataFrame(data)

            df_filtrado = df[df["AnoMes"] == int(mes)]

            nome_arquivo = f"estatisticas_pix_{mes}_filtrado.csv"
            df_filtrado.to_csv(nome_arquivo, index=False, encoding="utf-8-sig")
            print(f"Dados salvos: {nome_arquivo}\n")

        except ValueError as e:
            print(f"Erro ao decodificar JSON para {mes}: {e}")
            print(response.text)
    else:
        print(f" Erro na requisição para {mes}: {response.status_code}")
        print(response.text)
