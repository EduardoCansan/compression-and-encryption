# ==========================
# == Console configuração ==
# ==========================

#biblioteca para melhorar a visão no terminal
from rich.console import Console
from rich.table import Table

# importa os métodos
from logic.golomb import Golomb
from logic.elias_gamma import EliasGamma
from logic.fibonacci import Fibonacci
from logic.huffman import Huffman

console = Console()

# Metodos disponíveis
METHODS: dict[str, type] = {
    "1": Fibonacci,
    "2": Golomb,
    "3": EliasGamma,
    "4": Huffman,
}

# Nome dos métodos
METHOD_NAMES = {
    "1": "Fibonacci",
    "2": "Golomb",
    "3": "Elias-Gamma",
    "4": "Huffman",
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
    

# Lida com a escolha do cliente (Encode ou Decode) e chama o método escolhido para processar a entrada do cliente
def handle_action(action: str):
    show_methods_menu(action)
    choice = input(f"\nChoose a method to {action.lower()}: ").strip()

    if choice not in METHOD_NAMES:
        console.print("\n[bold red]Invalid option![/bold red]")
        return

    method_class = METHODS[choice]
    hint = METHOD_HINTS.get((choice, action), "Enter input: ")
    text = input(hint).strip()

    try:
        # Golomb precisa do divisor K
        if choice == "2":
            while True:
                try:
                    k = int(input("Digite o divisor (K) - apenas potencia de 2 : "))
                    if k >= 1 and (k & (k - 1)) == 0:
                        break
                    console.print("\n[bold red]K precisa ser potencia de 2![/bold red]")
                except ValueError:
                    console.print("\n[bold red]Numero Invalido![/bold red]")

            if action == "Encode":
                result = method_class.encode(text, k)
            else:
                result = method_class.decode(text, k)

        else:
            if action == "Encode":
                result = method_class.encode(text)
            else:
                result = method_class.decode(text)

        if result is not None:
            console.print(f"\n[default]Result: {result}[/default]")

    except (NotImplementedError, ValueError) as e:
        console.print(f"\n[yellow]{e}[/yellow]")
