#!/usr/bin/env python3

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

# Test with the message
encrypted_message = "Eztjrhfnokdjrd,fdobiqhhohtflz."

# Try key "HILL"
result = vigenere_decrypt(encrypted_message, "HILL")
print(f"HILL: {result}")

# Try key "HOUSE"  
result = vigenere_decrypt(encrypted_message, "HOUSE")
print(f"HOUSE: {result}")

# Try key "HAUNTED"
result = vigenere_decrypt(encrypted_message, "HAUNTED")
print(f"HAUNTED: {result}")
