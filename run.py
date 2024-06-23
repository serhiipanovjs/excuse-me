import gspread
from google.oauth2.service_account import Credentials

import colorama
from colorama import Fore, Back, Style
import sys
import time
import random

import pyperclip
colorama.init(autoreset=True)

# Define the scope for accessing Google Sheets and Google Drive
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials from the service account file and authorize the gspread client
CREDENTIALS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDENTIALS = CREDENTIALS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDENTIALS)
SHEET = GSPREAD_CLIENT.open('my_excuse_sheet')

def clear_terminal():
    """Clears the terminal screen."""
    print(end="\033c", flush=True)

def animated_print(text):
    """Prints text with an animated effect."""
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)

def animated_input(text):
    """Prompts user input with an animated effect."""
    animated_print(text)
    return input()

def error_message(type):
    """Generates error messages based on the type of error."""
    messages = {
        "number": "Invalid input. Enter valid number for Menu choice.\n",
        "short": "Invalid input. Enter non-empty value.\n",
        "long": "Invalid input. Entered value is too long.\n",
        "default": "Invalid input.\n"
    }
    print(Fore.RED + messages.get(type, messages["default"]))

def validate_number_input(valid_values):
    """Validates that user input is a number and within the specified valid values."""
    while True:
        try:
            choice = int(input("Please enter your choice: \n"))
            if choice in valid_values:
                return choice
            error_message("number")
        except ValueError:
            error_message("number")


def validate_text_input(text):
    """Validates that user input is a non-empty string and not too long."""
    while True:
        choice = animated_input(text)
        if len(choice) == 0:
            error_message("short")
            continue
        if len(choice) >= 25:
            error_message("long")
            continue
        return choice

def format_result_array_to_text(selected_cells, person_to_excuse_name, user_name):
    """Formats the selected excuse sentences into a complete text."""
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

def show_menu(options, prompt="Please enter your choice: \n"):
    """Displays a menu with options and validates the user input."""
    for i, option in enumerate(options):
        print(Fore.GREEN + Style.BRIGHT + f"{i + 1}. {option}\n")
    return validate_number_input(list(range(1, len(options) + 1)))

def main():
    """Main function to display the initial menu and handle user choices."""
    clear_terminal()
    print(Back.GREEN + Fore.WHITE + Style.BRIGHT + "*** WELCOME TO 'EXCUSE ME' APPLICATION ***\n")
    print("Please use our navigation and make your choice.\n")
    print("\n")

    options = ["Generate new excuse", "Show already generated excuses", "Show information about application"]
    menu_id = show_menu(options)

    match menu_id:
        case 1:
            show_excuse_generator_page()
        case 2:
            show_customers_excuses_page()
        case 3:
            show_about_page()

def show_registration_names_block():
    """Displays the registration block to gather names from the user."""
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
    """Displays the generated excuse and provides options to the user."""
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
    """Guides the user through the process of generating a new excuse."""
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
    """Displays already generated excuses for the user to view and manage."""
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

        options = ["Show next excuse", "Show previous excuse", "Copy this excuse to clipboard", "Return to the main page"]
        menu_id = show_menu(options)

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
    """Displays information about the application."""
    clear_terminal()
    print(Back.GREEN + Fore.WHITE + Style.BRIGHT + "*** ABOUT 'EXCUSE ME' APPLICATION ***\n")

    print("*******************************************************************************")
    print("-- Need a quick excuse?\n")
    print("-- 'EXCUSE ME' has you covered!\n")
    print("-- Whether you're late, missing a deadline, or need a graceful exit,\n")
    print("-- our app offers a vast library of tailored excuses for every situation.\n")
    print("*******************************************************************************")
    print("\n")

    options = ["Generate new excuse", "Return to the main page"]
    menu_id = show_menu(options)

    match menu_id:
        case 1:
            show_excuse_generator_page()
        case 2:
            main()

def show_non_content_page():
    """Displays a message when there are no data and returns to the main page."""
    clear_terminal()
    print(Back.GREEN + Fore.WHITE + Style.BRIGHT + "*** EMPTY DATA ***\n")
    print("Sorry, but we did not find any data\n")
    print("After 5 seconds you will be return to the main page\n")
    time.sleep(5)
    main()

main()
