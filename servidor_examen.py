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

	def procesarC(self):  # La función procesar se encarga de manejar los mensajes enviados
		print("Procesamiento de mensajes iniciado")
		print("La dirección ip del servidor es: " +
			socket.gethostbyname(socket.gethostname()))
		while True:  # Mientras que el programa este activo
			if len(self.clientes) > 0:  # Si hay al menos un cliente
				for c in self.clientes:  # Recorre la lista de clientes
					try:  # Intenta recibir un mensaje
						# Guarda el mensaje en la variable data
						data = c.recv(64)
						if data:  # Si hay data
							self.listaNicks()  # Imprime la lista de nicknames conectados
							matriz = pickle.loads(data) #Añado todo lo de matrices
							print(matriz) # Imprime el mensaje
							matrizFinal = matriz.split(',')
							print(matrizFinal)
							self.multiplicacionMatrices(matrizFinal[0], matrizFinal[1], matrizFinal[2], matrizFinal[3])
							# multiplicacionMatrices()
							# Manda el mensaje al resto de clientes, si hay
							self.broadcast(data, c)
					except:  # Sino recibe un mensaje pasa
						pass
            
	def historial(self, n):  # La función historial se encarga de guardar el historial de mensajes de cada sesión en un txt
                                # Manejamos un documento externo para que guarde el nick con el mensaje
		with open("ue22166209AI1.txt", 'a') as f:
			f.write("Historial " + str(n) + ":\n") 
            
        # La función listaNicks se encarga de imprimir el listado actual de nicks conectados
	def listaNicks(self):
		print("Lista de Nicknames:")
		with open("u22166209nicknames.txt", 'r') as f:
			print(f.read())
            



arrancar = Servidor() 