import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

vm = pd.read_csv("../data/vaca_muerta_filtrado.csv")

pozo = 155785
datos_pozo = vm[vm['idpozo'] == pozo].copy()
datos_pozo = datos_pozo.sort_values(['anio', 'mes']).reset_index(drop=True)

# Nos quedamos solo con los meses desde el pico en adelante (ahí es donde aplica el declino)
idx_pico = datos_pozo['prod_pet'].idxmax()
post_pico = datos_pozo.loc[idx_pico:].reset_index(drop=True)
post_pico['meses_desde_pico'] = range(len(post_pico))

# La fórmula de Arps hiperbólica: el estándar de la industria para curvas de declino
def arps_hiperbolico(t, qi, Di, b):
    return qi / (1 + b * Di * t) ** (1 / b)

t = post_pico['meses_desde_pico'].values
q = post_pico['prod_pet'].values

# Valores iniciales de referencia para que el ajuste arranque cerca de la solución
p0 = [q[0], 0.1, 0.5]
parametros, _ = curve_fit(arps_hiperbolico, t, q, p0=p0, maxfev=10000)
qi, Di, b = parametros

print(f"Pozo {pozo} — parámetros ajustados del modelo de Arps:")
print(f"  qi (producción inicial): {qi:.1f} m³/mes")
print(f"  Di (tasa de declino inicial): {Di:.3f} por mes")
print(f"  b (exponente hiperbólico): {b:.3f}")

# Graficamos: datos reales vs. la curva que ajustó el modelo
q_modelo = arps_hiperbolico(t, qi, Di, b)

plt.figure(figsize=(10, 5))
plt.scatter(t, q, s=15, color='#1f6f5c', label='Producción real')
plt.plot(t, q_modelo, color='crimson', linewidth=2, label='Curva de Arps ajustada')
plt.title(f"Ajuste de curva de declino (Arps) — Pozo {pozo}")
plt.xlabel("Meses desde el pico")
plt.ylabel("Producción de petróleo (m³/mes)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("../data/ajuste_arps_pozo155785.png", dpi=150)
plt.show()
print("Gráfico guardado en data/ajuste_arps_pozo155785.png")