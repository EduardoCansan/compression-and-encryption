#librarys for better output in terminal 
from rich.console import Console
from rich.table import Table

# import the methods
from logic.golomb import Golomb
from logic.elias_gamma import EliasGamma
from logic.fibonacci import Fibonacci
from logic.huffman import Huffman

console = Console()

METHODS: dict[str, type] = {
    "1": Fibonacci,
    "2": Golomb,
    "3": EliasGamma,
    "4": Huffman,
}

METHOD_NAMES = {
    "1": "Fibonacci",
    "2": "Golomb",
    "3": "Elias-Gamma",
    "4": "Huffman",
}

METHOD_HINTS = {
    ("1", "Encode"): "\nEnter text — letters, numbers and symbols are accepted as characters (ex: hello or 123): ",
    ("1", "Decode"): "\nEnter a Fibonacci encoded binary string (ex: 11011010): ",
    ("2", "Encode"): "\nEnter a positive integer (ex: 10): ",
    ("2", "Decode"): "\nEnter a Golomb encoded binary string (ex: 11011010): ",
    ("3", "Encode"): "\nEnter a non-zero positive integer (ex: 7): ",
    ("3", "Decode"): "\nEnter an Elias-Gamma encoded binary string (ex: 11011010): ",
    ("4", "Encode"): "\nEnter text to compress (ex: hello world): ",
    ("4", "Decode"): "\nFormat: a:0 b:10 n:11|100110110 (ex: banana)\nEnter a Huffman encoded binary string: ",
}

def show_main_menu():
    table = Table(title="\nEncode or Decode")
    table.add_column("OPTION 1", style="steel_blue1")
    table.add_column("OPTION 2", style="sea_green1")
    table.add_row("Encode", "Decode")
    console.print(table)

def show_methods_menu(action: str):
    table = Table(title=f"\nMethods — {action}")
    for key, name in METHOD_NAMES.items():
        table.add_column(f"OPTION {key}", style="khaki1")
    table.add_row(*METHOD_NAMES.values())
    console.print(table)

def handle_action(action: str):
    show_methods_menu(action)
    choice = input(f"Choose a method to {action.lower()}: ").strip()

    if choice not in METHOD_NAMES:
        console.print("\n[bold red]Invalid option![/bold red]")
        return

    name = METHOD_NAMES[choice]

    method_class = METHODS[choice]
    hint = METHOD_HINTS.get((choice, action), "Enter input: ")
    text = input(hint).strip()

    try:
        if action == "Encode":
            result = method_class.encode(text)
        else:
            result = method_class.decode(text)
        if result is not None:
            console.print(f"\n[default]Result: {result}[/default]")
    except NotImplementedError as e:
        console.print(f"\n[yellow]{e}[/yellow]")

def main():
    show_main_menu()
    option = input("Enter the option: ").strip()

    if option == "1":
        handle_action("Encode")
    elif option == "2":
        handle_action("Decode")
    else:
        console.print("\n[bold red]Invalid option![/bold red]")

if __name__ == "__main__":
    main()