
import pandas as pd
from pathlib import Path

pasta_projeto = Path(__file__).resolve().parent.parent
pasta_dados = pasta_projeto / "dados" / "brutos"

arquivos = [
    "consulta_cand_2024_BRASIL.csv",
    "receitas_candidatos_2024_BRASIL.csv"
]

for arquivo in arquivos:
    caminho = pasta_dados / arquivo
    total = 0

    for bloco in pd.read_csv(
        caminho,
        sep=";",
        encoding="latin-1",
        chunksize=100000
    ):
        total += len(bloco)

    print(f"{arquivo}: {total:,} registros")
