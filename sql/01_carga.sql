-- 01_carga.sql
-- Carga el CSV crudo (Capítulo IV, Secretaría de Energía) en la tabla produccion_raw.
-- El CSV no está en el repo por su peso: descargarlo de datos.gob.ar
-- y guardarlo como data/produccion_no_convencional.csv antes de correr este script.
CREATE
OR REPLACE TABLE produccion_raw AS
SELECT
    *
FROM
    read_csv ('data/produccion_no_convencional.csv');