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

print("\nConnected to server!")

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
        print("\nClosing connection...")
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
    print(f"Method: {auxiliar.METHOD_NAMES.get(request.get('method'))}")
    print(f"Error method: {auxiliar.ERROR_METHOD_NAMES.get(request.get('error_method'))}")

    if response.get("ok"):
        details = response.get("details", {})

        if request.get("action") == "Encode":
            print(f"Original text: {request.get('text')}")
            print(f"Codeword: {details.get('codeword')}")
            if request.get("error_method") == "1":
                print(f"CRC: {details.get('crc')}")
            elif request.get("error_method") == "2":
                print(f"Repetition ({request.get('repeticao')}): {details.get('protected_message')}")

            print("\n==================== TRANSMISSION ====================")
            print(f"Protected message: {details.get('protected_message')}")
            print(f"Mode: {auxiliar.TRANSMISSION_MODE_NAMES.get(request.get('transmission_mode'))}")
            if details.get("changed_positions") is not None:
                print(f"Changed positions: {details.get('changed_positions')}")
            print(f"Transmitted message: {response.get('result')}")
        else:
            print(f"Received message: {request.get('text')}")
            print(f"Verification result: {details.get('verification_result')}")
            print(f"Message without error control: {details.get('unprotected_message')}")
            print(f"Decoded message: {response.get('result')}")
    else:
        if request.get("action") == "Decode" and request.get("error_method") == "1":
            print("Verification result: ERROR DETECTED")
        print(f"Error: {response.get('error')}")

    print("\n\nReturning to main menu...")
    time.sleep(7)
