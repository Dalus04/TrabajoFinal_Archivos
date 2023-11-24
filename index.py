import json

class Tarea:
    def __init__(self, descripcion, fecha_limite, estado):
        self.descripcion = descripcion
        self.fecha_limite = fecha_limite
        self.estado = estado
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.inicio = None

    def agregar_tarea(self, tarea):
        if not self.inicio:
            self.inicio = tarea
        else:
            actual = self.inicio
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = tarea

    def mostrar_tareas(self):
        actual = self.inicio
        while actual:
            print(f"Descripción: {actual.descripcion}, Fecha límite: {actual.fecha_limite}, Estado: {actual.estado}")
            actual = actual.siguiente

    def cambiar_propiedad_en_lista(self, propiedad, valor_a_buscar, nuevo_valor):
        actual = self.inicio
        while actual:
            if getattr(actual, propiedad) == valor_a_buscar:
                setattr(actual, propiedad, nuevo_valor)
            actual = actual.siguiente

    def eliminar_tarea(self, valor_a_buscar):
        if not self.inicio:
            return

        if self.inicio.descripcion == valor_a_buscar:
            self.inicio = self.inicio.siguiente
            return

        actual = self.inicio
        while actual.siguiente:
            if actual.siguiente.descripcion == valor_a_buscar:
                actual.siguiente = actual.siguiente.siguiente
                return
            actual = actual.siguiente

    def to_dict(self):
        data = []
        actual = self.inicio
        while actual:
            tarea_dict = {
                "descripcion": actual.descripcion,
                "fecha_limite": actual.fecha_limite,
                "estado": actual.estado
            }
            data.append(tarea_dict)
            actual = actual.siguiente
        return data

    def from_dict(self, data):
        for tarea_dict in data:
            tarea = Tarea(
                tarea_dict["descripcion"],
                tarea_dict["fecha_limite"],
                tarea_dict["estado"]
            )
            self.agregar_tarea(tarea)

    def guardar_en_archivo(self, archivo):
        data = self.to_dict()
        with open(archivo, 'w') as f:
            json.dump(data, f, indent=2)

    def cargar_desde_archivo(self, archivo):
        try:
            with open(archivo, 'r') as f:
                data = json.load(f)
            self.from_dict(data)
            print("Lista de tareas cargada desde el archivo.")
        except FileNotFoundError:
            print("Archivo no encontrado. Se creará uno nuevo.")

# Función para ingresar una tarea desde el usuario
def ingresar_tarea():
    descripcion = input("Ingrese la descripción de la tarea: ")
    fecha_limite = input("Ingrese la fecha límite de la tarea: ")
    estado = input("Ingrese el estado de la tarea: ")
    return Tarea(descripcion, fecha_limite, estado)

# Función para realizar cambios en una tarea
def realizar_cambio(lista_tareas):
    propiedad = input("Ingrese la propiedad que desea cambiar (descripcion/fecha_limite/estado): ")
    valor_a_buscar = input("Ingrese el valor actual de la propiedad: ")
    nuevo_valor = input(f"Ingrese el nuevo valor para la propiedad {propiedad}: ")
    lista_tareas.cambiar_propiedad_en_lista(propiedad, valor_a_buscar, nuevo_valor)

# Función para eliminar una tarea
def eliminar_tarea(lista_tareas):
    valor_a_buscar = input("Ingrese la descripción de la tarea que desea eliminar: ")
    lista_tareas.eliminar_tarea(valor_a_buscar)

# Nombre del archivo para almacenar las tareas
archivo_tareas = "tasks.txt"

# Intentar cargar la lista de tareas desde el archivo
lista_tareas = ListaEnlazada()
try:
    lista_tareas.cargar_desde_archivo(archivo_tareas)
    print("\nTareas después de cargar:")
    lista_tareas.mostrar_tareas()
except FileNotFoundError:
    print("Archivo no encontrado. Se creará uno nuevo.")

# Menú principal
while True:
    print("\n1. Agregar tarea")
    print("2. Mostrar tareas")
    print("3. Realizar cambios en una tarea")
    print("4. Eliminar tarea")
    print("5. Guardar y salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        tarea = ingresar_tarea()
        lista_tareas.agregar_tarea(tarea)
    elif opcion == "2":
        print("\nTareas:")
        lista_tareas.mostrar_tareas()
    elif opcion == "3":
        realizar_cambio(lista_tareas)
    elif opcion == "4":
        eliminar_tarea(lista_tareas)
    elif opcion == "5":
        # Guardar la lista de tareas en el archivo y salir
        lista_tareas.guardar_en_archivo(archivo_tareas)
        break
    else:
        print("Opción no válida. Inténtelo de nuevo.")
