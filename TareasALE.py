import pickle

class Encabezado:
    def __init__(self, NRS, PR, URE):
        self.NRS = NRS
        self.PR = PR
        self.URE = URE

class Registro:
    def __init__(self, NR, SR, ARE, nom, estado):
        self.NR = NR
        self.SR = SR
        self.ARE = ARE
        self.nom = nom.ljust(20)[:20]
        self.estado = estado.ljust(20)[:20]

e = Encabezado(0, -1, -1)
n = Registro(0, -1, 0, "", "")
a = Registro(0, -1, 0, "", "")
s = Registro(0, -1, 0, "", "")
r = Registro(0, -1, 0, "", "")

le = len(pickle.dumps(e))
lr = len(pickle.dumps(n))

def escribir():
    e.NRS = 0 
    e.PR = -1
    e.URE = -1
    n.NR = 0

    try:
        with open("TareasALE.txt", "wb+") as fd:
            pickle.dump(e, fd)

            while True:
                print(f"\nTAREA {n.NR + 1}:")
                n.nom = input("Nombre: ")
                n.estado = input("Estado: ")
                n.ARE = 0
                sgte = e.PR
                nomRepetido = False

                while sgte != -1:
                    pos = (sgte - 1) * lr + le
                    fd.seek(pos)
                    s = pickle.load(fd)

                    if n.nom == s.nom:
                        nomRepetido = True
                        print("Ya existe una Tarea con el mismo nombre. Ingrese otro nombre.")
                        break

                    sgte = s.SR
                
                if nomRepetido == False:
                    e.NRS += 1
                    n.NR = e.NRS

                    if e.PR == -1:
                        n.SR = e.PR
                        e.PR = n.NR
                        pickle.dump(n, fd)
                    else:
                        sgte = e.PR
                        band = False

                        while sgte != -1:
                            pos = (sgte - 1) * lr + le
                            fd.seek(pos)
                            s = pickle.load(fd)

                            if(n.nom > s.nom):
                                band = True
                                a = s
                                sgte = s.SR
                                continue
                            break

                        if band == False:
                            n.SR = e.PR
                            e.PR = n.NR
                        
                        if band == True:
                            n.SR = a.SR
                            a.SR = n.NR

                            pos = (a.NR-1) * lr + le
                            fd.seek(pos)
                            pickle.dump(a, fd)

                        pos = (n.NR-1) * lr + le
                        fd.seek(pos)
                        pickle.dump(n, fd)
                            

                rpta = input("Desea mas registros? (s/n): ")
                if rpta.lower() != 's':
                    break

            fd.seek(0)
            pickle.dump(e, fd)

    except FileNotFoundError:
        print("El archivo no existe.")
    except pickle.UnpicklingError:
        print("Error al deserializar el archivo.")

    
def mostrar():
    try:
        with open("TareasALE.txt", "rb") as fd:
            e = pickle.load(fd)
            sgte = e.PR

            print("\nTAREAS:")

            while sgte != -1:
                pos = (sgte - 1) * lr + le
                fd.seek(pos)
                s = pickle.load(fd)
                print(f"Nombre: {s.nom}, Estado: {s.estado}")
                sgte = s.SR

    except FileNotFoundError:
        print("El archivo no existe.")
    except pickle.UnpicklingError:
        print("Error al deserializar el archivo.")

def agregar():
    try:
        with open("TareasALE.txt", "r+b") as fd:
            fd.seek(0)
            e = pickle.load(fd)

            while True:
                n.nom = input("\nNombre: ")
                n.estado = input("Estado: ")
                n.ARE = 0
                sgte = e.PR 
                nomRepetido = False

                while sgte != -1:
                    pos = (sgte - 1) * lr + le
                    fd.seek(pos)
                    s = pickle.load(fd)

                    if n.nom == s.nom:
                        nomRepetido = True
                        print("Ya existe una Tarea con el mismo nombre. Ingrese otro nombre.")
                        break

                    sgte = s.SR

                if nomRepetido == False:
                    e.NRS += 1
                    n.NR = e.NRS

                    if e.PR == -1:
                        n.SR = e.PR
                        e.PR = n.NR
                        pos = (n.NR - 1) * lr + le
                        fd.seek(pos)
                        pickle.dump(n, fd)
                    else:
                        sgte = e.PR
                        band = False

                        while (sgte != -1):
                            pos = (sgte - 1) * lr + le
                            fd.seek(pos)
                            s = pickle.load(fd)

                            if (n.nom > s.nom):
                                band = True
                                a = s
                                sgte = s.SR
                                continue
                            break

                        if band == False:
                            n.SR = e.PR
                            e.PR = n.NR

                        if band == True:
                            n.SR = a.SR
                            a.SR = n.NR
                            pos = (a.NR - 1) * lr + le
                            fd.seek(pos)
                            pickle.dump(a, fd)

                        pos = (n.NR - 1) * lr + le
                        fd.seek(pos)
                        pickle.dump(n, fd)

                rpta = input("Desea mas registros? (s/n): ")
                if rpta.lower() != 's':
                    break

            fd.seek(0)
            pickle.dump(e, fd)

    except FileNotFoundError:
        print("El archivo no existe.")
    except pickle.UnpicklingError:
        print("Error al deserializar el archivo.")

def eliminar():
    try:
        with open("TareasALE.txt", "r+b") as fd:
            fd.seek(0)
            e = pickle.load(fd)

            nom_eliminar = input("\nNombre de la tarea a eliminar: ")
            flag = False
            sgte = e.PR

            while sgte != -1:
                pos = (sgte - 1) * lr + le
                fd.seek(pos)
                r = pickle.load(fd)
                
                if nom_eliminar == r.nom:
                    flag = True
                    r.ARE = e.URE
                    e.URE = r.NR
                    break

                sgte = r.SR

            if flag == False:
                print("La tarea no existe")
            else:    
                sgte = e.PR
                band = False

                while sgte != -1:
                    pos = (sgte - 1) * lr + le
                    fd.seek(pos)
                    s = pickle.load(fd)

                    if r.nom > s.nom:
                        band = True
                        a = s
                        sgte = s.SR
                        continue
                    break

                if band == False:
                    e.PR = r.SR
            
                if band == True:
                    a.SR = r.SR
                    pos = (a.NR - 1) * lr + le
                    fd.seek(pos)
                    pickle.dump(a, fd)
                    print("Tarea Eliminada")

                pos = (r.NR - 1) * lr + le
                fd.seek(pos)
                pickle.dump(r, fd)

                fd.seek(0)
                pickle.dump(e, fd)

    except FileNotFoundError:
        print("El archivo no existe.")
    except pickle.UnpicklingError:
        print("Error al deserializar el archivo.")

def buscar():
    try:
        with open("TareasALE.txt", "rb") as fd:
            fd.seek(0)
            e = pickle.load(fd)
            sgte = e.PR

            nombre = input("\nIngrese el nombre de la tarea a buscar: ")
            encontrado = False

            while sgte != -1:
                pos = (sgte -1) * lr + le
                fd.seek(pos)
                s = pickle.load(fd)

                if (s.nom == nombre):
                    encontrado = True
                    break

                a = s
                sgte = s.SR

            if encontrado == True:
                print(f"{nombre} ha sido encotrado")
                print(f"Estado: {s.estado}")
            else:
                print(f"{nombre} no ha sido encotrado")

    except FileNotFoundError:
        print("El archivo no existe.")
    except pickle.UnpicklingError:
        print("Error al deserializar el archivo.")

def modificar():
    try:
        with open("TareasALE.txt", "r+b") as fd:
            fd.seek(0)
            e = pickle.load(fd)
            sgte = e.PR

            nombre = input("\nIngrese el nombre de la tarea a modificar: ")
            encontrado = False

            while sgte != -1:
                pos = (sgte - 1) * lr + le
                fd.seek(pos)
                s = pickle.load(fd)

                if s.nom == nombre:
                    encontrado = True
                    break

                sgte = s.SR

            if encontrado == True:
                print(f"Nombre: {s.nom}, Estado: {s.estado}")
                s.estado = input("Ingrese el nuevo estado: ")

                pos = (s.NR - 1) * lr + le
                fd.seek(pos)
                pickle.dump(s, fd)

                print("Tarea modificada exitosamente")
            else:
                print(f"{nombre} no ha sido encontrado")

    except FileNotFoundError:
        print("El archivo no existe.")
    except pickle.UnpicklingError:
        print("Error al deserializar el archivo.")

def ver_archivo():
    try:
        with open("TareasALE.txt", "rb") as fd:
            e = pickle.load(fd)

            print(f"\nNRS: {e.NRS}\tPR: {e.PR}\tURE: {e.URE}")
            print("NR\tNombre\tEstado\tSR\tARE")
            
            sgte = e.NRS
            pos = le
    
            while sgte != 0:
                fd.seek(pos)
                s = pickle.load(fd)
                print(f"{s.NR}\t{s.nom}\t{s.estado}\t{s.SR}\t{s.ARE}")
                sgte -= 1
                pos += lr
        
    except FileNotFoundError:
        print("El archivo no existe.")
    except pickle.UnpicklingError:
        print("Error al deserializar el archivo.")

def main():
    while True:
        print("\nMENU GESTION DE TAREAS\n[1] Escribir\n[2] Mostrar\n[3] Agregar\n[4] Eliminar\n[5] Buscar\n[6] Modificar\n[7] Ver Archivo\n[8] Salir")
        
        opc = input("Seleccione una opcion: ")

        if opc == "1":
            escribir()
        elif opc == "2":
            mostrar()
        elif opc == "3":
            mostrar()
            agregar()
        elif opc == "4":
            mostrar()
            eliminar()
        elif opc == "5":
            buscar()
        elif opc == "6":
            mostrar()
            modificar()
        elif opc == "7":
            ver_archivo()
        elif opc == "8":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

        input("Presiona cualq. tecla para continuar...")

if __name__ == "__main__":
    main()