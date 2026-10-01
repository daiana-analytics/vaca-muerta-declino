import pandas as pd

vm = pd.read_csv("../data/vaca_muerta_filtrado.csv")

pozo = 155785
datos_pozo = vm[vm['idpozo'] == pozo].copy()
datos_pozo = datos_pozo.sort_values(['anio', 'mes']).reset_index(drop=True)

# Buscamos el pico de producción y en qué mes ocurrió
pico = datos_pozo['prod_pet'].max()
fila_pico = datos_pozo[datos_pozo['prod_pet'] == pico].iloc[0]
print(f"Pico de producción: {pico:.1f} m³/mes, en {fila_pico['mes']}/{fila_pico['anio']}")

idx_pico = datos_pozo[datos_pozo['prod_pet'] == pico].index[0]

# Qué producía 12 meses después del pico
idx_12m = idx_pico + 12
if idx_12m < len(datos_pozo):
    valor_12m = datos_pozo.loc[idx_12m, 'prod_pet']
    caida = (1 - valor_12m / pico) * 100
    print(f"Producción 12 meses después del pico: {valor_12m:.1f} m³/mes")
    print(f"Caída a los 12 meses: {caida:.0f}%")

# Y la producción más reciente
ultimo = datos_pozo.iloc[-1]
print(f"Producción más reciente ({ultimo['mes']}/{ultimo['anio']}): {ultimo['prod_pet']:.1f} m³/mes")
caida_total = (1 - ultimo['prod_pet'] / pico) * 100
print(f"Caída total desde el pico: {caida_total:.0f}%")