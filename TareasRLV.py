def escribir():
    with open("TareasRLV.txt", "w") as fd:
        while True:
            nom = input("\nNombre: ")
            estado = input("Estado: ")
            fd.write(f"{nom};{estado}^\n")
            rpt = input("Desea ingresar más registros [S/N]: ").upper()
            if rpt != 'S':
                break

def mostrar():
    try:
        with open("TareasRLV.txt", "r") as fd:
            print("\nTAREAS:")
            n = 1
            for line in fd:
                line = line.replace(";", " ").replace("^", "\n").strip()
                print(f"{n} {line}")
                n += 1
    except FileNotFoundError:
        print("No se puede abrir el archivo")

def agregar():
    with open("TareasRLV.txt", "a+") as fd:
        while True:
            nom = input("\nNombre: ")
            estado = input("Estado: ")
            fd.write(f"{nom};{estado}^\n")
            rpt = input("Desea ingresar más registros [S/N]: ").upper()
            if rpt != 'S':
                break

def eliminar():
    obj = input("\nIngrese el nombre de la tarea a eliminar: ")

    try:
        with open("TareasRLV.txt", "r") as fd:
            lines = fd.readlines()

        with open("TareasRLV.txt", "w") as fd:
            found = False
            for line in lines:
                nombre, _ = line.split(";")
                if nombre == obj:
                    found = True
                else:
                    fd.write(line)

            if not found:
                print(f"No se encontró la tarea '{obj}' en el archivo.")
            else:
                print(f"Registro '{obj}' eliminado exitosamente.")
        
    except FileNotFoundError:
        print("Verifique, no se puede abrir el archivo")

def buscar():
    obj = input("\nIngrese el nombre para buscar su registro: ")
    
    try:
        with open("TareasRLV.txt", "r") as fd:
            print("\nTAREAS:")
            for line in fd.readlines():
                nombre, estado = line.split(";")
                if obj == nombre:
                    print(line.replace(";", " ").replace("^", "\n").strip())
                    break
            else:
                print(f"No se encontró ninguna tarea con el nombre '{obj}'.")
    except FileNotFoundError:
        print("Verifique, no se puede abrir el archivo")

def modificar():
    obj = input("Ingrese el nombre de la tarea a modificar: ")
    nuevo_estado = input("Ingrese el nuevo estado de la tarea: ")

    try:
        with open("TareasRLV.txt", "r") as fd:
            lines = fd.readlines()

        with open("TareasRLV.txt", "w") as fd:
            found = False
            for line in lines:
                nombre, estado = line.split(";")
                if nombre == obj:
                    found = True
                    fd.write(f"{nombre};{nuevo_estado}^\n")
                else:
                    fd.write(line)

            if not found:
                print(f"No se encontró la tarea '{obj}' en el archivo.")
            else:
                print(f"Tarea '{obj}' modificada exitosamente.")

    except FileNotFoundError:
        print("Verifique, no se puede abrir el archivo")


def ver_archivo():
    try:
        with open("TareasRLV.txt", "r") as fd:
            print(fd.read())
    except FileNotFoundError:
        print("Verifique, no se puede abrir el archivo")

def main():
    while True:
        print("\nMENU GESTION DE TAREAS\n[1] Escribir\n[2] Mostrar\n[3] Agregar\n[4] Eliminar\n[5] Buscar\n[6] Modificar\n[7] Ver Archivo\n[8] Salir")

        opc = int(input("Seleccione una opción: "))

        if opc == 1:
            escribir()
        elif opc == 2:
            mostrar()
        elif opc == 3:
            mostrar()
            agregar()
        elif opc == 4:
            mostrar()
            eliminar()
        elif opc == 5:
            buscar()
        elif opc == 6:
            mostrar()
            modificar()
        elif opc == 7:
            ver_archivo()
        elif opc == 8:
            break
        else:
            print("Opción no válida. Intente de nuevo.")

        input("Presiona cualq. tecla para continuar...")

if __name__ == "__main__":
    main()