-- 05_pico_declino_sqlserver.sql
-- La misma consulta que sql/05_pico_declino.sql, escrita para SQL Server (T-SQL).
--
-- Diferencias de sintaxis entre DuckDB y SQL Server:
--   1. Limitar filas: DuckDB usa LIMIT 10 al final; SQL Server usa SELECT TOP 10 al principio.
--   2. Crear o reemplazar una vista: DuckDB usa CREATE OR REPLACE VIEW;
--      SQL Server usa CREATE OR ALTER VIEW.
--   3. Cargar el CSV: DuckDB lo lee directo con read_csv(); SQL Server necesita
--      crear la tabla primero y cargarla con BULK INSERT o el asistente de importación.
--   4. Esquema: en SQL Server las tablas y vistas suelen nombrarse con su esquema (dbo.).
--
-- Lo que NO cambia: las CTE (WITH), ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...),
-- los JOIN y ROUND funcionan igual en los dos motores, porque son SQL estándar.
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
            dbo.vm_produccion
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
SELECT TOP 10
    p.idpozo,
    p.pico_pet,
    v.prod_pet AS pet_12m,
    ROUND(100 * (1 - v.prod_pet / p.pico_pet), 1) AS caida_pct
FROM
    pico AS p
    JOIN dbo.vm_produccion AS v ON v.idpozo = p.idpozo
    AND v.anio * 12 + v.mes = p.mes_pico + 12;
