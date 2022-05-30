#!/usr/bin/env python3

import re

from src.misc import *

class Printer:
    def print(self, word, response):
        raise NotImplementedError("A subclass of this one should be made, defining this method.")

# Simple output of the tool
class SimplePrinter(Printer):
    def __init__(self, pattern):
        self.pattern = pattern

    def print(self, word, response):
        print(f"{word} => status: {response.status_code} | size: {len(response.text)}", end='')
        if self.pattern:
            regexp = re.compile(self.pattern)
            if regexp.search(response.text):
                print(' | Pattern: Match')
            else:
                print(' | Pattern: Do not match')
        else:
            print()

# Colored output of the tool
class RichPrinter(Printer):
    def __init__(self, pattern, align = 20):
        from rich.console import Console
        self.pattern = pattern
        self.console = Console()
        self.align = align

    def print(self, word, response):
        if response.status_code < 200:
            status = f"[yellow]{response.status_code}[/yellow]"
        elif response.status_code < 300:
            status = f"[green]{response.status_code}[/green]"
        elif response.status_code < 400:
            status = f"[cyan]{response.status_code}[/cyan]"
        elif response.status_code < 500:
            status = f"[purple]{response.status_code}[/purple]"
        elif response.status_code < 600:
            status = f"[red]{response.status_code}[/red]"
        if self.pattern:
            self.console.print(f"[bold blue]{word}[/bold blue]{' ' * (self.align - len(word))} => status: {status} | size: [orange]{len(response.text)}[/orange]", end='')
            regexp = re.compile(self.pattern)
            if regexp.search(response.text):
                self.console.print(' | Pattern: [green]Match[/green]')
            else:
                self.console.print(' | Pattern: [red]Do not match[/red]')
        else:
            self.console.print(f"[bold blue]{word}[/bold blue]{' ' * (self.align - len(word))} => status: {status} | size: [orange]{len(response.text)}[/orange]")


# Code-based output of the tool
class CodePrinter(Printer):
    def __init__(self, code, pattern):
        self.code = code
        self.pattern = pattern

    def print(self, word, response):
        pattern = self.pattern
        exec(self.code)

# This function returns the correct printer class depending on the arguments sent to the tool
def choose_printer(args):
    if not single_true([args['print_simple'], args['print_colored'], args['print_code']]):
        print("Please only select only one printer (-Ps, -Pc or PC)")
        exit()
    if args['print_simple']:
        return SimplePrinter(args['pattern'])
    elif args['print_colored']:
        return RichPrinter(args['pattern'])
    elif args['print_code']:
        return CodePrinter(args['print_code'], args['pattern'])
    else:
        return RichPrinter(args['pattern'])

