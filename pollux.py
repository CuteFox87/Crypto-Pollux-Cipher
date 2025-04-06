# pollux cipher
import re
import string
import random
import itertools
from tqdm import tqdm

MORSE_CODE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
}

def parse_key(key):
    if not re.fullmatch(r'[.\-x]{10}', key):
        raise ValueError("Key must be 10 characters long and contain only '.' and '-'")
    
    key_map = {'.': [], '-': [], 'x': []}
    for digit, symbol in enumerate(key):
        key_map[symbol].append(str(digit))
    return key_map

def text2morse(text):
    text = text.translate(str.maketrans('', '', string.punctuation))
    return 'x'.join([''.join('x'+MORSE_CODE[c] for c in word) for word in text.upper().split()])[1:]

def morse2text(morse_text):
    # Split Morse symbols by 'x' which we used as separator
    morse_letters = morse_text.split('x')

    decoded_text = ''
    current_word = ''

    for symbol in morse_letters:
        if symbol == '':  # double 'x' indicates a space between words
            if current_word:
                decoded_text += current_word + ' '
                current_word = ''
        else:
            for letter, code in MORSE_CODE.items():
                if code == symbol:
                    current_word += letter
                    break

    if current_word:
        decoded_text += current_word

    return decoded_text.strip()

def pollux_encrypt(plaintext, key, method='rand'):
    if not isinstance(plaintext, str) or not isinstance(key, str):
        raise TypeError("Plaintext and key must be strings")
    if method not in ['rand', 'seq']:
        raise ValueError("Method must be 'rand' or 'seq'")
    
    morse_text = text2morse(plaintext)
    print("Morse Text:", morse_text)
    key_map = parse_key(key)
    print("Key Map:", key_map)
    encrypted_text = []

    if re.fullmatch(r'[.\-x]', morse_text):
        raise ValueError("Morse text must contain only '.', '-', 'x' characters")

    for char in morse_text:
        if char in key_map:
            indices = key_map[char]
            index = random.choice(indices)
            encrypted_text.append(index)

    plaintext = plaintext.upper()
    plaintext = plaintext.translate(str.maketrans('', '', string.punctuation))
    process = ""
    for i in range(len(plaintext)):
        if plaintext[i] != ' ':
            process += plaintext[i]
            process += len(MORSE_CODE[plaintext[i]]) * ' '
        else:
            process += ' '
    process += '\n' + morse_text + '\n'
    process += ''.join(encrypted_text) + '\n'
    
    return ''.join(encrypted_text), process, key_map

def pollux_decrypt(ciphertext, key):
    if not isinstance(ciphertext, str) or not isinstance(key, str):
        raise TypeError("Ciphertext and key must be strings")
    
    key_map = parse_key(key)
    decrypted_text = []
    for char in ciphertext:
        for symbol, indices in key_map.items():
            if char in indices:
                decrypted_text.append(symbol)
                break
    morse_code =  ''.join(decrypted_text)
    return morse2text(morse_code)

if __name__ == "__main__":
    plaintext = "When one teaches, two learn."
    key = "x.--.x.-x."
    print("Plaintext:", plaintext)
    print("Key:", key)

    encrypt, process, key_map = pollux_encrypt(plaintext, key)
    print("Encrypted:", encrypt)
    print(process)

    decrypt = pollux_decrypt(encrypt, key)
    print("Decrypted:", decrypt)

    
