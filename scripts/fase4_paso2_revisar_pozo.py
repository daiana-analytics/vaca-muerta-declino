import pandas as pd

vm = pd.read_csv("../data/vaca_muerta_filtrado.csv")

pozo = 42900
datos_pozo = vm[vm['idpozo'] == pozo].copy()

print(f"Filas para el pozo {pozo}: {len(datos_pozo)}")

# Chequeamos si hay meses repetidos (mismo año y mes apareciendo dos veces)
duplicados = datos_pozo.duplicated(subset=['anio', 'mes'], keep=False)
print(f"Filas con mes repetido: {duplicados.sum()}")

# Ordenamos por fecha y miramos el principio y el final de la historia del pozo
datos_pozo = datos_pozo.sort_values(['anio', 'mes'])
print()
print("Primeros meses de producción:")
print(datos_pozo[['anio', 'mes', 'prod_pet', 'prod_gas', 'tef']].head(5))
print()
print("Últimos meses de producción:")
print(datos_pozo[['anio', 'mes', 'prod_pet', 'prod_gas', 'tef']].tail(5))