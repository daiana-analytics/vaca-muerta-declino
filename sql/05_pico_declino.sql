-- 05_pico_declino.sql
-- Pico de petróleo de cada pozo y producción 12 meses calendario después.
WITH
    ranking AS (
        SELECT
            idpozo,
            prod_pet,
            anio * 12 + mes AS mes_idx,
            ROW_NUMBER() OVER (
                PARTITION BY
                    idpozo
                ORDER BY
                    prod_pet DESC,
                    anio,
                    mes
            ) AS posicion
        FROM
            vm_produccion
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
            AND prod_pet > 0 -- descarta pozos sin petróleo
    )
SELECT
    p.idpozo,
    p.pico_pet,
    v.prod_pet AS pet_12m,
    ROUND(100 * (1 - v.prod_pet / p.pico_pet), 1) AS caida_pct
FROM
    pico AS p
    JOIN vm_produccion AS v ON v.idpozo = p.idpozo
    AND v.anio * 12 + v.mes = p.mes_pico + 12
LIMIT
    10;