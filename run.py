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

def error_generator(type):
    match type:
        case "number":
            print(Fore.RED + "Invalid input. Enter valid number for Menu choice.\n")
        case _:
            print(Fore.RED + "Invalid input.\n")

def validate_number_input(validValues):
    while True:
        try:
            choice = int(input("Please enter your choice: \n"))
            if choice in validValues:
                break
            error_generator("number")
            continue
        except ValueError:
            error_generator("number")
            continue
    return choice

def main():
    clear_terminal()
    print(Back.GREEN + Fore.WHITE + Style.BRIGHT + "*** WELCOME TO 'EXCUSE ME' APPLICATION ***\n")
    print("Please use our navigation and make your choice.\n")
    print("\n")
    print(Fore.GREEN + Style.BRIGHT + "1. Generate new excuse\n")
    print(Fore.GREEN + Style.BRIGHT + "2. Show already generated excuses\n")
    print(Fore.GREEN + Style.BRIGHT + "3. Show information about application\n")

    menu_id = validate_number_input([1, 2, 3])

    match menu_id:
        case 1:
            show_excuse_generator_page()
        case 2:
            show_customers_excuses_page()
        case 3:
            show_about_page()

def show_registration_names_block():
    clear_terminal()
    print(Back.GREEN + Fore.WHITE + Style.BRIGHT + "*** REGISTRATION BLOCK ***\n")
    animated_print("Let's gather some information.\n\n")
    animated_print("Please type the name of the person who wants to excuse.\n\n")

    user_name = animated_input("Enter name: \n")
    clear_terminal()

    print(Back.GREEN + Fore.WHITE + Style.BRIGHT + "*** REGISTRATION BLOCK ***\n")
    animated_print("Good job!\n\n")
    animated_print("And now, please enter the name of the person you would like to excuse to.\n\n")

    person_to_excuse_name = animated_input("Enter name: \n")

    return {"user_name": user_name, "person_to_excuse_name": person_to_excuse_name}

def show_excuse_generator_page():
    participants = show_registration_names_block()
    clear_terminal()
    user_name = participants["user_name"]
    person_to_excuse_name = participants["person_to_excuse_name"]
    print(user_name, person_to_excuse_name)

def show_customers_excuses_page():
    clear_terminal()

    excuse_answers_sheet = SHEET.worksheet('excuse_answers')
    customers_excuses = excuse_answers_sheet.col_values(1)
    customers_excuses.reverse()
    customers_excuses_length = len(customers_excuses)
    current_customers_excuse_index = 0

    if customers_excuses_length == 0:
        show_non_content_page()
        return

    while True:
        current_customers_excuse = customers_excuses[current_customers_excuse_index]
        print(Back.GREEN + Fore.WHITE + Style.BRIGHT + "*** CUSTOMERS EXCUSES ***\n")
        print("*******************************************************************************")
        print(current_customers_excuse)
        print("*******************************************************************************")

        print(Fore.GREEN + Style.BRIGHT + "1. Show next excuse\n")
        print(Fore.GREEN + Style.BRIGHT + "2. Show previous excuse\n")
        print(Fore.GREEN + Style.BRIGHT + "3. Copy this excuse to clipboard\n")
        print(Fore.GREEN + Style.BRIGHT + "4. Return to the main page\n")

        menu_id = validate_number_input([1, 2, 3, 4])
        match menu_id:
            case 1:
                if current_customers_excuse_index + 1 == customers_excuses_length:
                    current_customers_excuse_index = 0
                else:
                    current_customers_excuse_index += 1

                clear_terminal()
                continue
            case 2:
                if current_customers_excuse_index == 0:
                    current_customers_excuse_index = customers_excuses_length - 1
                else:
                    current_customers_excuse_index -= 1

                clear_terminal()
                continue
            case 3:
                pyperclip.copy(current_customers_excuse)
                animated_print("Excuse copied to clipboard...")
                time.sleep(1)
                clear_terminal()
                continue
            case 4:
                main()
                break

def show_about_page():
    clear_terminal()
    print(Back.GREEN + Fore.WHITE + Style.BRIGHT + "*** ABOUT 'EXCUSE ME' APPLICATION ***\n")

    print("*******************************************************************************")
    print("-- Need a quick excuse?\n")
    print("-- 'EXCUSE ME' has you covered!\n")
    print("-- Whether you're late, missing a deadline, or need a graceful exit,\n")
    print("-- our app offers a vast library of tailored excuses for every situation.\n")
    print("*******************************************************************************")

    print("\n")
    print(Fore.GREEN + Style.BRIGHT + "1. Generate new excuse\n")
    print(Fore.GREEN + Style.BRIGHT + "2. Return to the main page\n")

    menu_id = validate_number_input([1, 2])

    match menu_id:
        case 1:
            show_excuse_generator_page()
        case 2:
            main()

def show_non_content_page():
    clear_terminal()
    print(Back.GREEN + Fore.WHITE + Style.BRIGHT + "*** EMPTY DATA ***\n")
    print("Sorry, but we did not find any data\n")
    print("After 5 seconds you will be return to the main page\n")
    time.sleep(5)
    main()

main()