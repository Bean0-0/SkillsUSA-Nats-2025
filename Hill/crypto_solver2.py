#!/usr/bin/env python3

def atbash_cipher(text):
    """Apply Atbash cipher (A=Z, B=Y, etc.)"""
    result = ""
    for char in text:
        if char.isalpha():
            if char.isupper():
                result += chr(ord('Z') - (ord(char) - ord('A')))
            else:
                result += chr(ord('z') - (ord(char) - ord('a')))
        else:
            result += char
    return result

def reverse_text(text):
    """Simple reverse of the text"""
    return text[::-1]

def keyboard_shift(text, shift_type='qwerty'):
    """Try keyboard shift patterns"""
    if shift_type == 'qwerty':
        # QWERTY keyboard layout shift
        qwerty_map = {
            'q': 'w', 'w': 'e', 'e': 'r', 'r': 't', 't': 'y', 'y': 'u', 'u': 'i', 'i': 'o', 'o': 'p',
            'a': 's', 's': 'd', 'd': 'f', 'f': 'g', 'g': 'h', 'h': 'j', 'j': 'k', 'k': 'l',
            'z': 'x', 'x': 'c', 'c': 'v', 'v': 'b', 'b': 'n', 'n': 'm'
        }
        # Create reverse mapping
        qwerty_reverse = {v: k for k, v in qwerty_map.items()}
        
        result = ""
        for char in text.lower():
            if char in qwerty_reverse:
                result += qwerty_reverse[char]
            else:
                result += char
        return result
    return text

def rail_fence_decrypt(text, rails):
    """Decrypt rail fence cipher"""
    # Remove non-alphabetic characters for rail fence
    clean_text = ''.join(c for c in text if c.isalpha())
    
    if rails == 1:
        return clean_text
    
    # Create the rail fence pattern
    fence = [['\n' for j in range(len(clean_text))] for i in range(rails)]
    
    # Mark the places in the fence
    rail = 0
    direction = False
    for i in range(len(clean_text)):
        fence[rail][i] = '*'
        if rail == 0 or rail == rails - 1:
            direction = not direction
        rail += 1 if direction else -1
    
    # Fill the fence with the encoded text
    index = 0
    for i in range(rails):
        for j in range(len(clean_text)):
            if fence[i][j] == '*' and index < len(clean_text):
                fence[i][j] = clean_text[index]
                index += 1
    
    # Read the fence to get the original text
    result = []
    rail = 0
    direction = False
    for i in range(len(clean_text)):
        result.append(fence[rail][i])
        if rail == 0 or rail == rails - 1:
            direction = not direction
        rail += 1 if direction else -1
    
    return ''.join(result)

def simple_substitution_analysis(text):
    """Try some common simple substitutions"""
    # ROT13
    rot13_result = ""
    for char in text:
        if char.isalpha():
            if char.isupper():
                rot13_result += chr((ord(char) - ord('A') + 13) % 26 + ord('A'))
            else:
                rot13_result += chr((ord(char) - ord('a') + 13) % 26 + ord('a'))
        else:
            rot13_result += char
    
    return rot13_result

# The encrypted message
encrypted_message = "Eztjrhfnokdjrd,fdobiqhhohtflz."

print("Original message:", encrypted_message)
print()

# Try Atbash cipher
print("=== Atbash Cipher ===")
atbash_result = atbash_cipher(encrypted_message)
print(f"Atbash: {atbash_result}")

print()

# Try reverse
print("=== Reverse Text ===")
reverse_result = reverse_text(encrypted_message)
print(f"Reversed: {reverse_result}")

print()

# Try ROT13
print("=== ROT13 ===")
rot13_result = simple_substitution_analysis(encrypted_message)
print(f"ROT13: {rot13_result}")

print()

# Try keyboard shift
print("=== Keyboard Shift ===")
keyboard_result = keyboard_shift(encrypted_message)
print(f"QWERTY shift: {keyboard_result}")

print()

# Try rail fence with different rail counts
print("=== Rail Fence Cipher ===")
for rails in range(2, 6):
    rail_result = rail_fence_decrypt(encrypted_message, rails)
    print(f"Rails {rails}: {rail_result}")

print()

# Let's also try looking at it as two separate words
print("=== Split Analysis ===")
parts = encrypted_message.replace('.', '').split(',')
print(f"Part 1: {parts[0]}")
print(f"Part 2: {parts[1]}")

# Try Caesar on each part separately
print("\n--- Caesar on Part 1 ---")
for shift in range(1, 26):
    decrypted = ""
    for char in parts[0]:
        if char.isalpha():
            if char.isupper():
                decrypted += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                decrypted += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
        else:
            decrypted += char
    if 'the' in decrypted.lower() or 'and' in decrypted.lower() or 'you' in decrypted.lower():
        print(f"Shift {shift:2d}: {decrypted}")

print("\n--- Caesar on Part 2 ---")
for shift in range(1, 26):
    decrypted = ""
    for char in parts[1]:
        if char.isalpha():
            if char.isupper():
                decrypted += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                decrypted += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
        else:
            decrypted += char
    if 'the' in decrypted.lower() or 'and' in decrypted.lower() or 'you' in decrypted.lower():
        print(f"Shift {shift:2d}: {decrypted}")
