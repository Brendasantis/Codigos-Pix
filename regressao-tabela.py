import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

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

coef_table = pd.concat(
    [coef_df.loc[[0]], coef_df[1:].sort_values("Coeficiente", ascending=False)],
    ignore_index=True
)

coef_table_abs = pd.concat(
    [coef_df.loc[[0]], coef_df[1:].reindex(coef_df[1:]["Coeficiente"].abs().sort_values(ascending=False).index)],
    ignore_index=True
)

def classifica_variavel(v):
    if v == "Intercepto":
        return "Intercepto"
    if v == "MES_NUM":
        return "Tempo"
    if v.startswith("PAG_IDADE_"):
        return "PAG_IDADE"
    if v.startswith("PAG_REGIAO_"):
        return "PAG_REGIAO"
    return "Outro"

def extrai_categoria(v):
    if v.startswith("PAG_IDADE_"):
        return v.replace("PAG_IDADE_", "")
    if v.startswith("PAG_REGIAO_"):
        return v.replace("PAG_REGIAO_", "")
    return ""

coef_table["Grupo"] = coef_table["Variável"].apply(classifica_variavel)
coef_table["Categoria"] = coef_table["Variável"].apply(extrai_categoria)

def categoria_referencia(serie_original, prefixo, df_dummies_cols):
    presentes = []
    for c in df_dummies_cols:
        if c.startswith(prefixo + "_"):
            presentes.append(c.split(prefixo + "_", 1)[1])
    todos = pd.Series(serie_original.unique()).tolist()
    ref = [x for x in todos if x not in presentes]
    return ref[0] if len(ref) > 0 else None

ref_idade = categoria_referencia(df["PAG_IDADE"], "PAG_IDADE", X.columns)
ref_regiao = categoria_referencia(df["PAG_REGIAO"], "PAG_REGIAO", X.columns)

referencias_df = pd.DataFrame({
    "Grupo": ["PAG_IDADE", "PAG_REGIAO"],
    "Categoria de referência (baseline)": [ref_idade, ref_regiao]
})

metrics_df = pd.DataFrame({"Métrica": ["R²", "RMSE"], "Valor": [r2, rmse]})

print("\n=== COEFICIENTES (ordenado) ===")
print(coef_table.to_string(index=False, formatters={"Coeficiente": "{:,.2f}".format}))
print("\n=== COEFICIENTES por |valor| (ordenado) ===")
print(coef_table_abs.to_string(index=False, formatters={"Coeficiente": "{:,.2f}".format}))
print("\n=== REFERÊNCIAS (baseline) ===")
print(referencias_df.to_string(index=False))
print("\n=== MÉTRICAS ===")
print(metrics_df.to_string(index=False, formatters={"Valor": "{:,.4f}".format}))

# só salvando
coef_table.to_csv("coeficientes_regressao.csv", index=False, encoding="utf-8-sig")
try:
    coef_table.to_excel("coeficientes_regressao.xlsx", index=False)
    with pd.ExcelWriter("saida_regressao.xlsx") as w:
        coef_table.to_excel(w, sheet_name="Coeficientes", index=False)
        coef_table_abs.to_excel(w, sheet_name="Coeficientes_abs", index=False)
        referencias_df.to_excel(w, sheet_name="Referencias", index=False)
        metrics_df.to_excel(w, sheet_name="Metricas", index=False)
    print("\nArquivos salvos: coeficientes_regressao.csv, coeficientes_regressao.xlsx, saida_regressao.xlsx")
except Exception as e:
    print("\n[AVISO] Não foi possível salvar XLSX.")
    print(f"Detalhe: {e}")
    print("CSV gerado: coeficientes_regressao.csv")
