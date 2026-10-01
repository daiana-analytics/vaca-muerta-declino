import pandas as pd

df = pd.read_csv("../data/produccion_no_convencional.csv", low_memory=False)

print("Formaciones distintas y cuántas filas tiene cada una:")
print(df['formacion'].value_counts())