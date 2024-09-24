import os
from colorama import Fore, Style, Back, init

# this will make it so colors don't persist (for ex: if I terminate program)
# and now my terminal console is now red, this prevents that, part of colorama.
init(autoreset=True)

def clear_screen() -> None:
    # if windows (NT type) use 'cls' to clear screen otherwise it's Unix, so use 'clear'.
    os.system('cls' if os.name == 'nt' else 'clear')



class Colors:
    BOLD: str = f"{Style.BRIGHT}"
    RED: str = f"{BOLD}{Fore.RED}"
    GREEN: str = f"{BOLD}{Fore.GREEN}"
    YELLOW: str = f"{BOLD}{Fore.YELLOW}"
    MAGENTA: str = f"{BOLD}{Fore.MAGENTA}"
    CYAN: str = f"{BOLD}{Fore.CYAN}"
Cols = Colors()

class Display:
    DISCORD_CONTACT: str = "alimuhammadsecured_65817"
    LINE: str = f"{Cols.RED}_"*30
    TITLE: str = f'''
                    {Cols.MAGENTA}

                         █████╗ ██╗     ██╗   ███████╗███████╗ ██████╗
                        ██╔══██╗██║     ██║   ██╔════╝██╔════╝██╔════╝
                        ███████║██║     ██║   ███████╗█████╗  ██║     
                        ██╔══██║██║     ██║   ╚════██║██╔══╝  ██║     
                        ██║  ██║███████╗██║██╗███████║███████╗╚██████╗
                        ╚═╝  ╚═╝╚══════╝╚═╝╚═╝╚══════╝╚══════╝ ╚═════╝                     
                '''
    