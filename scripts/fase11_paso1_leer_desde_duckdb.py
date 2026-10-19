import duckdb

# Abrimos la base en modo solo lectura: Python lee, no modifica.
con = duckdb.connect("../vaca_muerta.duckdb", read_only=True)

# Traemos la vista limpia que armamos en SQL, directo a un DataFrame de pandas.
vm = con.execute("""
    SELECT *
    FROM vm_produccion
    ORDER BY idpozo, anio, mes
""").df()
con.close()

print(f"Filas: {len(vm):,}")
print(f"Pozos: {vm['idpozo'].nunique():,}")
print(vm.head())