# lab 4 - rsa
'''
(i) setting - the alphabet has 27 characters. the blank and the 26 letters of the alphabet
(ii) public key and private key randomly generated in a required interval
(iii) encrypt a given plaintext using the public key. need plaintext validation
(iv) decrypt a given ciphertext, using the private key. need ciphertext validation
'''
import math
import random

# defining the constant alphabet size and variable
alphabet_size = 27
# alphabet = '_abcdefghijklmnopqrstuvwxyz'
# underscore instead of space for index 0
alphabet = ['_'] + [chr(i) for i in range(ord('a'), ord('z') + 1)]

k = 2  # number of symbols in a block of plaintext
l = 3  # number of symbols in a block of ciphertext

# gcd euclidean algorithm
def gcd(a, b):
    while b != 0:
        r = b
        b = a % b
        a = r
    return a

# checking if a number is prime
def is_prime(n):
    if n <= 1 or (n % 2 == 0 and n != 2):
        return False  # 0 and 1 are not prime, as well as even numbers (apart from 2)
    for i in range(2, math.isqrt(n) + 1):
        if n % i == 0:
            return False  # if a divisor is found, the number is composite
    return True  # if no divisors are found, the number is prime

# generating a prime number in a given interval
def generate_random_prime_within_interval(minimum, maximum):
    prime = -1  # initializing to a non-valid prime number
    while not is_prime(prime):
        prime = random.randint(minimum, maximum)
    return prime


# computing a^(-1) mod n
def modular_multiplicative_inverse(a, n):
    # used for computing d
    # (compute = calculate)
    a = a % n
    for x in range(1, n):
        if (a * x) % n == 1:
            return x
    return -1

# finding an encryption exponent given euler's totient function (phi_n)
def find_e(phi_n):
    for e in range(2, phi_n):  # this way we get the lowest possible value of e
        if gcd(e, phi_n) == 1:
            return e
    return -1  # not found an encryption exponent. this usually shouldn't happen

# plaintext validation
def is_valid_plaintext(text, alphabet):
    # looking for characters / symbols not found in the alphabet and empty inputs
    return all(symbol in alphabet for symbol in text) and text.strip() != ''

# ciphertext validation
def is_valid_ciphertext(text, alphabet):
    # looking for characters / symbols not found in the alphabet and empty inputs
    return all(symbol in alphabet or symbol == '_' for symbol in text) and text.strip() != ''

# RSA encrypt function
def encrypt_text(plaintext, alphabet, k, l, n, e):
    # splitting the plaintext into k-sized blocks
        # if the last block is shorter than k characters, it's padded with underscores to make it the required size
        # ljust(k, '_') function - used for left-justifying the block and filling any remaining space with underscores
    blocks = [plaintext[i:i + k].ljust(k, '_') for i in range(0, len(plaintext), k)]
    print("splitting the text:", blocks)

    # converting each block into its numerical equivalent using positional notation
        # basically a base-10 system representation
        # enumerate(block) - used to iterate the characters in each "block", along with their indices
        # raising 27 to the power of the position of the character within the block
        # computing each character's contribution (numerical value)
        # summing it all up
    numbers = [sum(alphabet.index(symbol) * (len(alphabet) ** (k - index - 1)) for index, symbol in enumerate(block))
               for block in blocks]
    print("writing the numerical equivalents:", numbers)

    # performing modular exponentiation for encryption
    encrypted_numbers = [pow(number, e, n) for number in numbers]
    print("writing the encrypted numbers:", encrypted_numbers)

    # converting encrypted numbers back to characters, thus forming encrypted blocks
    encrypted_blocks = []  # initializing an empty list to store the final encrypted character blocks
    for number in encrypted_numbers:
        block = ''  # initializing an empty string to construct the character block
        for i in range(l):
            current_digit = number % len(alphabet)
            if 0 <= current_digit < len(alphabet):  # checking if the current digit is within the valid range
                block = alphabet[current_digit] + block
            else:
                print("error: invalid digit during encryption")
                return
            number //= len(alphabet)
        # after constructing the encrypted block, appending it to the list
        # if the block is shorter than the specified length l, it's left-justified and padded with the first character of the alphabet
        encrypted_blocks.append(block.ljust(l, alphabet[0]))

    print("writing the encrypted equivalents:", encrypted_blocks)

    # joining encrypted blocks into final encrypted text
    encrypted_text = ''.join(encrypted_blocks)
    return encrypted_text


# RSA decrypt function
def decrypt_text(ciphertext, alphabet, k, l, n, d):
    # splitting the ciphertext into l-sized blocks
        # in range: generating a sequence of indices for each block of length l in the ciphertext
        # extracting a block (substring) from the ciphertext, so we can grab the portion we need corresponding to a block
    blocks = [ciphertext[i:i + l] for i in range(0, len(ciphertext), l)]
    print("splitting the text:", blocks)

    # converting each block into its numerical equivalent using positional notation
    numbers = [sum(alphabet.index(symbol) * (len(alphabet) ** (l - index - 1)) for index, symbol in enumerate(block))
               for block in blocks]
    print("writing the numerical equivalents:", numbers)

    # performing modular exponentiation for decryption
    decrypted_numbers = [pow(number, d, n) for number in numbers]
    print("writing the decrypted numbers:", decrypted_numbers)

    # converting decrypted numbers back to characters, thus forming decrypted blocks
    decrypted_blocks = []  # initializing an empty list to store the final decrypted character blocks
    for number in decrypted_numbers:
        block = ''  # initializing an empty string to construct the character block
        for i in range(k):
            current_digit = number % len(alphabet)
            if 0 <= current_digit < len(alphabet):  # checking if the current digit is within the valid range
                block = alphabet[current_digit] + block
            else:
                print("error: invalid digit during decryption")
                return
            number //= len(alphabet)
        # after constructing the decrypted block, appending it to the list
        decrypted_blocks.append(block)

    print("writing the decrypted equivalents:", decrypted_blocks)

    # joining decrypted blocks into the final decrypted text
    decrypted_text = ''.join(decrypted_blocks)
    return decrypted_text


# main
if __name__ == '__main__':
    print("in order to generate a public key Ke we need to assign n a value.")
    minimum = int(input("input the inferior limit of the interval: "))
    maximum = int(input("input the superior limit of the interval: "))
    print("n is to be generated in the interval [", minimum, ",", maximum, "]")
    print("generating values for two prime numbers...")

    # generator: two random prime numbers the specified interval
    while True:
        p = generate_random_prime_within_interval(1, 10000)
        q = generate_random_prime_within_interval(1, 10000)
        n = p * q
        if minimum <= n <= maximum and p != q:
            # making sure that the two prime numbers' product is in the given range
            # making sure that the two prime numbers are not equal
            break

    print("p =", p, ", q =", q)
    n = p * q
    print("n =", n, "(p*q)")
    print("computing phi_n...")
    phi_n = (p - 1) * (q - 1)
    print("phi_n =", phi_n, "[(p-1)*(q-1)]")
    print("finding the lowest possible value for the encryption exponent e...")

    # finding the encryption exponent (e)
    if find_e(phi_n) != -1:
        e = find_e(phi_n)
        print("e =", e)
    else:
        print("there was no encryption exponent found")
    print("the randomly generated public key is (", n, ",", e, ")\n")

    # console
    while True:
        print("menu")
        print("1. print the alphabet")
        print("2. encrypt a given plaintext")
        print("3. decrypt a given ciphertext")
        print("x. exit")

        option = input("\nchoose your option:\n")

        if option == '1':
            print("printing the English alphabet, index 0 being underscore...")
            print(alphabet, "\n")
        if option == '2':
            plaintext = input("input plaintext: ").strip()
            if not is_valid_plaintext(plaintext, alphabet):
                print("invalid characters or empty input in the plaintext\n")
                continue
            encrypted_text = encrypt_text(plaintext, alphabet, k, l, n, e)
            print("encrypted text:", encrypted_text + "\n")
        if option == '3':
            ciphertext = input("input ciphertext: ").strip()
            if not is_valid_ciphertext(ciphertext, alphabet):
                print("invalid characters or empty input in the ciphertext\n")
                continue
            d = modular_multiplicative_inverse(e, phi_n)
            decrypted_text = decrypt_text(ciphertext, alphabet, k, l, n, d)
            print("decrypted text:", decrypted_text + "\n")
        if option == 'x':
            print("exiting...")
            break
