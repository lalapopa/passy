import random
import os
import sys
import string


def generate_random_string(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(characters) for i in range(length))
    return password


def generate():
    words_amount = random.randint(6, 16)
    password = ""
    max_length = 32
    for i in range(words_amount):
        taken_word = get_random_words()
        password += make_manipulation(taken_word)
        password += "_"
    if len(password) > max_length:
        password = password[0:max_length]
    if is_correct_password(password):
        return password
    else:
        return generate()


def get_random_words():
    with open(resource_path("words_alpha.txt"), "r") as f:
        words = f.readlines()
    return words[random.randint(0, len(words) - 1)].strip()


def make_manipulation(word):
    word_len = len(word)
    crash_symbol_amount = random.randint(1, 3)
    word = list(word)
    for i in range(crash_symbol_amount):
        word[random.randint(0, word_len - 1)] = generate_random_string(1)
    return "".join(word)


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def is_correct_password(password):
    if "\\" not in password:
        return True
    else:
        return False


def main():
    while True:
        print(generate())


if __name__ == "__main__":
    main()
