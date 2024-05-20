import os
import sys
import time
import concurrent.futures as cf
import requests
from blessed import Terminal
import psutil
from rich.panel import Panel
from rich.console import Console
from rich.style import Style
from cryptofuzz import Ethereum
from random import randint

eth = Ethereum()
console = Console()


def OnClear():
    if "win" in sys.platform.lower():
        os.system("cls")
    else:
        os.system("clear")


def balance(addr):
    url_n = f"https://ethbook.guarda.co/api/v2/address/{addr}"
    req = requests.get(url_n)
    if req.status_code == 200:
        return dict(req.json())["balance"]
    else:
        return "0"


def transaction(addr):
    req = requests.get(f"https://ethbook.guarda.co/api/v2/address/{addr}")
    if req.status_code == 200:
        return int(dict(req.json())["txs"])
    else:
        return 0


def draw_system_status(term):
    cpu_percent = psutil.cpu_percent()
    ram_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent
    termWidth = term.width
    system_status = (
        f'\n{draw_graph("CPU", cpu_percent, termWidth)}\n'
        f'\n{draw_graph("RAM", ram_percent, termWidth)}\n'
        f'\n{draw_graph("HDD", disk_percent, termWidth)}\n'
    )
    return system_status


def draw_ethereum_info(z, w, addr, priv, txs):
    ethPanel = (
        f'\n[gold1]Total Checked: [orange_red1]{z}[/][gold1]  Win: [white]{w}[/]'
        f'[gold1]  Transaction: [/][aquamarine1]{txs}\n\n[/][gold1]ADDR: [white] {addr}[/white]\n\n'
        f'PRIVATE: [grey54]{priv}[/grey54]\n'
    )
    return ethPanel


def draw_graph(title, percent, width):
    bar_length = int(width - 17)
    num_blocks = int(percent * bar_length / 100)
    dash = "[grey54]–[/]"
    barFill = "[green]▬[/]"
    bar = barFill * num_blocks + dash * (bar_length - num_blocks)
    return f"[white]{title}[/]: |{bar}| {percent}%"


def generate_private_key():
    # Generate a random number within the valid range
    while True:
        private_key_int = randint(1, 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141)
        private_key_hex = hex(private_key_int)[2:].zfill(64)  # Ensure the hex string is 64 characters long
        if len(private_key_hex) == 64:  # Check if the generated private key is of correct length
            return private_key_hex


def main():
    term = Terminal()
    with term.fullscreen():
        with term.cbreak(), term.hidden_cursor():
            OnClear()
            with open("addresses.txt", "r") as address_file:
                addresses = address_file.read().splitlines()  # Read addresses from the file
            while True:
                z = 0
                w = 0
                for addr_file in addresses:
                    system_status = draw_system_status(term)
                    draw_system_status_panel = Panel(system_status, border_style="grey66")
                    priv = generate_private_key()
                    addr = eth.hex_addr(priv)
                    txs = 0
                    if addr == addr_file:  # Check if generated address matches any address in the file
                        txs = transaction(addr)
                        if txs > 0:
                            w += 1
                            with open("Found.txt", "a") as fr:
                                fr.write(f"{addr} TXS: {txs} BAL: {balance(addr)}\n")
                                fr.write(f"{priv}\n")
                                fr.write(f"{'-' * 50}\n")
                    ethPanel = draw_ethereum_info(z, w, addr, priv, txs)
                    with term.location(0, 1):
                        console.print(draw_system_status_panel, justify="full", soft_wrap=True)
                        console.print(Panel(ethPanel, title="[white]Ethereum Private Key Checker V1[/]",
                                            subtitle="[green_yellow blink] itrebel.eth [/]", style="green"),
                                      justify="full", soft_wrap=True)
                    z += 1


if __name__ == "__main__":
    with cf.ProcessPoolExecutor(max_workers=8) as executor:
        for _ in range(8):
            executor.submit(main).result()
