import requests
import json
import os
from colorama import Fore, Style, init
import msvcrt

init()

SERVER_URL = "http://37.114.46.139:7006"

def password_input():
    password = ""
    print(Fore.CYAN + "Password: " + Style.RESET_ALL, end='', flush=True)
    while True:
        char = msvcrt.getch()
        if char == b'\r':
            break
        elif char == b'\x08':
            if len(password) > 0:
                password = password[:-1]
                print('\b \b', end='', flush=True)
        else:
            password += char.decode('utf-8')
            print('*', end='', flush=True)
    return password

def end():
    print(Fore.MAGENTA + '''
╔═══════════════════════════╗
║     Thanks for using      ║
║      ATLEX KEYAUTH        ║
╚═══════════════════════════╝
''' + Style.RESET_ALL)
    exit()

def show_menu():
    print(Fore.MAGENTA + '''
╔═══════════════════════╗
║      Select key       ║
╠═══════════════════════╣
║  1. Testing (3 days)  ║
║  2. 1 Week            ║
║  3. 1 Month           ║
║  4. 3 Months          ║
║  5. Lifetime          ║
╚═══════════════════════╝
''' + Style.RESET_ALL)

def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def login():
    try:
        if os.path.exists('temp'):
            with open('temp', 'r') as f:
                existing_token = f.read().strip()
                
            check_response = requests.post(
                f"{SERVER_URL}/check_login",
                json={"token": existing_token}
            )
            
            if check_response.status_code == 200:
                if check_response.json()['valid']:
                    return existing_token

    except:
        pass

    print(Fore.MAGENTA + '''
╔══════════════════════════╗
║           Login          ║
╚══════════════════════════╝
''' + Style.RESET_ALL)

    try:
        username = input(Fore.CYAN + "Username: " + Style.RESET_ALL)
        password = password_input()

        credentials = {
            "username": username,
            "password": password
        }
    except KeyboardInterrupt:
        end()

    try:
        response = requests.post(
            f"{SERVER_URL}/login",
            json=credentials
        )

        if response.status_code == 200:
            token = response.json()['token']
            with open('temp', 'w') as f:
                f.write(token)
            return token
        else:
            print(Fore.RED + "\n[ERROR] Login failed. Invalid username or password." + Style.RESET_ALL)
            return None

    except requests.exceptions.ConnectionError:
        print(Fore.RED + "\n[ERROR] Server unreachable. Please make sure the server is running." + Style.RESET_ALL)
        return None

def gen(token):
    show_menu()
    try:
        choice = str(input(Fore.CYAN + "Enter choice (1-5): " + Style.RESET_ALL))
        username = str(input(Fore.CYAN + "Enter Discord ID of key owner: " + Style.RESET_ALL))
    except KeyboardInterrupt:
        end()

    data = {
        "token": token,
        "type": choice,
        "owner": username
    }

    try:
        response = requests.post(
            f"{SERVER_URL}/getkey",
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                clear_console()
                print(Fore.MAGENTA + '''
╔═════════════════════════════════════════╗
║               Key Generated             ║
╠═════════════════════════════════════════╣
║ Key: {} ║
║ Expiration: {}         ║
║ Owner: {}              ║
╚═════════════════════════════════════════╝
'''.format(result["key"], result["expiration"], result["owner"]) + Style.RESET_ALL)
            else:
                print(Fore.RED + "\n[ERROR] Request failed." + Style.RESET_ALL)
        else:
            print(Fore.RED + "\n[ERROR] Invalid token or server error." + Style.RESET_ALL)
            
    except requests.exceptions.ConnectionError:
        print(Fore.RED + "\n[ERROR] Server unreachable." + Style.RESET_ALL)

if __name__ == "__main__":
    try:
        clear_console()
        token = login()
        if token:
            while True:
                clear_console()
                gen(token)
                another = input(Fore.CYAN + "\nGenerate another key? (y/n): " + Style.RESET_ALL)
                if another.lower() != 'y':
                    break
        end()
    except KeyboardInterrupt:
        clear_console()
        end()
