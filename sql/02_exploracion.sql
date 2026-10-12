SELECT
    COUNT(*) AS total,
    COUNT(*) - COUNT(idpozo) AS nulos_idpozo,
    COUNT(*) - COUNT(formacion) AS nulos_formacion,
    COUNT(*) - COUNT(prod_pet) AS nulos_prod_pet,
    COUNT(*) - COUNT(prod_gas) AS nulos_prod_gas,
    COUNT(*) - COUNT(tef) AS nulos_tef,
    COUNT(*) - COUNT(fecha_data) AS nulos_fecha
FROM
    produccion_raw;