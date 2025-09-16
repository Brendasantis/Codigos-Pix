import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("C:/Users/brenda/Downloads/Req-BACEN/pix_pag_idade_valor_202110_202410_filtrado.csv")

df["QUANTIDADE"] = pd.to_numeric(df["QUANTIDADE"], errors="coerce")
df["VALOR"] = pd.to_numeric(df["VALOR"], errors="coerce")
df["VALOR_MEDIO"] = df["VALOR"] / df["QUANTIDADE"]
df["MES"] = pd.to_datetime(df["MES"].astype(str), format="%Y%m")
df["MES_NUM"] = (df["MES"].dt.year - 2021) * 12 + (df["MES"].dt.month - 10)

df["PAG_IDADE"] = df["PAG_IDADE"].astype(str).str.strip().str.lower()
df["PAG_REGIAO"] = df["PAG_REGIAO"].astype(str).str.strip().str.title()
invalidos = ["não informado", "nao informado", "não se aplica", "nao se aplica"]
df = df[~df["PAG_IDADE"].isin(invalidos)]
df = df[~df["PAG_REGIAO"].str.lower().isin(invalidos)]

dummies = pd.get_dummies(df[["PAG_IDADE", "PAG_REGIAO"]], drop_first=True)
df_corr = pd.concat([df[["QUANTIDADE", "VALOR", "VALOR_MEDIO", "MES_NUM"]], dummies], axis=1)

correlation_matrix = df_corr.corr()

plt.figure(figsize=(16, 10))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5)
plt.xticks(rotation=45, ha="right")
plt.yticks(rotation=0)
plt.tight_layout()
plt.show() #bomdms
