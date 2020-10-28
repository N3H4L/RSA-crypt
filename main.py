#!/usr/bin/python

import sys
from rsa import *

def usageHelp():
    print "\nUsage :\nmain.py -g"
    print "main.py -e <input file> -o <output file> -k <public key>"
    print "main.py -d <input file> -o <output file>"
    print "\nOptions:\n-g,--generate : to generate public key and private key"
    print "-e,--encrypt : to encrypt a text/message"
    print "-d,--decrypt : to decrypt a text/message"
    print "-i,--input : input file"
    print "-o,--output : output file"
    print "-k,--key : public key file\n"

def generateKeys():
    e,d,n = generate(find_prime(), find_prime(), key_size = 128)
    export(e,d,n)
    print "[*] Keys generated..."

def getPubKey(public_key):
    with open(public_key, "r") as fp:
        _,e,n = fp.readline(), int(fp.readline()), int(fp.readline())
    return e,n

def encipher(public_key, text_file):
    text = ""
    e = 0
    n = 0
    with open(public_key, "r") as fp:
        _,e,n = fp.readline(), int(fp.readline()), int(fp.readline())
    with open(text_file, "r") as fp:
        text = fp.read()
    cipher_text = encrypt(text,e ,n)
    with open("encrypted.txt","w") as fp:
        for i in cipher_text:
            fp.write("%d\n"%i)
    print "[*] File encrypted..."

def decipher(text_file):
    e = 0
    n = 0
    cipher_text = []
    with open('private.key','r') as fp:
        _,d,n = fp.readline(), int(fp.readline()), int(fp.readline())
    with open(text_file, 'r') as fp:
        for i in fp.readlines():
            cipher_text.append(int(i))
    decrypted_message = decrypt(cipher_text, d, n)
    with open("decrypted.txt","w") as fp:
        fp.write(decrypted_message)
    print "[*] File decrypted..."

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        usageHelp()
    else:
        banner = """
 ____________________________________________________________________
|       ____  _____  ___                                     __      |
|      / __ \/ ___/ /   |         _____ _____ __  __ ____   / /_     |
|     / /_/ /\__ \ / /| | ______ / ___// ___// / / // __ \ / __/     |
|    / _, _/___/ // ___ |/_____// /__ / /   / /_/ // /_/ // /_       |
|   /_/ |_|/____//_/  |_|       \___//_/    \__, // .___/ \__/       |
|                                          /____//_/                 |
|____________________________________________________________________|
|                                                                    |
|                         Coded By : n3hal                           |
|____________________________________________________________________|
        """
        print banner
        public_key = ""
        text_file = ""
        keyfile = ""
        outputfile = ""
        gen = False
        enc = False
        dec = False
        i = 1
        while i != len(sys.argv):
            if sys.argv[i] == '-g' or sys.argv[i] == '--generate':
                gen = True
                i += 1
            elif sys.argv[i] == '-e' or sys.argv[i] == '--encrypt':
                enc = True
                i += 1
            elif sys.argv[i] == '-d' or sys.argv[i] == '--decrypt':
                dec = True
                i += 1
            elif sys.argv[i] == '-i' or sys.argv[i] == '--input':
                i += 1
                text_file = sys.argv[i]
            elif sys.argv[i] == '-o' or sys.argv[i] == '--output':
                i += 1
                outputfile = sys.argv[i]
            elif sys.argv[i] == '-k' or sys.argv[i] == '--key':
                i += 1
                public_key = sys.argv[i]
            else:
                i += 1
        if gen == True:
            generateKeys()
            exit(0)
        if enc == True:
            if public_key == "" or text_file == "":
                usageHelp()
                exit(0)
            else:
                encipher(public_key, text_file)
        if dec == True:
            if text_file == "":
                usageHelp()
                exit(0)
            else:
                decipher(text_file)
