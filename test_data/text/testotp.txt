from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sqlite3
from PyQt5.uic import loadUiType
from Encrypter import Encrypter
from Decrypter import Decrypter
from pymsgbox import *
import base64
from Crypto.Cipher import AES
import os
import sys
import requests

Qt = QtCore.Qt
ui, _ = loadUiType('ui.ui')

def start():
    global m
    m = Main_Window()
    m.show()

class encrypt_page():
    def __init__(self):
        self.file = {}
        self.stri = ""
        self.Handel_Buttons()
        self.pushButton_3.clicked.connect(self.chooseFile)
        self.pushButton_4.clicked.connect(self.onClickEncrypt)

    def Handel_Buttons(self):
        self.pushButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))

    def chooseFile(self):
        self.file = QFileDialog.getOpenFileName(self, 'Open Image File', 'F:/Decode/Image_and_text_Encryption/', 'Image files (*.jpg *.jpeg *.png *.bmp *.gif)')
        pixmap = QtGui.QPixmap(self.file[0])
        self.lbl.setPixmap(pixmap.scaledToHeight(250))
        if self.file != None:
            ba = QtCore.QByteArray()
            buff = QtCore.QBuffer(ba)
            buff.open(QtCore.QIODevice.WriteOnly)
            ok = pixmap.save(buff, "PNG")
            pixmap_bytes = ba.data()
            self.stri = base64.b64encode(pixmap_bytes)

    def onClickEncrypt(self):
        f1 = open("id.txt", "r")
        id = f1.read()
        f1.close()
        myKey = self.lineEdit.text()
        sqliteConnection = sqlite3.connect('evaluation.db')
        print("Connected to SQLite")
        r_set = sqliteConnection.execute("select id from registration where id =" + str(id))
        for row in r_set:
            b = row[0]
            r_set1 = sqliteConnection.execute("select * from registration where id =" + str(b))
            with open(r"number.txt", 'w') as f:
                for row in r_set1:
                    line = str(row[5])
                    f.write(line)
                    print("Number: ", row[5])
        num = row[5]
        url = "https://www.fast2sms.com/dev/bulkV2"
        params = {
            "authorization": "nBfowN57tWxzgdlh6YHGUciT3EqrmMPCQ9pDZ2baIOX0J4k8uyJ6dGoTpx9FDykragYVwjv3KXf2tB5Q",
            "route": "otp",
            "variables_values": "",
            "numbers": num,
            "flash": "1"
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            print("OTP sent successfully")
        else:
            print("Failed to send OTP")

        x = Encrypter(self.stri, myKey)
        cipher = x.encrypt_image()
        fh = open("cipher.txt", "wb")
        fh.write(cipher)
        fh.close()
        QMessageBox.information(self, "QMessageBox.information()", "Encryption Successful !")

class decrypt_page():
    def __init__(self):
        self.cipher = {}
        self.Handel_Buttons()
        self.pushButton_5.clicked.connect(self.chooseFile1)
        self.pushButton_6.clicked.connect(self.onClickDecrypt)

    def Handel_Buttons(self):
        self.pushButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))

    def chooseFile1(self):
        file = QFileDialog.getOpenFileName(self, 'Upload File')
        text = open(file[0]).read()
        self.cipher = text.encode('utf-8')

    def onClickDecrypt(self):
        myKey = self.lineEdit_2.text()
        x = Decrypter(self.cipher)
        image = x.decrypt_image(myKey)
        ba = QtCore.QByteArray(image)
        pixmap = QtGui.QPixmap()
        ok = pixmap.loadFromData(ba, "PNG")
        assert ok
        self.lbl_2.setPixmap(pixmap.scaledToHeight(201))
        QMessageBox.information(self, "QMessageBox.information()", "Decryption Successful !")

class Main_Window(QMainWindow, QWidget, ui, encrypt_page, decrypt_page):
    def __init__(self):
        QMainWindow.__init__(self)
        QWidget.__init__(self)
        self.setupUi(self)
        encrypt_page.__init__(self)
        decrypt_page.__init__(self)
        self.Handel_Buttons()
        self.stackedWidget.setCurrentIndex(0)

    def Handel_Buttons(self):
        self.pushButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.pushButton_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.pushButton_8.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pushButton_7.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = start()
    app.exec_()
