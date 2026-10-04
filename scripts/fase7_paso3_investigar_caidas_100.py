import pandas as pd

declino = pd.read_csv("../data/declino_pozos_modernos.csv")

# ¿Cuántos pozos cayeron prácticamente al 100%?
al_100 = declino[declino['caida_12m_pct'] >= 99]
print(f"Pozos con caída >= 99% a los 12 meses: {len(al_100)} de {len(declino)}")
print()
print(al_100[['idpozo', 'empresa', 'areayacimiento', 'meses_historia', 'pico_prod_pet']].head(10))

# Miramos de cerca uno de estos pozos, con la columna 'tef' incluida,
# para ver si el pozo realmente se secó o si dejó de operar
vm = pd.read_csv("../data/vaca_muerta_filtrado.csv")
pozo_ejemplo = al_100['idpozo'].iloc[0]
datos = vm[vm['idpozo'] == pozo_ejemplo].sort_values(['anio', 'mes'])

print()
print(f"Historia completa del pozo {pozo_ejemplo} (con tef = tiempo efectivo de producción):")
print(datos[['anio', 'mes', 'prod_pet', 'tef']].to_string(index=False))