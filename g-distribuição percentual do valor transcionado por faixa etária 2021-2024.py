import pandas as pd
import matplotlib.pyplot as plt

csv_path = "C:/Users/brenda/Downloads/Req-BACEN/pix_pag_idade_valor_202110_202410_filtrado.csv"
df = pd.read_csv(csv_path)

print("Valores únicos em PAG_IDADE:")
print(df["PAG_IDADE"].unique())

valores_para_remover = [
    "nao se aplica", 
    "nao informado", 
    "não se aplica", 
    "não informado",
    "Nao se aplica",
    "Nao informado",
    "NAO SE APLICA",
    "NAO INFORMADO"
]

df = df[~df["PAG_IDADE"].isin(valores_para_remover)]

df_grouped = df.groupby("PAG_IDADE")["QUANTIDADE"].sum()

print("\nFaixas etárias após filtro:")
print(df_grouped)

plt.figure(figsize=(10, 8))
colors = ["#f30000", "#007efc", "#00ff00", "#ff8000", "#ff0080", "#06067e"]
wedges, texts, autotexts = plt.pie(df_grouped.values, labels=df_grouped.index, autopct='%1.1f%%', 
                                  startangle=90, colors=colors)

plt.axis('equal')

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')

plt.tight_layout()
plt.show()