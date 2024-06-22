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
