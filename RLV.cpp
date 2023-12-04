#include<iostream>
#include<stdio.h>
#include<stdlib.h>
#include<string.h>

using namespace std;

#define D_REGISTRO "^"
#define D_CAMPO ";"

FILE *fd;

void escribir()
{
    char nom[20], estado[20], rpt;

    if((fd=fopen("RLV.txt","w")) == NULL)
    {
        cout << "No se puede crear el archivo";
        return;
    }

    cout << "\nTAREAS:"; 

    do
    {
        cout<<"\nNombre: "; cin>>nom;
        cout<<"Estado: "; cin>>estado;
        fwrite(nom, strlen(nom), 1, fd);
        fwrite(D_CAMPO, 1, 1, fd);
        fwrite(estado, strlen(estado), 1, fd);
        fwrite(D_CAMPO, 1, 1, fd);
        fwrite(D_REGISTRO,1,1,fd);

        cout << "Desea ingresar mas registros [S/N]: "; cin >> rpt;
    } while (rpt == 'S' || rpt == 's');
    fclose(fd);
}

void mostrar()
{
    char k;

    if((fd=fopen("RLV.txt","r")) == NULL)
    {
        cout << "No se puede abrir el archivo";
        return;
    }

    cout << "TAREAS:" <<endl;

    while (!feof(fd))
    {
        fflush(stdin);
        k = fgetc(fd);

        if (k != '^')
        {
            if (k == ';')
            {
                cout<<" ";
            }
            else
            {
                cout<<k;
            }
        }
        else
        {
            cout<<"\n";
        }
    }
    fclose(fd);
}

void agregar()
{
    char nom[20], estado[20], rpt;

    if((fd=fopen("RLV.txt","a+")) == NULL)
    {
        cout << "No se puede crear el archivo";
        return;
    }

    do
    {
        cout<<"\nNombre: "; cin>>nom;
        cout<<"Estado: "; cin>>estado;
        fwrite(nom, strlen(nom), 1, fd);
        fwrite(D_CAMPO, 1, 1, fd);
        fwrite(estado, strlen(estado), 1, fd);
        fwrite(D_CAMPO, 1, 1, fd);
        fwrite(D_REGISTRO,1,1,fd);

        cout << "Desea ingresar mas registros [S/N]: "; cin >> rpt;
    } while (rpt == 'S' || rpt == 's');
    fclose(fd);
}

void buscar(){
  string obj; 	
  string k;
  string RE;
  string ext;

  if((fd=fopen("RLV.txt","r"))==NULL){
    cout<<"Verifique, no se puede abrir el archivo"<<endl;
    return ;
  }
  cout<<"Ingrese el nombre para buscar su registro: ";cin>>obj;
  cout<<"\n\t";
  while(!feof(fd)){
    fflush(stdin);
    k = fgetc(fd);    
	if(k=="^"){
		for(int i=0;i<RE.length();i++){
			if(RE.substr(i,1)==";"){
				if(obj == ext){
					cout<<RE<<endl;
					break;
				}else{
					k = "";
					i = RE.length();
					ext = "";
					RE = "";
				}
			}else{
				ext = ext + RE.substr(i,1);
			}
		}
	}else{
		RE = RE + k;
	}
  }
  fclose(fd);
   cout<<endl;
}

void ver_archivo(){
	
	string k;
	string cadena;
		
  if((fd=fopen("RLV.txt","r"))==NULL){
    cout<<"\n\tVerifique, no se puede abrir el archivo"<<endl;
    return ;
  }
   while(!feof(fd)){
    fflush(stdin);
    k = fgetc(fd);
	cadena = cadena + k;
  }
  cout<<cadena;
    fclose(fd);
   cout<<endl;
}

int main (int argc, char *argv[]){
    int opc = 0;

    do
    {
        cout << "\nMENU"; 
        cout << "\n1. Escribir Tareas";
        cout << "\n2. Mostrar Tareas";
        cout << "\n3. Agregar Tarea";
        cout << "\n4. Eliminar Tarea";
        cout << "\n5. Buscar Tarea";
        cout << "\n6. Modificar Tarea";
        cout << "\n7. Ver Archivo";
        cout << "\n8. Salir";
        cout << "\nSeleecione una opcion: "; cin >> opc;

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
            //eliminar();
            break;

        case 5:
            buscar();
            break;
        
        case 6:
            //modificar();
            break;
        case 7:
            ver_archivo();
            break;
    
        default:
            break;
        }
    } while (opc != 8);

    return 0;
}