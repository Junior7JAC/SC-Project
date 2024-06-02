import random  # For generating random numbers
import sympy  # For generating prime numbers

# Function to generate a key pair
def generate_keypair():
    p = sympy.randprime(10000, 99999)
    q = sympy.randprime(10000, 99999)
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = random.randrange(1, phi)
    while sympy.gcd(e, phi) != 1:
        e = random.randrange(1, phi)
    
    d = sympy.mod_inverse(e, phi)
    
    return ((e, n), (d, n))

# Function to save the key to a file
def save_key(filename, key):
    with open(filename, 'w') as f:
        key_str = ','.join(map(str, key))
        f.write(key_str)

# Function to load the key from a file
def load_key(filename):
    with open(filename, 'r') as f:
        key_str = f.read().strip()
        key = tuple(map(int, key_str.split(',')))
    return key

# Function to save a message to a file
def save_message(filename, message, mode='w'):
    with open(filename, mode) as f:
        f.write(message + '\n')

def load_message(filename):
    with open(filename, 'r') as f:
        return f.read().strip()

# Function to encrypt a message
def encrypt(public_key, plaintext):
    e, n = public_key
    ciphertext = [pow(ord(char), e, n) for char in plaintext]  # Convert each character to a number
    return ' '.join(map(str, ciphertext))

# Function to decrypt a message
def decrypt(private_key, ciphertext):
    d, n = private_key
    plaintext = [chr(pow(char, d, n)) for char in map(int, ciphertext.split())]  # Convert each number to a character
    return ''.join(plaintext)

# Function to initialize or load keys
def initialize_keys():
    choice = input("Do you want to generate new keys? (yes/no): ")
    if choice.lower() == 'yes':
        public_key, private_key = generate_keypair()
        save_key('public_key.txt', public_key)
        save_key('private_key.txt', private_key)
        print("New keys generated and saved.")
    else:
        try:
            public_key = load_key('public_key.txt')
            private_key = load_key('private_key.txt')
        except FileNotFoundError:
            print("No existing keys found, generating new ones.")
            public_key, private_key = generate_keypair()
            save_key('public_key.txt', public_key)
            save_key('private_key.txt', private_key)
    return public_key, private_key

# Initialize or load keys
public_key, private_key = initialize_keys()

# Main loop
while True:
    print("\n1. Encrypt message")
    print("2. Decrypt message")
    print("3. Exit")
    choice = input("Choose an option: ")

    if choice == '1':
        message = input("Enter the message to encrypt: ")
        save_message("input_messages.txt", message, 'a')  # Append each message to the input_messages.txt file
        encrypted_message = encrypt(public_key, message)
        save_message("encrypted_message.txt", encrypted_message)
        print("Encrypted message saved in 'encrypted_message.txt'")
    elif choice == '2':
        encrypted_message = input("Enter the encrypted message for decryption: ")
        decrypted_message = decrypt(private_key, encrypted_message)
        save_message("decrypted_message.txt", decrypted_message)
        print("Decrypted message saved in 'decrypted_message.txt'")
    elif choice == '3':
        print("Program ended.")
        break
    else:
        print("Invalid option. Please choose again.")
