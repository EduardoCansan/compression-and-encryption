# ========================
# === Configuração TCP ===
# ========================

import socket
import auxiliar

host = '127.0.0.1'  # IP do servidor
port = 12345  # Porta do servidor

# Conectando ao servidor 
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((host, port))

print("Conectado ao servidor!")

# Recebe a mensagem do servidor antes do looping
mensagem = cliente.recv(1024).decode()
print(mensagem)

while True:
    # Comando para o cliente escolher entre Encode ou Decode e o método de codificação/decodificação
    auxiliar.show_main_menu()
    option = input("Enter the option: ").strip()

    if option == "1":
        auxiliar.handle_action("Encode")
    elif option == "2":
        auxiliar.handle_action("Decode")
    else:
        auxiliar.console.print("\n[bold red]Invalid option![/bold red]")

    mensagem = input("Digite uma mensagem: ")
    cliente.send(mensagem.encode())

    if(mensagem == '0'):
        print("Conexão Encerrada")
        cliente.close()
        break