import socket

# Configuração do TCP do servidor 
host = '127.0.0.1'  # Endereço IP do servidor (localhost)
port = 12345  # Porta para o servidor

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((host, port))
servidor.listen(1)

print("Aguardando conexao...")

# Aceitando a conexão cliente
cliente, addr = servidor.accept()
print(f"Cliente Conectado: {addr}")

while True:
    mensagem = input("Digite uma mensagem: ")
    cliente.send(mensagem.encode())

    mensagem = cliente.recv(1024).decode()

    if(mensagem == '0'):
        # Fechar conexões
        print("Cliente encerrou conexao!")
        cliente.close()
        servidor.close()
        break
    print(mensagem)