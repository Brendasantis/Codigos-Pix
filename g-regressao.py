import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt

csv_path = "C:/Users/brenda/Downloads/Req-BACEN/pix_pag_idade_valor_202110_202410_filtrado.csv"
df = pd.read_csv(csv_path)

df["QUANTIDADE"] = pd.to_numeric(df["QUANTIDADE"], errors="coerce")
df["PAG_IDADE"] = df["PAG_IDADE"].astype(str).str.strip().str.lower()
df["PAG_REGIAO"] = df["PAG_REGIAO"].astype(str).str.strip().str.title()
df["MES"] = pd.to_datetime(df["MES"].astype(str), format="%Y%m")

faixas_invalidas = ["não se aplica", "nao se aplica", "não informado", "nao informado"]
df = df[~df["PAG_IDADE"].isin(faixas_invalidas)]
df = df[~df["PAG_REGIAO"].str.lower().isin(faixas_invalidas)]

df["MES_NUM"] = (df["MES"].dt.year - 2021) * 12 + (df["MES"].dt.month - 10)

dummies = pd.get_dummies(df[["PAG_IDADE", "PAG_REGIAO"]], drop_first=True).astype(float)

X = pd.concat([dummies, df["MES_NUM"]], axis=1)
y = df["QUANTIDADE"].astype(float)

model = LinearRegression()
model.fit(X, y)

y_pred = model.predict(X)

r2 = r2_score(y, y_pred)
rmse = np.sqrt(mean_squared_error(y, y_pred))

print(f"R²: {r2:.4f}")
print(f"RMSE: {rmse:,.2f}")

coef_df = pd.DataFrame({
    "Variável": ["Intercepto"] + list(X.columns),
    "Coeficiente": [model.intercept_] + list(model.coef_)
})

coef_df_sorted = coef_df[1:].sort_values(by="Coeficiente", ascending=False)

plt.figure(figsize=(12, 6))
plt.barh(coef_df_sorted["Variável"], coef_df_sorted["Coeficiente"])
plt.title("Coeficientes da Regressão Linear (Quantidade ~ Idade + Região + Tempo)", fontsize=13)
plt.xlabel("Coeficiente")
plt.grid(True)
plt.tight_layout()
plt.show() #amém
