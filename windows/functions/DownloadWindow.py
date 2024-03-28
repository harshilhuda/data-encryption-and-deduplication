from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QMessageBox

import rust_hash_module

class DownloadWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()

        self.fileName_label = QLabel("FileName:")
        self.fileName_label.setStyleSheet("""
                QLabel{
                font-size: 30px;
                font: bold;
                text-transform: capitalize;   
                }
        """)
        self.fileName_input = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_label.setStyleSheet("""
                QLabel{
                font-size: 30px;
                font: bold;
                text-transform: capitalize;   
                }
        """)
        self.decrypt_button = QPushButton("Decrypt File")
        self.decrypt_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; /* Green */
                border: none;
                color: white;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                font: bold;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #45a049; /* Darker Green */
            }
            QPushButton:pressed {
                background-color: #4CAF50; /* Green */
            }
        """)
        self.back_button = QPushButton("Back")
        self.back_button.setStyleSheet("""
            QPushButton{
            background-color: #428df5;
            color:White;
            margin: 4px 2px;
            border: none;
            padding: 15px 32px;
            font-size: 16px;
            font: bold;                           
            border-radius: 10px;
            text-align: center;
            display: inline-block;
            }
             QPushButton:hover {
                cursor:pointer;
                background-color:#42e6f5;
            }                                   
        """)
        self.layout.addWidget(self.fileName_label)
        self.layout.addWidget(self.fileName_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.decrypt_button)
        self.layout.addWidget(self.back_button)

        self.decrypt_button.clicked.connect(self.decrypt)
        self.back_button.clicked.connect(parent.go_to_main_page)
        self.parentClass = parent

        self.setLayout(self.layout)

    def decrypt(self):
        fileName = self.fileName_input.text()
        password = self.password_input.text()

        fileNameEdited = fileName.split("/")[-1]
        print(fileName)
        result = rust_hash_module.decrypt_file(fileName, f"D:/finalproject/cloud_downloads/{fileNameEdited}", password)
        if (result == "Success"):
            QMessageBox.information(self, "Success", f"File Saved at : D:/finalproject/cloud_downloads/{fileNameEdited}")
