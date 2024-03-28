from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtSvg import QSvgRenderer

class WelcomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.welcome_label = QLabel("Welcome to the Application!")
        self.login_button = QPushButton("Login")
        self.register_button = QPushButton("Register")
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
        self.register_button.setStyleSheet("""
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
        

        self.renderer = QSvgRenderer("./images/bg.svg")

        # Create a QPixmap to render the SVG onto
        pixmap = QPixmap(400, 340)  # Adjust the size as needed
        pixmap.fill()  # Fill with a transparent background
        painter = QPainter(pixmap)

        # Render the SVG onto the QPixmap
        self.renderer.render(painter)
        painter.end()

        # Create a QLabel to display the QPixmap
        self.svg_label = QLabel(self)
        self.svg_label.setPixmap(pixmap)

        # Create a QLabel to display the QPixmap

        self.layout.addWidget(self.svg_label)

        self.layout.addWidget(self.welcome_label)
        self.layout.addWidget(self.login_button)
        self.layout.addWidget(self.register_button)

        self.login_button.clicked.connect(parent.go_to_login_page)
        self.register_button.clicked.connect(parent.go_to_register_page)

        self.setLayout(self.layout)
        self.setGeometry(100, 200, 800, 800)