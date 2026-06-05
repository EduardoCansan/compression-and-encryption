import socket

host = '127.0.0.1'  # IP do servidor
port = 12345  # Porta do servidor

#Conectando ao servidor 
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((host, port))

print("Conectado ao servidor!")

while True:
    mensagem = cliente.recv(1024).decode()
    print(mensagem)

    mensagem = input("Digite uma mensagem: ")
    cliente.send(mensagem.encode())

    if(mensagem == '0'):
        print("Conexão Encerrada")
        cliente.close()
        break