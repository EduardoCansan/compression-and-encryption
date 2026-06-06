# ========================
# === Configuração TCP ===
# ========================

import auxiliar
import socket
import json
import time

host = '127.0.0.1'  # IP do servidor
port = 12345  # Porta do servidor

# Conectando ao servidor 
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((host, port))

print("\nConectado ao servidor!")

# Recebe a mensagem do servidor antes do looping
mensagem = cliente.recv(1024).decode()
print(mensagem)

while True:
    # Comando para o cliente escolher entre Encode ou Decode e o método de codificação/decodificação
    auxiliar.show_main_menu()
    option = input("\nEnter the option: ").strip()

    if option == "1":
        request = auxiliar.handle_action("Encode")
    elif option == "2":
        request = auxiliar.handle_action("Decode")
    elif option == "0":
        print("\nEncerrando conexao...")
        cliente.send('0'.encode())
        cliente.close()
        break
    else:
        auxiliar.console.print("\n[bold red]Invalid option![/bold red]")
        continue

    if request is None:
        continue

    cliente.send(json.dumps(request).encode())
    response = json.loads(cliente.recv(4096).decode())

    if response.get("ok"):
        auxiliar.console.print(f"\n[default](Server) Result: {response.get('result')}[/default]")
    else:
        auxiliar.console.print(f"\n[yellow](Server) Error: {response.get('error')}[/yellow]")

    print("\n\nReturning to main menu...")
    time.sleep(7)