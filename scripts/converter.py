import pandas as pd
import sys
from pathlib import Path

arquivo = Path(sys.argv[1])

sheets = pd.read_excel(arquivo, sheet_name=None)

pasta = Path("dados/csv") / arquivo.stem
pasta.mkdir(parents=True, exist_ok=True)

for nome, df in sheets.items():
    nome_limpo = nome.replace(" ", "_").replace(".", "")
    saida = pasta / f"{nome_limpo}.csv"
    df.to_csv(saida, index=False, encoding="utf-8-sig")
    print(f"Salvo: {saida}")