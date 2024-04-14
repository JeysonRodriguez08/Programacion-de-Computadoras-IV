import sqlite3

# Configurar la conexión a la base de datos SQLite
DATABASE_FILE = "presupuesto.db"
conexion = sqlite3.connect(DATABASE_FILE)
cursor = conexion.cursor()

# Crear la tabla de presupuesto si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS presupuesto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        categoria TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        monto REAL NOT NULL
    )
''')
conexion.commit()

# Función para agregar un nuevo artículo al presupuesto
def agregar_articulo():
    categoria = input("Categoría del artículo: ")
    descripcion = input("Descripción del artículo: ")
    monto = float(input("Monto del artículo: "))

    cursor.execute('INSERT INTO presupuesto (categoria, descripcion, monto) VALUES (?, ?, ?)', (categoria, descripcion, monto))
    conexion.commit()
    print("Artículo agregado al presupuesto.")

# Función para buscar artículos en el presupuesto
def buscar_articulo():
    categoria = input("Ingrese la categoría para buscar artículos (deje en blanco para buscar todos): ")
    
    if categoria:
        cursor.execute('SELECT * FROM presupuesto WHERE categoria=?', (categoria,))
    else:
        cursor.execute('SELECT * FROM presupuesto')

    resultados = cursor.fetchall()

    if not resultados:
        print("No se encontraron artículos en la categoría proporcionada.")
    else:
        for resultado in resultados:
            print(f"\nID: {resultado[0]}")
            print(f"Categoría: {resultado[1]}")
            print(f"Descripción: {resultado[2]}")
            print(f"Monto: {resultado[3]}")

# Función para editar un artículo en el presupuesto
def editar_articulo():
    id_articulo = input("Ingrese el ID del artículo que desea editar: ")
    nueva_descripcion = input("Nueva descripción del artículo (deje en blanco para mantener la actual): ")
    nuevo_monto = input("Nuevo monto del artículo (deje en blanco para mantener el actual): ")

    consulta = 'UPDATE presupuesto SET '
    parametros = []

    if nueva_descripcion:
        consulta += 'descripcion=?, '
        parametros.append(nueva_descripcion)

    if nuevo_monto:
        consulta += 'monto=?, '
        parametros.append(float(nuevo_monto))

    # Eliminar la coma final y agregar la condición WHERE
    consulta = consulta.rstrip(', ')
    consulta += ' WHERE id=?'
    parametros.append(id_articulo)

    cursor.execute(consulta, tuple(parametros))
    conexion.commit()
    print("Artículo actualizado en el presupuesto.")

# Función para eliminar un artículo del presupuesto
def eliminar_articulo():
    id_articulo = input("Ingrese el ID del artículo que desea eliminar: ")
    
    cursor.execute('DELETE FROM presupuesto WHERE id=?', (id_articulo,))
    conexion.commit()
    print("Artículo eliminado del presupuesto.")

# Función principal del programa
def main():
    while True:
        print("\n--- Sistema de Registro de Presupuesto ---")
        print("a) Agregar nuevo artículo")
        print("b) Buscar artículos")
        print("c) Editar artículo")
        print("d) Eliminar artículo")
        print("e) Salir")

        opcion = input("\nSeleccione una opción: ").lower()

        if opcion == 'a':
            agregar_articulo()
        elif opcion == 'b':
            buscar_articulo()
        elif opcion == 'c':
            editar_articulo()
        elif opcion == 'd':
            eliminar_articulo()
        elif opcion == 'e':
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Inténtelo de nuevo.")

if __name__ == "__main__":
    main()

# Cerrar la conexión a la base de datos al salir del programa
conexion.close()
