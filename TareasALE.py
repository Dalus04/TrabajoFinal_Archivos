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
                print(f"\nTarea {n.NR + 1}:")
                n.nom = input("Nombre: ")
                n.estado = input("Estado: ")
                n.ARE = 0
                sgte = e.PR
                nomReptido = False
                
                if nomReptido == False:
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

#escribir()
mostrar()