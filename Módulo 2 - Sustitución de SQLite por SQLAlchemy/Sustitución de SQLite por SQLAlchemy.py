from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session

# Configurar la conexión a MariaDB
DATABASE_URL = "mysql+mysqlconnector://JeysonRodriguez:123456789@localhost/recetas"
engine = create_engine(DATABASE_URL)

# Crear la sesión para interactuar con la base de datos
Base = declarative_base()
session = Session(engine)

# Definir el modelo de recetas
class Receta(Base):
    __tablename__ = 'recetas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    ingredientes = Column(String(1000), nullable=False)
    pasos = Column(String(2000), nullable=False)

# Función para conectar a la base de datos y crear la tabla de recetas
def conectar_bd():
    Base.metadata.create_all(bind=engine)
    return engine

# Función para agregar una nueva receta
def agregar_receta():
    nombre = input("Nombre de la receta: ")
    ingredientes = input("Ingredientes (separados por coma): ")
    pasos = input("Pasos de la receta: ")

    nueva_receta = Receta(nombre=nombre, ingredientes=ingredientes, pasos=pasos)
    session.add(nueva_receta)
    session.commit()
    print("Receta agregada exitosamente.")

# Función para actualizar una receta existente
def actualizar_receta():
    id_receta = input("Ingrese el ID de la receta que desea actualizar: ")
    receta = session.get(Receta, id_receta)
 

    if receta:
        nuevo_nombre = input("Nuevo nombre de la receta (deje en blanco para mantener el actual): ")
        nuevos_ingredientes = input("Nuevos ingredientes (deje en blanco para mantener los actuales): ")
        nuevos_pasos = input("Nuevos pasos de la receta (deje en blanco para mantener los actuales): ")

        if nuevo_nombre:
            receta.nombre = nuevo_nombre
        if nuevos_ingredientes:
            receta.ingredientes = nuevos_ingredientes
        if nuevos_pasos:
            receta.pasos = nuevos_pasos

        session.commit()
        print("Receta actualizada exitosamente.")
    else:
        print("No se encontró la receta con el ID proporcionado.")

# Función para eliminar una receta existente
def eliminar_receta():
    id_receta = input("Ingrese el ID de la receta que desea eliminar: ")
    receta = session.get(Receta, id_receta)


    if receta:
        session.delete(receta)
        session.commit()
        print("Receta eliminada exitosamente.")
    else:
        print("No se encontró la receta con el ID proporcionado.")

# Función para ver el listado de recetas
def ver_recetas():
    recetas = session.query(Receta).all()

    if not recetas:
        print("No hay recetas en el libro.")
    else:
        for receta in recetas:
            print(f"\nID: {receta.id}")
            print(f"Nombre: {receta.nombre}")
            print(f"Ingredientes: {receta.ingredientes}")
            print(f"Pasos: {receta.pasos}")

# Función para buscar ingredientes y pasos de receta
def buscar_receta():
    keyword = input("Ingrese el ingrediente o paso que desea buscar: ")
    resultados = session.query(Receta).filter(Receta.ingredientes.like(f"%{keyword}%") | Receta.pasos.like(f"%{keyword}%")).all()

    if not resultados:
        print(f"No se encontraron recetas que contengan '{keyword}'.")
    else:
        for resultado in resultados:
            print(f"\nID: {resultado.id}")
            print(f"Nombre: {resultado.nombre}")
            print(f"Ingredientes: {resultado.ingredientes}")
            print(f"Pasos: {resultado.pasos}")

# Función principal del programa
def main():
    conectar_bd()

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
