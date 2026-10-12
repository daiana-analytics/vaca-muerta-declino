-- 03_vaca_muerta.sql
-- Vista con los registros de Vaca Muerta y solo las columnas del análisis.
CREATE
OR REPLACE VIEW vm_produccion AS
SELECT
    idpozo,
    empresa,
    areayacimiento,
    formacion,
    anio,
    mes,
    fecha_data,
    prod_pet,
    prod_gas,
    prod_agua,
    tef
FROM
    produccion_raw
WHERE
    formacion = 'vaca muerta';

-- Control: tiene que dar 219.848 (lo que vimos en el GROUP BY)
SELECT
    COUNT(*) AS registros_vm
FROM
    vm_produccion;