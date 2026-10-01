import pandas as pd
import matplotlib.pyplot as plt

vm = pd.read_csv("../data/vaca_muerta_filtrado.csv")

pozo = 155785
datos_pozo = vm[vm['idpozo'] == pozo].copy()
datos_pozo = datos_pozo.sort_values(['anio', 'mes']).reset_index(drop=True)
datos_pozo['tiempo'] = datos_pozo['anio'] + (datos_pozo['mes'] - 1) / 12

pico = datos_pozo['prod_pet'].max()
idx_pico = datos_pozo[datos_pozo['prod_pet'] == pico].index[0]
tiempo_pico = datos_pozo.loc[idx_pico, 'tiempo']

idx_12m = idx_pico + 12
tiempo_12m = datos_pozo.loc[idx_12m, 'tiempo']
valor_12m = datos_pozo.loc[idx_12m, 'prod_pet']

plt.figure(figsize=(10, 5))
plt.plot(datos_pozo['tiempo'], datos_pozo['prod_pet'], color='#1f6f5c')

# Marcamos el pico con un punto rojo y un cartelito
plt.scatter([tiempo_pico], [pico], color='crimson', zorder=5)
plt.annotate(f"Pico: {pico:.0f} m³/mes", xy=(tiempo_pico, pico),
             xytext=(tiempo_pico + 0.5, pico), fontsize=10, color='crimson')

# Marcamos el punto de los 12 meses después
plt.scatter([tiempo_12m], [valor_12m], color='crimson', zorder=5)
plt.annotate("-85% a los 12 meses", xy=(tiempo_12m, valor_12m),
             xytext=(tiempo_12m + 0.3, valor_12m + 20), fontsize=10, color='crimson')

plt.title(f"Curva de declino — Pozo {pozo} (Vaca Muerta)")
plt.xlabel("Año")
plt.ylabel("Producción de petróleo (m³/mes)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("../data/curva_declino_pozo155785.png", dpi=150)
plt.show()
print("Gráfico guardado en data/curva_declino_pozo155785.png")