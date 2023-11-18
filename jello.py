#!/usr/bin/env python3

import subprocess

from colorama import Fore, Style, init
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory

import tokens


def cprint(s: str, c, newline: bool):
    end = "" if newline else "\n"
    print(Style.BRIGHT + c + s + Fore.RESET, end=end)

def run_jelly(expr: str, arg: str):
    try:
        command = ["jelly", "eun", expr, arg]
        result = subprocess.run(command, text=True, capture_output=True, check=True)
        output_text = result.stdout.strip()

        cprint(output_text, Fore.GREEN, False)

    except subprocess.CalledProcessError as e:
        # Print the stderr output for more information about the error
        print(Fore.RED + f"Error: {e}")
        print(Fore.RED + "stderr:", e.stderr)

completer = WordCompleter(tokens.monadic.keys())
history = FileHistory("jello_history.txt")

def to_jelly(token: str) -> str | None:
    if token in tokens.monadic:
        return tokens.monadic[token]
    return None

def convert(expr: list[str]) -> str:
    return "".join([to_jelly(t) for t in expr])

if __name__ == "__main__":
    init()  # for colorama

    print("🟢🟡🔴 Jello 🔴🟡🟢\n")

    while True:
        user_input = prompt("> ", completer=completer, history=history)

        expr = user_input.strip().split()
        arg = expr[-1]
        converted_expr = convert(expr[:-1])
        for i in range(1, len(converted_expr) + 1):
            cprint(f"   {converted_expr[:i]:<{len(converted_expr)}}", Fore.YELLOW, True)
            cprint(f" {arg} ➡️ ", Fore.BLUE, True)
            run_jelly(converted_expr[:i], arg)
