import pandas as pd
import matplotlib.pyplot as plt

vm = pd.read_csv("../data/vaca_muerta_filtrado.csv")

pozo = 155785
datos_pozo = vm[vm['idpozo'] == pozo].copy()
datos_pozo = datos_pozo.sort_values(['anio', 'mes'])

# Armamos un eje de tiempo continuo (año + fracción del mes) para que se lea bien
datos_pozo['tiempo'] = datos_pozo['anio'] + (datos_pozo['mes'] - 1) / 12

plt.figure(figsize=(10, 5))
plt.plot(datos_pozo['tiempo'], datos_pozo['prod_pet'], marker='o', markersize=2)
plt.title(f"Producción de petróleo - Pozo {pozo}")
plt.xlabel("Año")
plt.ylabel("Producción de petróleo (m³/mes)")
plt.grid(True, alpha=0.3)
plt.show()