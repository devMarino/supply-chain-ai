import pandas as pd
from pathlib import Path

# ─────────────────────────────────────────────
# 1. CARREGAR OS DADOS
# ─────────────────────────────────────────────
caminho_csv = Path("dados/csv/suprimentos_abc/1_Dados_de_Estoque.csv")
df = pd.read_csv(caminho_csv, skiprows=2)
print(df.columns.tolist())
# Remove linhas vazias e a linha de total
df = df.dropna(subset=["Produto"])
df = df[df["Código"].str.startswith("PRD", na=False)]

print("=== DADOS CARREGADOS ===")
print(df[["Produto", "Qtd/Mês", "Preço Unit (R$)"]].to_string(index=False))


# ─────────────────────────────────────────────
# 2. CALCULAR CONSUMO ANUAL
# ─────────────────────────────────────────────
df["consumo_anual"] = df["Qtd/Mês"] * df["Preço Unit (R$)"] * 12
total = df["consumo_anual"].sum()

print(f"\n=== CONSUMO TOTAL ANUAL: R$ {total:,.2f} ===\n")


# ─────────────────────────────────────────────
# 3. CALCULAR CURVA ABC
# ─────────────────────────────────────────────

# Ordena do maior consumo para o menor
df = df.sort_values("consumo_anual", ascending=False).reset_index(drop=True)

# Calcula percentual de cada item sobre o total
df["pct_total"] = (df["consumo_anual"] / total) * 100

# Acumula os percentuais linha a linha
df["pct_acumulada"] = df["pct_total"].cumsum()

# Classifica com base no percentual acumulado
def classificar(pct):
    if pct <= 80:
        return "A"
    elif pct <= 95:
        return "B"
    else:
        return "C"

df["classe"] = df["pct_acumulada"].apply(classificar)


# ─────────────────────────────────────────────
# 4. EXIBIR RESULTADO
# ─────────────────────────────────────────────
print("=== CURVA ABC ===")
colunas = ["Produto", "consumo_anual", "pct_total", "pct_acumulada", "classe"]
print(df[colunas].to_string(index=False, float_format="%.1f"))

print("\n=== RESUMO POR CLASSE ===")
resumo = df.groupby("classe").agg(
    qtd_itens=("Produto", "count"),
    gasto_total=("consumo_anual", "sum")
).reset_index()
resumo["pct_gasto"] = (resumo["gasto_total"] / total * 100).round(1)
print(resumo.to_string(index=False))


# ─────────────────────────────────────────────
# 5. EXPORTAR RESULTADO
# ─────────────────────────────────────────────
saida = Path("dados/csv/suprimentos_abc/resultado_abc.csv")
df.to_csv(saida, index=False, encoding="utf-8-sig")
print(f"\nResultado salvo em: {saida}")