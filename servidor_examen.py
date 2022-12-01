import socket									#libreria para comunicarse con otra consola
import threading								#libreria para hilos
import sys										#libreria para hablar con el sistema
import pickle									#pasar a binario (serializar y desserializar)
import os										#hablar con el sistema operativo

class Servidor():

	def __init__(self, host=socket.gethostname(), port=int(input("Que puerto quiere usar ? "))): #pide el host y el puerto en el que se alojará el servidor
		self.clientes = []  #se crea el array que almacenará los clientes
		print('\nSu IP actual es : ',socket.gethostbyname(host)) #imprimo la ip
		print('\n\tProceso con PID = ',os.getpid(), '\n\tHilo PRINCIPAL con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(), '\n\tTotal Hilos activos en este punto del programa =', threading.active_count()) #saber que hilo está trabajando en cada momento.
		self.s = socket.socket()   #creacion del socket
		self.s.bind((str(host), int(port)))    #conecto
		self.s.listen(30) #servidor a la escucha 
		self.s.setblocking(False) #evita el bloqueo

		threading.Thread(target=self.aceptarC, daemon=True).start()
		threading.Thread(target=self.procesarC, daemon=True).start()

		while True: #función que cierra el servidor al intruducir "1"
			msg = input('\n << SALIR = 1 >> \n')
			if msg == '1':
				print(" **** Me piro vampiro; cierro socket y mato SERVER con PID = ", os.getpid())
				with open("nicknameList.txt", "w") as f:
					f.write(" ")
				self.s.close()
				sys.exit()
			else: pass

	def aceptarC(self):  #función para entrar al chat
		print('\nHilo ACEPTAR con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count())
		
		while True:
			try:
				conn, addr = self.s.accept()
				print(f"\nConexion aceptada via {addr}\n")
				conn.setblocking(False)      #hacemos que no se bloquee 
				self.clientes.append(conn)   #añadimos al array cliente
				self.readNick
			except: pass
        
	def readNick(self):
		with open("nicknameList.txt", "r") as f:
			print("Clientes conectados actualmente \n--------------------------" + f.read() + "--------------------------")   #leemos el archivo de los nombre para mostrar los usuarios actuales

	def procesarC(self):
		print('\nHilo PROCESAR con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count())
		while True:
			if len(self.clientes) > 0:
				for c in self.clientes:
					try:
						data = c.recv(128)        #recibimos y guardamos c
						if data: self.broadcast(data,c)  #cuando data es verdadero se abre el broadcast
					except: pass

	def broadcast(self, msg, cliente):
		auxiliar = 0
		for c in self.clientes:
			try:
				if c != cliente:
					if auxiliar == 0:
						print("Clientes conectados actualmente = ", len(self.clientes))
						self.readNick()
						print(pickle.loads(msg))
						auxiliar = 1
					c.send(msg)
			except: self.clientes.remove(c)

arrancar = Servidor() 