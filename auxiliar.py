# ============================
# === Console configuração ===
# ============================

#biblioteca para melhorar a visão no terminal
from rich.console import Console
from rich.table import Table
from typing import Optional

# importa os métodos
from logic.elias_gamma import EliasGamma
from logic.fibonacci import Fibonacci
from logic.huffman import Huffman
from logic.golomb import Golomb
from error_control.crc import crc_generator
from error_control.repetition_ri import repetition_ri

console = Console()

# Metodos disponíveis
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
    "3": None,  # Hamming ainda não implementado
}

# Nome dos métodos
METHOD_NAMES = {
    "1": "Fibonacci",
    "2": "Golomb",
    "3": "Elias-Gamma",
    "4": "Huffman",
}

# Nome dos métodos de controle de erro
ERROR_METHOD_NAMES = {
    "1": "CRC",
    "2": "Repetition",
    "3": "Hamming (em breve)",
}

# Dicas para cliente inserir as codificacoes/decodificacoes
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
def show_main_menu():
    table = Table(title="\nEncode or Decode")
    table.add_column("OPTION 1", style="steel_blue1")
    table.add_column("OPTION 2", style="sea_green1")
    table.add_column("OPTION 0", style="red")
    table.add_row("Encode", "Decode", "Exit")
    console.print(table)

# Mostra o menu de métodos (Fibonacci, Golomb, Elias-Gamma ou Huffman) 
def show_methods_menu(action: str):
    table = Table(title=f"\nMethods — {action}")
    for key, name in METHOD_NAMES.items():
        table.add_column(f"OPTION {key}", style="khaki1")
    table.add_row(*METHOD_NAMES.values())
    console.print(table)


# Mostra o menu de métodos de controle de erro
def show_error_methods_menu(action: str):
    table = Table(title=f"\nError Control Methods — {action}")
    for key, name in ERROR_METHOD_NAMES.items():
        table.add_column(f"OPTION {key}", style="khaki1")
    table.add_row(*ERROR_METHOD_NAMES.values())
    console.print(table)


# Lida com a escolha do cliente (Encode ou Decode) e monta a requisicao para o servidor
def handle_action(action: str):
    show_methods_menu(action)
    choice = input(f"\nChoose a method to {action.lower()}: ").strip()

    if choice not in METHOD_NAMES:
        console.print("\n[bold red]Invalid option![/bold red]")
        return None

    show_error_methods_menu(action)
    error_choice = input(f"\nChoose an error control method to {action.lower()}: ").strip()

    if error_choice not in ERROR_METHOD_NAMES:
        console.print("\n[bold red]Invalid option![/bold red]")
        return None

    if ERROR_METHODS[error_choice] is None:
        console.print("\n[bold yellow]Hamming is not implemented yet![/bold yellow]")
        return None

    hint = METHOD_HINTS.get((choice, action), "Enter input: ")
    text = input(hint).strip()
    request = {
        "action": action,
        "method": choice,
        "error_method": error_choice,
        "text": text,
    }

    if choice == "2":
        while True:
            try:
                k = int(input("\nDigite o divisor (K) - apenas potencia de 2 : "))
                if k >= 1 and (k & (k - 1)) == 0:
                    request["k"] = k
                    break
                console.print("\n[bold red]K precisa ser potencia de 2![/bold red]")
            except ValueError:
                console.print("\n[bold red]Numero Invalido![/bold red]")

    if error_choice == "2":
        while True:
            try:
                repeticao = int(input("\nDigite o numero de repeticoes: "))
                if repeticao > 0:
                    request["repeticao"] = repeticao
                    break
                console.print("\n[bold red]O numero de repeticoes precisa ser positivo![/bold red]")
            except ValueError:
                console.print("\n[bold red]Numero Invalido![/bold red]")

    return request


# Processa a requisicao recebida pelo servidor
def process_request(action: str, choice: str, text: str, k: Optional[int] = None):
    if action not in ("Encode", "Decode"):
        raise ValueError("Invalid action.")

    if choice not in METHOD_NAMES:
        raise ValueError("Invalid option.")

    method_class = METHODS[choice]

    try:
        result = None
        if choice == "2":
            if k is None:
                raise ValueError("K is required for Golomb.")

            if action == "Encode":
                result = method_class.encode(text, k)
            else:
                result = method_class.decode(text, k)

        else:
            if action == "Encode":
                result = method_class.encode(text)
            else:
                result = method_class.decode(text)

        return result

    except (NotImplementedError, ValueError) as e:
        raise ValueError(str(e)) from e


# Aplica ou remove o controle de erro antes/depois da compressao
def process_error_control(
    action: str,
    choice: Optional[str],
    bits: str,
    repeticao: Optional[int] = None,
):
    if choice is None:
        return bits

    if choice not in ERROR_METHOD_NAMES:
        raise ValueError("Invalid error control option.")

    method_class = ERROR_METHODS[choice]
    if method_class is None:
        raise ValueError("Hamming is not implemented yet.")

    if choice == "1":
        if any(bit not in "01" for bit in bits):
            raise ValueError("CRC requires a binary string.")

        crc = method_class()
        if action == "Encode":
            return crc.gerar_mensagem_crc(bits)

        crc_size = len(crc.gerador_crc) - 1
        if len(bits) < crc_size:
            raise ValueError("Invalid CRC message.")
        
        resultado_crc = crc.verificar_crc(bits)
        if set(resultado_crc) != {"0"}:
            raise ValueError("CRC error detected.")
        return bits[:-crc_size]

    if repeticao is None or repeticao <= 0:
        raise ValueError("Repeticao is required and must be positive.")

    repetition = method_class()
    if action == "Encode":
        return repetition.encode(bits, repeticao)
    return repetition.decode(bits, repeticao)
