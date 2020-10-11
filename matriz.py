#-------Librerias----------
import numpy as np
import pandas as pd 
import sys
#-----Extraccion de datos------
nombre=sys.argv[1]
data = pd.read_excel (nombre) 
#-----Extraccion de datos------

#extraemos los datos del excel x , y , sector , i, velocidad
x = pd.DataFrame(data, columns= ['x']) #posicion x
y = pd.DataFrame(data, columns= ['y']) #posicion y
sector = pd.DataFrame(data, columns= ['Sector*'])  #sector
i = pd.DataFrame(data, columns= ['i'])  #posicion i
v = pd.DataFrame(data, columns= ['Velocidad'])  #velocidad
# extraemos la cantidad de elementos 
elementos = len(x)
#volvemos matrices los datos
x = np.array( x.values)
y = np.array( y.values)
v = np.array( v.values)
i = np.array( i.values)
sector = np.array( sector.values)

#--------Arreglos------------

#arreglamos las matrices de los sectores y la cantidad de datos(i)y las transformamos en tuplas para generar los ejes del excel
i=i.T
sector=sector.T
i_list = i.tolist()
sector_list= sector.tolist()
lateral=list(zip(sector_list[0],i_list[0]))
#generamos los index y columnas
index = pd.MultiIndex.from_tuples(lateral, names=['(Xi,Yi)', 'i/j'])
columns = pd.MultiIndex.from_tuples(lateral, names=['(Xj,Yj)', 'i/j'])

#-------------Matrices------
#generamos una matriz unitaria del tamaño de los elementos
matriz_d=np.ones((elementos, elementos))


#hacemos un barrido en lso ejes I y J , e caso sean igual el valor a colocar es 1
for i in range(elementos):
	for j in range(elementos):
		if i == j:
			matriz_d[i][j]=1
		else:
			d=abs(x[i]-x[j])+abs(y[i]-y[j])
			matriz_d[i][j]=d


#generamos una matriz unitaria del tamaño de los elementos
matriz_t=np.ones((elementos, elementos))

#hacemos un barrido en lso ejes I y J dividiendo los valores con la matriz V

for i in range(elementos):
	for j in range(elementos):
		matriz_t[i][j]=matriz_d[i][j]/v[j]
matriz_t=matriz_t*60
 
#-----------------
#generamos nuevas listas para almacenar datos 
a=[]
b=[]
c=[]
d=[]
for i in range(elementos):
	for j in range(elementos):
		a.append(sector[0][i])
		b.append(sector[0][j])
		c.append(matriz_t[i][j])
		d.append(matriz_d[i][j])
data = {'i':a, 'j':b,"Val_T":c,"Val_D":d}
#las agregamos en diccionarios y las mostramos
# ------------------------------
excel1 = pd.DataFrame (matriz_d,index=index, columns=columns)
excel2 = pd.DataFrame (matriz_t,index=index, columns=columns)
excel3 = pd.DataFrame (data)

nombre = ".".join(nombre.split(".")[:-1])
filepath1 = nombre + '_distancias.xlsx'
filepath2 = nombre +'_tiempos.xlsx'
filepath3 = nombre +'_valores.xlsx'
excel1.to_excel(filepath1)
excel2.to_excel(filepath2)
excel3.to_excel(filepath3)

