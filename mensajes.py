from colorama import Fore, Style, init

init(autoreset=True)


def titulo(texto: str) -> None:
    print(Fore.CYAN + Style.BRIGHT + "\n" + "=" * 40)
    print(Fore.CYAN + Style.BRIGHT + "  " + texto.upper())
    print(Fore.CYAN + Style.BRIGHT + "=" * 40)


def exito(texto: str) -> None:
    print(Fore.GREEN + Style.BRIGHT + texto)


def error(texto: str) -> None:
    print(Fore.RED + Style.BRIGHT + "ERROR - " + texto)


def advertencia(texto: str) -> None:
    print(Fore.YELLOW + Style.BRIGHT + "ATENCIÓN - " + texto)


def encabezado(texto: str) -> None:
    print(Fore.MAGENTA + Style.BRIGHT + texto)
    print(Fore.MAGENTA + "-" * len(texto))
