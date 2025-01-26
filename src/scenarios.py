from typing import Sequence
from dataclasses import dataclass
import time
import os
import hashlib
import getpass
import pyperclip
import security
import password


APP_DIR = os.path.join(os.getenv("HOME"), ".passy")
VAULT_FILE = os.path.join(APP_DIR, "main.vault")


def first_run_check(action_func):
    def wrapper():
        if is_first_setup():
            make_first_setup()
        action_func()

    return wrapper


@dataclass
class Vault:
    path: str
    key: str
    load: list[str]


@first_run_check
def get_password():
    inputed_master_password = getpass.getpass("Masterpassword is required: ")
    if master_password_correct(inputed_master_password):
        all_keys = get_all_keys_from_vault(inputed_master_password)
        all_vault = get_vaults_path()
        all_data = parse_vault(all_vault, all_keys)
        if all_data:
            print("What pass do u need?")
            for i, vault in enumerate(all_data):
                print(f"{i+1} - {vault.load[0]}")

            chosen_app = get_chosen_app(len(all_data))
            chosen_vault = all_data[chosen_app - 1]
            render_chosen_app(chosen_vault)
        else:
            print("No passwords in vaults. You can create one using 'passy -a'")
            return


@first_run_check
def add_password():
    application_name = input("For what site or application: ")
    username = input("Username: ")
    if application_name and username:
        password = get_input_password()
        note = input("Note: ")
        text_for_key = f"{security.generate_random_light_string(8)}{application_name}\n{username}\n{password}\n{note}\n{time.time()}"
        key = get_hash(text_for_key)
        add_key_to_vault(key)
        text_for_save = f"{application_name}\n{username}\n{password}\n{note}"
        save_text_in_vault(text_for_save, key)
    else:
        return add_password()


@first_run_check
def delete_password():
    inputed_master_password = getpass.getpass("Masterpassword is required: ")
    if master_password_correct(inputed_master_password):
        all_keys = get_all_keys_from_vault(inputed_master_password)
        all_vault = get_vaults_path()
        all_data = parse_vault(all_vault, all_keys)
        if all_data:
            print("What pass u want delete?")
            for i, app in enumerate(all_data):
                print(f"{i+1} - {app.load[0]}")
            chosen_app = get_chosen_app(len(all_data))
            chosen_vault = all_data[chosen_app - 1]
            render_deletion_app(inputed_master_password, chosen_vault)
        else:
            print("Vault empty. You can create one using `passy -a`")
            return


def is_first_setup():
    if os.path.exists(APP_DIR):
        if os.path.isfile(VAULT_FILE):
            return False
    return True


def render_chosen_app(vault):
    print(f"Login: {vault.load[1]}")
    answer = input("Can I show pass? (y/n) ").lower()
    print("\033[A                             \033[A")
    if answer == "y":
        print(f"Password: {vault.load[2]}")
    else:
        pyperclip.copy(vault.load[2])
    if len(vault.load) == 4:
        print(f"Note: {vault.load[3]}")


def render_deletion_app(master_pass, vault):
    confirmed = confirm_deletion(vault)
    if confirmed:
        os.remove(vault.path)
        with open(VAULT_FILE, "r") as f:
            encrypted_line = f.readline()
            decrypted_lines = security.decrypt(encrypted_line, master_pass).split("\n")
        decrypted_lines.remove(vault.key)
        new_secret = "\n".join(decrypted_lines)
        with open(VAULT_FILE, "w") as f:
            f.write(security.encrypt(new_secret, master_pass))
            print(f"Key for {vault.load[0]} was deleted.")
    else:
        print("You typed bullshit, I wont delete that")


def get_chosen_app(max_number):
    if max_number == 1:
        return 1
    chosen_app = False
    while not chosen_app:
        try:
            chosen_app = int(input(f"Choose app [1 - {max_number}]: "))
        except ValueError:
            print("\033[A                             \033[A")
            chosen_app = False
        if chosen_app > max_number or chosen_app < 1:
            chosen_app = False
    return chosen_app


def make_first_setup():
    if not os.path.exists(APP_DIR):
        os.mkdir(APP_DIR)
    print(f"All passwords will be stored in '{APP_DIR}'")
    master_password = input_password_verify(
        "Input new master password: ", "Rewrite it again: "
    )
    master_password_hash = get_hash(master_password)
    if not os.path.isfile(VAULT_FILE):
        with open(VAULT_FILE, "w") as f:
            f.write(security.encrypt(master_password_hash, master_password))


def input_password_verify(first_text, second_text):
    first_input = getpass.getpass(first_text)
    second_input = getpass.getpass(second_text)
    if first_input == second_input:
        return first_input
    else:
        print("Password don't match. Try again.")
        return input_password_verify(first_text, second_text)


def get_hash(text):
    return hashlib.sha512(text.encode("utf-8")).hexdigest()


def master_password_correct(password):
    with open(VAULT_FILE, "r") as f:
        encrypted_line = f.readline()
        decrypted_lines = security.decrypt(encrypted_line, password).split("\n")
    if get_hash(password) == decrypted_lines[0]:
        print("\033[A                             \033[A")  # Clean current line
        return True
    else:
        print("\033[A                             \033[A")
        print("Masterpassword is wrong!")
        return False


def get_input_password():
    user_password = input_password_verify(
        "Password (default random): ", "Rewrite same password: "
    )
    if user_password:
        return user_password
    else:
        return password.generate()


def add_key_to_vault(key):
    inputed_master_password = getpass.getpass("Masterpassword is required: ")
    if master_password_correct(inputed_master_password):
        with open(VAULT_FILE, "r") as f:
            encrypted_line = f.readline()
            decrypted_lines = security.decrypt(
                encrypted_line, inputed_master_password
            ).split("\n")
        decrypted_lines.append(key)
        new_secret = "\n".join(decrypted_lines)
        with open(VAULT_FILE, "w") as f:
            f.write(security.encrypt(new_secret, inputed_master_password))
            print(f"Key written in main.vault")


def save_text_in_vault(text, key):
    all_files = os.listdir(APP_DIR)
    generated_vault_name = security.generate_random_light_string(5) + ".vault"
    while generated_vault_name in all_files:
        generated_vault_name = security.generate_random_light_string(5) + ".vault"

    with open(os.path.join(APP_DIR, generated_vault_name), "w") as f:
        f.write(security.encrypt(text, key))


def unlock_vault(path, key):
    with open(path, "r") as f:
        encrypted_line = f.readline()
        decrypted_lines = security.decrypt(encrypted_line, key).split("\n")
    if len(decrypted_lines) >= 3 and len(decrypted_lines) <= 4:
        return decrypted_lines
    return False


def get_all_keys_from_vault(password):
    with open(VAULT_FILE, "r") as f:
        encrypted_line = f.readline()
        decrypted_lines = security.decrypt(encrypted_line, password).split("\n")
    return decrypted_lines[1::]  # first item is master password hash


def get_vaults_path():
    vault_list = []
    for file_name in os.listdir(APP_DIR):
        if ("main" not in file_name) and (".vault" in file_name):
            vault_list.append(os.path.join(APP_DIR, file_name))
    return vault_list


def parse_vault(vault_paths, keys) -> Sequence[Vault]:
    all_data = []
    for key in keys:
        for vault_path in vault_paths:
            vault_value = unlock_vault(vault_path, key)
            if vault_value:
                vault = Vault(path=vault_path, key=key, load=vault_value)
                all_data.append(vault)
                vault_paths.remove(vault_path)
                break
    return all_data


def confirm_deletion(vault):
    verify_login_string = input(
        f"For deletion type login '{vault.load[1]}' for {vault.load[0]}: "
    )
    if verify_login_string == vault.load[1]:
        return True
    else:
        return False
