from PyQt5.QtSql import QSqlDatabase

def create_connection():
    # Create a connection to the SQLite database
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('data.db')

    if not db.open():
        print("Error: Unable to open database")
        return False

    print("Securing Database Connection")
    return True