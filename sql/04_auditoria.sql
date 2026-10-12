-- 04_auditoria.sql
-- Control 1: pozos con más de un registro en el mismo mes.
SELECT
    idpozo,
    anio,
    mes,
    COUNT(*) AS veces
FROM
    vm_produccion
GROUP BY
    idpozo,
    anio,
    mes
HAVING
    COUNT(*) > 1
ORDER BY
    veces DESC
LIMIT
    10;

-- Control 2: pozos con meses faltantes entre su primer y último registro.
SELECT
    COUNT(*) AS pozos_con_huecos
FROM
    (
        SELECT
            idpozo,
            MAX(anio * 12 + mes) - MIN(anio * 12 + mes) + 1 AS meses_esperados,
            COUNT(*) AS meses_con_dato
        FROM
            vm_produccion
        GROUP BY
            idpozo
    ) AS t
WHERE
    meses_con_dato < meses_esperados;

-- Contexto: total de pozos en Vaca Muerta.
SELECT
    COUNT(DISTINCT idpozo) AS pozos_vm
FROM
    vm_produccion;

-- Control 3: meses con tef = 0 (pozo parado) y posibles inconsistencias.
SELECT
    COUNT(*) AS registros_tef_cero,
    SUM(
        CASE
            WHEN prod_pet > 0
            OR prod_gas > 0 THEN 1
            ELSE 0
        END
    ) AS tef_cero_con_produccion
FROM
    vm_produccion
WHERE
    tef = 0;