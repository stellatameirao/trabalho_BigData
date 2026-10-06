SELECT COUNT(*) AS total_registros
FROM candidaturas_2024;

SELECT COUNT(DISTINCT sq_candidato) AS candidaturas_unicas
FROM candidaturas_2024;

SELECT ano_eleicao, COUNT(*)
FROM candidaturas_2024
GROUP BY ano_eleicao;