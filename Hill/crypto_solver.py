#!/usr/bin/env python3

def caesar_cipher_decrypt(text, shift):
    """Decrypt text using Caesar cipher with given shift"""
    result = ""
    for char in text:
        if char.isalpha():
            # Preserve case
            if char.isupper():
                result += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                result += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
        else:
            result += char
    return result

def vigenere_decrypt(text, key):
    """Decrypt text using Vigenere cipher with given key"""
    result = ""
    key = key.upper()
    key_index = 0
    
    for char in text:
        if char.isalpha():
            # Get the shift value from the key
            shift = ord(key[key_index % len(key)]) - ord('A')
            
            if char.isupper():
                result += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                result += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            
            key_index += 1
        else:
            result += char
    
    return result

def analyze_frequency(text):
    """Basic frequency analysis"""
    freq = {}
    for char in text.upper():
        if char.isalpha():
            freq[char] = freq.get(char, 0) + 1
    return freq

# The encrypted message
encrypted_message = "Eztjrhfnokdjrd,fdobiqhhohtflz."

print("Encrypted message:", encrypted_message)
print("Length:", len(encrypted_message.replace(',', '').replace('.', '')))
print("=" * 50)

# Try Caesar cipher with different shifts
print("=== Caesar Cipher Analysis ===")
for shift in range(1, 26):
    decrypted = caesar_cipher_decrypt(encrypted_message, shift)
    print(f"Shift {shift:2d}: {decrypted}")

print("=" * 50)

# Try Vigenere with various keys related to "House on Haunted Hill"
keys_to_try = [
    "HILL", 
    "HAUNTED", 
    "HOUSE", 
    "GHOST", 
    "SPIRIT", 
    "SCARY", 
    "HORROR",
    "VINCENT",  # Vincent Price was in the movie
    "PRICE",
    "SKELETON",
    "DEATH",
    "FEAR"
]

print("=== Vigenere Cipher Analysis ===")
for key in keys_to_try:
    vigenere_result = vigenere_decrypt(encrypted_message, key)
    print(f"Key '{key}': {vigenere_result}")

print("=" * 50)

# Frequency analysis
print("=== Frequency Analysis ===")
freq = analyze_frequency(encrypted_message)
for char, count in sorted(freq.items(), key=lambda x: x[1], reverse=True):
    print(f"{char}: {count}")

print("=" * 50)

# Let's also try some manual analysis - look for common patterns
print("=== Pattern Analysis ===")
print(f"Message without punctuation: {encrypted_message.replace(',', '').replace('.', '')}")
print(f"Length of clean message: {len(encrypted_message.replace(',', '').replace('.', ''))}")

# Check if it might be a simple substitution
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
clean_msg = encrypted_message.replace(',', '').replace('.', '').upper()
print(f"Clean uppercase: {clean_msg}")

# Check for repeated patterns
print("\n=== Looking for repeated patterns ===")
for i in range(2, 6):  # Check for patterns of length 2-5
    patterns = {}
    for j in range(len(clean_msg) - i + 1):
        pattern = clean_msg[j:j+i]
        if pattern.isalpha():
            patterns[pattern] = patterns.get(pattern, 0) + 1
    
    repeated = {k: v for k, v in patterns.items() if v > 1}
    if repeated:
        print(f"Length {i} patterns: {repeated}")
