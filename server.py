import auxiliar
import socket
import json
from error_control.error import error_simulator

# Configuração do TCP do servidor 
# Define o endereço e a porta nos quais o servidor aguardará conexões.
host = '127.0.0.1'  # Endereço IP do servidor (localhost)
port = 12345  # Porta para o servidor

# Cria um socket TCP usando IPv4.
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Associa o socket ao endereço local e à porta escolhida.
servidor.bind((host, port))
# Coloca o socket em modo de escuta, aceitando uma conexão pendente.
servidor.listen(1)

print("\nWaiting for connection...")

# Aceitando a conexão cliente
# accept bloqueia a execução até um cliente se conectar.
# O retorno contém o socket do cliente e seu endereço de rede.
cliente, addr = servidor.accept()
print(f"\nClient connected: {addr}")

# Enviando mensagem de boas-vindas para o cliente
# Converte a mensagem inicial para bytes e a envia ao cliente conectado.
cliente.send("\nStarting encoding and decoding!".encode())

# Fluxo geral:
# Cliente -> Servidor -> Compressão -> Controle de erro -> Simulação de erro -> Resposta
# Mantém o servidor recebendo operações enquanto o cliente estiver conectado.
while True:
# Recebe bytes enviados pelo cliente e os converte para texto.
    mensagem = cliente.recv(1024).decode()

# O valor "0" é o comando usado pelo cliente para encerrar a sessão.
    if(mensagem == '0'):
        # Fechar conexões
        print("\nClient closed the connection!")
        cliente.close()
        servidor.close()
        break
    
# Protege o servidor contra JSON inválido e erros esperados no processamento.
    try:
# Converte o texto JSON recebido em um dicionário Python.
        payload = json.loads(mensagem)
# Obtém os identificadores dos métodos escolhidos pelo cliente.
        method = payload.get("method")
        error_method = payload.get("error_method")

# Registra no terminal os dados recebidos para acompanhar a requisição.
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

# Separa os campos principais usados nas próximas etapas.
        action = payload.get("action")
        text = payload.get("text", "")
# details reúne resultados intermediários que serão mostrados pelo cliente.
        details = {}

# Fluxo Decode:
# Mensagem recebida -> Verificação/correção de erro -> Remoção da proteção -> Decodificação
        if action == "Decode":
# Verifica ou remove o controle de erro antes de descomprimir a mensagem.
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

# Executa Encode ou Decode usando o método de compressão selecionado.
        result = auxiliar.process_request(action, method, text, payload.get("k"))

# Fluxo Encode:
# Texto -> Compressão -> Controle de erro -> Simulação de erro
        if action == "Encode":
# Guarda a palavra-código produzida pela compressão.
            details["codeword"] = result
            codeword = result
# Acrescenta à palavra-código a proteção do método de controle de erro.
            result = auxiliar.process_error_control(
                action,
                error_method,
                result,
                payload.get("repeticao"),
            )
# No CRC, os bits adicionados ficam após a palavra-código original.
            if error_method == "1":
                details["crc"] = result[len(codeword):]

# Guarda a mensagem antes de qualquer erro de transmissão ser simulado.
            details["protected_message"] = result
            transmission_mode = payload.get("transmission_mode", "1")
# Cria o objeto responsável por simular alterações nos bits transmitidos.
            simulator = error_simulator()

# No modo manual, inverte exatamente o bit escolhido pelo usuário.
            if transmission_mode == "2":
                simulation = simulator.inverter_bit(result, payload.get("error_position"))
# Uma string retornada pelo simulador representa uma mensagem de erro.
                if isinstance(simulation, str):
                    raise ValueError(simulation)
                result, position = simulation
                details["changed_positions"] = [position]
# No modo aleatório, altera a quantidade de bits solicitada.
            elif transmission_mode == "3":
                simulation = simulator.inserir_erros_aleatorios(result, payload.get("error_quantity"))
                if isinstance(simulation, str):
                    raise ValueError(simulation)
                result, positions = simulation
                details["changed_positions"] = positions
        # Server não mostra a resposta ainda
        # print(f"\n(Server) Result: {result}")
# Monta a resposta de sucesso com o resultado final e os detalhes intermediários.
        response = {"ok": True, "result": result, "details": details}
# Converte falhas conhecidas em uma resposta que o cliente consegue exibir.
    except (json.JSONDecodeError, ValueError) as e:
        print(f"\n(Server) Error: {e}")
        response = {"ok": False, "error": str(e)}

# Converte o dicionário de resposta para JSON, transforma em bytes e envia ao cliente.
    cliente.send(json.dumps(response).encode())
