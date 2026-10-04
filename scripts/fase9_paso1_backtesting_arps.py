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

t = post_pico['meses_desde_pico'].values
q = post_pico['prod_pet'].values

# Separamos en entrenamiento (70%) y prueba (30%), respetando el orden temporal
corte = int(len(t) * 0.7)
t_train, q_train = t[:corte], q[:corte]
t_test, q_test = t[corte:], q[corte:]

print(f"Pozo {pozo} — {len(t)} meses de historia post-pico")
print(f"  Entrenamiento: meses 0 a {corte-1} ({len(t_train)} meses)")
print(f"  Prueba (oculta al ajuste): meses {corte} a {len(t)-1} ({len(t_test)} meses)")

def arps_hiperbolico(t, qi, Di, b):
    return qi / (1 + b * Di * t) ** (1 / b)

# Ajustamos SOLO con los datos de entrenamiento, con los mismos límites de la fase 8
p0 = [q_train[0], 0.1, 0.5]
limites_inferiores = [0, 0, 0]
limites_superiores = [q_train.max() * 2, 50, 2]

parametros, _ = curve_fit(
    arps_hiperbolico, t_train, q_train, p0=p0,
    bounds=(limites_inferiores, limites_superiores),
    maxfev=10000
)
qi, Di, b = parametros
print(f"\nParámetros ajustados (solo con entrenamiento):")
print(f"  qi={qi:.1f}  Di={Di:.3f}  b={b:.3f}")

# "Predecimos" los meses de prueba, que el modelo nunca vio
q_pred_test = arps_hiperbolico(t_test, qi, Di, b)

# Métricas de error sobre el período de prueba
error_abs = np.abs(q_test - q_pred_test)
mae = error_abs.mean()
rmse = np.sqrt(((q_test - q_pred_test) ** 2).mean())
mape = (error_abs / q_test).mean() * 100

print(f"\nError del modelo sobre los {len(t_test)} meses de prueba (no vistos al ajustar):")
print(f"  MAE  (error absoluto promedio): {mae:.2f} m³/mes")
print(f"  RMSE (raíz del error cuadrático medio): {rmse:.2f} m³/mes")
print(f"  MAPE (error porcentual promedio): {mape:.1f}%")

# Gráfico: entrenamiento, prueba real, y lo que predijo el modelo
q_pred_completo = arps_hiperbolico(t, qi, Di, b)

plt.figure(figsize=(11, 6))
plt.scatter(t_train, q_train, s=15, color='#1f6f5c', label='Entrenamiento (usado para ajustar)', zorder=3)
plt.scatter(t_test, q_test, s=15, color='darkorange', label='Prueba (real, oculta al ajuste)', zorder=3)
plt.plot(t, q_pred_completo, color='crimson', linewidth=2, label=f'Modelo ajustado (b={b:.2f})')
plt.axvline(x=corte, color='gray', linestyle=':', alpha=0.6, label='Corte entrenamiento/prueba')
plt.title(f"Backtesting del modelo de Arps — Pozo {pozo}")
plt.xlabel("Meses desde el pico")
plt.ylabel("Producción de petróleo (m³/mes)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("../data/backtesting_arps_pozo155785.png", dpi=150)
plt.show()
print("\nGráfico guardado en data/backtesting_arps_pozo155785.png")