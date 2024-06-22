import gspread
from google.oauth2.service_account import Credentials

import colorama
from colorama import Fore, Back, Style
import sys
import time
import random

import pyperclip

colorama.init(autoreset=True)

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDENTIALS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDENTIALS = CREDENTIALS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDENTIALS)
SHEET = GSPREAD_CLIENT.open('my_excuse_sheet')

def clear_terminal():
    print(end="\033c", flush=True)

def animated_print(text):
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)


def animated_input(text):
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    return input()

def main():
    clear_terminal()
    print(Back.GREEN + Fore.WHITE + Style.BRIGHT + "*** WELCOME TO 'EXCUSE ME' APPLICATION ***\n")
    print("Please use our navigation and make your choice.\n")
    print("\n")
    print(Fore.GREEN + Style.BRIGHT + "1. Generate new excuse\n")
    print(Fore.GREEN + Style.BRIGHT + "2. Show already generated excuses\n")
    print(Fore.GREEN + Style.BRIGHT + "3. Show information about application\n")

main()