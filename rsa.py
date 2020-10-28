#!/usr/bin/python

import random
import base64

upper_limit = 1000000000000
def is_prime(num):
    if num < 2 :
        return False
    if num == 2:
        return True
    if num & 0x01 == 0:
        return False
    n = int(num ** 0.5)
    for i in range(3,n,2):
        if num%i == 0:
            return False
    return True

def find_prime(limit = upper_limit):
    num = 0
    while True:
        num = random.randint(0, limit)
        if is_prime(num):
            break
    print "[*] Generated Prime number : "+str(num)
    return num

def gcd(a, b):
    temp = 0
    while True:
        temp = a%b
        if temp == 0:
            return b
        a = b
        b = temp

def egcd(a, b):
    if a == 0:
        return (b,0,1)
    else:
        g,y,x = egcd(b % a,a)
    return (g,x-(b // a)*y,y)

def encrypt(message, e, n):
    cipher = []
    for char in message:
        cipher.append(pow(ord(char), e, n))
    return cipher

def decrypt(cipher, d, n):
    plain = ""
    for i in cipher:
        plain += chr(pow(i, d, n))
    return plain

def genPubKey(phi, key_size):
    e = random.randint(2**(key_size - 1), (2 ** key_size - 1))
    g = gcd(e, phi)
    while g != 1:
        e = random.randint(2**(key_size - 1), (2 ** key_size - 1))
        g = gcd(e, phi)
    return e

def genPrivKey(phi, e):
    d = egcd(e, phi)[1]
    d = d % phi
    if d < 0:
        d += phi
    return d

def generate(p, q, key_size = 128):
    n = p * q
    phi = (p - 1)*(q - 1)
    e = genPubKey(phi, key_size)
    d = genPrivKey(phi, e)
    print "[*] n\t=\t"+str(n)
    print "[*] phi\t=\t"+str(phi)
    print "[*] e\t=\t"+str(e)
    print "[*] d\t=\t"+str(d)
    return (e,d,n)

def export(e,d,n):
    with open("public.key","w") as fp:
        fp.write("RSA PUBLIC KEY:\n%d\n%d\nEND\n"%(e,n))
        print "[*] Public Key saved..."
    with open("private.key","w") as fp:
        fp.write("RSA PRIVATE KEY:\n%d\n%d\nEND\n"%(d,n))
        print "[*] Private Key saved..."

if __name__ == '__main__':
    e,d,n = generate(find_prime(), find_prime(), key_size = 128)
    export(e,d,n)
    plain = "This is a test"
    print "[*] Plaintext\t=\t"+plain
    cipher = encrypt(plain, e, n)
    print "[*] Ciphertext\t=\t"+str(cipher)
    decoded = decrypt(cipher,d,n)
    print "[*] Decoded-text\t=\t"+decoded
    
