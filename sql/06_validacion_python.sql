-- 06_validacion_python.sql
-- Replica la lógica de fase7_paso1 (12 FILAS después del pico) para validar contra Python.
WITH
    modernos AS (
        SELECT
            idpozo
        FROM
            vm_produccion
        GROUP BY
            idpozo
        HAVING
            MIN(anio) >= 2016 -- arrancó a producir en 2016 o después
    ),
    serie AS (
        SELECT
            v.idpozo,
            v.prod_pet,
            ROW_NUMBER() OVER (
                PARTITION BY
                    v.idpozo
                ORDER BY
                    v.prod_pet DESC,
                    v.anio,
                    v.mes
            ) AS posicion,
            LEAD (v.prod_pet, 12) OVER (
                PARTITION BY
                    v.idpozo
                ORDER BY
                    v.anio,
                    v.mes
            ) AS pet_12_filas
        FROM
            vm_produccion AS v
            JOIN modernos AS m ON m.idpozo = v.idpozo
    )
SELECT
    COUNT(*) AS pozos,
    ROUND(AVG(100 * (1 - pet_12_filas / prod_pet)), 1) AS caida_promedio_pct
FROM
    serie
WHERE
    posicion = 1 -- fila del pico
    AND prod_pet > 0 -- descarta pozos sin petróleo
    AND pet_12_filas IS NOT NULL;

