from PyQt5.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QPushButton, QWidget, QMessageBox, QErrorMessage
from modules.auth import login

import execjs

class RegisterPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.username_label.setStyleSheet("""
                QLabel{
                font-size: 30px;
                font: bold;
                text-transform: capitalize;   
                }
        """)
        self.username_input.setStyleSheet("""
            QLineEdit{
                height: 30px;
                border-radius:5px;
            }
        """)
        self.password_label = QLabel("Password:")
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
        self.password_input.textChanged.connect(self.onTextChanged)
        self.password_error_label = QLabel("Error")
        self.password_error_label.setStyleSheet("color: red; font:bold")
        
        self.register_button = QPushButton("Register")
        self.register_button.setStyleSheet("""
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
        self.layout.addWidget(self.password_error_label)
        self.layout.addWidget(self.register_button)
        self.layout.addWidget(self.back_button)

        self.register_button.clicked.connect(self.register)
        self.back_button.clicked.connect(parent.go_to_welcome_page)

        self.parentClass = parent
        self.setLayout(self.layout)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        # Here you would implement your registration logic
        result = login.register(username, password)
        print(result)
        if (result == "Success"):
            self.parentClass.isLoggedIn = True
            self.parentClass.loggedInUser = username
            QMessageBox.information(self, "Registration", f"Registered with\nUsername: {username}\nPassword: {password}")
            #self.parentClass.go_to_home_page()
        else:
            QMessageBox.critical(None, "Error", f"Error encountered: {result}")
        
    def onTextChanged(self, text):
        result = ctx.call("verifyPassword", text)
        if(result == 1):
            self.password_error_label.setText("Error: Password length is less than 8 characters")
        elif (result == 2):
            self.password_error_label.setText("Error: Password should contain special characters")
        elif (result == 3):
            self.password_error_label.setText("Error: Password should contain a digit")
        else:
            self.password_error_label.setText("")

        
ctx = execjs.compile("""
    const specialCharacters = ["$", "#", "@"];
    const digits = ["1","2","3","4","5","6","7","8","9","0"];

    function verifyPassword(password) {
    //returns true of false;
    
    //Check if length is valid
    if(password.length < 8){
        return 1;
    }
    
    //Check for special character
    let flag = false;
    for(let i of specialCharacters) {
        if( password.includes(i) ){
            flag = flag || true;
        }
    }
    if(flag == false){
        return 2;
    }
    //Is Digit present
    flag = false;
    for(let i of digits) {
        if( password.includes(i) ){
            flag = flag || true;
        }
    }
    if(flag==false)
    {
        return 3;
    }
    
    return 0;
}

""")