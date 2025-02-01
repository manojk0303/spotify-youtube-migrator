import logging
from colorama import Fore, Style, init

init(autoreset=True)

def setup_logging(enable_logging):
    if enable_logging:
        logging.basicConfig(level=logging.INFO, format="%(message)s")

def print_colored(message, color):
    color_map = {
        "red": Fore.RED,
        "green": Fore.GREEN,
        "blue": Fore.BLUE,
        "yellow": Fore.YELLOW,
    }
    print(color_map.get(color, Fore.WHITE) + message + Style.RESET_ALL)