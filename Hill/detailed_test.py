#!/usr/bin/env python3

def vigenere_decrypt_detailed(text, key):
    """Vigenere decrypt with detailed output"""
    result = ""
    key = key.upper()
    key_index = 0
    
    print(f"Decrypting '{text}' with key '{key}':")
    
    for i, char in enumerate(text):
        if char.isalpha():
            key_char = key[key_index % len(key)]
            shift = ord(key_char) - ord('A')
            
            if char.isupper():
                decrypted = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                decrypted = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            
            print(f"  {char} - {key_char}({shift}) = {decrypted}")
            result += decrypted
            key_index += 1
        else:
            result += char
            print(f"  {char} = {char}")
    
    print(f"Result: {result}")
    return result

# Test short keys
encrypted = "Eztjrhfnokdjrd,fdobiqhhohtflz."

print("Trying short keys:")
print("=" * 40)

# Try very short keys
short_keys = ["H", "I", "L", "HI", "IL", "HL"]
for key in short_keys:
    print()
    vigenere_decrypt_detailed(encrypted, key)
    print("-" * 30)
