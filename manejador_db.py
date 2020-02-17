from tinydb import TinyDB, where
from itertools import tee, islice, chain, izip
from math import sqrt
from sklearn.cluster import KMeans

import matplotlib.pyplot as plt
import numpy as np

class manejador_db: 

	def agregar_num(self, estampa, HR, RR, sesion):
		db=TinyDB("sesiones.json")
		lista=db.search(where("estampa")==estampa)
		if(len(lista)==0):
			
			db.insert({"estampa":estampa, "HR":HR, "RR":RR, "sesion":sesion})
			
	def consultarTodo(self):
		db=TinyDB("sesiones.json")
		lista=db.all()
		cad="<table border='2' title='Todo'>"
		for elem in lista:
			cad=cad+"<tr><td colspan='4' align='center' bgcolor='666666'><font color='#FFFFFF'><strong>Todas la sesiones</strong></font></td></tr>"
			cad=cad+"<tr><td>Sesion</td><td>"+str(elem["sesion"])+"</td></tr>"
			cad=cad+"<tr><td>HR</td><td>"+str(elem["HR"])+"</td></tr>"
			cad=cad+"<tr><td>RR</td><td>"+str(elem["RR"])+"</td></tr>"
		cad=cad+"</table>"
		return cad
			
	def consultarNumero(self, sesion):
		db=TinyDB("sesiones.json")
		lista=db.search(where("sesion")==sesion)
		cad="<table border='2' title='Datos por Sesion'>"
		for elem in lista:
			cad=cad+"<tr><td colspan='4' align='center' bgcolor='666666'><font color='#FFFFFF'><strong>Datos por sesion</strong></font></td></tr>"
			cad=cad+"<tr><td>Sesion</td><td>"+str(elem["sesion"])+"</td></tr>"
			cad=cad+"<tr><td>HR</td><td>"+str(elem["HR"])+"</td></tr>"
			cad=cad+"<tr><td>RR</td><td>"+str(elem["RR"])+"</td></tr>"
		cad=cad+"</table>"
		return cad
		
	def consultarHR(self, sesion):
		db=TinyDB("sesiones.json")
		lista=db.search(where("sesion")==sesion)
		resultHR=0
		resultRR=0
		for elem in lista:
			resultHR=resultHR + int(elem["HR"])
			resultRR=resultRR + int(elem["RR"])
		resultHR=resultHR/len(lista)
		resultRR=resultRR/len(lista)
		cad="<table border='2' title='Promedio HR y RR'>"
		cad=cad+"<tr><td colspan='4' align='center' bgcolor='666666'><font color='#FFFFFF'><strong>Promedio HR y RR</strong></font></td></tr>"
		cad=cad+"<tr><td>Sesion</td><td>"+str(elem["sesion"])+"</td></tr>"
		cad=cad+"<tr><td>Promedio HR</td><td>"+str(resultHR)+"</td></tr>"
		cad=cad+"<tr><td>Promedio RR</td><td>"+str(resultRR)+"</td></tr>"
		cad=cad+"</table>"
		return cad
		
	def max(self, sesion):
		db=TinyDB("sesiones.json")
		lista=db.search(where("sesion")==sesion)
		maxHR=0
		maxRR=0
		for elem in lista:
			if(int(elem["HR"]) > maxHR):
				maxHR=int(elem["HR"])
			if(int(elem["RR"]) > maxRR):
				maxRR=int(elem["RR"])
		cad="<table border='2' Valores Maximos>"
		cad=cad+"<tr><td colspan='4' align='center' bgcolor='666666'><font color='#FFFFFF'><strong>Valores Maximos HR y RR</strong></font></td></tr>"
		cad=cad+"<tr><td>Sesion</td><td>"+str(elem["sesion"])+"</td></tr>"
		cad=cad+"<tr><td>Maximo HR</td><td>"+str(maxHR)+"</td></tr>"
		cad=cad+"<tr><td>Maximo RR</td><td>"+str(maxRR)+"</td></tr>"
		cad=cad+"</table>"
		return cad
	
	def min(self, sesion):
		db=TinyDB("sesiones.json")
		lista=db.search(where("sesion")==sesion)
		minHR=200
		minRR=1000
		for elem in lista:
			if(int(elem["HR"]) < minHR):
				minHR=int(elem["HR"])
			if(int(elem["RR"]) < minRR):
				minRR=int(elem["RR"])
		cad="<table border='2' title='Valores Minimos'>"
		cad=cad+"<tr><td colspan='4' align='center' bgcolor='666666'><font color='#FFFFFF'><strong>Valores Minimos HR y RR</strong></font></td></tr>"
		cad=cad+"<tr><td>Sesion</td><td>"+str(elem["sesion"])+"</td></tr>"
		cad=cad+"<tr><td>Minimo HR</td><td>"+str(minHR)+"</td></tr>"
		cad=cad+"<tr><td>Minimo RR</td><td>"+str(minRR)+"</td></tr>"
		cad=cad+"</table>"
		return cad
	
	def pRR50(self, sesion):
		db=TinyDB("sesiones.json")
		lista=db.search(where("sesion")==sesion)
		cont=0
		pRR50=0.0
		nextelem=0
		texto=""
		for elem in lista:
			if(abs(int(elem["RR"]) - nextelem) > 50 ):
				cont=cont+1	
			nextelem=int(elem["RR"])
		cont=cont-1
		pRR50 =float(cont) / float(len(lista))*100
		
		if(pRR50 > 3):
			texto="ALTO"
		else:
			texto="BAJO"
			
		cad="<table border='2' title='pRR50'>"
		cad=cad+"<tr><td colspan='4' align='center' bgcolor='666666'><font color='#FFFFFF'><strong>Porcentaje de intervalos RR > 50ms </strong></font></td></tr>"
		cad=cad+"<tr><td>Sesion</td><td>"+str(elem["sesion"])+"</td></tr>"
		cad=cad+"<tr><td>pRR50</td><td>"+str(pRR50)+"</td></tr>"
		cad=cad+"<tr><td>Nivel de Riesgo</td><td>"+texto+"</td></tr>"
		cad=cad+"</table>"
		return cad
	
	
	def SDRR(self, sesion):
		db=TinyDB("sesiones.json")
		lista=db.search(where("sesion")==sesion)
		cont=0
		SDRR=0.0
		nextelem=0
		texto=""
		listaIRR=[]
		for elem in lista:
			if(abs(int(elem["RR"]) - nextelem) > 50 ):
				listaIRR.append(abs(int(elem["RR"]) - nextelem))
				cont=cont+1	
			nextelem=int(elem["RR"])

		listaIRR.pop(0)
		np.asarray(listaIRR)
		SDRR= np.std(listaIRR)
		
		
		if(SDRR < 50):
			texto="ALTO"
		if(SDRR > 50 and SDRR < 100):
			texto="MODERADO"
		if(SDRR > 100):
			texto="BAJO"
			
		cad="<table border='2' title='SDRR'>"
		cad=cad+"<tr><td colspan='4' align='center' bgcolor='666666'><font color='#FFFFFF'><strong>Desviacion Estandar de intervarlos RR</strong></font></td></tr>"
		cad=cad+"<tr><td>Sesion</td><td>"+str(elem["sesion"])+"</td></tr>"
		cad=cad+"<tr><td>SDRR</td><td>"+str(SDRR)+"</td></tr>"
		cad=cad+"<tr><td>Nivel de Riesgo</td><td>"+texto+"</td></tr>"
		cad=cad+"</table>"
		return cad
		
	def centHR (self, sesion):
		db=TinyDB("sesiones.json")
		lista=db.search(where("sesion")==sesion)
		listaCentHR=[]
		n=0
		for elem in lista:
			listaCentHR.append([n,int(elem["HR"])])
			n=n+1
		
		np.asarray(listaCentHR)
		kmeans = KMeans(n_clusters=2)
		kmeans.fit(listaCentHR)
		centroides=kmeans.cluster_centers_
		cad="<table border='2' title='Centroides HR'>"
		for elem in centroides:
			cad=cad+"<tr><td colspan='4' align='center' bgcolor='666666'><font color='#FFFFFF'><strong>Centroides HR</strong></font></td></tr>"
			cad=cad+"<tr><td>X</td><td>"+str(elem[0])+"</td></tr>"
			cad=cad+"<tr><td>Y</td><td>"+str(elem[1])+"</td></tr>"
		cad=cad+"</table>"
		return cad
		
	def centRR (self, sesion):
		db=TinyDB("sesiones.json")
		lista=db.search(where("sesion")==sesion)
		listaCentRR=[]
		n=0
		for elem in lista:
			listaCentRR.append([n,int(elem["RR"])])
			n=n+1
		
		np.asarray(listaCentRR)
		kmeans = KMeans(n_clusters=2)
		kmeans.fit(listaCentRR)
		centroides=kmeans.cluster_centers_
		cad="<table border='2' title='Centroides RR'>"
		for elem in centroides:
			#print "X",elem[0]
			#cad=cad+"<tr><td>Sesion</td><td>"+str(elem["sesion"])+"</td></tr>"
			cad=cad+"<tr><td colspan='4' align='center' bgcolor='666666'><font color='#FFFFFF'><strong>Centroides RR</strong></font></td></tr>"
			cad=cad+"<tr><td>X</td><td>"+str(elem[0])+"</td></tr>"
			cad=cad+"<tr><td>Y</td><td>"+str(elem[1])+"</td></tr>"
		cad=cad+"</table>"
		return cad
