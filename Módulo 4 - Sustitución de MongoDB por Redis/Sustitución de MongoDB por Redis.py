from redis import StrictRedis
import json

# Configurar la conexión a Redis
DATABASE_URL = "redis://localhost:6379/0"
redis_client = StrictRedis.from_url(DATABASE_URL)

# Función para agregar una nueva receta
def agregar_receta():
    nombre = input("Nombre de la receta: ")
    ingredientes = input("Ingredientes (separados por coma): ")
    pasos = input("Pasos de la receta: ")

    receta = {
        "nombre": nombre,
        "ingredientes": ingredientes,
        "pasos": pasos
    }

    # Almacenar la receta en Redis como un JSON
    redis_client.set(f"receta:{nombre}", json.dumps(receta))
    print("Receta agregada exitosamente.")

# Función para actualizar una receta existente
def actualizar_receta():
    nombre = input("Ingrese el nombre de la receta que desea actualizar: ")
    receta_json = redis_client.get(f"receta:{nombre}")

    if receta_json:
        receta = json.loads(receta_json.decode('utf-8'))
        nuevo_nombre = input("Nuevo nombre de la receta (deje en blanco para mantener el actual): ")
        nuevos_ingredientes = input("Nuevos ingredientes (deje en blanco para mantener los actuales): ")
        nuevos_pasos = input("Nuevos pasos de la receta (deje en blanco para mantener los actuales): ")

        if nuevo_nombre:
            receta["nombre"] = nuevo_nombre
        if nuevos_ingredientes:
            receta["ingredientes"] = nuevos_ingredientes
        if nuevos_pasos:
            receta["pasos"] = nuevos_pasos

        # Actualizar la receta en Redis
        redis_client.set(f"receta:{nuevo_nombre}", json.dumps(receta))
        print("Receta actualizada exitosamente.")
    else:
        print("No se encontró la receta con el nombre proporcionado.")

# Función para eliminar una receta existente
def eliminar_receta():
    nombre = input("Ingrese el nombre de la receta que desea eliminar: ")

    # Eliminar la receta de Redis
    result = redis_client.delete(f"receta:{nombre}")

    if result > 0:
        print("Receta eliminada exitosamente.")
    else:
        print("No se encontró la receta con el nombre proporcionado.")

# Función para ver el listado de recetas
def ver_recetas():
    keys = redis_client.keys("receta:*")

    if not keys:
        print("No hay recetas en el libro.")
    else:
        for key in keys:
            receta_json = redis_client.get(key)
            receta = json.loads(receta_json.decode('utf-8'))

            print(f"\nNombre: {receta['nombre']}")
            print(f"Ingredientes: {receta['ingredientes']}")
            print(f"Pasos: {receta['pasos']}")

# Función para buscar ingredientes y pasos de receta
def buscar_receta():
    keyword = input("Ingrese el ingrediente o paso que desea buscar: ")
    keys = redis_client.keys("receta:*")

    resultados = []

    for key in keys:
        receta_json = redis_client.get(key)
        receta = json.loads(receta_json.decode('utf-8'))

        if keyword.lower() in receta["ingredientes"].lower() or keyword.lower() in receta["pasos"].lower():
            resultados.append(receta)

    if not resultados:
        print(f"No se encontraron recetas que contengan '{keyword}'.")
    else:
        for resultado in resultados:
            print(f"\nNombre: {resultado['nombre']}")
            print(f"Ingredientes: {resultado['ingredientes']}")
            print(f"Pasos: {resultado['pasos']}")

# Función principal del programa
def main():
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
