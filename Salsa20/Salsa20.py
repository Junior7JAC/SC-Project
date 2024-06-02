import os
import random

# Constants
ROUNDS = 20
KEY_SIZE = 32  # Salsa20 uses a 256-bit key

# Rotating function to rotate bits to the left
def rotl(value, shift):
    return ((value << shift) & 0xffffffff) | (value >> (32 - shift))

# Quarter round function 
def qr(a, b, c, d):
    a = (a + b) & 0xffffffff; d ^= a; d = rotl(d, 16)
    c = (c + d) & 0xffffffff; b ^= c; b = rotl(b, 12)
    a = (a + b) & 0xffffffff; d ^= a; d = rotl(d, 8)
    c = (c + d) & 0xffffffff; b ^= c; b = rotl(b, 7)
    return a, b, c, d

# The Salsa20 transformation function
def salsa20_block(key, nonce, counter):
    const = [1634760805, 857760878, 2036477234, 1797285236]
    key_words = [int.from_bytes(key[i:i+4], 'little') for i in range(0, KEY_SIZE, 4)]
    nonce_words = [int.from_bytes(nonce[i:i+4], 'little') for i in range(0, 8, 4)]
    counter_words = [int.from_bytes(counter[i:i+4], 'little') for i in range(0, 8, 4)]
    
    x = const[:1] + key_words[:4] + nonce_words + counter_words + key_words[4:] + const[1:]
    orig_x = x[:]
    
    for _ in range(ROUNDS//2):
        # Column rounds
        x[0], x[4], x[8], x[12] = qr(x[0], x[4], x[8], x[12])
        x[1], x[5], x[9], x[13] = qr(x[1], x[5], x[9], x[13])
        x[2], x[6], x[10], x[14] = qr(x[2], x[6], x[10], x[14])
        x[3], x[7], x[11], x[15] = qr(x[3], x[7], x[11], x[15])
        # Diagonal rounds
        x[0], x[5], x[10], x[15] = qr(x[0], x[5], x[10], x[15])
        x[1], x[6], x[11], x[12] = qr(x[1], x[6], x[11], x[12])
        x[2], x[7], x[8], x[13] = qr(x[2], x[7], x[8], x[13])
        x[3], x[4], x[9], x[14] = qr(x[3], x[4], x[9], x[14])
    
    return bytes((orig_x[i] + x[i]) & 0xff for i in range(16))

# Function to generate a new key and save it
def generate_and_save_key(filename):
    key = bytes(random.getrandbits(8) for _ in range(KEY_SIZE))
    with open(filename, 'w') as f:
        f.write(key.hex())

# Save input to file
def save_input(filename, input_data):
    with open(filename, 'w') as f:
        f.write(input_data)

# Save output to file
def save_output(filename, output_data):
    with open(filename, 'w') as f:
        f.write(output_data)

# Helper function to read key from file
def read_key_from_file(filename):
    with open(filename, 'r') as f:
        key_hex = f.read().strip()
        return bytes.fromhex(key_hex)

def main():
    filename = 'key.txt'
    # Ask user if a new key is needed
    if input("Generate a new key? (yes/no) ").lower() == 'yes':
        generate_and_save_key(filename)
    
    try:
        key = read_key_from_file(filename)
    except FileNotFoundError:
        print(f"Key file {filename} not found. Generating a new key.")
        generate_and_save_key(filename)
        key = read_key_from_file(filename)
    except ValueError:
        print("Key file is not in the correct hex format. Generating a new key.")
        generate_and_save_key(filename)
        key = read_key_from_file(filename)

    # Constants for nonce and counter
    nonce = bytes.fromhex('0102030405060708')
    counter = bytes.fromhex('0102030405060708')

    while True:
        print("\n1. Encrypt message")
        print("2. Decrypt message")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            plaintext = input("Please enter the plaintext: ")
            save_input('input.txt', plaintext)  # Save plaintext to file
            keystream = salsa20_block(key, nonce, counter)
            encrypted = bytes(a ^ b for a, b in zip(plaintext.encode(), keystream))
            encrypted_hex = encrypted.hex()
            save_output('output.txt', encrypted_hex)  # Save encrypted output to file
            print("Encrypted output:", encrypted_hex)

        elif choice == '2':
            encrypted_hex = input("Enter encrypted output (hex): ")
            save_input('decrypted_input.txt', encrypted_hex)  # Save encrypted hex to file
            encrypted = bytes.fromhex(encrypted_hex)
            keystream = salsa20_block(key, nonce, counter)
            decrypted = bytes(a ^ b for a, b in zip(encrypted, keystream))
            decrypted_text = decrypted.decode()
            save_output('decrypted_output.txt', decrypted_text)  # Save decrypted output to file
            print("Decrypted output:", decrypted_text)

        elif choice == '3':
            break
        else:
            print("Invalid option. Please choose a valid number (1, 2, or 3).")

if __name__ == "__main__":
    main()
