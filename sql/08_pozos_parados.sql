-- 08_pozos_parados.sql
-- Replica en SQL la clasificación de fase7_paso4_clasificar_pozos.py:
-- de los pozos modernos (iniciados desde 2016) con al menos 13 meses de historia,
-- qué porcentaje estaba parado (tef = 0) en su último registro.
WITH
    resumen AS (
        SELECT
            idpozo,
            MIN(anio) AS anio_inicio,
            COUNT(*) AS meses_historia
        FROM
            vm_produccion
        GROUP BY
            idpozo
    ),
    modernos AS (
        SELECT
            idpozo
        FROM
            resumen
        WHERE
            anio_inicio >= 2016
            AND meses_historia >= 13
    ),
    ultimo AS (
        SELECT
            v.idpozo,
            v.tef,
            ROW_NUMBER() OVER (
                PARTITION BY
                    v.idpozo
                ORDER BY
                    v.anio DESC,
                    v.mes DESC
            ) AS posicion
        FROM
            vm_produccion AS v
            JOIN modernos AS m ON m.idpozo = v.idpozo
    )
SELECT
    COUNT(*) AS pozos_modernos,
    SUM(CASE WHEN tef = 0 THEN 1 ELSE 0 END) AS parados_al_cierre,
    ROUND(100.0 * SUM(CASE WHEN tef = 0 THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_parados
FROM
    ultimo
WHERE
    posicion = 1;
