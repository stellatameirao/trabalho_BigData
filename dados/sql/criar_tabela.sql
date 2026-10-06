CREATE TABLE candidaturas_2024 (
    sq_candidato BIGINT PRIMARY KEY,
    ano_eleicao INTEGER NOT NULL,
    sg_uf CHAR(2) NOT NULL,
    nm_ue TEXT NOT NULL,
    ds_cargo TEXT NOT NULL,
    nm_candidato TEXT NOT NULL,
    sg_partido TEXT NOT NULL,
    dt_nascimento DATE,
    ds_genero TEXT NOT NULL,
    ds_cor_raca TEXT NOT NULL,
    ds_grau_instrucao TEXT NOT NULL,
    ds_ocupacao TEXT NOT NULL,
    ds_situacao_candidatura TEXT NOT NULL,
    ds_sit_tot_turno TEXT,
    total_receitas NUMERIC(15,2) NOT NULL
);