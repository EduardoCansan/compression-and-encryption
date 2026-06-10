import auxiliar
import socket
import json

# Configuração do TCP do servidor 
host = '127.0.0.1'  # Endereço IP do servidor (localhost)
port = 12345  # Porta para o servidor

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((host, port))
servidor.listen(1)

print("\nAguardando conexao...")

# Aceitando a conexão cliente
cliente, addr = servidor.accept()
print(f"\nCliente Conectado: {addr}")

# Enviando mensagem de boas-vindas para o cliente
cliente.send("\nIniciando codificacao e decodificacao!".encode())

while True:
    mensagem = cliente.recv(1024).decode()

    if(mensagem == '0'):
        # Fechar conexões
        print("\nCliente encerrou conexao!")
        cliente.close()
        servidor.close()
        break
    
    try:
        payload = json.loads(mensagem)
        method = payload.get("method")
        error_method = payload.get("error_method")

        print(f"\n(Client) Action: {payload.get('action')}")
        print(f"(Client) Method: {auxiliar.METHOD_NAMES.get(method, method)}")
        if error_method is not None:
            print(f"(Client) Error Method: {auxiliar.ERROR_METHOD_NAMES.get(error_method, error_method)}")
        if payload.get("k") is not None:
            print(f"(Client) k: {payload.get('k')}")
        if payload.get("repeticao") is not None:
            print(f"(Client) Repeticao: {payload.get('repeticao')}")
        print(f"(Client) Text: {payload.get('text', '')}")

        action = payload.get("action")
        text = payload.get("text", "")
        details = {}

        if action == "Decode":
            text = auxiliar.process_error_control(
                action,
                error_method,
                text,
                payload.get("repeticao"),
            )
            details["unprotected_message"] = text
            if error_method == "1":
                details["verification_result"] = "CRC VALIDO"
            elif error_method == "2":
                details["verification_result"] = "Repetition Decode aplicado"

        result = auxiliar.process_request(action, method, text, payload.get("k"))

        if action == "Encode":
            details["codeword"] = result
            codeword = result
            result = auxiliar.process_error_control(
                action,
                error_method,
                result,
                payload.get("repeticao"),
            )
            if error_method == "1":
                details["crc"] = result[len(codeword):]
        # Server não mostra a resposta ainda
        # print(f"\n(Server) Result: {result}")
        response = {"ok": True, "result": result, "details": details}
    except (json.JSONDecodeError, ValueError) as e:
        print(f"\n(Server) Erro: {e}")
        response = {"ok": False, "error": str(e)}

    cliente.send(json.dumps(response).encode())
