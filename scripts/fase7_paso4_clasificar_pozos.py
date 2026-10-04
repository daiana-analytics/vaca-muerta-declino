import pandas as pd

vm = pd.read_csv("../data/vaca_muerta_filtrado.csv")

inicio_por_pozo = vm.groupby('idpozo')['anio'].min()
pozos_modernos = inicio_por_pozo[inicio_por_pozo >= 2016].index

clasificacion = []

for pozo in pozos_modernos:
    datos_pozo = vm[vm['idpozo'] == pozo].copy()
    datos_pozo = datos_pozo.sort_values(['anio', 'mes']).reset_index(drop=True)

    if len(datos_pozo) < 13:
        continue

    ultimo = datos_pozo.iloc[-1]
    # Un pozo "activo" es el que todavía tenía tiempo efectivo de producción (tef > 0)
    # en su último registro. Si tef = 0, el pozo está parado, no en declino natural.
    activo = ultimo['tef'] > 0

    clasificacion.append({
        'idpozo': pozo,
        'empresa': datos_pozo['empresa'].iloc[0],
        'meses_historia': len(datos_pozo),
        'activo_al_final': activo,
    })

df_clas = pd.DataFrame(clasificacion)

print(f"Total de pozos modernos con suficiente historia: {len(df_clas)}")
print()
print(df_clas['activo_al_final'].value_counts())
print()
print(f"Porcentaje parados: {(~df_clas['activo_al_final']).mean()*100:.1f}%")

df_clas.to_csv("../data/clasificacion_pozos_modernos.csv", index=False)
print()
print("Guardado en data/clasificacion_pozos_modernos.csv")