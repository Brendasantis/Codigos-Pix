import pandas as pd
import matplotlib.pyplot as plt

csv_path = "C:/Users/brenda/Downloads/Req-BACEN/pix_pag_idade_valor_202110_202410_filtrado.csv"
df = pd.read_csv(csv_path)

df["QUANTIDADE"] = pd.to_numeric(df["QUANTIDADE"], errors="coerce")
df["MES"] = pd.to_datetime(df["MES"].astype(str), format="%Y%m")
df["PAG_IDADE"] = df["PAG_IDADE"].astype(str).str.strip().str.lower()

faixas_invalidas = ["não se aplica", "nao se aplica", "não informado", "nao informado"]
df = df[~df["PAG_IDADE"].isin(faixas_invalidas)]

df_grouped = df.groupby(["MES", "PAG_IDADE"])["QUANTIDADE"].sum().unstack(fill_value=0)

plt.figure(figsize=(14, 7))
for idade in df_grouped.columns:
    plt.plot(df_grouped.index, df_grouped[idade], marker="o", label=idade)

plt.title("Evolução mensal da quantidade de transações por faixa etária (2021-10 a 2024-10)", fontsize=14)
plt.xlabel("Mês")
plt.ylabel("Quantidade de Transações")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(title="Faixa Etária", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.show()
