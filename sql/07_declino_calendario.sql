-- 07_declino_calendario.sql
-- Declino a 12 MESES CALENDARIO del pico (corrige el sesgo de contar filas
-- en pozos con huecos). Comparar contra 06_validacion_python.sql.
WITH
    modernos AS (
        SELECT
            idpozo
        FROM
            vm_produccion
        GROUP BY
            idpozo
        HAVING
            MIN(anio) >= 2016
    ),
    ranking AS (
        SELECT
            v.idpozo,
            v.prod_pet,
            v.anio * 12 + v.mes AS mes_idx,
            ROW_NUMBER() OVER (
                PARTITION BY
                    v.idpozo
                ORDER BY
                    v.prod_pet DESC,
                    v.anio,
                    v.mes
            ) AS posicion
        FROM
            vm_produccion AS v
            JOIN modernos AS m ON m.idpozo = v.idpozo
    ),
    pico AS (
        SELECT
            idpozo,
            mes_idx AS mes_pico,
            prod_pet AS pico_pet
        FROM
            ranking
        WHERE
            posicion = 1
            AND prod_pet > 0
    )
SELECT
    COUNT(*) AS pozos,
    ROUND(AVG(100 * (1 - v.prod_pet / p.pico_pet)), 1) AS caida_promedio_pct
FROM
    pico AS p
    JOIN vm_produccion AS v ON v.idpozo = p.idpozo
    AND v.anio * 12 + v.mes = p.mes_pico + 12;