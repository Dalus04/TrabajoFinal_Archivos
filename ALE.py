class Encabezado:
    def __init__(self):
        self.NRS = 0
        self.PR = -1
        self.URE = -1

class Registro:
    def __init__(self, NR, nom, estado):
        self.NR = NR
        self.nom = nom
        self.estado = estado
        self.SR = -1
        self.ARE = 0

def escribir():
    registros = []
    encabezado = Encabezado()

    try:
        with open("personasALEP.txt", "w") as file:
            while True:
                NR = encabezado.NRS + 1
                nom = input("Nombre: ")
                estado = input("Estado: ")

                nuevo_registro = Registro(NR, nom, estado)

                if encabezado.PR == -1:
                    nuevo_registro.SR = encabezado.PR
                    encabezado.PR = NR
                else:
                    sgte = encabezado.PR
                    anterior = None

                    while sgte != -1 and nuevo_registro.nom > registros[sgte - 1].nom:
                        anterior = sgte
                        sgte = registros[sgte - 1].SR

                    nuevo_registro.SR = sgte

                    if anterior is not None:
                        registros[anterior - 1].SR = NR
                    else:
                        encabezado.PR = NR

                registros.append(nuevo_registro)
                encabezado.NRS += 1

                respuesta = input("Desea más registros? (s/n): ")
                if respuesta.lower() != 's':
                    break

            # Escribir el encabezado actualizado al archivo
            file.write(f"{encabezado.NRS} {encabezado.PR} {encabezado.URE}\n")

            # Escribir registros al archivo
            for registro in registros:
                file.write(f"{registro.NR} {registro.nom} {registro.estado} {registro.SR} {registro.ARE}\n")

    except IOError:
        print("No se pudo crear el archivo.")

def eliminar():
    try:
        with open("personasALEP.txt", "r") as file:
            lines = file.readlines()

        # Leer el encabezado
        encabezado_data = lines[0].split()
        encabezado = Encabezado()
        encabezado.NRS, encabezado.PR, encabezado.URE = map(int, encabezado_data)

        # Obtener el nombre de la tarea a eliminar
        nom_eliminado = input("Nombre de la tarea a eliminar: ")

        # Buscar el registro a eliminar y actualizar la lista de registros
        registros = []
        flag = False
        for line in lines[1:]:
            data = line.split()
            registro = Registro(int(data[0]), data[1], data[2])
            registro.SR, registro.ARE = map(int, data[3:5])

            if registro.nom == nom_eliminado:
                flag = True
                registro.ARE = encabezado.URE
                encabezado.URE = registro.NR
            registros.append(registro)

        if not flag:
            print("La tarea no existe.")
            return

        # Verificar si la tarea eliminada es la primera y actualizar PR
        if registros and registros[0].nom == nom_eliminado:
            encabezado.PR = registros[0].SR

        # Escribir la información actualizada al archivo
        with open("personasALEP.txt", "w") as file:
            file.write(f"{encabezado.NRS} {encabezado.PR} {encabezado.URE}\n")
            for registro in registros:
                file.write(f"{registro.NR} {registro.nom} {registro.estado} {registro.SR} {registro.ARE}\n")

        print("Tarea eliminada con éxito.")

    except IOError:
        print("No se pudo abrir o modificar el archivo.")


def ver_archivo():
    try:
        with open("personasALEP.txt", "r") as file:
            line = file.readline().split()
            encabezado = Encabezado()
            encabezado.NRS, encabezado.PR, encabezado.URE = map(int, line)
            
            print(f"NRS: {encabezado.NRS}\tPR: {encabezado.PR}\tURE: {encabezado.URE}")
            print("NR\tNombre\tEstado\tSR\tARE")

            for line in file:
                data = line.split()
                registro = Registro(int(data[0]), data[1], data[2])
                registro.SR, registro.ARE = map(int, data[3:5])
                print(f"{registro.NR}\t{registro.nom}\t{registro.estado}\t{registro.SR}\t{registro.ARE}")

    except IOError:
        print("No se pudo abrir el archivo.")

def main():
    escribir()
    ver_archivo()
    eliminar()
    ver_archivo()

if __name__ == "__main__":
    main()