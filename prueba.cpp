//Listas enlazadas
#include<iostream>
#include<stdio.h>
#include<string.h>

using namespace std;

struct encabezado{
		int NRS;
		int PR;
		int URE;
}e;

struct registro{
		int NR;
		char nom[20];
		int SR;
		int ARE;
}n,a,s,r;

FILE *fd;
int le = sizeof(struct encabezado);
int lr = sizeof(struct registro);

void escribir(){
		char rpta; int sgte,pos; bool band;
		e.NRS=0; e.PR = -1; e.URE = -1;
		if((fd=fopen("personas.txt","w+t"))==NULL){
				cout<<"no se pudo crear el archivo"<<endl;
				return;
		}
		fwrite(&e,le,1,fd); //deja un espacio reservado para el encabezado		
		do{
				n.NR = ++e.NRS;
				fflush(stdin);
				cout<<"nombre:"<<endl; cin>>n.nom; n.ARE = 0;
				if(e.PR == -1){//se guardar? el primer registro f?sico
						n.SR = e.PR;
						e.PR = n.NR;
						fwrite(&n,lr,1,fd);
				}
				else{//se guardar? un registro que no es primer reg f?sico
					//Lectura lista enlazada
					sgte = e.PR; band=false;
					while(sgte!= -1){
						pos = (sgte-1)*lr + le;
						fseek(fd,pos,0);
						fread(&s,lr,1,fd);
						if(strcmp(n.nom,s.nom)>0){
							band=true;
							a = s;
							sgte = s.SR;
							continue;
						}
						break;
					}
					//fin de lectura de lista enlazada
					if(band==false){//caso 1:actualiza encabezado
						n.SR = e.PR;
						e.PR = n.NR;
					}
					if(band==true){//caso 2:actualiza reg anterior
						n.SR = a.SR;
						a.SR = n.NR;
						pos=(a.NR-1)*lr + le;
						fseek(fd,pos,0);
						fwrite(&a,lr,1,fd);
					}
					pos=(n.NR-1)*lr + le;
					fseek(fd,pos,0);
					fwrite(&n,lr,1,fd);
				}
				cout<<"desea m?s registros?"<<endl;
				cin>>rpta;
		} while(rpta=='s' || rpta=='S');
		fseek(fd,0,0);
		fwrite(&e,le,1,fd);
		fclose(fd);
}

void eliminar(){
	char rpta; int sgte,pos; bool band,flag=false;
	char nom_eliminado[20];
	if((fd=fopen("personas.txt","r+t"))==NULL){
		cout<<"no se pudo abrir el archivo"<<endl;
		return;
	}
	fread(&e,le,1,fd); //deja un espacio reservado para el encabezado		
	fflush(stdin);
	cout<<"nombre:"<<endl; cin>>nom_eliminado;
	//1.Buscar secuencialmente el registro a eliminar
	while(fread(&r,lr,1,fd)==1){
		if(strcmp(nom_eliminado,r.nom)==0){
			flag=true;
			//2. actualizar URE/ARE
			r.ARE = e.URE;
			e.URE = r.NR;
			break;
		}
	}
	if(flag==false){
		cout<<"nombre no existe!"<<endl;
		return;
	}
	//3. Actualizar la lista PR/SR
	sgte = e.PR; band=false;
	while(sgte!= -1){
		pos = (sgte-1)*lr + le;
		fseek(fd,pos,0);
		fread(&s,lr,1,fd);
		if(strcmp(r.nom,s.nom)>0){
			band=true;
			a = s;
			sgte = s.SR;
			continue;
		}
		break;
	}
			//fin de lectura de lista enlazada
	if(band==false){//caso 1:actualiza encabezado
		e.PR = r.SR;
	}
	if(band==true){//caso 2:actualiza reg anterior
		a.SR = r.SR;
		pos=(a.NR-1)*lr + le;
		fseek(fd,pos,0);
		fwrite(&a,lr,1,fd);
	}
	pos=(r.NR-1)*lr + le;
	fseek(fd,pos,0);
	fwrite(&r,lr,1,fd);

	fseek(fd,0,0);
	fwrite(&e,le,1,fd);
	fclose(fd);
}

void insertar(){
	char rpta; int sgte,pos; bool band;
	if((fd=fopen("personas.txt","r+t"))==NULL){
		cout<<"no se pudo crear el archivo"<<endl;
		return;
	}
	fread(&e,le,1,fd); 
	do{
		n.NR = ++e.NRS;
		fflush(stdin);
		cout<<"nombre:"<<endl; cin>>n.nom; n.ARE =0;
		if(e.PR == -1){//se guardar? el primer registro f?sico
			n.SR = e.PR;
			e.PR = n.NR;
			pos = (n.NR -1)*lr + le;
			fseek(fd,pos,0);
			fwrite(&n,lr,1,fd);
		}
		else{//se guardar? un registro que no es primer reg f?sico
			//Lectura lista enlazada
			sgte = e.PR; band=false;
			while(sgte!= -1){
				pos = (sgte-1)*lr + le;
				fseek(fd,pos,0);
				fread(&s,lr,1,fd);
				if(strcmp(n.nom,s.nom)>0){
					band=true;
					a = s;
					sgte = s.SR;
					continue;
				}
				break;
			}
			//fin de lectura de lista enlazada
			if(band==false){//caso 1:actualiza encabezado
				n.SR = e.PR;
				e.PR = n.NR;
			}
			if(band==true){//caso 2:actualiza reg anterior
				n.SR = a.SR;
				a.SR = n.NR;
				pos=(a.NR-1)*lr + le;
				fseek(fd,pos,0);
				fwrite(&a,lr,1,fd);
			}
			pos=(n.NR-1)*lr + le;
			fseek(fd,pos,0);
			fwrite(&n,lr,1,fd);
		}
		cout<<"desea m?s registros?"<<endl;
		cin>>rpta;
	} while(rpta=='s' || rpta=='S');
	fseek(fd,0,0);
	fwrite(&e,le,1,fd);
	fclose(fd);
}

void ver_archivo(){
		if((fd=fopen("personas.txt","rt"))==NULL){
				cout<<"no se pudo abrir el archivo"<<endl;
				return;
		}
		fread(&e,le,1,fd);
		cout<<"NRS:"<<e.NRS<<"\t"<<"PR:"<<e.PR<<"URE"<<"\t"<<e.URE<<endl;
		while(fread(&s,lr,1,fd)==1){
				cout<<s.NR<<"\t"<<s.nom<<"\t"<<s.SR<<"\t"<<s.ARE<<endl;
		}
		fclose(fd);
}

void buscarnombre(){
 	char nuevonombre[20];
 	bool encontrado = false;
 	fflush(stdin);
 	cout<<"\nIngrese nombre a buscar: "; cin>>nuevonombre;

	int sgte,pos;
	if((fd=fopen("personas.txt","rt"))==NULL){
  		cout<<"no se pudo abrir el archivo"<<endl;
		return;
	}
	fread(&e,le,1,fd);

	sgte = e.PR;
	while(sgte!= -1){
		pos = (sgte-1)*lr + le;
		fseek(fd,pos,0);
		fread(&s,lr,1,fd);

  		if(strcmp(s.nom,nuevonombre) == 0){
  			encontrado = true;
			break;
  		}
  		a = s;  
		sgte = s.SR;
	}
	if(encontrado == true){
 		cout<<nuevonombre<<" ha sido encontrado"<<endl;
	}
	else{
 		cout<<nuevonombre<<" NO encontrado"<<endl;
	}
	fclose(fd);
}

void ver_lista(){
	int sgte,pos;
	if((fd=fopen("personas.txt","rt"))==NULL){
		cout<<"no se pudo abrir el archivo"<<endl;
		return;
	}
	fread(&e,le,1,fd);
	cout<<"NRS:"<<e.NRS<<"\t"<<"PR:"<<e.PR<<"URE"<<"\t"<<e.URE<<endl;
	//Lectura lista enlazada
	sgte = e.PR; 
	while(sgte!= -1){
		pos = (sgte-1)*lr + le;
		fseek(fd,pos,0);
		fread(&s,lr,1,fd);
		cout<<s.NR<<"\t"<<s.nom<<"\t"<<s.SR<<endl;
		sgte = s.SR;
	}
	//fin de lectura de lista enlazada	
	fclose(fd);
}

int main (int argc, char *argv[]) {
	int op;
	do{
			cout<<"\tMENU"<<endl;
			cout<<"\n1. Escribir"
			<<"\n2. Ver_lista"
			<<"\n3. Buscar_nombre"
			<<"\n4. Insertar"
			<<"\n5. Eliminar"
			<<"\n6. Ver_Archivo"
			<<"\n7. Salir"<<endl;
			cin>>op;
			switch(op){
					case 1: escribir();break;
					case 2: ver_lista(); break;
					case 3: buscarnombre(); break;
					case 4: insertar(); break;
					case 5: eliminar(); break;
					case 6: ver_archivo(); break;
			}
	} while(op!= 7);
	return 0;
}