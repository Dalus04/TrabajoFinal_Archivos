import os

class Encabezado:
    def __init__(self):
        self.NRS = 0
        self.PR = -1
        self.URE = -1

class Registro:
    def __init__(self):
        self.NR = 0
        self.SR = 0
        self.ARE = 0
        self.nom = ""
        self.estado = ""

def escribir():
    global e, n, a, s, r
    rpta = 's'

    try:
        with open("personasALE.txt", "w+t") as fd:
            e.NRS = 0
            e.PR = -1
            e.URE = -1
            n.NR = 0
            fd.write(f"{e.NRS} {e.PR} {e.URE}\n")

            while rpta.lower() == 's':
                print(f"\nTarea {n.NR + 1}")
                n.nom = input("Nombre: ")
                n.estado = input("Estado: ")
                n.ARE = 0
                sgte = e.PR
                nomRepetido = False

                while sgte != -1:
                    pos = (sgte - 1) * lr + le
                    fd.seek(pos, 0)
                    s = Registro()
                    s.__dict__ = leer_registro(fd)

                    if n.nom == s.nom:
                        nomRepetido = True
                        print("Ya existe un registro con el mismo nombre. Ingrese otro nombre.")
                        break

                    sgte = s.SR

                if not nomRepetido:
                    n.NR = e.NRS + 1
                    if e.PR == -1:
                        n.SR = e.PR
                        e.PR = n.NR
                        escribir_registro(fd, n)
                    else:
                        sgte = e.PR
                        band = False

                        while sgte != -1:
                            pos = (sgte - 1) * lr + le
                            fd.seek(pos, 0)
                            s = Registro()
                            s.__dict__ = leer_registro(fd)

                            if n.nom > s.nom:
                                band = True
                                a = s
                                sgte = s.SR
                                continue
                            break

                        if not band:
                            n.SR = e.PR
                            e.PR = n.NR
                        elif band:
                            n.SR = a.SR
                            a.SR = n.NR
                            pos = (a.NR - 1) * lr + le
                            fd.seek(pos, 0)
                            escribir_registro(fd, a)

                        pos = (n.NR - 1) * lr + le
                        fd.seek(pos, 0)
                        escribir_registro(fd, n)

                rpta = input("Desea más registros? (s/n): ")

        with open("personasALE.txt", "r+t") as fd:
            fd.write(f"{e.NRS} {e.PR} {e.URE}\n")

    except Exception as ex:
        print(f"Error: {ex}")

def mostrar():
    global e, s
    sgte = 0
    pos = 0

    try:
        with open("personasALE.txt", "rt") as fd:
            e = Encabezado()
            e.__dict__ = leer_encabezado(fd)
            sgte = e.PR
            print("\nTAREAS:")

            while sgte != -1:
                pos = (sgte - 1) * lr + le
                fd.seek(pos, 0)
                s = Registro()
                s.__dict__ = leer_registro(fd)
                print(f"Nombre: {s.nom}, Estado: {s.estado}")
                sgte = s.SR

    except Exception as ex:
        print(f"Error: {ex}")

def agregar():
    global e, n, a, s
    rpta = 's'

    try:
        with open("personasALE.txt", "r+t") as fd:
            e.__dict__ = leer_encabezado(fd)

            while rpta.lower() == 's':
                n.nom = input("Nombre: ")
                n.estado = input("Estado: ")
                n.ARE = 0
                sgte = e.PR
                nomRepetido = False

                while sgte != -1:
                    pos = (sgte - 1) * lr + le
                    fd.seek(pos, 0)
                    s = Registro()
                    s.__dict__ = leer_registro(fd)

                    if n.nom == s.nom:
                        nomRepetido = True
                        print("Ya existe un registro con el mismo nombre. Ingrese otro nombre.")
                        break

                    sgte = s.SR

                if not nomRepetido:
                    n.NR = e.NRS + 1

                    if e.PR == -1:
                        n.SR = e.PR
                        e.PR = n.NR
                        pos = (n.NR - 1) * lr + le
                        fd.seek(pos, 0)
                        escribir_registro(fd, n)
                    else:
                        sgte = e.PR

                        while sgte != -1:
                            pos = (sgte - 1) * lr + le
                            fd.seek(pos, 0)
                            s = Registro()
                            s.__dict__ = leer_registro(fd)

                            if n.nom > s.nom:
                                band = True
                                a = s
                                sgte = s.SR
                                continue
                            break

                        if not band:
                            n.SR = e.PR
                            e.PR = n.NR
                        elif band:
                            n.SR = a.SR
                            a.SR = n.NR
                            pos = (a.NR - 1) * lr + le
                            fd.seek(pos, 0)
                            escribir_registro(fd, a)

                        pos = (n.NR - 1) * lr + le
                        fd.seek(pos, 0)
                        escribir_registro(fd, n)

                rpta = input("Desea más registros? (s/n): ")

            fd.seek(0, 0)
            escribir_encabezado(fd, e)

    except Exception as ex:
        print(f"Error: {ex}")

def eliminar():
    global e, r
    flag = False
    nom_eliminado = input("Nombre: ")

    try:
        with open("personasALE.txt", "r+t") as fd:
            e.__dict__ = leer_encabezado(fd)

            while True:
                r = Registro()
                r.__dict__ = leer_registro(fd)

                if nom_eliminado == r.nom:
                    flag = True
                    r.ARE = e.URE
                    e.URE = r.NR
                    break

            if not flag:
                print("El nombre no existe.")
                return

            sgte = e.PR
            band = False

            while sgte != -1:
                pos = (sgte - 1) * lr + le
                fd.seek(pos, 0)
                s = Registro()
                s.__dict__ = leer_registro(fd)

                if r.nom > s.nom:
                    band = True
                    a = s
                    sgte = s.SR
                    continue
                break

            if not band:
                e.PR = r.SR

            if band:
                a.SR = r.SR
                pos = (a.NR - 1) * lr + le
                fd.seek(pos, 0)
                escribir_registro(fd, a)
                print("Registro Eliminado")

            pos = (r.NR - 1) * lr + le
            fd.seek(pos, 0)
            escribir_registro(fd, r)
            fd.seek(0, 0)
            escribir_encabezado(fd, e)

    except Exception as ex:
        print(f"Error: {ex}")

def buscar():
    global e, s
    encontrado = False
    nombre = input("Ingrese el nombre a buscar: ")
    sgte = 0
    pos = 0

    try:
        with open("personasALE.txt", "rt") as fd:
            e.__dict__ = leer_encabezado(fd)
            sgte = e.PR

            while sgte != -1:
                pos = (sgte - 1) * lr + le
                fd.seek(pos, 0)
                s = Registro()
                s.__dict__ = leer_registro(fd)

                if s.nom == nombre:
                    encontrado = True
                    break

                a = s
                sgte = s.SR

            if encontrado:
                print(f"{nombre} ha sido encontrado")
                print(f"Estado: {s.estado}")
            else:
                print(f"{nombre} no ha sido encontrado")

    except Exception as ex:
        print(f"Error: {ex}")

def modificar():
    global e, s
    encontrado = False
    nombre = input("Ingrese el nombre de la tarea: ")

    try:
        with open("personasALE.txt", "r+t") as fd:
            e.__dict__ = leer_encabezado(fd)
            sgte = e.PR

            while sgte != -1:
                pos = (sgte - 1) * lr + le
                fd.seek(pos, 0)
                s = Registro()
                s.__dict__ = leer_registro(fd)

                if s.nom == nombre:
                    encontrado = True
                    break

                sgte = s.SR

            if encontrado:
                print(f"Nombre: {s.nom}, Estado: {s.estado}")
                nuevo_estado = input("Ingrese el nuevo estado: ")
                pos = (s.NR - 1) * lr + le
                fd.seek(pos, 0)
                s.estado = nuevo_estado
                escribir_registro(fd, s)
                print("Registro modificado exitosamente.")
            else:
                print(f"{nombre} no ha sido encontrado")

    except Exception as ex:
        print(f"Error: {ex}")

def ver_archivo():
    global e, s
    try:
        with open("personasALE.txt", "rt") as fd:
            e.__dict__ = leer_encabezado(fd)
            print(f"\nNRS: {e.NRS}\tPR: {e.PR}\tURE: {e.URE}")
            print("NR\tNombre\tEstado\tSR\tARE")

            while True:
                s = Registro()
                s.__dict__ = leer_registro(fd)

                if not s.NR:
                    break

                print(f"{s.NR}\t{s.nom}\t{s.estado}\t{s.SR}\t{s.ARE}")

    except Exception as ex:
        print(f"Error: {ex}")

def leer_encabezado(fd):
    line = fd.readline().strip()
    e = Encabezado()
    e.NRS, e.PR, e.URE = map(int, line.split())
    return e.__dict__

def escribir_encabezado(fd, e):
    fd.seek(0, 0)
    fd.write(f"{e['NRS']} {e['PR']} {e['URE']}\n")

def leer_registro(fd):
    line = fd.readline().strip()
    r = Registro()
    r.NR, r.SR, r.ARE, r.nom, r.estado = line.split()
    r.NR, r.SR, r.ARE = map(int, [r.NR, r.SR, r.ARE])
    return r.__dict__

def escribir_registro(fd, r):
    fd.write(f"{r['NR']} {r['SR']} {r['ARE']} {r['nom']} {r['estado']}\n")

if __name__ == "__main__":
    fd = None
    le = 28
    lr = 68
    e = Encabezado()
    n = Registro()
    a = Registro()
    s = Registro()
    r = Registro()

    try:
        opc = 0
        while opc != 8:
            print("\nMENU")
            print("1. Escribir Tareas")
            print("2. Mostrar Tareas")
            print("3. Agregar Tarea")
            print("4. Eliminar Tarea")
            print("5. Buscar Tarea")
            print("6. Modificar Tarea")
            print("7. Ver Archivo")
            print("8. Salir")

            opc = int(input("Seleccione una opción: "))

            if opc == 1:
                escribir()
            elif opc == 2:
                mostrar()
            elif opc == 3:
                agregar()
            elif opc == 4:
                eliminar()
            elif opc == 5:
                buscar()
            elif opc == 6:
                modificar()
            elif opc == 7:
                ver_archivo()

    except Exception as ex:
        print(f"Error: {ex}")

    finally:
        if fd:
            fd.close()