from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog, QMessageBox, QLineEdit

import rust_hash_module

class UploadWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()

        self.backButton = QPushButton("Back")
        self.backButton.setStyleSheet("""
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
        self.backButton.clicked.connect(parent.go_to_main_page)

        self.upload_button = QPushButton("Upload File", self)
        self.upload_button.setStyleSheet("""
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
        self.upload_button.setGeometry(50, 50, 150, 30)
        self.upload_button.clicked.connect(self.upload_file)

        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.file_label = QLabel(f"Choose the file you want to upload", self)
        self.file_label.setGeometry(50, 100, 300, 30)
        self.file_label.setStyleSheet("""
                QLabel{
                font-size: 30px;
                font: bold;
                text-transform: capitalize;   
                }
        """)
        self.file1_label = QLabel(f"Enter Encryption Key", self)
        self.file1_label.setGeometry(200, 200, 300, 30)
        self.file1_label.setStyleSheet("""
                QLabel{
                font-size: 30px;
                font: bold;
                text-transform: capitalize;   
                }
        """)
        self.username = parent.username
        self.layout.addWidget(self.file_label)
        self.layout.addWidget(self.file1_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.upload_button)
        self.layout.addWidget(self.backButton)
        self.setLayout(self.layout)

    def upload_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Text Files (*.txt);;All Files (*)")

        if file_dialog.exec_():
            file_names = file_dialog.selectedFiles()
            if file_names:
                file_name = file_names[0]
                hashValue = rust_hash_module.calculate_file_hash(file_name)
                print(hashValue)
                fileName = getFileName(file_name)
                self.file_label.setText(f"Selected File: {fileName}")
                result = verifyHash(fileName, hashValue, self.username)
                print(result)
                if(result == "Success"):
                    password = self.password_input.text()
                    #                                   Filename   Filepath                       Password
                    r1 = rust_hash_module.encrypt_file(file_name, f"D:/finalproject/cloud/{fileName}", password)
                    QMessageBox.information(self, "Success", f"File Added to cloud: {file_name}")
            else:
                self.file_label.setText("No file selected")


def getFileName(absolutePath):
    return absolutePath.split("/")[-1]

from PyQt5.QtSql import QSqlQuery

def verifyHash(filename, hash, username):
    query = QSqlQuery()
    query.exec_("CREATE TABLE IF NOT EXISTS files (filename TEXT, hash TEXT UNIQUE, username TEXT, FOREIGN KEY(username) REFERENCES users(username))")
    if not query.exec_():
        return "Duplicate Username"
    query.prepare("SELECT filename FROM files where hash=(?)")
    query.bindValue(0, hash)
    if not query.exec_():
        return "Invalid"
    if query.next():
        return "File Already Exists"
    else:
        query.prepare("INSERT INTO files (filename, hash, username) VALUES (?, ?, ?)")
        query.bindValue(0, filename)
        query.bindValue(1, hash)
        query.bindValue(2, username)
        if not query.exec_():
            return "Error in adding files"
        return "Success"