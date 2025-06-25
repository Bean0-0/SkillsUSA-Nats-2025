#!/usr/bin/env python3

def decrypt_with_key(encrypted, key):
    result = ""
    key = key.upper()
    key_index = 0
    
    for char in encrypted:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            
            if char.isupper():
                result += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                result += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            
            key_index += 1
        else:
            result += char
    
    return result

encrypted_message = "Eztjrhfnokdjrd,fdobiqhhohtflz."

# Try multiple keys
keys = ["HILL", "HOUSE", "HAUNTED", "GHOST", "HORROR", "VINCENT", "PRICE", "SCARY"]

print("Trying different Vigenère keys:")
print("=" * 40)

for key in keys:
    result = decrypt_with_key(encrypted_message, key)
    print(f"{key:8}: {result}")

print("\n" + "=" * 40)
print("Let's also try Caesar cipher (single character shift):")

def caesar_decrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            if char.isupper():
                result += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                result += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
        else:
            result += char
    return result

# Try Caesar shifts that might be meaningful
for shift in [8, 9, 12, 13, 16, 19, 20]:  # H, I, L, M, P, S, T
    result = caesar_decrypt(encrypted_message, shift)
    print(f"Shift {shift:2} ({chr(shift + ord('A'))}): {result}")
