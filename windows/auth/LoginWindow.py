from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
from modules.auth import login
from ..HomeWindow import HomePage

class LoginPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.username_label = QLabel("Enter Username:")
        self.username_label.setStyleSheet("""
                QLabel{
                font-size: 30px;
                font: bold;
                text-transform: capitalize;   
                }
        """)
        self.username_input = QLineEdit()
        self.username_input.setStyleSheet("""
            QLineEdit{
                height: 30px;
                border-radius:5px;
            }
        """)
        self.password_label = QLabel("Enter Password:")
        self.password_label.setStyleSheet("""
                QLabel{
                font-size: 30px;
                font: bold;
                text-transform: capitalize;   
                }
        """)
        self.password_input = QLineEdit()
        self.password_input.setStyleSheet("""
            QLineEdit{
                height: 30px;
                border-radius:5px;
            }
        """)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet("""
            QPushButton{
            background-color:Black;
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
                background-color:#454545;
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
        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)
        self.layout.addWidget(self.back_button)

        self.login_button.clicked.connect(self.login)
        self.back_button.clicked.connect(parent.go_to_welcome_page)
        self.parentClass = parent
        self.setLayout(self.layout)

    def login(self, parent):
        username = self.username_input.text()
        password = self.password_input.text()
        # Here you would implement your login logic
        result = login.login(username, password)
        if(result == "Success"):
            self.parentClass.home_page = HomePage(username, self.parentClass)
            self.parentClass.stacked_widget.addWidget(self.parentClass.home_page)
            self.parentClass.isLoggedIn = True
            self.parentClass.loggedInUser = username
            QMessageBox.information(self, "Logged In", f"Logged in with\nUsername: {username}\nPassword: {password}")
            print(self.parentClass.isLoggedIn)
            self.parentClass.go_to_home_page()
        else:
            QMessageBox.critical(self, "Error", f"Error Encountered: {result}")

