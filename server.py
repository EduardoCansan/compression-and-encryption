import auxiliar
import socket
import json
from error_control.error import error_simulator

# Configuração do TCP do servidor 
host = '127.0.0.1'  # Endereço IP do servidor (localhost)
port = 12345  # Porta para o servidor

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((host, port))
servidor.listen(1)

print("\nWaiting for connection...")

# Aceitando a conexão cliente
cliente, addr = servidor.accept()
print(f"\nClient connected: {addr}")

# Enviando mensagem de boas-vindas para o cliente
cliente.send("\nStarting encoding and decoding!".encode())

while True:
    mensagem = cliente.recv(1024).decode()

    if(mensagem == '0'):
        # Fechar conexões
        print("\nClient closed the connection!")
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
            print(f"(Client) Repetition: {payload.get('repeticao')}")
        if payload.get("transmission_mode") is not None:
            print(f"(Client) Transmission Mode: {auxiliar.TRANSMISSION_MODE_NAMES.get(payload.get('transmission_mode'))}")
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
                details["verification_result"] = "VALID CRC"
            elif error_method == "2":
                details["verification_result"] = "Repetition decoding applied"

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

            details["protected_message"] = result
            transmission_mode = payload.get("transmission_mode", "1")
            simulator = error_simulator()

            if transmission_mode == "2":
                simulation = simulator.inverter_bit(result, payload.get("error_position"))
                if isinstance(simulation, str):
                    raise ValueError(simulation)
                result, position = simulation
                details["changed_positions"] = [position]
            elif transmission_mode == "3":
                simulation = simulator.inserir_erros_aleatorios(result, payload.get("error_quantity"))
                if isinstance(simulation, str):
                    raise ValueError(simulation)
                result, positions = simulation
                details["changed_positions"] = positions
        # Server não mostra a resposta ainda
        # print(f"\n(Server) Result: {result}")
        response = {"ok": True, "result": result, "details": details}
    except (json.JSONDecodeError, ValueError) as e:
        print(f"\n(Server) Error: {e}")
        response = {"ok": False, "error": str(e)}

    cliente.send(json.dumps(response).encode())
