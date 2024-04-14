import sqlite3

# Función para conectarse a la base de datos SQLite
def conectar_bd():
    return sqlite3.connect('libro_recetas.db')

# Función para crear la tabla de recetas si no existe
def crear_tabla():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recetas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            ingredientes TEXT NOT NULL,
            pasos TEXT NOT NULL
        )
    ''')
    conexion.commit()
    
    conexion.close()

# Función para agregar una nueva receta
def agregar_receta():
    nombre = input("Nombre de la receta: ")
    ingredientes = input("Ingredientes (separados por coma): ")
    pasos = input("Pasos de la receta: ")

    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute('INSERT INTO recetas (nombre, ingredientes, pasos) VALUES (?, ?, ?)', (nombre, ingredientes, pasos))
    conexion.commit()
    conexion.close()
    print("Receta agregada exitosamente.")

# Función para actualizar una receta existente
def actualizar_receta():
    id_receta = input("Ingrese el ID de la receta que desea actualizar: ")
    nuevo_nombre = input("Nuevo nombre de la receta (deje en blanco para mantener el actual): ")
    nuevos_ingredientes = input("Nuevos ingredientes (deje en blanco para mantener los actuales): ")
    nuevos_pasos = input("Nuevos pasos de la receta (deje en blanco para mantener los actuales): ")

    # Construir la consulta de actualización
    consulta = 'UPDATE recetas SET '
    parametros = []

    if nuevo_nombre:
        consulta += 'nombre=?, '
        parametros.append(nuevo_nombre)

    if nuevos_ingredientes:
        consulta += 'ingredientes=?, '
        parametros.append(nuevos_ingredientes)

    if nuevos_pasos:
        consulta += 'pasos=?, '
        parametros.append(nuevos_pasos)

    # Eliminar la coma final y agregar la condición WHERE
    consulta = consulta.rstrip(', ')
    consulta += ' WHERE id=?'
    parametros.append(id_receta)

    try:
        with conectar_bd() as conexion:
            cursor = conexion.cursor()
            cursor.execute(consulta, tuple(parametros))
            conexion.commit()
            print("Receta actualizada exitosamente.")
    except sqlite3.Error as e:
        print("Error al actualizar la receta:", e)

# Función para eliminar una receta existente
def eliminar_receta():
    id_receta = input("Ingrese el ID de la receta que desea eliminar: ")

    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM recetas WHERE id=?', (id_receta,))
    conexion.commit()
    conexion.close()
    print("Receta eliminada exitosamente.")

# Función para ver el listado de recetas
def ver_recetas():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM recetas')
    recetas = cursor.fetchall()
    conexion.close()

    if not recetas:
        print("No hay recetas en el libro.")
    else:
        for receta in recetas:
            print(f"\nID: {receta[0]}")
            print(f"Nombre: {receta[1]}")
            print(f"Ingredientes: {receta[2]}")
            print(f"Pasos: {receta[3]}")

# Función para buscar ingredientes y pasos de receta
def buscar_receta():
    keyword = input("Ingrese el ingrediente o paso que desea buscar: ")

    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM recetas WHERE ingredientes LIKE ? OR pasos LIKE ?', ('%'+keyword+'%', '%'+keyword+'%'))
    resultados = cursor.fetchall()
    conexion.close()

    if not resultados:
        print(f"No se encontraron recetas que contengan '{keyword}'.")
    else:
        for resultado in resultados:
            print(f"\nID: {resultado[0]}")
            print(f"Nombre: {resultado[1]}")
            print(f"Ingredientes: {resultado[2]}")
            print(f"Pasos: {resultado[3]}")

# Función principal del programa
def main():
    crear_tabla()

    while True:
        print("\n--- Libro de Recetas ---")
        print("a) Agregar nueva receta")
        print("b) Actualizar receta existente")
        print("c) Eliminar receta existente")
        print("d) Ver listado de recetas")
        print("e) Buscar ingredientes y pasos de receta")
        print("f) Salir")

        opcion = input("\nSeleccione una opción: ").lower()

        if opcion == 'a':
            agregar_receta()
        elif opcion == 'b':
            actualizar_receta()
        elif opcion == 'c':
            eliminar_receta()
        elif opcion == 'd':
            ver_recetas()
        elif opcion == 'e':
            buscar_receta()
        elif opcion == 'f':
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Inténtelo de nuevo.")

if __name__ == "__main__":
    main()
