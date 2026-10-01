import pandas as pd

vm = pd.read_csv("../data/vaca_muerta_filtrado.csv")

# Agrupamos por pozo y contamos cuántas filas (meses) tiene cada uno
meses_por_pozo = vm.groupby('idpozo').size().sort_values(ascending=False)

print("Los 10 pozos con más meses de producción registrados:")
print(meses_por_pozo.head(10))