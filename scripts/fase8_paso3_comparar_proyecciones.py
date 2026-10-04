import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

vm = pd.read_csv("../data/vaca_muerta_filtrado.csv")

pozo = 155785
datos_pozo = vm[vm['idpozo'] == pozo].copy()
datos_pozo = datos_pozo.sort_values(['anio', 'mes']).reset_index(drop=True)

idx_pico = datos_pozo['prod_pet'].idxmax()
post_pico = datos_pozo.loc[idx_pico:].reset_index(drop=True)
post_pico['meses_desde_pico'] = range(len(post_pico))

def arps_hiperbolico(t, qi, Di, b):
    return qi / (1 + b * Di * t) ** (1 / b)

t = post_pico['meses_desde_pico'].values
q = post_pico['prod_pet'].values

# Ajuste LIBRE (sin límites)
p0 = [q[0], 0.1, 0.5]
params_libre, _ = curve_fit(arps_hiperbolico, t, q, p0=p0, maxfev=10000)
qi_libre, Di_libre, b_libre = params_libre

# Ajuste ACOTADO (con límites: b entre 0 y 2)
limites_inferiores = [0, 0, 0]
limites_superiores = [q.max() * 2, 50, 2]
params_acotado, _ = curve_fit(
    arps_hiperbolico, t, q, p0=p0,
    bounds=(limites_inferiores, limites_superiores),
    maxfev=10000
)
qi_acotado, Di_acotado, b_acotado = params_acotado

print(f"Comparación de ajustes — Pozo {pozo}")
print(f"  Libre:   qi={qi_libre:.1f}  Di={Di_libre:.3f}  b={b_libre:.3f}")
print(f"  Acotado: qi={qi_acotado:.1f}  Di={Di_acotado:.3f}  b={b_acotado:.3f}")

# Proyectamos ambas curvas 15 años (180 meses) hacia adelante
meses_proyeccion = 180
t_proyeccion = np.arange(0, meses_proyeccion)

q_libre = arps_hiperbolico(t_proyeccion, qi_libre, Di_libre, b_libre)
q_acotado = arps_hiperbolico(t_proyeccion, qi_acotado, Di_acotado, b_acotado)

acumulado_libre = q_libre.sum()
acumulado_acotado = q_acotado.sum()
diferencia_pct = (acumulado_libre - acumulado_acotado) / acumulado_acotado * 100

print(f"\nProducción acumulada proyectada a {meses_proyeccion} meses ({meses_proyeccion/12:.0f} años):")
print(f"  Ajuste libre:   {acumulado_libre:,.0f} m³")
print(f"  Ajuste acotado: {acumulado_acotado:,.0f} m³")
print(f"  El ajuste libre sobreestima un {diferencia_pct:.0f}% respecto al acotado")

# Gráfico comparativo
plt.figure(figsize=(11, 6))
plt.scatter(t, q, s=15, color='#1f6f5c', label='Producción real', zorder=3)
plt.plot(t_proyeccion, q_libre, color='darkorange', linewidth=2, linestyle='--', label=f'Proyección libre (b={b_libre:.2f})')
plt.plot(t_proyeccion, q_acotado, color='crimson', linewidth=2, label=f'Proyección acotada (b={b_acotado:.2f})')
plt.axvline(x=len(t), color='gray', linestyle=':', alpha=0.6, label='Fin de datos observados')
plt.title(f"Proyección de reservas a {meses_proyeccion/12:.0f} años — Pozo {pozo}")
plt.xlabel("Meses desde el pico")
plt.ylabel("Producción de petróleo (m³/mes)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("../data/comparacion_proyecciones_pozo155785.png", dpi=150)
plt.show()
print("\nGráfico guardado en data/comparacion_proyecciones_pozo155785.png")