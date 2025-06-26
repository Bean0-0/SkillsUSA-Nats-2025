from random import randint, seed
seed(10)
randoms = [randint(1, 100) for _ in range(624)]
class EmptyError(Exception):
    pass

def encrypt(plaintext, key):
    ct = []
    try:
        if key=='':
            raise EmptyError
        key=int(key)

    except ValueError:
        return "Error: Key an integer less than 256"
    except EmptyError:
        return "Enter a key as an integer less than 256"

    try:
        for n,i in enumerate(plaintext):
            ct.append(ord(i) + randoms[n] + key)
        return bytes(ct).hex()
    except ValueError:
        return "Error: Enter a smaller integer for the key"