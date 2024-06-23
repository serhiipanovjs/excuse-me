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
        case "short":
            print(Fore.RED + "Invalid input. Enter non empty value.\n")
        case "long":
            print(Fore.RED + "Invalid input. Entered value is to long.\n")
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

def validate_text_input(text):
    while True:
        choice = animated_input(text)
        if len(choice) == 0:
            error_generator("short")
            continue
        if len(choice) >= 25:
            error_generator("long")
            continue
        break
    return choice

def format_result_array_to_text(selected_cells, person_to_excuse_name, user_name):
    format_text = ''
    for cell_index in range(len(selected_cells)):
         current_sentence = selected_cells[cell_index]
         match cell_index:
             case 0:
                format_text += f"{current_sentence} {person_to_excuse_name}, {user_name} here, "
                continue
             case 1:
                format_text += f"{current_sentence}"
                continue
             case 2:
                format_text += f"\n\n{current_sentence}"
                continue
             case 7:
                format_text += f"\n\n{current_sentence}, {user_name}."
                continue
             case _:
                 format_text += f"\n{current_sentence}"
    return format_text

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

    user_name = validate_text_input("Enter name: \n")
    clear_terminal()

    print(Back.GREEN + Fore.WHITE + Style.BRIGHT + "*** REGISTRATION BLOCK ***\n")
    animated_print(f"Good job {user_name}!\n\n")
    animated_print("And now, please enter the name of the person you would like to excuse to.\n\n")

    person_to_excuse_name = validate_text_input("Enter name: \n")

    return {"user_name": user_name, "person_to_excuse_name": person_to_excuse_name}

def show_result_excuse_block(format_result):
    clear_terminal()

    print(Back.GREEN + Fore.WHITE + Style.BRIGHT + "*** YOUR EXCUSE IS CREATED ***\n")
    print("*******************************************************************************")
    print(format_result)
    print("*******************************************************************************")

    print(Fore.GREEN + Style.BRIGHT + "1. Copy this excuse to clipboard\n")
    print(Fore.GREEN + Style.BRIGHT + "2. Generate new excuse\n")
    print(Fore.GREEN + Style.BRIGHT + "3. Return to the main page\n")

    menu_id = validate_number_input([1, 2, 3])
    match menu_id:
        case 1:
            pyperclip.copy(format_result)
            animated_print("Excuse copied to clipboard...")
            time.sleep(1)
            show_result_excuse_block(format_result)
        case 2:
            show_excuse_generator_page()
        case 3:
            main()

def show_excuse_generator_page():
    participants = show_registration_names_block()
    clear_terminal()

    user_name = participants["user_name"]
    person_to_excuse_name = participants["person_to_excuse_name"]
    template_variants_sheet = SHEET.worksheet('template_variants')
    column_count = template_variants_sheet.col_count
    current_column = 1
    selected_cells = []

    while column_count >= current_column:
        column_values = template_variants_sheet.col_values(current_column)
        random.shuffle(column_values)
        current_variant = 0

        while True:
            first_four_variants = column_values[current_variant * 4 : 4 + (current_variant * 4)]

            if len(first_four_variants) < 4:
                random.shuffle(column_values)
                current_variant = 0
                continue

            clear_terminal()
            print(Back.GREEN + Fore.WHITE + Style.BRIGHT + "*** CONSTRUCT YOUR EXCUSE ***\n")

            format_text = format_result_array_to_text(selected_cells, person_to_excuse_name, user_name)
            print("*******************************************************************************")
            if (current_column != 1):
                print(format_text)
            else:
                print("Your result will be here after the first choice.")
            print("*******************************************************************************")
            print("\nChoose from the first four options or 'Generate new Variants'.\n")

            menu_options = first_four_variants
            valid_options_list = [1, 2, 3, 4, 5, 6]
            menu_options.append("Generate new Variants")
            if (current_column != 1):
                menu_options.append("Step Back")
                valid_options_list.append(7)
            menu_options.append("Exit to main menu")

            for menu_index in range(len(menu_options)):
                print(Fore.GREEN + Style.BRIGHT + f"{menu_index + 1}. {menu_options[menu_index]}")

            menu_id = validate_number_input(valid_options_list)

            match menu_id:
                case 1 | 2 | 3 | 4:
                    current_column += 1
                    selected_cells.append(first_four_variants[menu_id - 1])
                    break
                case 5:
                    current_variant += 1
                    continue
                case 6:
                    if (current_column == 1):
                        main()
                    current_column -= 1
                    del selected_cells[-1]
                    break
                case 7:
                    main()

    format_result = format_result_array_to_text(selected_cells, person_to_excuse_name, user_name)
    excuse_answers_sheet = SHEET.worksheet('excuse_answers')
    excuse_answers_sheet.append_row([format_result])
    show_result_excuse_block(format_result)

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