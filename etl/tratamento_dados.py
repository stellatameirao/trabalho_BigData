import pandas as pd
from pathlib import Path


PASTA_PROJETO = Path(__file__).resolve().parent.parent
PASTA_BRUTOS = PASTA_PROJETO / "dados" / "brutos"
PASTA_TRATADOS = PASTA_PROJETO / "dados" / "tratados"

arquivo_candidatos = PASTA_BRUTOS / "consulta_cand_2024_BRASIL.csv"
arquivo_receitas = PASTA_BRUTOS / "receitas_candidatos_2024_BRASIL.csv"

PASTA_TRATADOS.mkdir(parents=True, exist_ok=True)


print("Lendo a base de candidaturas...")

candidatos = pd.read_csv(
    arquivo_candidatos,
    sep=";",
    encoding="latin1",
    dtype=str
)

colunas_candidatos = [
    "ANO_ELEICAO",
    "SG_UF",
    "NM_UE",
    "DS_CARGO",
    "SQ_CANDIDATO",
    "NM_CANDIDATO",
    "SG_PARTIDO",
    "DT_NASCIMENTO",
    "DS_GENERO",
    "DS_COR_RACA",
    "DS_GRAU_INSTRUCAO",
    "DS_OCUPACAO",
    "DS_SITUACAO_CANDIDATURA",
    "DS_SIT_TOT_TURNO"
]

candidatos = candidatos[colunas_candidatos].copy()

candidatos["ANO_ELEICAO"] = pd.to_numeric(
    candidatos["ANO_ELEICAO"],
    errors="coerce"
).astype("Int64")

candidatos["SQ_CANDIDATO"] = pd.to_numeric(
    candidatos["SQ_CANDIDATO"],
    errors="coerce"
).astype("Int64")

candidatos["DT_NASCIMENTO"] = pd.to_datetime(
    candidatos["DT_NASCIMENTO"],
    format="%d/%m/%Y",
    errors="coerce"
)

colunas_texto = [
    "SG_UF",
    "NM_UE",
    "DS_CARGO",
    "NM_CANDIDATO",
    "SG_PARTIDO",
    "DS_GENERO",
    "DS_COR_RACA",
    "DS_GRAU_INSTRUCAO",
    "DS_OCUPACAO",
    "DS_SITUACAO_CANDIDATURA",
    "DS_SIT_TOT_TURNO"
]

for coluna in colunas_texto:
    candidatos[coluna] = candidatos[coluna].str.strip()

candidatos["DS_SIT_TOT_TURNO"] = candidatos[
    "DS_SIT_TOT_TURNO"
].replace("#NULO", pd.NA)


print("Processando a base de receitas...")

colunas_receitas = [
    "SQ_CANDIDATO",
    "VR_RECEITA"
]

receitas_por_candidato = {}

# Leitura em blocos para evitar carregar todo o arquivo na memória
chunks = pd.read_csv(
    arquivo_receitas,
    sep=";",
    encoding="latin1",
    dtype=str,
    usecols=colunas_receitas,
    chunksize=100000
)

for numero_chunk, chunk in enumerate(chunks, start=1):

    chunk["SQ_CANDIDATO"] = pd.to_numeric(
        chunk["SQ_CANDIDATO"],
        errors="coerce"
    ).astype("Int64")

    chunk["VR_RECEITA"] = (
        chunk["VR_RECEITA"]
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
    )

    chunk["VR_RECEITA"] = pd.to_numeric(
        chunk["VR_RECEITA"],
        errors="coerce"
    )

    soma_chunk = chunk.groupby("SQ_CANDIDATO")["VR_RECEITA"].sum()

    for candidato, valor in soma_chunk.items():
        receitas_por_candidato[candidato] = (
            receitas_por_candidato.get(candidato, 0) + valor
        )

    print(f"Bloco {numero_chunk} processado.")


receitas_agrupadas = pd.DataFrame(
    list(receitas_por_candidato.items()),
    columns=["SQ_CANDIDATO", "TOTAL_RECEITAS"]
)

receitas_agrupadas["SQ_CANDIDATO"] = (
    receitas_agrupadas["SQ_CANDIDATO"].astype("Int64")
)

receitas_agrupadas["TOTAL_RECEITAS"] = (
    receitas_agrupadas["TOTAL_RECEITAS"].round(2)
)


print("Integrando as bases...")

base_final = candidatos.merge(
    receitas_agrupadas,
    on="SQ_CANDIDATO",
    how="left"
)

base_final["TOTAL_RECEITAS"] = (
    base_final["TOTAL_RECEITAS"]
    .fillna(0)
    .round(2)
)

# Remove registros intermediários de candidatos que foram ao segundo turno
base_final = base_final[
    base_final["DS_SIT_TOT_TURNO"] != "2º TURNO"
].copy()

# Nos casos repetidos, prioriza o registro que possui resultado eleitoral
base_final["_tem_resultado"] = (
    base_final["DS_SIT_TOT_TURNO"].notna()
)

base_final = base_final.sort_values(
    by=["SQ_CANDIDATO", "_tem_resultado"],
    ascending=[True, False]
)

base_final = base_final.drop_duplicates(
    subset="SQ_CANDIDATO",
    keep="first"
)

base_final = base_final.drop(columns="_tem_resultado")


print("\nValidação final")

print("\nDimensão:")
print(base_final.shape)

print("\nCandidaturas duplicadas:")
print(base_final["SQ_CANDIDATO"].duplicated().sum())

print("\nValores ausentes:")
print(base_final.isna().sum())

print("\nDistribuição por gênero:")
print(base_final["DS_GENERO"].value_counts())

print("\nDistribuição por raça/cor:")
print(base_final["DS_COR_RACA"].value_counts())

print("\nDistribuição por cargo:")
print(base_final["DS_CARGO"].value_counts())

print("\nSituação eleitoral:")
print(base_final["DS_SIT_TOT_TURNO"].value_counts(dropna=False))

print("\nResumo das receitas:")
print(base_final["TOTAL_RECEITAS"].describe())

print("\nReceitas negativas:")
print((base_final["TOTAL_RECEITAS"] < 0).sum())

print("\nAnos encontrados:")
print(base_final["ANO_ELEICAO"].value_counts())


arquivo_saida = PASTA_TRATADOS / "base_eleicoes_2024_tratada.csv"

base_final.to_csv(
    arquivo_saida,
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

print("\nBase tratada salva com sucesso!")


# Ordem utilizada na tabela do PostgreSQL
colunas_banco = [
    "SQ_CANDIDATO",
    "ANO_ELEICAO",
    "SG_UF",
    "NM_UE",
    "DS_CARGO",
    "NM_CANDIDATO",
    "SG_PARTIDO",
    "DT_NASCIMENTO",
    "DS_GENERO",
    "DS_COR_RACA",
    "DS_GRAU_INSTRUCAO",
    "DS_OCUPACAO",
    "DS_SITUACAO_CANDIDATURA",
    "DS_SIT_TOT_TURNO",
    "TOTAL_RECEITAS"
]

base_banco = base_final[colunas_banco].copy()

arquivo_banco = PASTA_TRATADOS / "base_eleicoes_2024_banco.csv"

base_banco.to_csv(
    arquivo_banco,
    sep=";",
    index=False,
    encoding="utf-8"
)

print("Arquivo para o PostgreSQL criado com sucesso!")