import pandas as pd
import matplotlib.pyplot as plt

csv_path = "C:/Users/brenda/Downloads/Req-BACEN/graficos/estatisticas_pix_202401_traduzido_com_formula.csv"
df = pd.read_csv(csv_path)

df["VALOR"] = pd.to_numeric(df["VALOR"], errors="coerce")

df_grouped = df.groupby("NATUREZA")["VALOR"].sum().reset_index()
df_grouped["VALOR_MILHOES"] = df_grouped["VALOR"] / 1_000_000

plt.figure(figsize=(12, 6))
bars = plt.bar(df_grouped["NATUREZA"], df_grouped["VALOR_MILHOES"])

plt.title("Valor total transferido por Natureza (Pix - Jan/2024)")
plt.xlabel("Natureza da Transação")
plt.ylabel("Valor Transferido (milhões de R$)")
plt.xticks(rotation=45)
plt.grid(axis="y")
plt.tight_layout()
plt.show()
