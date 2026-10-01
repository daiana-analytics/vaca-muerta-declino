import pandas as pd

df = pd.read_csv("../data/produccion_no_convencional.csv", low_memory=False)

# Nos quedamos solo con las filas de la formación Vaca Muerta
vm = df[df['formacion'] == 'vaca muerta'].copy()

print(f"Filas totales del archivo: {len(df)}")
print(f"Filas que son realmente Vaca Muerta: {len(vm)}")

# Nos quedamos solo con las columnas que nos importan para la curva de declino
columnas_utiles = ['idpozo', 'empresa', 'areayacimiento', 'anio', 'mes',
                    'prod_pet', 'prod_gas', 'prod_agua', 'tef', 'fecha_data']
vm = vm[columnas_utiles]

print()
print("Cuántos datos faltantes hay en cada columna:")
print(vm.isnull().sum())

print()
print("Cuántos pozos distintos de Vaca Muerta hay:")
print(vm['idpozo'].nunique())

# Guardamos esta versión más chica, para no abrir el archivo de 140 MB cada vez
vm.to_csv("../data/vaca_muerta_filtrado.csv", index=False)
print()
print("Guardado como data/vaca_muerta_filtrado.csv")