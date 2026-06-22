# Biblioteca para melhorar a visão no terminal
from rich.console import Console
from rich.table import Table
from typing import Optional

# Importa os métodos 
# Métodos de codificação/decodificação
from logic.elias_gamma import EliasGamma
from logic.fibonacci import Fibonacci
from logic.huffman import Huffman
from logic.golomb import Golomb
# Métodos de controle de erro
from error_control.crc import crc_generator
from error_control.repetition_ri import repetition_ri
from error_control.hamming import hamming

# Console do Rich 
console = Console()

# Metodos de codificação disponíveis
METHODS: dict[str, type] = {
    "1": Fibonacci,
    "2": Golomb,
    "3": EliasGamma,
    "4": Huffman,
}

# Metodos de controle de erro disponíveis
ERROR_METHODS: dict[str, Optional[type]] = {
    "1": crc_generator,
    "2": repetition_ri,
    "3": hamming,
}

# Nome dos métodos de codificação
# é usado na criação dos menus e na exibição das escolhas.
METHOD_NAMES = {
    "1": "Fibonacci",
    "2": "Golomb",
    "3": "Elias-Gamma",
    "4": "Huffman",
}

# Nome dos métodos de controle de erro
# é usado na criação dos menus e na exibição das escolhas.
ERROR_METHOD_NAMES = {
    "1": "CRC",
    "2": "Repetition",
    "3": "Hamming",
}

# Modos de simulação de erro na transmissão
# é usado na criação dos menus e na exibição das escolhas.
TRANSMISSION_MODE_NAMES = {
    "1": "No error",
    "2": "Manual error",
    "3": "Random error",
}

# Dicas para cliente inserir as codificacoes/decodificacoes
# ajuda o usuário a informar dados no formato esperado.
METHOD_HINTS = {
    ("1", "Encode"): "\nEnter text — letters, numbers and symbols are accepted as characters (ex: hello or 123): ",
    ("1", "Decode"): "\nEnter a Fibonacci encoded binary string (ex: 11011010): ",
    ("2", "Encode"): "\nEnter text (letters) or positive integer (ex: 10): ",
    ("2", "Decode"): "\nEnter a Golomb encoded binary string (ex: 11011010): ",
    ("3", "Encode"): "\nEnter text (letters) or non-zero positive integer (ex: 7): ",
    ("3", "Decode"): "\nEnter an Elias-Gamma encoded binary string (ex: 11011010): ",
    ("4", "Encode"): "\nEnter text to compress (ex: hello world): ",
    ("4", "Decode"): "\nFormat: a:0 b:10 n:11|100110110 (ex: banana)\nEnter a Huffman encoded binary string: ",
}

# Mostra o menu principal (Encode ou Decode)
# Exibe as ações principais disponíveis para o cliente.
# nao recebe nenhum valor e nao retorna nada
# é chamada pelo cliente no início de cada operação.
def show_main_menu():
# Cria uma tabela Rich e adiciona as opções Encode, Decode e Exit.
    table = Table(title="\nEncode or Decode")
    table.add_column("OPTION 1", style="steel_blue1")
    table.add_column("OPTION 2", style="sea_green1")
    table.add_column("OPTION 0", style="red")
    table.add_row("Encode", "Decode", "Exit")
    console.print(table)

# Mostra o menu de métodos (Fibonacci, Golomb, Elias-Gamma ou Huffman) 
# recebe action, que informa se a operação é Encode ou Decode.
# é chamada por handle_action durante a montagem da requisição.
def show_methods_menu(action: str):
# Os nomes das colunas e da linha vêm da tabela de mapeamento METHOD_NAMES.
    table = Table(title=f"\nMethods — {action}")
    for key, name in METHOD_NAMES.items():
        table.add_column(f"OPTION {key}", style="khaki1")
    table.add_row(*METHOD_NAMES.values())
    console.print(table)


# Mostra o menu de métodos de controle de erro
# Recebe: action, usada no título para indicar Encode ou Decode.
# é chamada por handle_action após a escolha da compressão.
def show_error_methods_menu(action: str):
    table = Table(title=f"\nError Control Methods — {action}")
    for key, name in ERROR_METHOD_NAMES.items():
        table.add_column(f"OPTION {key}", style="khaki1")
    table.add_row(*ERROR_METHOD_NAMES.values())
    console.print(table)


# Mostra o menu de simulação de erro na transmissão
# é chamado durante Encode para escolher se bits serão alterados.
def show_transmission_menu():
    table = Table(title="\nTransmission Error Simulation")
    for key, name in TRANSMISSION_MODE_NAMES.items():
        table.add_column(f"OPTION {key}", style="khaki1")
    table.add_row(*TRANSMISSION_MODE_NAMES.values())
    console.print(table)


# Lida com a escolha do cliente (Encode ou Decode) e monta a requisicao para o servidor
# coleta escolhas e dados do usuário e montar a requisição.
# recebe action, indicando se o usuário quer codificar ou decodificar.
# retorna um dicionário para o servidor ou None quando uma escolha é inválida.
# é chamada pelo loop principal do cliente antes do envio do JSON.
def handle_action(action: str):
    # Primeiro, solicita e valida o método de compressão.
    show_methods_menu(action)
    choice = input(f"\nChoose a method to {action.lower()}: ").strip()

    if choice not in METHOD_NAMES:
        console.print("\n[bold red]Invalid option![/bold red]")
        return None

    # Depois, solicita e valida o método de controle de erro.
    show_error_methods_menu(action)
    error_choice = input(f"\nChoose an error control method to {action.lower()}: ").strip()

    if error_choice not in ERROR_METHOD_NAMES:
        console.print("\n[bold red]Invalid option![/bold red]")
        return None

    # guarda campos relacionados à simulação de transmissão.
    transmission_data = {}
    # Hamming já corrige erro simples no próprio decode, então não passa pelo menu de simulação.
    if action == "Encode" and error_choice == "3":
        transmission_data["transmission_mode"] = "1"

    # A simulação de transmissão é configurada apenas no fluxo Encode.
    elif action == "Encode":
        show_transmission_menu()
        transmission_mode = input("\nChoose a transmission mode: ").strip()

        if transmission_mode not in TRANSMISSION_MODE_NAMES:
            console.print("\n[bold red]Invalid option![/bold red]")
            return None

        transmission_data["transmission_mode"] = transmission_mode

        # no modo manual, solicita a posição exata dos bits que serao invertidos.
        if transmission_mode == "2":
            try:
                posicoes = input("\nEnter the positions of the bits to invert (ex: 2 4 5): ").split()
                transmission_data["error_positions"] = [int(posicao) for posicao in posicoes]
            except ValueError:
                console.print("\n[bold red]Invalid number![/bold red]")
                return None
            
        # no modo aleatório, solicita quantos bits devem ser alterados.
        elif transmission_mode == "3":
            try:
                transmission_data["error_quantity"] = int(input("\nNumber of errors: "))
            except ValueError:
                console.print("\n[bold red]Invalid number![/bold red]")
                return None

    # seleciona a dica correspondente e lê a mensagem que será processada.
    hint = METHOD_HINTS.get((choice, action), "Enter input: ")
    text = input(hint).strip()
    
    # monta o dicionário básico que posteriormente será convertido para JSON.
    request = {
        "action": action,
        "method": choice,
        "error_method": error_choice,
        "text": text,
    }
    
    # adiciona ao pedido os dados opcionais da transmissão.
    request.update(transmission_data)

    # Apenas Golomb precisa do parâmetro K; a validação de potência de 2 ocorre em golomb.py.
    if choice == "2":
        try:
            request["k"] = int(input("\nEnter the divisor (K) - powers of 2 only: "))
        except ValueError:
            console.print("\n[bold red]Invalid number![/bold red]")
            return None

    # o método Repetition precisa saber quantas vezes cada informação será repetida.
    if error_choice == "2":
        while True:
            try:
                repeticao = int(input("\nEnter the number of repetitions: "))
                if repeticao > 0:
                    request["repeticao"] = repeticao
                    break
                console.print("\n[bold red]The number of repetitions must be positive![/bold red]")
            except ValueError:
                console.print("\n[bold red]Invalid number![/bold red]")

    # entrega ao cliente a requisição completa para envio ao servidor.
    return request


# Processa a requisicao recebida pelo servidor
# Objetivo: executar a compressão ou descompressão escolhida.
# Recebe: ação, opção do método, texto e o K opcional usado por Golomb.
# Retorna: o resultado produzido pelo método de compressão selecionado.
# Fluxo: é chamada pelo servidor após preparar ou remover o controle de erro.
def process_request(action: str, choice: str, text: str, k: Optional[int] = None):
# Valida a ação e a opção antes de acessar a tabela METHODS.
    if action not in ("Encode", "Decode"):
        raise ValueError("Invalid action.")

    if choice not in METHOD_NAMES:
        raise ValueError("Invalid option.")

# Usa a opção como chave para encontrar a classe responsável pelo processamento.
    method_class = METHODS[choice]

# Transforma erros esperados dos métodos em ValueError para o servidor tratar.
    try:
        result = None
# Golomb recebe o parâmetro K além do texto.
        if choice == "2":
            if k is None:
                raise ValueError("K is required for Golomb.")

            if action == "Encode":
                result = method_class.encode(text, k)
            else:
                result = method_class.decode(text, k)

# Os demais métodos precisam apenas do texto para Encode ou Decode.
        else:
            if action == "Encode":
                result = method_class.encode(text)
            else:
                result = method_class.decode(text)

# Retorna ao servidor a palavra-código ou a mensagem decodificada.
        return result

    except (NotImplementedError, ValueError) as e:
        raise ValueError(str(e)) from e

def separar_huffman(bits):
    if "|" not in bits:
        return None, bits

    tabela, bits = bits.split("|", 1)

    return tabela.strip(), bits.strip()


def remontar_huffman(tabela, bits):
    if tabela is None:
        return bits

    return f"{tabela} | {bits}"

# Aplica ou remove o controle de erro antes/depois da compressao
# Objetivo: adicionar proteção no Encode ou verificar/remover proteção no Decode.
# Recebe: ação, método escolhido, sequência de bits e repetição opcional.
# Retorna: bits protegidos no Encode ou bits sem a proteção no Decode.
# Fluxo: conecta as etapas de compressão e transmissão dentro do servidor.
def process_error_control(
    action: str,
    choice: Optional[str],
    bits: str,
    repeticao: Optional[int] = None,
):
# Sem método escolhido, mantém a mensagem exatamente como foi recebida.
    if choice is None:
        return bits

    if choice not in ERROR_METHOD_NAMES:
        raise ValueError("Invalid error control option.")
    
    huffman_table, bits = separar_huffman(bits)

# Encontra a classe de controle de erro usando a tabela ERROR_METHODS.
    method_class = ERROR_METHODS[choice]

# O CRC trabalha apenas com bits e permite detectar alterações na mensagem.
    if choice == "1":
        if any(bit not in "01" for bit in bits):
            raise ValueError("CRC requires a binary string.")

        crc = method_class()
# No Encode, calcula o CRC e o acrescenta à mensagem.
        if action == "Encode":
            return remontar_huffman(
            huffman_table,
            crc.gerar_mensagem_crc(bits)
        )

# No Decode, verifica o CRC antes de remover os bits usados na proteção.
        crc_size = len(crc.gerador_crc) - 1
        if len(bits) < crc_size:
            raise ValueError("Invalid CRC message.")
        
        resultado_crc = crc.verificar_crc(bits)
        if set(resultado_crc) != {"0"}:
            raise ValueError("CRC error detected.")
        return remontar_huffman(huffman_table,bits[:-crc_size])

# O Hamming adiciona bits de paridade nas posições 1, 2, 4, 8...
# No Decode, corrige um erro simples e remove os bits de paridade.
    if choice == "3":
        if any(bit not in "01" for bit in bits):
            raise ValueError("Hamming requires a binary string.")

        if action == "Encode":
            return remontar_huffman(
                huffman_table,
                method_class.encode(bits)
            )
        return remontar_huffman(huffman_table,method_class.decode(bits))

# Repetition exige uma quantidade positiva de repetições.
    if repeticao is None or repeticao <= 0:
        raise ValueError("Repetition is required and must be positive.")

    repetition = method_class()
# No Encode repete os dados; no Decode recupera os dados a partir das repetições.
    if action == "Encode":
        return remontar_huffman(
            huffman_table,
            repetition.encode(bits, repeticao)
        )

    return remontar_huffman(huffman_table,repetition.decode(bits, repeticao))
