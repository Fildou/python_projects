import sys
import ctypes
import re
import unidecode

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic

qtCreatorFile = "GUI.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
m = len(alpha)

def keyControl(keyA, keyB):
    if (keyA == 0):
        return ctypes.windll.user32.MessageBoxW(0, "Kľúč A sa nesmie rovnať 0", "CHYBA", 0)
    if (keyB == 0):
        return ctypes.windll.user32.MessageBoxW(0, "Kľúč B sa nesmie rovnať 0", "CHYBA", 0)
    if (keyA > keyB):
        return ctypes.windll.user32.MessageBoxW(0, "Kľúč A nesmie byť väčší ako kľúč B", "CHYBA", 0)

def euclid(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y

def mmi(a, m):
    gcd, x, y = euclid(a, m)
    if gcd != 1:
        return ctypes.windll.user32.MessageBoxW(0, "není možné nájsť MMI", "CHYBA", 0)
    else:
        return x % m

def removeDiacritics(text):
    text = unidecode.unidecode(text)
    return text

def removeSpecialChars(text):
    text = numbersCipher(text)
    text = removeDiacritics(text)
    text = re.sub('[^A-Za-z ]+', '', text)
    return text

def numbersCipher(text):
    text = text.replace('0', 'XQW')
    text = text.replace('1', 'XWQ')
    text = text.replace('2', 'QWX')
    text = text.replace('3', 'QWY')
    text = text.replace('4', 'YQW')
    text = text.replace('5', 'WQY')
    text = text.replace('6', 'XWT')
    text = text.replace('7', 'TWX')
    text = text.replace('8', 'WXT')
    text = text.replace('9', 'XQV')
    return text

def numbersDecipher(text):
    text = text.replace('XQW', '0')
    text = text.replace('XWQ', '1')
    text = text.replace('QWX', '2')
    text = text.replace('QWY', '3')
    text = text.replace('YQW', '4')
    text = text.replace('WQY', '5')
    text = text.replace('XWT', '6')
    text = text.replace('TWX', '7')
    text = text.replace('WXT', '8')
    text = text.replace('XQV', '9')
    return text

def splitAt(w,n):
    for i in range(0,len(w),n):
        yield w[i:i+n]

class GUI(QMainWindow, Ui_MainWindow):
    def cipher(self):
        
        keyA = int(self.keyA.text())
        keyB = int(self.keyB.text())
        keyControl(keyA, keyB)
        text = removeSpecialChars(self.cipherText.toPlainText())
        result = ''.join([ chr((( keyA*(ord(t) - ord('A')) + keyB ) % m)
                + ord('A')) for t in text.upper().replace(' ', 'XMEDZERAX') ])

        result = " ".join(splitAt(result, 5))
        self.cipherResult.setPlainText(str(result))

    def decipher(self):
        keyA = int(self.keyA.text())
        keyB = int(self.keyB.text())
        keyControl(keyA, keyB)
        cipher = numbersDecipher(self.decipherText.toPlainText())
        cipher = cipher.replace(' ', '')
        result = ''.join([ chr(((mmi(keyA, m)*(ord(c) - ord('A') - keyB)) % m)
                  + ord('A')) for c in cipher])
        result = result.replace('XMEDZERAX', ' ')
        self.decipherResult.setPlainText(str(numbersDecipher(result)))

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.cipherButton.clicked.connect(self.cipher)
        self.decipherButton.clicked.connect(self.decipher)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec_())
