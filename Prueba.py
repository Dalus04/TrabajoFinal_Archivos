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
    registros = []
    e = Encabezado()
    le = 12  # Tamaño de la estructura Encabezado en bytes
    lr = 44  # Tamaño de la estructura Registro en bytes

    try:
        with open("pruebaALE.txt", "w+") as fd:
            fd.write(f"{e.NRS} {e.PR} {e.URE}\n")

            while True:
                n = Registro()
                n.NR = e.NRS + 1

                print(f"\nTarea {n.NR}")
                n.nom = input("Nombre: ")
                n.estado = input("Estado: ")
                n.ARE = 0

                nom_repetido = any(registro.nom == n.nom for registro in registros)
                if nom_repetido:
                    print("Ya existe un registro con el mismo nombre. Ingrese otro nombre.")
                else:
                    registros.append(n)

                    if e.PR == -1:
                        n.SR = e.PR
                        e.PR = n.NR
                    else:
                        sgte = e.PR
                        a = None
                        band = False

                        while sgte != -1:
                            pos = (sgte - 1) * lr + le
                            fd.seek(pos, os.SEEK_SET)
                            s = Registro()
                            s.__dict__ = read_registro(fd)

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
                            fd.seek(pos, os.SEEK_SET)
                            write_registro(fd, a)

                        pos = (n.NR - 1) * lr + le
                        fd.seek(pos, os.SEEK_SET)
                        write_registro(fd, n)

                rpta = input("Desea más registros? (s/n): ").lower()
                if rpta != 's':
                    break

            fd.seek(0, os.SEEK_SET)
            fd.write(f"{e.NRS} {e.PR} {e.URE}\n")

            for registro in registros:
                write_registro(fd, registro)

    except Exception as ex:
        print(f"Error: {ex}")

def ver_archivo():
    try:
        with open("pruebaALE.txt", "r") as fd:
            e = Encabezado()
            e.__dict__ = read_encabezado(fd)
            print(f"\nNRS: {e.NRS}\tPR: {e.PR}\tURE: {e.URE}")
            print("NR\tNombre\tEstado\tSR\tARE")

            while True:
                s = Registro()
                s.__dict__ = read_registro(fd)
                if not s or not s.NR:
                    break

                print(f"{s.NR}\t{s.nom}\t{s.estado}\t{s.SR}\t{s.ARE}")

    except Exception as ex:
        print(f"Error: {ex}")

def read_encabezado(fd):
    line = fd.readline()
    values = list(map(int, line.split()))
    e = Encabezado()
    e.NRS, e.PR, e.URE = values
    return e.__dict__

def read_registro(fd):
    line = fd.readline()
    if not line or not line.strip():
        return {'NR': 0}  # Retornar un diccionario con NR 0 cuando no hay más registros

    values = line.split()
    r = Registro()
    r.NR, r.SR, r.ARE, r.nom, r.estado = int(values[0]), int(values[1]), int(values[2]), values[3], values[4]
    return r.__dict__

def write_registro(fd, registro):
    fd.write(f"{registro.NR} {registro.SR} {registro.ARE} {registro.nom} {registro.estado}\n")

# Comentado para que no se ejecute automáticamente al correr el script
escribir()
ver_archivo()