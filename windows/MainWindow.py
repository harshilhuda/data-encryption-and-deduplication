from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QLineEdit, QHBoxLayout, QStackedWidget, QDesktopWidget
from PyQt5.QtGui import QIcon
from .WelcomeWindow import WelcomePage
from .auth.LoginWindow import LoginPage
from .auth.RegisterWindow import RegisterPage
from .HomeWindow import HomePage

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.isLoggedIn = False
        self.loggedInUser = None
        
        self.stacked_widget = QStackedWidget()
        self.welcome_page = WelcomePage(self)
        self.register_page = RegisterPage(self)
        self.login_page = LoginPage(self)
        self.home_page = HomePage("harshil", self)

        screen = QDesktopWidget().screenGeometry()
        center_point = screen.center()

        # Calculate the top-left corner of the window
        window_width = self.frameGeometry().width()
        window_height = self.frameGeometry().height()
        window_top_left_x = center_point.x() - window_width // 2
        window_top_left_y = center_point.y() - window_height // 2

        # Set the geometry of the window to the calculated top-left corner
        self.setGeometry(window_top_left_x, window_top_left_y, window_width, window_height)
        self.setMinimumSize(window_width, window_height)

        self.stacked_widget.addWidget(self.welcome_page)
        self.stacked_widget.addWidget(self.register_page)
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.home_page)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.stacked_widget)
        self.setLayout(self.layout)

        self.setWindowIcon(QIcon("./images/favicon.ico"))

    def go_to_register_page(self):
        self.stacked_widget.setCurrentWidget(self.register_page)

    def go_to_login_page(self):
        self.stacked_widget.setCurrentWidget(self.login_page)

    def go_to_welcome_page(self):
        self.stacked_widget.setCurrentWidget(self.welcome_page)

    def go_to_home_page(self):
        self.stacked_widget.setCurrentWidget(self.home_page)