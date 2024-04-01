import sqlite3
from constant import TEMPERATURE, MOISTURE, SOILPH, SALINITY, DATABASE_NAME

class DatabaseAccess:
    
    def __init__(self):
        self.tableNames = [TEMPERATURE, MOISTURE, SOILPH, SALINITY]
        self.initializeTableIfNotExist()

    def initializeTableIfNotExist(self):
        for table in self.tableNames:
            if not self.tableExists(table):
                self.createTable(table)

    def tableExists(self, tableName):
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()

        sqlQuery = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}'".format(tableName)
        cursor.execute(sqlQuery)

        result = cursor.fetchone()

        connection.close()

        return result
        
    def createTable(self, tableName):
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()

        sqlQuery = '''CREATE TABLE {} (
                    id INTEGER PRIMARY KEY,
                    timestamp TEXT,
                    {} REAL
                )'''.format(tableName, tableName)
        print('Sql query: ', sqlQuery)
        cursor.execute(sqlQuery)
        connection.commit()

        connection.close()

    def storeData(self, tableName, data):

        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()

        if tableName not in self.tableNames:
            raise ValueError("Invalid table name")
        
        sqlQuery = "INSERT INTO {} ('timestamp', {}) VALUES(datetime('now', 'localtime'), {})".format(tableName, tableName, data)
        cursor.execute(sqlQuery)
        connection.commit()

        connection.close()

