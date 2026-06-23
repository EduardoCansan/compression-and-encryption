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
    # comando para o cliente escolher entre Encode ou Decode
    # exibe o menu principal e lê a opção escolhida pelo usuário.
    auxiliar.show_main_menu()
    option = input("\nEnter the option: ").strip()

    # faz uma requisição de codificação quando o usuário escolhe Encode.
    if option == "1":
        request = auxiliar.handle_action("Encode")
    # faz uma requisição de decodificação quando o usuário escolhe Decode.
    elif option == "2":
        request = auxiliar.handle_action("Decode")
    #informa o servidor sobre a saída, fecha o socket e encerra o loop.
    elif option == "0":
        print("\nClosing connection...")
        cliente.send('0'.encode())
        cliente.close()
        break
    # rejeita opções que não existem e volta ao início do menu.
    else:
        auxiliar.console.print("\n[bold red]Invalid option![/bold red]")
        continue

    # se algum dado informado no menu for inválido, nenhuma requisição é enviada.
    if request is None:
        continue

    # converte o dicionário da requisição para JSON, transforma em bytes e envia ao servidor.
    cliente.send(json.dumps(request).encode())
    # recebe a resposta, converte os bytes para texto JSON e depois para dicionário Python.
    response = json.loads(cliente.recv(4096).decode())

    # mostra um resumo dos métodos escolhidos para a operação atual.
    print(f"\n==================== {request.get('action').upper()} ====================")
    print(f"Method: {auxiliar.METHOD_NAMES.get(request.get('method'))}")
    print(f"Error method: {auxiliar.ERROR_METHOD_NAMES.get(request.get('error_method'))}")

    # uma resposta com ok=True contém o resultado e detalhes das etapas realizadas.
    if response.get("ok"):
        details = response.get("details", {})

        # no Encode, mostra a compressão, a proteção e a transmissão simulada.
        if request.get("action") == "Encode":
            print(f"Original text: {request.get('text')}")
            print(f"Codeword: {details.get('codeword')}")
            # CRC acrescenta bits usados posteriormente para detectar erros.
            if request.get("error_method") == "1":
                print(f"CRC: {details.get('crc')}")
            # repetition protege a mensagem repetindo seus bits.
            elif request.get("error_method") == "2":
                print(f"Repetition ({request.get('repeticao')}): {details.get('protected_message')}")

            # mostra como a mensagem protegida ficou após a simulação da transmissão.
            print("\n==================== TRANSMISSION ====================")
            print(f"Protected message: {details.get('protected_message')}")
            if request.get("error_method") == "3":
                print("Mode: Automatic")
            else:
                print(f"Mode: {auxiliar.TRANSMISSION_MODE_NAMES.get(request.get('transmission_mode'))}")
            
            # posições alteradas só existem quando a simulação introduz erros.
            if details.get("changed_positions") is not None:
                print(f"Changed positions: {details.get('changed_positions')}")
            print(f"Transmitted message: {response.get('result')}")
        
        # no Decode, mostra a verificação do erro e o conteúdo recuperado.
        else:
            print(f"Received message: {request.get('text')}")
            print(f"Verification result: {details.get('verification_result')}")
            print(f"Message without error control: {details.get('unprotected_message')}")
            print(f"Decoded message: {response.get('result')}")
    
    # uma resposta com ok=False informa que o servidor não conseguiu concluir a operação.
    else:
        # quando o CRC falha durante Decode, destaca que um erro foi detectado.
        if request.get("action") == "Decode" and request.get("error_method") == "1":
            print("Verification result: ERROR DETECTED")
        print(f"Error: {response.get('error')}")

    # aguarda alguns segundos antes de exibir novamente o menu principal.
    print("\n\nReturning to main menu...")
    time.sleep(7)
