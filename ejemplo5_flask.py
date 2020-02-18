from flask import Flask, jsonify, request, render_template
from manejador_db import manejador_db

import math
import random
import time
import numpy
import serial

app = Flask(__name__)
man=manejador_db()


@app.route("/")
def home():
	return render_template("index.html")

@app.route("/historico")
def historico():
	return render_template("historico.html")

@app.route("/indexchart")
def inicio():
	return render_template("indexchart.html")

@app.route("/aleatorio")
def aleatorio():
	
	port = "COM10"
	ser = serial.Serial(port,9600)
	RR = ser.readline().decode()
	RR = RR.replace("\r\n","")
	print(RR)

	HR = ser.readline().decode()
	HR = HR.replace("\r\n","")
	print(HR)
	#HR=ser.read(ser.inWaiting()).split()
	#print "tipo de dato:",type(HR)
	#if HR >= "201":
	#	HR=1
	#print HR
	#HR = HR[0]
	#HR=random.randint(1,200)
	#RR=random.randint(1,1000)
	sesion=1
	estampa=time.time()*1000
	#if ser.isOpen():
	#	print "open:", ser.portstr
	#	print "traigo algo:",HR
	
	ser.close()
	man.agregar_num(estampa, HR, RR, sesion)
	
	#print "Serial:",respuesta
	#print "HR",HR, "RR",RR, "sesion", sesion
	return "{\"HR\":"+str(HR)+",\"RR\":" +str(RR)+",\"sesion\":" +str(sesion)+"}"
	


@app.route("/consultar")
def consultar():
	return man.consultarTodo()

@app.route("/buscar")
def buscar():
	sesion=int(request.args['sesion'])
	print "Pasamos"+str(sesion)
	return man.consultarNumero(sesion)
	
@app.route("/promHR")
def promedioHR():
	sesion=int(request.args['sesion'])
	print "Pasamos"+str(sesion)
	return man.consultarHR(sesion)

@app.route("/max")
def max():
	sesion=int(request.args['sesion'])
	print "Pasamos"+str(sesion)
	return man.max(sesion)
	
@app.route("/min")
def min():
	sesion=int(request.args['sesion'])
	print "Pasamos"+str(sesion)
	return man.min(sesion)
	
@app.route("/pRR50")
def pRR50():
	sesion=int(request.args['sesion'])
	print "Pasamos"+str(sesion)
	return man.pRR50(sesion)

@app.route("/SDRR")
def SDRR():
	sesion=int(request.args['sesion'])
	print "Pasamos"+str(sesion)
	return man.SDRR(sesion)
	
@app.route("/centHR")
def centHR():
	sesion=int(request.args['sesion'])
	print "Pasamos"+str(sesion)
	return man.centHR(sesion)

@app.route("/centRR")
def centRR():
	sesion=int(request.args['sesion'])
	print "Pasamos"+str(sesion)
	return man.centRR(sesion)

if __name__ == "__main__":
	app.run("0.0.0.0")



