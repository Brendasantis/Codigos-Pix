import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

csv_path = "C:/Users/brenda/Downloads/Req-BACEN/pix_pag_idade_valor_202110_202410_filtrado.csv"
df = pd.read_csv(csv_path)

df["QUANTIDADE"] = pd.to_numeric(df["QUANTIDADE"], errors="coerce")
df["PAG_IDADE"] = df["PAG_IDADE"].astype(str).str.strip().str.lower()
df["PAG_REGIAO"] = df["PAG_REGIAO"].astype(str).str.strip().str.title()

faixas_invalidas = ["não informado", "nao informado", "não se aplica", "nao se aplica"]
df = df[~df["PAG_IDADE"].isin(faixas_invalidas)]
df = df[~df["PAG_REGIAO"].str.lower().isin(faixas_invalidas)]

df_grouped = df.groupby(["PAG_IDADE", "PAG_REGIAO"])["QUANTIDADE"].sum().unstack(fill_value=0)

idade_order = df_grouped.sum(axis=1).sort_values(ascending=False).index
regiao_order = df_grouped.sum(axis=0).sort_values(ascending=False).index

plt.figure(figsize=(12, 6))
sns.heatmap(
    df_grouped.loc[idade_order, regiao_order],
    annot=True,
    fmt=",.0f",
    cmap="YlGnBu",
    linewidths=.5,
    cbar=False 
)

plt.title("Quantidade total de transações por faixa etária e região (2021-10 a 2024-10)", fontsize=14)
plt.xlabel("Região")
plt.ylabel("Faixa Etária")
plt.tight_layout()
plt.show()
