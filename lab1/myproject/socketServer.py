import socket #подключаем сокет
import os

host = "localhost" #адрес
port = 8000 #порт
buffer_size = 1024 #размер буффера
current_directory = os.getcwd()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #создаем сокет
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((host, port)) #связываем сокет с хостом и портом
sock.listen(1) #запускаем режим прослушивания. Аргумент - максимальное количество подключений в очереди (1)

#Общаемся с клиентом:
while True:
	conn, addr = sock.accept()  # принимаем подключение
	request = conn.recv(buffer_size) # получить данные

	try:
		address = str(request).split(' ')[1]#получить адресс страницы из запроса
	except:
		address = ""

	if (os.path.exists(current_directory+address)):  #если запрошенный ресурс существует, отправить его
		if address == "/":
			address="/index.html"
		file = open(current_directory+address, mode='rb')
		conn.send(b"HTTP/1.1 200 OK\n" + file.read()+b"\n")
		file.close()
	else:
		conn.send(b"HTTP/1.1 404 Not Found\n") #сообщить, что запрошенной страницы нет
	conn.close()
sock.close()