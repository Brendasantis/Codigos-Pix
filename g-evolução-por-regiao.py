import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

csv_path = "C:/Users/brenda/Downloads/Req-BACEN/pix_pag_idade_valor_202110_202410_filtrado.csv"
df = pd.read_csv(csv_path)

df["QUANTIDADE"] = pd.to_numeric(df["QUANTIDADE"], errors="coerce")
df["MES"] = pd.to_datetime(df["MES"].astype(str), format="%Y%m")
df["PAG_REGIAO"] = df["PAG_REGIAO"].astype(str).str.strip().str.title()

df = df[~df["PAG_REGIAO"].str.lower().isin(["não informado", "nao informado"])]

df_grouped = df.groupby(["MES", "PAG_REGIAO"])["QUANTIDADE"].sum().unstack(fill_value=0)

plt.figure(figsize=(14, 7))
for regiao in df_grouped.columns:
    plt.plot(df_grouped.index, df_grouped[regiao], marker="o", label=regiao)

plt.xlabel("Mês")
plt.ylabel("Quantidade de Transações")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(title="Região")

def format_y(value, _):
    if value >= 1_000_000:
        return f'{value / 1_000_000:.1f}M'
    elif value >= 1_000:
        return f'{value / 1_000:.0f} mil'
    else:
        return str(int(value))

plt.gca().yaxis.set_major_formatter(FuncFormatter(format_y))

plt.tight_layout()
plt.show()
