from base64 import b64encode, b64decode
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import random
import string


def generate_random_string(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(characters) for i in range(length))
    return password


def generate_random_light_string(length):
    characters = string.ascii_letters + string.digits
    password = "".join(random.choice(characters) for i in range(length))
    return password


def encrypt(plain_text, password):
    # generate a random salt
    salt = get_random_bytes(AES.block_size)

    # use the Scrypt KDF to get a private key from the password
    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32
    )

    # create cipher config
    cipher_config = AES.new(private_key, AES.MODE_GCM)

    # return a dictionary with the encrypted text
    cipher_text, tag = cipher_config.encrypt_and_digest(bytes(plain_text, "utf-8"))
    return (
        b64encode(salt).decode("utf-8")
        + b64encode(cipher_config.nonce).decode("utf-8")
        + b64encode(tag).decode("utf-8")
        + b64encode(cipher_text).decode("utf-8")
    )


def decrypt(enc_string, password):
    # decode the dictionary entries from base64
    salt = b64decode(enc_string[0:24])
    nonce = b64decode(enc_string[24:48])
    tag = b64decode(enc_string[48:72])
    cipher_text = b64decode(enc_string[72:])

    # generate the private key from the password and salt
    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32
    )

    # create the cipher config
    cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)

    # decrypt the cipher text
    try:
        decrypted = cipher.decrypt_and_verify(cipher_text, tag)
    except ValueError:
        decrypted = generate_random_string(len(cipher_text)).encode("utf-8")
    return bytes.decode(decrypted)


def main():
    password = input("Password: ")

    # First let us encrypt secret message
    encrypted = encrypt(
        "SECRET_TEXT",
        password,
    )
    print(encrypted)
    check_pass = input("For unlock: ")
    # Let us decrypt using our original password
    decrypted = decrypt(encrypted, check_pass)
    print(decrypted)


if __name__ == "__main__":
    main()
