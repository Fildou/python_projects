import sys
import ctypes
import unidecode
import random
import sympy
import re

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic

qtCreatorFile = "GUI.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


def splitAt(w, n):
    for i in range(0, len(w), n):
        yield w[i:i+n]


def removeDiacritics(text):
    text = unidecode.unidecode(text)
    return text


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def MMI(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi//e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi


def isPrime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True


def generateKeys():
    p = sympy.randprime(10**12, 10**13)
    q = sympy.randprime(10**12, 10**13)

    if not (isPrime(p) and isPrime(q)):
        return ctypes.windll.user32.MessageBoxW(0, 'p and q must be prime', 0)
    elif p == q:
        return ctypes.windll.user32.MessageBoxW(0, 'p and q cannot be equal', 0)

    n = p * q
    phi = (p-1) * (q-1)
    e = random.randrange(1, phi)

    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    d = MMI(e, phi)

    keys = {'e': e, 'd': d, 'n': n}
    return keys


block_len = 5
bin_len = 8


def encrypt(e, n, text):
    text = removeDiacritics(text)
    blocks = []
    cipher = ''

    for index in range(0, len(text), block_len):
        blocks.append(text[index: index + block_len])

    for block in blocks:
        chars = []
        bin_chars = []
        for char in block:
            chars.append(ord(char))
        for char in chars:
            bin_chars.append(format(char, 'b').zfill(bin_len))
        bin_block = int(''.join(bin_chars), 2)
        result = pow(bin_block, e, n)
        cipher += str(result) + ' '

    return cipher


def decrypt(d, n, text):
    text = re.sub(r'[^0-9 ]', '', text)
    blocks = text.split()
    absolute_len = block_len * bin_len
    decipher = ''

    for block in blocks:
        result = pow(int(block), d, n)
        bin_block = format(result, 'b').zfill(absolute_len)
        bin_chars = []
        for index in range(0, len(bin_block), bin_len):
            bin_chars.append(bin_block[index: index + bin_len])
        chars = []
        for bin_char in bin_chars:
            if int(bin_char, 2) != 0:
                chars.append(int(bin_char, 2))
        for char in chars:
            decipher += chr(char)
    return decipher
