# Análise de Suprimentos com IA

Sistema de análise de estoque com classificação **Curva ABC** automatizada e **chatbot inteligente** para suporte à decisão de compras, desenvolvido em Python com integração à API do Google Gemini.

> Este projeto foi desenvolvido com auxílio do assistente de IA **Claude (Anthropic)**, seguindo boas práticas de arquitetura de software e engenharia de prompts. O objetivo é demonstrar na prática o uso de **LLMs**, **IA Generativa**, **Few-shot prompting** e integração com APIs externas aplicados a um problema real de supply chain.

---

## Objetivo de aprendizado

Este projeto foi construído para aprender e demonstrar na prática:

- **Curva ABC** — classificação de estoque por impacto financeiro
- **LLM e IA Generativa** — integração com modelo de linguagem via API
- **Few-shot prompting** — técnica de direcionamento de comportamento da IA com exemplos
- **API com boas práticas** — autenticação segura com variáveis de ambiente
- **Pandas** — análise e manipulação de dados tabulares com Python
- **.env** — separação de configurações sensíveis do código-fonte

---

## Funcionalidades

- Conversão automática de arquivos `.xlsx` para `.csv`
- Cálculo da Curva ABC a partir dos dados de estoque
- Geração de relatório com classificação por produto
- Chatbot em linguagem natural para consultas sobre o estoque
- Contexto injetado dinamicamente na IA com os dados reais do estoque

---

## Estrutura do projeto

```
analiseSuprimentos-IA/
│
├── dados/
│   ├── excel/
│   │   └── suprimentos_abc.xlsx       # Planilha de entrada
│   └── csv/
│       └── suprimentos_abc/           # CSVs gerados automaticamente
│           ├── 1_Dados_de_Estoque.csv
│           └── resultado_abc.csv
│
├── scripts/
│   ├── converter.py                   # Converte xlsx → csv
│   ├── analise.py                     # Calcula Curva ABC com Pandas
│   └── chatbot.py                     # Chatbot com Gemini API
│
├── .env                               # Chave da API (não versionado)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Pré-requisitos

- Python 3.10 ou superior
- Conta no [Google AI Studio](https://aistudio.google.com) para obter a chave da API Gemini (gratuito)

---

## Como usar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/analiseSuprimentos-IA.git
cd analiseSuprimentos-IA
```

### 2. Crie e ative o ambiente virtual

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure a chave da API

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```
GEMINI_API_KEY=sua_chave_aqui
```

Para obter sua chave gratuita:
1. Acesse [aistudio.google.com](https://aistudio.google.com)
2. Clique em **Get API Key**
3. Crie um novo projeto e copie a chave gerada

### 5. Adicione sua planilha

Coloque seu arquivo `.xlsx` na pasta `dados/excel/`. O arquivo deve conter as colunas:
`Código`, `Produto`, `Categoria`, `Qtd/Mês`, `Preço Unit (R$)`

### 6. Execute na ordem

```bash
# Converte xlsx para csv
python scripts/converter.py dados/excel/suprimentos_abc.xlsx

# Calcula a Curva ABC
python scripts/analise.py

# Inicia o chatbot
python scripts/chatbot.py
```

---

## Conceitos aplicados

### Curva ABC
Técnica de priorização onde os produtos são ordenados por consumo anual e classificados:
- **Classe A** → até 80% do gasto acumulado → monitoramento diário
- **Classe B** → de 80% a 95% → revisão semanal
- **Classe C** → acima de 95% → revisão mensal

### Few-shot prompting
O chatbot utiliza a técnica de few-shot prompting — exemplos de perguntas e respostas são injetados no contexto antes da conversa começar, direcionando o comportamento da IA para o domínio de suprimentos sem necessidade de treinamento formal do modelo.

### Injeção de contexto dinâmico
Os dados reais do estoque são carregados do CSV e inseridos automaticamente no prompt do sistema, permitindo que a IA raciocine sobre os dados específicos do usuário em tempo real.

---

## Dependências

```
pandas
openpyxl
python-dotenv
google-genai
```

---

## Segurança

- A chave da API **nunca** é exposta no código
- O arquivo `.env` está listado no `.gitignore` e não é versionado
- Cada usuário deve gerar sua própria chave no Google AI Studio

---

## Desenvolvido com

- [Python](https://python.org)
- [Pandas](https://pandas.pydata.org)
- [Google Gemini API](https://aistudio.google.com)
- [Claude - Anthropic](https://claude.ai) — assistente de IA utilizado durante o desenvolvimento
