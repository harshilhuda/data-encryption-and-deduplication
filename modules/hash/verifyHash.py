from PyQt5.QtSql import QSqlQuery

def verifyHash(filename, hash, username):
    query = QSqlQuery()
    query.exec_("CREATE TABLE IF NOT EXISTS files (filename TEXT, hash TEXT UNIQUE, username TEXT, FOREIGN KEY(user) REFERENCES users(username))")
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