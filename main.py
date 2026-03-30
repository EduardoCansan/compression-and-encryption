from rich.console import Console
from rich.table import Table

console = Console()

def show_main_menu():
    table = Table(title="\nEncode or Decode")
    table.add_column("OPTION 1", style="steel_blue1")
    table.add_column("OPTION 2", style="sea_green1")
    table.add_row("Encode", "Decode")
    console.print(table)


def show_methods_menu(action: str):
    table = Table(title=f"\nMethods — {action}")
    for col, method in [("A", "Golomb"), ("B", "Elias-Gamma"), ("C", "Fibonacci"), ("D", "Huffman")]:
        table.add_column(f"OPTION {col}", style="khaki1")
    table.add_row("Golomb", "Elias-Gamma", "Fibonacci", "Huffman")
    console.print(table)


METHODS = {
    "A": "Golomb",
    "B": "Elias-Gamma",
    "C": "Fibonacci",
    "D": "Huffman",
}


def handle_action(action: str):
    show_methods_menu(action)
    choice = input(f"Choose a method to {action.lower()}: ").upper()
    if choice in METHODS:
        console.print(f"[bold green]{action}ing with {METHODS[choice]}...[/bold green]")
    else:
        console.print("[bold red]Invalid option![/bold red]")


def main():
    show_main_menu()
    option = input("Enter the option: ").strip()

    if option == "1":
        handle_action("Encode")
    elif option == "2":
        handle_action("Decode")
    else:
        console.print("[bold red]Invalid option![/bold red]")


if __name__ == "__main__":
    main()