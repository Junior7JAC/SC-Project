import codecs
import os
import random

MOD = 256  # 2^8

# Function to generate a random key
def generate_key(length=16):  # Default length of 16 bytes
    key = os.urandom(length)
    return key

# Key-Scheduling Algorithm (KSA)
def KSA(key):
    key_length = len(key)
    S = list(range(MOD))
    j = 0
    for i in range(MOD):
        j = (j + S[i] + key[i % key_length]) % MOD
        S[i], S[j] = S[j], S[i]
    return S

# Pseudo-Random Generation Algorithm (PRGA)
def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % MOD
        j = (j + S[i]) % MOD
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % MOD]
        yield K

# Function to get the keystream
def get_keystream(key):
    S = KSA(key)
    return PRGA(S)

# Function to encrypt/decrypt
def encrypt_logic(key, text):
    key = [ord(c) for c in key.decode('latin-1')]  # Use latin-1 to ensure proper byte-to-char mapping
    keystream = get_keystream(key)
    res = []
    for c in text:
        val = ("%02X" % (c ^ next(keystream)))
        res.append(val)
    return ''.join(res)

# Function to encrypt
def encrypt(key, plaintext):
    plaintext = [ord(c) for c in plaintext]
    return encrypt_logic(key, plaintext)

# Function to decrypt
def decrypt(key, ciphertext):
    ciphertext = codecs.decode(ciphertext, 'hex_codec')
    res = encrypt_logic(key, ciphertext)
    return codecs.decode(res, 'hex_codec').decode('utf-8')

# Save and read functions
def save_to_file(filename, data):
    with open(filename, 'wb') as file:
        file.write(data)

def read_from_file(filename):
    with open(filename, 'rb') as file:
        return file.read().strip()

# Check for key existence and ask user
def get_key():
    if os.path.exists('key.txt'):
        with open('key.txt', 'rb') as file:
            key = file.read()
            use_existing = input("An existing key has been found. Do you want to use the existing key? (yes/no): ").strip().lower()
            if use_existing == 'yes':
                return key
            else:
                print("Generating a new key...")
                new_key = generate_key()
                save_to_file('key.txt', new_key)
                return new_key
    else:
        print("No existing key found. Generating a new key...")
        new_key = generate_key()
        save_to_file('key.txt', new_key)
        return new_key

# Main function
def main():
    key = get_key()  # Get or generate a new key

    while True:
        print("\n1. Encrypt a message")
        print("2. Decrypt a message")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            plaintext = input("Please enter the plaintext: ")
            encrypted = encrypt(key, plaintext)
            save_to_file('input_text.txt', plaintext.encode())
            save_to_file('encrypted_text.txt', encrypted.encode())
            print("Encrypted output:", encrypted)

        elif choice == '2':
            ciphertext = input("Enter encrypted hex: ")
            decrypted = decrypt(key, ciphertext)
            save_to_file('encrypted_text.txt', ciphertext.encode())
            save_to_file('decrypted_text.txt', decrypted.encode())
            print("Decrypted output:", decrypted)

        elif choice == '3':
            print("Exiting...")
            break

        else:
            print("Invalid option. Please choose a valid number (1, 2, or 3).")

if __name__ == '__main__':
    main()
