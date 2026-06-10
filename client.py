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

    print(f"\n==================== {request.get('action').upper()} ====================")
    print(f"Método: {auxiliar.METHOD_NAMES.get(request.get('method'))}")
    print(f"Método de erro: {auxiliar.ERROR_METHOD_NAMES.get(request.get('error_method'))}")

    if response.get("ok"):
        details = response.get("details", {})

        if request.get("action") == "Encode":
            print(f"Texto original: {request.get('text')}")
            print(f"Codeword: {details.get('codeword')}")
            if request.get("error_method") == "1":
                print(f"CRC: {details.get('crc')}")
            elif request.get("error_method") == "2":
                print(f"Repetition ({request.get('repeticao')}): {details.get('protected_message')}")

            print("\n==================== TRANSMISSÃO ====================")
            print(f"Mensagem protegida: {details.get('protected_message')}")
            print(f"Modo: {auxiliar.TRANSMISSION_MODE_NAMES.get(request.get('transmission_mode'))}")
            if details.get("changed_positions") is not None:
                print(f"Posições alteradas: {details.get('changed_positions')}")
            print(f"Mensagem transmitida: {response.get('result')}")
        else:
            print(f"Mensagem recebida: {request.get('text')}")
            print(f"Resultado da verificação: {details.get('verification_result')}")
            print(f"Mensagem sem controle de erro: {details.get('unprotected_message')}")
            print(f"Mensagem decodificada: {response.get('result')}")
    else:
        if request.get("action") == "Decode" and request.get("error_method") == "1":
            print("Resultado da verificação: ERRO DETECTADO")
        print(f"Erro: {response.get('error')}")

    print("\n\nReturning to main menu...")
    time.sleep(7)