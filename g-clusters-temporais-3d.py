import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D

csv_path = "C:/Users/brenda/Downloads/Req-BACEN/pix_pag_idade_valor_202110_202410_filtrado.csv"
df = pd.read_csv(csv_path)

df_mensal = df.groupby("AnoMes").agg({
    "VALOR": "sum",
    "QUANTIDADE": "sum"
}).sort_index()

df_mensal["VALOR_MEDIA_MOVEL"] = df_mensal["VALOR"].rolling(window=3, min_periods=1).mean()
df_mensal["QTD_MEDIA_MOVEL"] = df_mensal["QUANTIDADE"].rolling(window=3, min_periods=1).mean()
df_mensal["VALOR_DIFF"] = df_mensal["VALOR"].diff().fillna(0)
df_mensal["QTD_DIFF"] = df_mensal["QUANTIDADE"].diff().fillna(0)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_mensal)

pca = PCA(n_components=3)
X_pca = pca.fit_transform(X_scaled)

kmeans = KMeans(n_clusters=4, random_state=42)
clusters = kmeans.fit_predict(X_pca)
df_mensal["Cluster"] = clusters

descricao_componentes = {
    "PCA1": "PCA1 - Volume Total (VALOR + QUANTIDADE)",
    "PCA2": "PCA2 - Variação Mensal (DIFs)",
    "PCA3": "PCA3 - Tendência Suavizada (Médias móveis)"
}

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

scatter = ax.scatter(X_pca[:, 0], X_pca[:, 1], X_pca[:, 2], 
                     c=clusters, cmap='tab10', s=80)

for i, label in enumerate(df_mensal.index):
    ax.text(X_pca[i, 0], X_pca[i, 1], X_pca[i, 2], str(label), fontsize=8)

ax.set_xlabel(descricao_componentes["PCA1"], labelpad=15)
ax.set_ylabel(descricao_componentes["PCA2"], labelpad=15)
ax.set_zlabel(descricao_componentes["PCA3"], labelpad=15)

plt.tight_layout()
plt.show()
