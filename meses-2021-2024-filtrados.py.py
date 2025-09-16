import requests
import pandas as pd
import time

meses = [f"{ano}{mes:02d}" for ano in range(2021, 2025) for mes in range(1, 13)
         if not (ano == 2021 and mes < 10) and not (ano == 2024 and mes > 10)]

df_total = pd.DataFrame()

for mes in meses:
    print(f"Iniciando requisição para {mes}...")

    url_base = (
        f"https://olinda.bcb.gov.br/olinda/servico/Pix_DadosAbertos/versao/v1/odata/"
        f"EstatisticasTransacoesPix(Database=@Database)?@Database='{mes}'"
        f"&$format=json&$select=PAG_REGIAO,PAG_IDADE,VALOR,QUANTIDADE,AnoMes"
    )

    while True:
        try:
            next_url = url_base
            visited_urls = set()
            df_mes_completo = pd.DataFrame()

            while next_url and next_url not in visited_urls:
                visited_urls.add(next_url)

                response = requests.get(next_url) 
                if response.status_code == 200:
                    data = response.json()
                    registros = data.get("value", [])
                    df_page = pd.DataFrame(registros)

                    if "AnoMes" in df_page.columns:
                        df_page = df_page[df_page["AnoMes"] == int(mes)]

                    df_page["MES"] = mes
                    df_mes_completo = pd.concat([df_mes_completo, df_page], ignore_index=True)
                    next_url = data.get("@odata.nextLink")

                else:
                    print(f"Erro {response.status_code} em {mes}. Nova tentativa em 30s...")
                    time.sleep(30)
                    break 

            if not df_mes_completo.empty:
                print(f"{len(df_mes_completo)} registros coletados para {mes}")
                df_mes_completo.to_csv(f"pix_mes_{mes}.csv", index=False, encoding="utf-8-sig")
                df_total = pd.concat([df_total, df_mes_completo], ignore_index=True)
            else:
                print(f"Nenhum dado coletado para {mes}, tentando novamente em 60s...")
                time.sleep(60)
                continue  

            break 

        except Exception as e:
            print(f"Erro fatal ao requisitar {mes}: {e}")
            print("Esperando 60 segundos antes de tentar novamente...")
            time.sleep(60)

output_csv = "pix_pag_idade_valor_202110_202410_filtrado.csv"
df_total.to_csv(output_csv, index=False, encoding="utf-8-sig")
print(f"\nArquivo final salvo com {len(df_total)} linhas: {output_csv}")

# glória a Deus
print("\nRegistros por mês coletados:")
print(df_total["MES"].value_counts().sort_index())
