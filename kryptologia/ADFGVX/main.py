import json
import random
import re
import sys
import unidecode

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5 import uic

qtCreatorFile = "GUI.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

ADFGX_alphabet = "ABCDEFGHIJKLMNOPQRSTUVXYZ"
ADFGVX_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def inputControl(text):
    text = unidecode.unidecode(text.upper())
    text = re.sub(r'[^\w\s]', '', text)
    text = ''.join(text.split())
    return text


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


def charsCipher(text):
    text = text.replace('!', 'QVYKRX')
    text = text.replace('?', 'QOTAZX')
    text = text.replace(',', 'QCIARX')
    text = text.replace('.', 'QBODKX')
    text = text.replace(' ', 'QMEDZX')
    return text


def charsDecipher(text):
    text = text.replace('QVYKRX', '!')
    text = text.replace('QOTAZX', '?')
    text = text.replace('QCIARX', ',')
    text = text.replace('QBODKX', '.')
    text = text.replace('QMEDZX', ' ')
    return text


def find_position(key_matrix: list, letter: str):
    position = [0, 0]
    for i in range(5):
        for j in range(5):
            if key_matrix[i][j] == letter:  # porovnava znak z inputu s polohou v tabulke
                position[0] = i  # riadok
                position[1] = j  # stlpec
    return position


def ADFGVX_find_position(key_matrix: list, letter: str):
    position = [0, 0]
    for i in range(6):
        for j in range(6):
            if key_matrix[i][j] == letter:  # porovnava znak z inputu s polohou v tabulke
                position[0] = i  # riadok
                position[1] = j  # stlpec
    return position


def ADFGX_preTransposition(text, grid):
    text = inputControl(text)
    result = ''
    columns = ['A', 'D', 'F', 'G', 'X']

    for i in range(len(text)):
        position = find_position(grid, text[i])
        result += columns[position[0]]
        result += columns[position[1]]

    return result


def ADFGVX_preTransposition(text, grid):
    text = inputControl(text)
    result = ''
    columns = ['A', 'D', 'F', 'G', 'V', 'X']

    for i in range(len(text)):
        position = ADFGVX_find_position(grid, text[i])
        result += columns[position[0]]
        result += columns[position[1]]

    return result


def transposition(keyword, pretrans):
    basekey = keyword
    sortkey = sorted(keyword)
    index = {}
    for i in range(len(sortkey)):
        index[i] = sortkey[i]
    trans = {}
    for i in range(len(basekey)):
        for x in index:
            if index[x] == basekey[i]:
                trans[x] = ''
                index.pop(x)
                break
    for i in range(0, len(pretrans), len(keyword)):
        for j, x in zip(range(len(keyword)), trans):
            if len(pretrans) > i + j:
                trans[x] += pretrans[i+j]
    result = ''
    for i in range(len(trans)):
        result += trans[i] + ' '
    return result

def ADFGX_restorePreTrans(text, grid):
    text = inputControl(text)
    trans = ''
    first_ch = ''
    second_ch = ''
    columns = ['A', 'D', 'F', 'G', 'X']
    for i in range(0, len(text), 2):
        for j in range(len(columns)):
            if text[i] == columns[j]:
                first_ch = j
            if text[i + 1] == columns[j]:
                second_ch = j
        trans += grid[first_ch][second_ch]
    return trans


def ADFGVX_restorePreTrans(text, grid):
    text = inputControl(text)
    trans = ''
    first_ch = ''
    second_ch = ''
    columns = ['A', 'D', 'F', 'G', 'V', 'X']
    for i in range(0, len(text), 2):
        for j in range(len(columns)):
            if text[i] == columns[j]:
                first_ch = j
            if text[i + 1] == columns[j]:
                second_ch = j
        trans += grid[first_ch][second_ch]
    return trans


def restoreTrans(text, keyword):
    basekey = keyword
    sortkey = sorted(keyword)
    index = {}
    for i in range(len(sortkey)):
        index[i] = sortkey[i]
    trans = {}
    for i in range(len(basekey)):
        for x in index:
            if index[x] == basekey[i]:
                trans[x] = 0
                index.pop(x)
                break
    for i in range(0, len(text), len(keyword)):
        for j, x in zip(range(len(keyword)), trans):
            if len(text) > i + j:
                trans[x] += 1
    restore = {}
    for i in range(len(trans)):
        restore[i] = trans[i]
    chars = 0
    for i in range(len(keyword)):
        basetext = text[chars: restore[i] + chars]
        chars += restore[i]
        restore[i] = basetext

    result = ''
    for i in range(trans[0]):
        for x in trans:
            if len(restore[x]) > i:
                result += restore[x][i]
    return result


class main(QMainWindow, Ui_MainWindow):

    def ADFGX_tableCreation(self):
        grid_alpha = str(self.ADFGX_alphabet.text())
        grid_alpha = distinctChar(grid_alpha)
        grid_alpha = grid_alpha.replace('W', 'V')
        grid_alpha = inputControl(grid_alpha)
        shuffled = list(ADFGX_alphabet)
        random.shuffle(shuffled)

        alpha = grid_alpha
        chars = []
        for c in alpha:
            chars.append(c)
        for s in shuffled:
            if s not in chars:
                chars.append(s)

        grid = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        grid_alpha = ''.join(chars)
        for i in range(5):
            for j in range(5):
                grid[i][j] = chars[5 * i + j]

        self.ADFGX_table.setRowCount(len(grid[0]))
        self.ADFGX_table.setColumnCount(len(grid))
        for i in range(len(grid[0])):
            for j in range(len(grid)):
                self.ADFGX_table.setItem(i, j, QTableWidgetItem(grid[i][j]))

        self.ADFGX_alphabet.setText(grid_alpha)
        return grid

    def ADFGX_encryption(self):
        text = self.ADFGX_input.toPlainText()
        text = charsCipher(text)
        text = numbersCipher(text)
        text = inputControl(text)
        keyword = self.ADFGX_keyword.text()
        grid = self.ADFGX_tableCreation()
        pretrans = ADFGX_preTransposition(text, grid)
        encrypt = transposition(keyword, pretrans)
        self.ADFGX_output.setPlainText(encrypt)

    def ADFGX_decryption(self):
        text = self.ADFGX_input.toPlainText()
        keyword = self.ADFGX_keyword.text()
        grid = self.ADFGX_tableCreation()
        trans = restoreTrans(text, keyword)
        decrypt = ADFGX_restorePreTrans(trans, grid)
        decrypt = charsDecipher(decrypt)
        decrypt = numbersDecipher(decrypt)
        self.ADFGX_output.setPlainText(decrypt)

    def ADFGVX_encryption(self):
        text = self.ADFGVX_input.toPlainText()
        text = charsCipher(text)
        text = inputControl(text)
        keyword = self.ADFGVX_keyword.text()
        grid = self.ADFGVX_tableCreation()
        pretrans = ADFGVX_preTransposition(text, grid)
        encrypt = transposition(keyword, pretrans)
        self.ADFGVX_output.setPlainText(encrypt)

    def ADFGVX_decryption(self):
        text = self.ADFGVX_input.toPlainText()
        keyword = self.ADFGVX_keyword.text()
        grid = self.ADFGVX_tableCreation()
        trans = restoreTrans(text, keyword)
        decrypt = ADFGVX_restorePreTrans(trans, grid)
        decrypt = charsDecipher(decrypt)
        self.ADFGVX_output.setPlainText(decrypt)

    def ADFGVX_tableCreation(self):
        grid_alpha = str(self.ADFGVX_alphabet.text())
        grid_alpha = inputControl(grid_alpha)
        grid_alpha = distinctChar(grid_alpha)
        shuffled = list(ADFGVX_alphabet)
        random.shuffle(shuffled)

        alpha = grid_alpha
        chars = []
        for c in alpha:
            chars.append(c)
        for s in shuffled:
            if s not in chars:
                chars.append(s)

        grid = [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ]
        grid_alpha = ''.join(chars)
        for i in range(6):
            for j in range(6):
                grid[i][j] = chars[6 * i + j]

        self.ADFGVX_table.setRowCount(len(grid[0]))
        self.ADFGVX_table.setColumnCount(len(grid))
        for i in range(len(grid[0])):
            for j in range(len(grid)):
                self.ADFGVX_table.setItem(i, j, QTableWidgetItem(grid[i][j]))

        self.ADFGVX_alphabet.setText(grid_alpha)
        return grid

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.ADFGX_gridCreate.clicked.connect(self.ADFGX_tableCreation)
        self.ADFGVX_gridCreate.clicked.connect(self.ADFGVX_tableCreation)
        self.ADFGX_encryptButton.clicked.connect(self.ADFGX_encryption)
        self.ADFGVX_encryptButton.clicked.connect(self.ADFGVX_encryption)
        self.ADFGX_decryptButton.clicked.connect(self.ADFGX_decryption)
        self.ADFGVX_decryptButton.clicked.connect(self.ADFGVX_decryption)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = main()
    window.show()
    sys.exit(app.exec_())