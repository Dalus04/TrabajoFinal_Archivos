#include<iostream>
#include<stdio.h>
#include<string.h>

using namespace std;

struct encabezado
{
    int NRS, PR, URE;
}e;

struct registro
{
    int NR, SR, ARE;
    char nom[50], estado[50];
}n,a,s,r;

FILE *fd;
int le = sizeof(struct encabezado);
int lr = sizeof(struct registro);

void escribir()
{
    char rpta; int sgte,pos; bool band;
    e.NRS = 0; e.PR = -1; e.URE = -1;

    if ((fd = fopen("personasALE.txt","w+t")) == NULL)
    {
        cout << "No se pudo crear el archivo." << endl;
        return;
    }
    
    fwrite(&e, le, 1, fd);

    do
    {
        n.NR = ++e.NRS;
        fflush(stdin);

        cout << "Tarea "<< n.NR << endl;
        cout << "Nombre: "; cin >> n.nom;
        cout << "Estado: "; cin >> n.estado;   
        n.ARE = 0;

        if (e.PR == -1)
        {
            n.SR = e.PR;
            e.PR = n.NR;
            fwrite(&n, lr, 1, fd);
        }
        else
        {
            sgte = e.PR; band = false;

            while (sgte != -1)
            {
                pos = (sgte-1) * lr + le;
                fseek(fd, pos, 0);
                fread(&s, lr, 1, fd);

                if (strcmp(n.nom, s.nom) > 0) 
                {
                    band = true;
                    a = s;
                    sgte = s.SR;
                    continue;
                }
                break;
            }
            
            if (band == false)
            {
                n.SR = e.PR;
                e.PR = n.NR;
            }
            if (band == true)
            {
                n.SR = a.SR;
                a.SR = n.NR;

                pos = (a.NR-1) * lr + le;
                fseek(fd, pos, 0);
                fwrite(&a, lr, 1, fd);
            }
            
            pos = (n.NR-1) * lr + le;
            fseek(fd, pos, 0);
            fwrite(&n, lr, 1, fd);
        }
        
        cout << "Desea mas registros?" <<endl; cin >> rpta;         
    } while (rpta == 's' || rpta == 'S');

    fseek(fd, 0, 0);
    fwrite(&e, le, 1, fd);
    fclose(fd);
}

void mostrar()
{
    int sgte,pos;

    if ((fd=fopen("personasALE.txt","rt")) == NULL)
    {
        cout << "No se puedo abrir el archivo" << endl;
        return;
    }

    fread(&e, le, 1, fd);
    sgte = e.PR;

    while (sgte != -1)
    {
        pos = (sgte - 1) * lr + le;
        fseek(fd, pos, 0);
        fread(&s, lr, 1, fd);
        cout << "Nombre: " << s.nom << ", Estado: " << s.estado << endl;
        sgte = s.SR;
    }
    
    fclose(fd);
}

void agregar()
{
    char rpta; int sgte,pos; bool band;

    if ((fd=fopen("personasALE.txt","r+t")) == NULL)
    {
        cout << "No se pudo crear el archivo" <<endl;
        return;
    }

    fread(&e, le, 1, fd);

    do
    {
        n.NR = ++e.NRS;
        fflush(stdin);
        cout << "Nombre: "; cin >> n.nom;
        cout << "Estado: "; cin >> n.estado;
        n.ARE = 0;

        if (e.PR == -1)
        {
            n.SR = e.PR;
            e.PR = n.NR;
            pos = (n.NR - 1) * lr + le;
            fseek(fd, pos, 0);
            fwrite(&n, lr, 1, fd);
        }
        else
        {
            sgte = e.PR;

            while (sgte != -1)
            {
                pos = (sgte - 1) * lr + le;
                fseek(fd, pos, 0);
                fread(&s, lr, 1, fd);
                if (strcmp(n.nom,s.nom) > 0)
                {
                    band = true;
                    a = s;
                    sgte = s.SR;
                    continue;
                }
                break;
            }
            
            if (band == false)
            {
                n.SR = e.PR;
                e.PR = n.NR;
            }
            
            if (band == true)
            {
                n.SR = a.SR;
                a.SR = n.NR;
                pos = (a.NR - 1) * lr + le;
                fseek(fd, pos, 0);
                fwrite(&a, lr, 1, fd);
            }
            
            pos = (n.NR - 1) * lr + le;
            fseek(fd, pos, 0);
            fwrite(&n, lr, 1, fd);
        }
    } while (rpta == 's' || rpta == 'S');
    
    fseek(fd, 0, 0);
    fwrite(&e, le, 1, fd);
    fclose(fd);
}

void eliminar()
{
    char rpta; int sgte,pos; bool band,flag=false;
    char nom_eliminado[20];

    if ((fd=fopen("personasALE.txt","r+t")) == NULL)
    {
        cout << "No se pudo abrir el archivo" << endl;
        return;
    }
    
    fread(&e, le, 1, fd);
    fflush(stdin);
    cout << "Nombre: "; cin >> nom_eliminado;

    while (fread(&r, lr, 1, fd) == 1)
    {
        if(strcmp(nom_eliminado,r.nom) == 0){
            flag = true;
            r.ARE = e.URE;
            e.URE = r.SR;
            break;
        }
    }
    
    if (flag == false)
    {
        cout << "El nombre no existe" << endl;
        return;
    }

    sgte = e.PR; band = false;

    while (sgte != -1)
    {
        pos = (sgte - 1) * lr + le;
        fseek(fd, pos, 0);
        fread(&s, lr, 1, fd);

        if (strcmp(r.nom,s.nom) > 0)
        {
            band = true;
            a = s;
            sgte = s.SR;
            continue;
        }
        break;
    }
    
    if (band == false)
    {
        e.PR = r.SR;
    }

    if (band == true)
    {
        a.SR = r.SR;
        pos = (a.NR - 1) * lr + le;
        fseek(fd, pos, 0);
        fwrite(&a, lr, 1, fd);
    }
    
    pos = (r.NR - 1) * lr + le;
    fseek(fd, pos, 0);
    fwrite(&r, lr, 1, fd);
    fseek(fd, 0, 0);
    fwrite(&e, le, 1, fd);
    fclose(fd);
}

void buscar()
{
    char nombre[20]; int sgte, pos; bool encontrado = false;

    fflush(stdin);
    cout << "Ingrese el nombre a buscar: "; cin >> nombre;

    if ((fd=fopen("personasALE.txt","rt")) == NULL)
    {
        cout << "No se pudo abrir el archivo" << endl;
        return;
    }

    fread(&e, le, 1, fd);
    sgte = e.PR;

    while (sgte != -1)
    {
        pos = (sgte -1) * lr + le;
        fseek(fd, pos, 0);
        fread(&s, lr, 1, fd);

        if (strcmp(s.nom,nombre) == 0)
        {
            encontrado = true;
            break;
        }
        
        a = s;
        sgte = s.SR;
    }
    
    if (encontrado == true)
    {
        cout << nombre << " ha sido encontrado" << endl;
        cout << "Estado: " << s.estado << endl;
    }
    else
    {
        cout << nombre << " no ha sido encontrado" << endl;
    }
    
    fclose(fd);
}

void modificar()
{
    char nombre[20]; int sgte, pos; bool encontrado = false;

    cout << "Ingrese el nombre a modificar: "; cin >> nombre;

    if ((fd = fopen("personasALE.txt", "r+t")) == NULL)
    {
        cout << "No se pudo abrir el archivo" << endl;
        return;
    }

    fread(&e, le, 1, fd);
    sgte = e.PR;

    while (sgte != -1)
    {
        pos = (sgte - 1) * lr + le;
        fseek(fd, pos, 0);
        fread(&s, lr, 1, fd);

        if (strcmp(s.nom, nombre) == 0)
        {
            encontrado = true;
            break;
        }

        sgte = s.SR;
    }

    if (encontrado)
    {
        cout << "Nombre: " << s.nom << ", Estado: " << s.estado << endl;
        cout << "Ingrese el nuevo estado: ";
        cin >> s.estado;

        pos = (s.NR - 1) * lr + le;
        fseek(fd, pos, 0);
        fwrite(&s, lr, 1, fd);

        cout << "Registro modificado exitosamente." << endl;
    }
    else
    {
        cout << nombre << " no ha sido encontrado" << endl;
    }

    fclose(fd);
}

void ver_archivo()
{
    if ((fd = fopen("personasALE.txt","rt")) == NULL)
    {
        cout << "No se puedo abrir el archivo." << endl;
        return;
    }

    fread(&e, le, 1, fd);
    cout << "NRS: " << e.NRS << "\tPR: " << e.PR << "\tURE: " << e.URE << endl; 
    cout << "NR\tNombre\tEstado\tSR\tARE" << endl;

    while (fread(&s, lr, 1, fd) == 1)
    {
        cout << s.NR << "\t" << s.nom << "\t" << s.estado << "\t" << s.SR << "\t" << s.ARE << endl;
    }
}

int main(int argc, char *argv[])
{
    int opc = 0;

    cout << "1. Escribir Tareas";
    cout << "\n2. Mostrar Tareas";
    cout << "\n3. Agregar Tarea";
    cout << "\n4. Eliminar Tarea";
    cout << "\n5. Buscar Tarea";
    cout << "\n6. Modificar Tarea";
    cout << "\n7. Ver Archivo";
    cout << "\n8. Salir" << endl;
    cin >> opc;

    switch (opc)
    {
    case 1:
        escribir();
        break;

    case 2:
        mostrar();
        break;

    case 3:
        agregar();
        break;

    case 4:
        eliminar();
        break;

    case 5:
        buscar();
        break;

    case 6:
        modificar();
        break;

    case 7:
        ver_archivo();
        break;
    
    default:
        break;
    }
}