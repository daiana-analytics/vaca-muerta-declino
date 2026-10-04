import pandas as pd

vm = pd.read_csv("../data/vaca_muerta_filtrado.csv")

# Los mismos "pozos modernos" que identificamos en la fase 4
inicio_por_pozo = vm.groupby('idpozo')['anio'].min()
pozos_modernos = inicio_por_pozo[inicio_por_pozo >= 2016].index

resultados = []

for pozo in pozos_modernos:
    datos_pozo = vm[vm['idpozo'] == pozo].copy()
    datos_pozo = datos_pozo.sort_values(['anio', 'mes']).reset_index(drop=True)

    # Necesitamos al menos 13 meses de historia para poder medir "12 meses después del pico"
    if len(datos_pozo) < 13:
        continue

    pico = datos_pozo['prod_pet'].max()
    if pico == 0:
        continue  # pozo sin producción real registrada, lo salteamos

    idx_pico = datos_pozo[datos_pozo['prod_pet'] == pico].index[0]
    idx_12m = idx_pico + 12

    if idx_12m >= len(datos_pozo):
        continue  # todavía no tiene 12 meses de historia después del pico

    valor_12m = datos_pozo.loc[idx_12m, 'prod_pet']
    caida_12m = (1 - valor_12m / pico) * 100

    ultimo = datos_pozo.iloc[-1]
    caida_total = (1 - ultimo['prod_pet'] / pico) * 100

    resultados.append({
        'idpozo': pozo,
        'empresa': datos_pozo['empresa'].iloc[0],
        'areayacimiento': datos_pozo['areayacimiento'].iloc[0],
        'meses_historia': len(datos_pozo),
        'pico_prod_pet': pico,
        'caida_12m_pct': caida_12m,
        'caida_total_pct': caida_total,
    })

df_resultados = pd.DataFrame(resultados)
print(f"Pozos modernos analizados: {len(df_resultados)}")
print()
print(df_resultados.describe())

df_resultados.to_csv("../data/declino_pozos_modernos.csv", index=False)
print()
print("Guardado en data/declino_pozos_modernos.csv")