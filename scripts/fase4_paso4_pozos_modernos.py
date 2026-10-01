import pandas as pd

vm = pd.read_csv("../data/vaca_muerta_filtrado.csv")

# Para cada pozo, buscamos en qué año arrancó a producir
inicio_por_pozo = vm.groupby('idpozo')['anio'].min()

# Nos quedamos solo con pozos que arrancaron en 2016 o después
pozos_modernos = inicio_por_pozo[inicio_por_pozo >= 2016].index
vm_modernos = vm[vm['idpozo'].isin(pozos_modernos)]

# De esos, ordenamos por cuántos meses de historia tienen
meses_por_pozo = vm_modernos.groupby('idpozo').size().sort_values(ascending=False)

print("Pozos que arrancaron en 2016 o después, con más meses de historia:")
print(meses_por_pozo.head(10))