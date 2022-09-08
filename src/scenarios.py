import time
import os
import hashlib
import getpass
import security

APP_DIR = os.path.join(os.getenv("HOME"), "passy")
VAULT_FILE = os.path.join(APP_DIR, "main.vault")


def first_run_check(action_func):
    def wrapper():
        if is_first_setup():
            make_first_setup()
        action_func()

    return wrapper


@first_run_check
def get_password():
    inputed_master_password = getpass.getpass("Masterpassword is required: ")
    if master_password_correct(inputed_master_password):
        with open(VAULT_FILE, "r") as f:
            encrypted_line = f.readline()
            decrypted_lines = security.decrypt(
                encrypted_line, inputed_master_password
            ).split("\n")
        all_keys = decrypted_lines[1::]  # first item is master password hash
        all_vault = [
            os.path.join(APP_DIR, i) for i in os.listdir(APP_DIR) if "main" not in i
        ]
        all_data = []
        for key in all_keys:
            for vault_path in all_vault:
                vault_value = unlock_vault(vault_path, key)
                if vault_value:
                    all_data.append(vault_value)
        print("What pass do u need?")
        for i, app in enumerate(all_data):
            print(f"{i+1} - {app[0]}")
        chosen_app = int(input("Chose app:"))
        print(
            f"Login: {all_data[chosen_app-1][1]}\nPassword: {all_data[chosen_app-1][2]}"
        )
        if len(all_data[chosen_app - 1]) == 4:
            print(f"Note: {all_data[chosen_app-1][3]}")


@first_run_check
def add_password():
    application_name = input("For what site or application: ")
    username = input("Username: ")
    password = get_input_password()
    note = input("Note: ")
    text_for_key = f"{application_name}\n{username}\n{password}\n{note}\n{time.time()}"
    key = get_hash(text_for_key)
    add_key_to_vault(key)
    text_for_save = f"{application_name}\n{username}\n{password}\n{note}"
    save_text_in_vault(text_for_save, key)


def is_first_setup():
    if os.path.exists(APP_DIR):
        if os.path.isfile(VAULT_FILE):
            return False
    return True


def make_first_setup():
    if not os.path.exists(APP_DIR):
        os.mkdir(APP_DIR)
    print(f"All your password will be in '{APP_DIR}'")
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
        print("Masterpassword is correct!")
        return True
    else:
        print("Masterpassword is wrong!")
        return False


def get_input_password():
    user_password = input_password_verify("Password: ", "Rewrite same password: ")
    if user_password:
        return user_password
    else:
        return "[TODO] Password generation"


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
    with open(
        os.path.join(APP_DIR, security.generate_random_light_string(5) + ".vault"), "w"
    ) as f:
        f.write(security.encrypt(text, key))


def unlock_vault(path, key):
    with open(path, "r") as f:
        encrypted_line = f.readline()
        decrypted_lines = security.decrypt(encrypted_line, key).split("\n")
    if len(decrypted_lines) >= 3 and len(decrypted_lines) <= 4:
        return decrypted_lines
    return False
