import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'RoSD04031998@'

)

cursorObject = dataBase.cursor()

cursorObject.execute('CREATE DATABASE crmpro')