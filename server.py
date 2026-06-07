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

        print(f"\n(Client) Action: {payload.get('action')}")
        print(f"(Client) Method: {auxiliar.METHOD_NAMES.get(method, method)}")
        if payload.get("k") is not None:
            print(f"(Client) k: {payload.get('k')}")
        print(f"(Client) Text: {payload.get('text', '')}")

        result = auxiliar.process_request(
            payload.get("action"),
            method,
            payload.get("text", ""),
            payload.get("k"),
        )
        # Server não mostra a resposta ainda
        # print(f"\n(Server) Result: {result}")
        response = {"ok": True, "result": result}
    except (json.JSONDecodeError, ValueError) as e:
        print(f"\n(Server) Erro: {e}")
        response = {"ok": False, "error": str(e)}

    cliente.send(json.dumps(response).encode())
