from pymongo import MongoClient

# Configurar la conexión a MongoDB
DATABASE_URL = "mongodb://JeysonRodriguez:123456789@localhost:27017/"
client = MongoClient(DATABASE_URL)
db = client["recetas"]

# Definir el modelo de Recetas
class Receta:
    def __init__(self, nombre, ingredientes, pasos):
        self.nombre = nombre
        self.ingredientes = ingredientes
        self.pasos = pasos

# Función para agregar una nueva receta
def agregar_receta():
    nombre = input("Nombre de la receta: ")
    ingredientes = input("Ingredientes (separados por coma): ")
    pasos = input("Pasos de la receta: ")

    nueva_receta = Receta(nombre=nombre, ingredientes=ingredientes, pasos=pasos)
    db.recetas.insert_one(vars(nueva_receta))
    print("Receta agregada exitosamente.")

# Función para actualizar una receta existente
def actualizar_receta():
    id_receta = input("Ingrese el ID de la receta que desea actualizar: ")
    receta = db.recetas.find_one({"_id": id_receta})

    if receta:
        nuevo_nombre = input("Nuevo nombre de la receta (deje en blanco para mantener el actual): ")
        nuevos_ingredientes = input("Nuevos ingredientes (deje en blanco para mantener los actuales): ")
        nuevos_pasos = input("Nuevos pasos de la receta (deje en blanco para mantener los actuales): ")

        if nuevo_nombre:
            receta['nombre'] = nuevo_nombre
        if nuevos_ingredientes:
            receta['ingredientes'] = nuevos_ingredientes
        if nuevos_pasos:
            receta['pasos'] = nuevos_pasos

        db.recetas.update_one({"_id": id_receta}, {"$set": receta})
        print("Receta actualizada exitosamente.")
    else:
        print("No se encontró la receta con el ID proporcionado.")

# Función para eliminar una receta existente
def eliminar_receta():
    id_receta = input("Ingrese el ID de la receta que desea eliminar: ")
    result = db.recetas.delete_one({"_id": id_receta})

    if result.deleted_count > 0:
        print("Receta eliminada exitosamente.")
    else:
        print("No se encontró la receta con el ID proporcionado.")

# Función para ver el listado de recetas
def ver_recetas():
    recetas = db.recetas.find()

    if recetas.count_documents({}) == 0:
        print("No hay recetas en el libro.")
    else:
        for receta in recetas:
            print(f"\nID: {receta['_id']}")
            print(f"Nombre: {receta['nombre']}")
            print(f"Ingredientes: {receta['ingredientes']}")
            print(f"Pasos: {receta['pasos']}")

# Función para buscar ingredientes y pasos de receta
def buscar_receta():
    keyword = input("Ingrese el ingrediente o paso que desea buscar: ")
    resultados = db.recetas.find({"$or": [{"ingredientes": {"$regex": keyword, "$options": "i"}},
                                          {"pasos": {"$regex": keyword, "$options": "i"}}]})

    if resultados.count_documents({}) == 0:
        print(f"No se encontraron recetas que contengan '{keyword}'.")
    else:
        for resultado in resultados:
            print(f"\nID: {resultado['_id']}")
            print(f"Nombre: {resultado['nombre']}")
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
