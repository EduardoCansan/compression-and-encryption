#librarys for better output in terminal 
from rich.console import Console
from rich.table import Table

# import the methods
from logic.golomb import Golomb
# from elias_gamma import EliasGamma
from logic.fibonacci import Fibonacci
# from huffman import Huffman

console = Console()

METHODS: dict[str, type] = {
    "1": Fibonacci,
    "2": Golomb,
    # "3": EliasGamma,
    # "4": Huffman,
}

METHOD_NAMES = {
    "1": "Fibonacci",
    "2": "Golomb",
    "3": "Elias-Gamma",
    "4": "Huffman",
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
    text = input("Enter text: ").strip()
    console.print(f"\n[bold green]{action}ing with {name}...[/bold green]")

    try:
        if action == "Encode":
            result = method_class.encode(text)
            console.print(f"Result: {result}")
        else:
            result = method_class.decode(text)
            console.print(f"Result: {result}")
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