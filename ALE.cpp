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

                if (strcmp(n.nom, s.nom) > 0) //ordenar
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
    escribir();
    ver_archivo();
}