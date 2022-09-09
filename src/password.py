import random
import string


def generate_random_string(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(characters) for i in range(length))
    return password


def generate():
    words_amount = random.randint(6, 16)
    password = ""
    for i in range(words_amount):
        taken_word = get_random_words()
        password += make_manipulation(taken_word)
        password += "_"
    if "\\" not in password:
        return password
    else:
        generate()


def get_random_words():
    with open("/home/lalapopa/Lab/python/codes/passy/words_alpha.txt", "r") as f:
        words = f.readlines()
    return words[random.randint(0, len(words) - 1)].strip()


def make_manipulation(word):
    word_len = len(word)
    crash_symbol_amount = random.randint(1, 3)
    word = list(word)
    for i in range(crash_symbol_amount):
        word[random.randint(0, word_len - 1)] = generate_random_string(1)
    return "".join(word)


def main():
    print(generate_password())


if __name__ == "__main__":
    main()
