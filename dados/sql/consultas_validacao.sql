SELECT
    COUNT(*) AS total_registros,
    COUNT(DISTINCT sq_candidato) AS candidaturas_unicas,
    COUNT(*) - COUNT(DISTINCT sq_candidato) AS duplicados
FROM candidaturas_2024;

SELECT
    ano_eleicao,
    COUNT(*) AS total_candidaturas
FROM candidaturas_2024
GROUP BY ano_eleicao
ORDER BY ano_eleicao;

SELECT
    COUNT(*) FILTER (WHERE dt_nascimento IS NULL) AS nascimento_ausente,
    COUNT(*) FILTER (WHERE ds_sit_tot_turno IS NULL) AS situacao_eleitoral_ausente,
    COUNT(*) FILTER (WHERE total_receitas IS NULL) AS receitas_nulas,
    COUNT(*) FILTER (WHERE total_receitas < 0) AS receitas_negativas
FROM candidaturas_2024;

SELECT
    ds_genero,
    COUNT(*) AS total_candidaturas
FROM candidaturas_2024
GROUP BY ds_genero
ORDER BY total_candidaturas DESC;

SELECT
    ds_cor_raca,
    COUNT(*) AS total_candidaturas
FROM candidaturas_2024
GROUP BY ds_cor_raca
ORDER BY total_candidaturas DESC;

SELECT
    COUNT(*) FILTER (WHERE total_receitas > 0) AS candidaturas_com_receita,
    COUNT(*) FILTER (WHERE total_receitas = 0) AS candidaturas_sem_receita,
    ROUND(SUM(total_receitas), 2) AS total_recursos
FROM candidaturas_2024;

SELECT
    ds_genero,
    COUNT(*) AS total_candidaturas,
    ROUND(SUM(total_receitas), 2) AS total_recursos,
    ROUND(AVG(total_receitas), 2) AS media_por_candidatura
FROM candidaturas_2024
GROUP BY ds_genero
ORDER BY total_recursos DESC;

SELECT
    ds_cor_raca,
    COUNT(*) AS total_candidaturas,
    ROUND(SUM(total_receitas), 2) AS total_recursos,
    ROUND(AVG(total_receitas), 2) AS media_por_candidatura
FROM candidaturas_2024
GROUP BY ds_cor_raca
ORDER BY total_recursos DESC;