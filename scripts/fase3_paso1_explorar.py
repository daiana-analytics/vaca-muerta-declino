# Fase 3, paso 1: abrir el archivo y mirar qué tiene (sin limpiar nada todavía)
import pandas as pd

# read_csv es el comando que "abre" un archivo CSV como si fuera una tabla de Excel
df = pd.read_csv("../data/produccion_no_convencional.csv", low_memory=False)

print("Cuántas filas y columnas tiene la tabla:")
print(df.shape)  # (filas, columnas)

print()
print("Los nombres de las columnas:")
print(list(df.columns))

print()
print("Las primeras 3 filas, para verlas con nuestros propios ojos:")
print(df.head(3))
