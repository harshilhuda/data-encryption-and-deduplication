from PyQt5.QtSql import QSqlQuery
from argon2 import PasswordHasher

passwordHasher = PasswordHasher()

def register(username, password):
    query = QSqlQuery()
    query.exec_("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)")
    query.prepare("INSERT INTO users (username, password) VALUES (?, ?)")
    hashedPassword = passwordHasher.hash(password)
    query.bindValue(0, username)
    query.bindValue(1, hashedPassword)
    if not query.exec_():
        return "Duplicate Username"
    return "Success"

def login(username, password):
    query = QSqlQuery()
    query.prepare("SELECT password FROM users where username=(?)")
    query.bindValue(0, username)
    if not query.exec_():
        return "Invalid"
    if query.next():
        if not passwordHasher.verify(query.value(0), password):
            return "Invalid Password"
        else:
            return "Success"
    return "No username found"

