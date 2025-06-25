#!/usr/bin/env python3

def manual_vigenere_decrypt():
    encrypted = "Eztjrhfnokdjrd,fdobiqhhohtflz."
    key = "HILL"
    
    result = ""
    key_index = 0
    
    print(f"Encrypted: {encrypted}")
    print(f"Key: {key}")
    print()
    
    for i, char in enumerate(encrypted):
        if char.isalpha():
            # Get current key character and its shift value
            key_char = key[key_index % len(key)]
            shift = ord(key_char) - ord('A')
            
            # Decrypt the character
            if char.isupper():
                decrypted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                decrypted_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            
            print(f"{char} (key: {key_char}, shift: {shift}) -> {decrypted_char}")
            result += decrypted_char
            key_index += 1
        else:
            result += char
            print(f"{char} -> {char} (punctuation)")
    
    print()
    print(f"Final result: {result}")
    return result

if __name__ == "__main__":
    manual_vigenere_decrypt()
