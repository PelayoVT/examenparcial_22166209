import threading								#libreria para hilos
import sys										#libreria para hablar con el sistema
import socket									#libreria para comunicarse con otra consola
import pickle									#pasar a binario (serializar y desserializar)
import os										#hablar con el sistema operativo

class Cliente():

	def __init__(self, host=input("Intoduzca la IP del servidor ?  "), port=int(input("Intoduzca el PUERTO del servidor ?  ")), nick=""): #pide el host y el puerto por el que se va a conectar
		self.s = socket.socket() #creo el shocket
		while (nick ==""):
			nick = input ("Introduce tu nombre de usuario: ")
		self.nick = nick
		with open("nicknameList.txt", "a") as f:  #creo el archivo donde se almacenan los usuarios
			f.write(self.nick + "\n")
		self.s.connect((host, int(port)))  #creamos la conexión
            
		print('\n\tProceso con PID = ',os.getpid(), '\n\tHilo PRINCIPAL con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\tTotal Hilos activos en este punto del programa =', threading.active_count()) 
		threading.Thread(target=self.recibir, daemon=True).start()  #instanciamos el hilo
		

		while True:   #función para salir del programa 
			msg = input('\nEscriba texto ?   ** Enviar = ENTER   ** Salir Chat = 1 \n')
			if msg != '1' : self.enviar(msg)
			else:
				print(" **** Me piro vampiro; cierro socket y mato al CLIENTE con PID = ", os.getpid())
				self.deleteNick(nick)
				self.s.close()      #cierro el shocket
				sys.exit()          #salgo del programa
                
	def deleteNick(self, nick):
		lines = []
		with open("nicknameList.txt", "r") as f:    #abrimos en modo lectura el txt
			nicknames = f.readlines()
			for n in nicknames:
				if (nick not in n):
					lines.append(n)
		with open ("nicknameList.txt", "w") as f:   #abrimos en modo escritura el txt para sobreescribir los datos 
			for n in lines:
				f.write(n)

	def recibir(self):
		print('\nHilo RECIBIR con ID =',threading.currentThread().getName(), '\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count()) #imprime quien maneja los hilos
		while True:
			try:
				data = self.s.recv(128)   #guardo la iformación del chat en binario
				if data: print(pickle.loads(data))  #desserializo de binario a texto plano
			except: pass

	def enviar(self, msg):
		self.s.send(pickle.dumps(self.nick + ": " + msg))
        
		with open ("u22166209AI.txt", "a") as f:
			f.write(self.nick + " : " + msg + "\n")   #creación del archivo donde se guarda el historial

arrancar = Cliente()

		