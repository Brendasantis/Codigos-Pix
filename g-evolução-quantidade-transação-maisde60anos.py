import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

csv_path = "C:/Users/brenda/Downloads/Req-BACEN/pix_pag_idade_valor_202110_202410_filtrado.csv"
df = pd.read_csv(csv_path)

df["QUANTIDADE"] = pd.to_numeric(df["QUANTIDADE"], errors="coerce")
df["MES"] = df["MES"].astype(str)
df["PAG_IDADE"] = df["PAG_IDADE"].astype(str).str.strip().str.lower()

df_60_plus = df[df["PAG_IDADE"].str.contains("mais de 60")]

df_mensal = df_60_plus.groupby("MES")["QUANTIDADE"].sum().reset_index()
df_mensal = df_mensal.sort_values("MES")
df_mensal["MES"] = pd.to_datetime(df_mensal["MES"], format="%Y%m")

plt.figure(figsize=(12, 6))
plt.plot(df_mensal["MES"], df_mensal["QUANTIDADE"], marker="o", color="darkred", label="Mais de 60 anos")

plt.xlabel("Mês")
plt.ylabel("Quantidade de Transações")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()

def format_y(value, _):
    if value >= 1_000_000:
        return f'{value/1_000_000:.1f}M'
    elif value >= 1_000:
        return f'{value/1_000:.0f} mil'
    else:
        return str(int(value))

plt.gca().yaxis.set_major_formatter(FuncFormatter(format_y))

plt.tight_layout()
plt.show()
