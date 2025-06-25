#!/usr/bin/env python3

def atbash_decrypt(text):
    """Atbash cipher: A=Z, B=Y, C=X, etc."""
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

def simple_substitution(text, shift=13):
    """ROT13 or other simple rotation"""
    result = ""
    for char in text:
        if char.isalpha():
            if char.isupper():
                result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                result += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        else:
            result += char
    return result

def reverse_alphabet_map(text):
    """Try mapping where the alphabet is reversed"""
    normal = "abcdefghijklmnopqrstuvwxyz"
    reversed_alpha = "zyxwvutsrqponmlkjihgfedcba"
    
    result = ""
    for char in text:
        if char.isalpha():
            if char.islower():
                idx = normal.index(char)
                result += reversed_alpha[idx]
            else:
                idx = normal.upper().index(char)
                result += reversed_alpha[idx].upper()
        else:
            result += char
    return result

encrypted_message = "Eztjrhfnokdjrd,fdobiqhhohtflz."

print("Trying different cipher types:")
print("=" * 50)
print(f"Original: {encrypted_message}")
print()

# Atbash
atbash_result = atbash_decrypt(encrypted_message)
print(f"Atbash: {atbash_result}")

# ROT13
rot13_result = simple_substitution(encrypted_message, 13)
print(f"ROT13: {rot13_result}")

# Reverse alphabet
reverse_result = reverse_alphabet_map(encrypted_message)
print(f"Reverse alphabet: {reverse_result}")

# Let's also manually check what ROT13 gives us:
# E -> R, z -> m, t -> g, j -> w, r -> e, h -> u, f -> s, n -> a, o -> b, k -> x, d -> q, j -> w, r -> e, d -> q
rot13_manual = ""
for char in encrypted_message:
    if char.isalpha():
        if char.isupper():
            rot13_manual += chr((ord(char) - ord('A') + 13) % 26 + ord('A'))
        else:
            rot13_manual += chr((ord(char) - ord('a') + 13) % 26 + ord('a'))
    else:
        rot13_manual += char

print(f"ROT13 manual: {rot13_manual}")

# Let's try a few specific rotations that might be meaningful
print("\nOther rotations:")
for i in [1, 7, 8, 11, 12, 15, 19, 25]:
    rot_result = simple_substitution(encrypted_message, i)
    print(f"ROT{i:2}: {rot_result}")
    
# Also try negative rotations (backwards)
print("\nBackward rotations:")
for i in [1, 7, 8, 11, 12, 15, 19, 25]:
    rot_result = simple_substitution(encrypted_message, -i)
    print(f"ROT-{i:2}: {rot_result}")
