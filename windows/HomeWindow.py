from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, QMessageBox, QHBoxLayout, QPushButton, QStackedWidget
from PyQt5.QtGui import QPixmap, QPainter, QIcon
from PyQt5.QtSvg import QSvgRenderer

from .functions.UploadWindow import UploadWindow
from .functions.DownloadWindow import DownloadWindow

class HomePage(QWidget):
    def __init__(self, username, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        
        self.username = username
        self.stackedWidget = QStackedWidget()

        self.mainPage = MainPage(username, self)
        self.uploadWindow = UploadWindow(self)
        self.downloadWindow = DownloadWindow(self)

        self.stackedWidget.addWidget(self.mainPage)
        self.stackedWidget.addWidget(self.uploadWindow)
        self.stackedWidget.addWidget(self.downloadWindow)

        self.layout.addWidget(self.stackedWidget)

        self.stackedWidget.setCurrentIndex(0)

        self.setLayout(self.layout)

    def go_to_main_page(self):
        self.stackedWidget.setCurrentWidget(self.mainPage)
    def go_to_upload_page(self):
        self.stackedWidget.setCurrentWidget(self.uploadWindow)
    def go_to_download_page(self):
        self.stackedWidget.setCurrentWidget(self.downloadWindow)

class MainPage(QWidget):
    def __init__(self, username, parent=None):
        super().__init__(parent)
        
        self.layout = QVBoxLayout()
        self.label = QLabel(f"Welcome {username}!")
        self.label.setStyleSheet("""
                QLabel{
                font-size: 30px;
                font: bold;
                text-transform: capitalize;   
                }
        """)
        self.layout.addWidget(self.label)

        self.buttonBoxLayout = QHBoxLayout() 
        self.uploadButton = QPushButton("Upload File")
        self.uploadButton.setStyleSheet("""
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
        self.downloadButton = QPushButton("Download File")
        self.downloadButton.setStyleSheet("""
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
        self.buttonBoxLayout.addWidget(self.uploadButton)
        self.buttonBoxLayout.addWidget(self.downloadButton)

        self.layout.addLayout(self.buttonBoxLayout)
        self.setLayout(self.layout)

        self.uploadButton.clicked.connect(parent.go_to_upload_page)
        self.downloadButton.clicked.connect(parent.go_to_download_page)        



