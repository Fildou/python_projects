import itertools
import sys
import ctypes
import re
import unidecode

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5 import uic

qtCreatorFile = "playfair_GUI.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


def removeSpecialChars(text):
    text = unidecode.unidecode(text)
    key = text.replace('W', 'V')
    key = key.replace(' ', '')
    key = numbersCipher(key)
    key = re.sub('[^A-Za-z ]+', '', key)
    key = key.upper()
    return key


def distinctChar(text):
    char_seen = []
    for char in text:
        if char not in char_seen:
            char_seen.append(char)
    return (''.join(char_seen))


def numbersCipher(text):
    text = text.replace('0', 'XQV')
    text = text.replace('1', 'XVQ')
    text = text.replace('2', 'QVX')
    text = text.replace('3', 'QVY')
    text = text.replace('4', 'YQV')
    text = text.replace('5', 'VQY')
    text = text.replace('6', 'XVT')
    text = text.replace('7', 'TVX')
    text = text.replace('8', 'VXT')
    text = text.replace('9', 'XQC')
    return text


def numbersDecipher(text):
    text = text.replace('XQV', '0')
    text = text.replace('XVQ', '1')
    text = text.replace('QVX', '2')
    text = text.replace('QVY', '3')
    text = text.replace('YQV', '4')
    text = text.replace('VQY', '5')
    text = text.replace('XVT', '6')
    text = text.replace('TVX', '7')
    text = text.replace('VXT', '8')
    text = text.replace('XQC', '9')
    return text


def splitAt(w, n):
    for i in range(0, len(w), n):
        yield w[i:i + n]


def get_coords(parser, key_matrix):
    coords = []
    for char in parser:
        for x in range(5):
            for y in range(5):
                if key_matrix[x][y] == char:
                    coords.append((x, y))
                else:
                    return None
    return coords


def find_position(key_matrix: list, letter: str):
    position = [0, 0]
    for i in range(5):
        for j in range(5):
            if key_matrix[i][j] == letter:  # porovnava znak z inputu s polohou v tabulke
                position[0] = i  # riadok
                position[1] = j  # stlpec
    return position


def editOpenText(text):
    pairs = []
    for m in range(len(text)-1):
        if text[m] != text[m + 1]:
            pairs.append(text[m])
        else:
            if text[m] != 'X':
                pairs.append(text[m])
                pairs.append('X')
            else:
                pairs.append(text[m])
                pairs.append('Q')
    pairs.append(text[len(text) - 1])
    result = "".join(map(str, pairs))
    if len(result) % 2 != 0:
        if result[len(result) - 1] != 'X':
            result += 'X'
        else:
            result += 'Q'
    result = " ".join(map(str, splitAt(result, 2)))
    return result


def encryption(text, key_matrix):
    cipher = []
    text = removeSpecialChars(text)
    for t in range(0, len(text), 2):
        position1 = find_position(key_matrix, text[t])
        position2 = find_position(key_matrix, text[t+1])
        if position1[0] == position2[0]:  # rovnaky riadok
            cipher.append(key_matrix[position1[0]][(position1[1] + 1) % 5])
            cipher.append(key_matrix[position2[0]][(position2[1] + 1) % 5])
        elif position1[1] == position2[1]:  # rovnaky stlpec
            cipher.append(key_matrix[(position1[0] + 1) % 5][position1[1]])
            cipher.append(key_matrix[(position2[0] + 1) % 5][position2[1]])
        else:  # uhlopriecka
            cipher.append(key_matrix[position1[0]][position2[1]])
            cipher.append(key_matrix[position2[0]][position1[1]])
    return ''.join(cipher)


def decryption(text, key_matrix):
    decipher = []
    for t in range(0, len(text), 2):
        position1 = find_position(key_matrix, text[t])
        position2 = find_position(key_matrix, text[t+1])
        if position1[0] == position2[0]:  # rovnaky riadok
            decipher.append(key_matrix[position1[0]][(position1[1] + 4) % 5])
            decipher.append(key_matrix[position2[0]][(position2[1] + 4) % 5])
        elif position1[1] == position2[1]:  # rovnaky stlpec
            decipher.append(key_matrix[(position1[0] + 4) % 5][position1[1]])
            decipher.append(key_matrix[(position2[0] + 4) % 5][position2[1]])
        else:  # uhlopriecka
            decipher.append(key_matrix[position1[0]][position2[1]])
            decipher.append(key_matrix[position2[0]][position1[1]])
    return ''.join(decipher)


class main(QMainWindow, Ui_MainWindow):


    def tableCreation(self):
        key = removeSpecialChars(self.keyWord.text())
        key = distinctChar(key)
        if len(key) < 5:
            ctypes.windll.user32.MessageBoxW(0, "kľúč musí mať aspoň 5 unikátnych písmen", "CHYBA", 0)
            return False
        else:
            chars = []
            key += 'ABCDEFGHIJKLMNOPQRSTUVXYZ'
            for k in key:
                if k not in chars:
                    chars.append(k)
            matrix = [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]
            ]
            for i in range(5):
                for j in range(5):
                    matrix[i][j] = chars[5 * i + j]
        self.tableInsert(matrix)
        return matrix


    def cipher(self):
        text = self.input.toPlainText()
        text = text.replace(' ', 'QMEDZERAX')
        text = removeSpecialChars(text)
        text = editOpenText(text)
        self.openText.setText(text)
        matrix = self.tableCreation()
        cipher = ' '.join(splitAt(encryption(text, matrix), 2))
        self.output.setPlainText(cipher)

    def decipher(self):
        text = removeSpecialChars(self.input.toPlainText())
        text = removeSpecialChars(text)
        matrix = self.tableCreation()
        decipher = decryption(text, matrix)
        decipher = decipher.replace('QMEDZERAX', ' ')
        decipher = numbersDecipher(decipher)
        self.output.setPlainText(decipher)


    def tableInsert(self, matrix):
        self.table.setRowCount(len(matrix[0]))
        self.table.setColumnCount(len(matrix))
        for i in range(len(matrix[0])):
            for j in range(len(matrix)):
                self.table.setItem(i, j, QTableWidgetItem(matrix[i][j]))


    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.tableButton.clicked.connect(self.tableCreation)
        self.cipherButton.clicked.connect(self.cipher)
        self.decipherButton.clicked.connect(self.decipher)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = main()
    window.show()
    sys.exit(app.exec_())
