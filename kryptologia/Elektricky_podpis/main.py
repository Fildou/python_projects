import base64
import hashlib
import sys
import ctypes
import os
import datetime

from tkinter import filedialog
from zipfile import ZipFile

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic

import RSA

qtCreatorFile = "GUI.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class GUI(QMainWindow, Ui_MainWindow):

    def signPath_file(self):
        filePath = filedialog.askopenfilename()
        if not filePath: return
        self.filePath_sign.setText(f'Path: {filePath}')
        self.fileName.setText(f'Name: {os.path.basename(filePath)}')
        self.fileType.setText(f'Type: {os.path.splitext(filePath)[1]}')
        self.fileSize.setText(f'Size: {os.stat(filePath).st_size} Byte')
        dateCreated = datetime.datetime.fromtimestamp(os.stat(filePath).st_ctime).strftime('%d/%m/%Y %H:%M:%S')
        self.fileCreated.setText(f'Time created: {dateCreated}')

    def pathPrivateKey(self):
        path = filedialog.askopenfilename()
        self.keyPath_private.setText(f'Path: {path}')

    def validPath_file(self):
        filePath = filedialog.askopenfilename()
        self.filePath_valid.setText(f'Path: {filePath}')

    def pathPublicKey(self):
        path = filedialog.askopenfilename()
        self.keyPath_public.setText(f'Path: {path}')

    def generateKeys(self):
        filePath = str(self.filePath_sign.text())
        filePath = filePath.removeprefix('Path: ')
        fileName = str(self.fileName.text())
        fileName = fileName.removeprefix('Name: ')
        filePath = filePath.removesuffix(f'/{fileName}')

        privateKey = filePath + f'/privateKey.priv'
        publicKey = filePath + f'/publicKey.pub'

        keys = RSA.generateKeys()
        base64_privateKey = self.doBase64(str(keys['e']) + ' ' + str(keys['n']))
        with open(privateKey, "w") as file:
            file.write('RSA ' + base64_privateKey)
        base64_publicKey = self.doBase64(str(keys['d']) + ' ' + str(keys['n']))
        with open(publicKey, "w") as file:
            file.write('RSA ' + base64_publicKey)

        ctypes.windll.user32.MessageBoxW(0, 'Keys were generated', 0)
        return keys

    def signature(self):
        fileName = str(self.fileName.text())
        fileName = fileName.removeprefix('Name: ')
        filePath = str(self.filePath_sign.text())
        filePath = filePath.removeprefix('Path: ')
        filePath = filePath.removesuffix(f'{fileName}')
        cleanFileName = fileName.split('.')[0]

        zipFilePath = filePath + f'{cleanFileName}.zip'
        keys = self.generateKeys()

        with open(filePath + fileName, 'r+b') as file:
            hashText = hashlib.sha3_512(file.read()).hexdigest()
        encrypted = RSA.encrypt(keys['e'], keys['n'], hashText)
        base64_text = self.doBase64(encrypted)

        with ZipFile(zipFilePath, 'w') as zipf:
            with open(filePath + fileName, 'r+b') as file:
                zipf.writestr(os.path.basename(fileName), file.read())
            zipf.writestr(cleanFileName + '.sign', 'RSA_SHA3-512 ' + base64_text)

        ctypes.windll.user32.MessageBoxW(0, 'Digital signature succeeded', 0)

    def doBase64(self, text):
        base64_b = base64.b64encode(text.encode('ascii'))
        return base64_b.decode('ascii')

    def undoBase64(self, text):
        text_b = base64.b64decode(text)
        return text_b.decode('ascii')

    def validation(self):
        zipFilePath = str(self.filePath_valid.text())
        zipFilePath = zipFilePath.removeprefix('Path: ')
        publicKeyPath = str(self.keyPath_public.text())
        publicKeyPath = publicKeyPath.removeprefix('Path: ')

        with ZipFile(zipFilePath, 'r') as zipf:
            if len(zipf.namelist()) != 2:
                ctypes.windll.user32.MessageBoxW(0, 'Wrong .zip file', 0)
            for file in zipf.namelist():
                if file.endswith('.sign'): signedFile = file
                else: filePath = file
            if not signedFile or not filePath:
                ctypes.windll.user32.MessageBoxW(0, 'Wrong .zip file', 0)
            valid = self.undoBase64(zipf.read(signedFile).split()[1])
            hash = hashlib.sha3_512(zipf.read(filePath)).hexdigest()

        with open(publicKeyPath, 'rb') as file:
            content = file.read().split()[1]
        keys = self.undoBase64(content).split()
        decryption = RSA.decrypt(int(keys[0]), int(keys[1]), valid)

        if decryption == hash:
            ctypes.windll.user32.MessageBoxW(0, 'File validation succeeded', 0)
        else:
            ctypes.windll.user32.MessageBoxW(0, 'Wrong signature, validation didnt succeed', 0)

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.filePath_sign_button.clicked.connect(self.signPath_file)
        self.keyPath_private_button.clicked.connect(self.pathPrivateKey)
        self.generateKeys_button.clicked.connect(self.generateKeys)
        self.signButton.clicked.connect(self.signature)
        self.filePath_balid_button.clicked.connect(self.validPath_file)
        self.keyPath_public_button.clicked.connect(self.pathPublicKey)
        self.validateButton.clicked.connect(self.validation)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec_())
