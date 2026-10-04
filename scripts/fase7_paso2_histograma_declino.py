import pandas as pd
import matplotlib.pyplot as plt

declino = pd.read_csv("../data/declino_pozos_modernos.csv")

plt.figure(figsize=(10, 5))
plt.hist(declino['caida_12m_pct'], bins=30, color='#1f6f5c', edgecolor='white')
plt.title(f"Distribución de la caída a los 12 meses — {len(declino)} pozos modernos (Vaca Muerta)")
plt.xlabel("Caída a los 12 meses (%)")
plt.ylabel("Cantidad de pozos")
plt.axvline(declino['caida_12m_pct'].mean(), color='crimson', linestyle='--',
            label=f"Promedio: {declino['caida_12m_pct'].mean():.0f}%")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("../data/histograma_declino_12m.png", dpi=150)
plt.show()
print("Gráfico guardado en data/histograma_declino_12m.png")