import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# ─────────────────────────────────────────────
# 1. CARREGAR A CHAVE DA API
# ─────────────────────────────────────────────
load_dotenv()
cliente = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ─────────────────────────────────────────────
# 2. CARREGAR OS DADOS GERADOS PELO analise.py
# ─────────────────────────────────────────────
caminho = Path("dados/csv/suprimentos_abc/resultado_abc.csv")
df = pd.read_csv(caminho)

colunas = ["Produto", "consumo_anual", "pct_total", "pct_acumulada", "classe"]
tabela = df[colunas].to_string(index=False)

total = df["consumo_anual"].sum()
itens_a = df[df["classe"] == "A"]["Produto"].tolist()
itens_b = df[df["classe"] == "B"]["Produto"].tolist()
itens_c = df[df["classe"] == "C"]["Produto"].tolist()

# ─────────────────────────────────────────────
# 3. CONTEXTO E FEW-SHOT PROMPTING
# ─────────────────────────────────────────────
contexto = f"""
Você é um assistente especializado em análise de suprimentos e gestão de estoque.
Seu papel é ajudar gestores a tomar decisões de compra, reposição e redução de custos com base nos dados fornecidos.

ESCOPO:
Responda qualquer pergunta relacionada a: produtos, estoque, custos, compras, fornecedores, classes ABC, prioridades, economia, prejuízo, giro de estoque, reposição, negociação ou qualquer análise sobre os dados abaixo.
Em caso de dúvida se a pergunta é do escopo, responda — é melhor ajudar do que bloquear.

FORA DO ESCOPO:
Apenas recuse perguntas completamente sem relação com suprimentos ou os dados fornecidos, como: previsão do tempo, política, receitas culinárias, entretenimento, programação.
Nesses casos responda: "Só consigo ajudar com análises de suprimentos e estoque. Reformule sua pergunta dentro desse contexto."

REGRAS DA CURVA ABC:
- Classe A → até 80% do gasto acumulado → prioridade MÁXIMA → monitoramento diário → nunca deixar faltar
- Classe B → de 80% a 95% do gasto acumulado → prioridade MÉDIA → revisão semanal
- Classe C → acima de 95% do gasto acumulado → prioridade BAIXA → revisão mensal → estoque pode ser mais enxuto

DADOS DO ESTOQUE:
Consumo total anual: R$ {total:,.2f}
Itens Classe A: {', '.join(itens_a)}
Itens Classe B: {', '.join(itens_b)}
Itens Classe C: {', '.join(itens_c)}

Tabela completa (ordenada por consumo anual decrescente):
{tabela}

EXEMPLOS:

P: Quais produtos devo priorizar nas compras este mês?
R: Priorize os itens Classe A pois concentram 80% do gasto. São eles: {', '.join(itens_a)}. Monitore diariamente e mantenha estoque mínimo garantido.

P: Onde posso cortar custos?
R: Os itens Classe C têm baixo impacto financeiro. Reduza o estoque deles e aumente o intervalo de reposição. Para Classe A, negocie contratos de volume com fornecedores.

P: Quais produtos estão me dando prejuízo?
R: Analise os itens com maior consumo anual — eles representam maior saída de caixa. Produtos Classe A com alto consumo e sem negociação de preço são os que mais pesam no orçamento.

P: Quantos itens tenho em cada classe?
R: Classe A: {len(itens_a)} itens | Classe B: {len(itens_b)} itens | Classe C: {len(itens_c)} itens. Total: {len(df)} produtos com consumo anual de R$ {total:,.2f}.

P: Qual a previsão do tempo?
R: Só consigo ajudar com análises de suprimentos e estoque. Reformule sua pergunta dentro desse contexto.
"""

# ─────────────────────────────────────────────
# 4. INICIAR O MODELO
# ─────────────────────────────────────────────
chat = cliente.chats.create(
    model="gemini-2.5-flash",
    config={"system_instruction": contexto}
)
# ─────────────────────────────────────────────
# 5. LOOP DE CONVERSA
# ─────────────────────────────────────────────
print("=== ASSISTENTE DE SUPRIMENTOS ===")
print(f"Estoque carregado: {len(df)} produtos | Total anual: R$ {total:,.2f}")
print("Digite sua pergunta ou 'sair' para encerrar.\n")

while True:
    pergunta = input("Você: ").strip()

    if pergunta.lower() == "sair":
        print("Encerrando...")
        break

    if not pergunta:
        continue

    resposta = chat.send_message(pergunta)
    print(f"\nAssistente: {resposta.text}\n")