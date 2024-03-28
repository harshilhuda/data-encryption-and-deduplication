import sys
from PyQt5.QtWidgets import QApplication
from windows.MainWindow import MainWindow
from modules import connect

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Anti De-Duplication In Cloud")
    window.show()
    connect.create_connection()
    sys.exit( app.exec_() )
