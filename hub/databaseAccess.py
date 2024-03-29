import sqlite3
from constant import TEMPERATURE, MOISTURE, SOILPH, SALINITY, DATABASE_NAME

class DatabaseAccess:
    
    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_NAME)
        self.cursor = self.connection.cursor()
        self.tableNames = [TEMPERATURE, MOISTURE, SOILPH, SALINITY]

        self.initializeTableIfNotExist()

    def initializeTableIfNotExist(self):
        for table in self.tableNames:
            if not self.tableExists(table):
                self.createTable(table)

    def tableExists(self, tableName):
        sqlQuery = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}'".format(tableName)
        self.cursor.execute(sqlQuery)
        return self.cursor.fetchone()
        
    def createTable(self, tableName):
        sqlQuery = '''CREATE TABLE {} (
                    id INTEGER PRIMARY KEY,
                    timestamp TEXT,
                    {} REAL,
                )'''.format(tableName, tableName)
        self.cursorexecute(sqlQuery)
        self.connection.commit()

    def storeData(self, tableName, data):
        if tableName not in self.tableNames:
            raise ValueError("Invalid table name")
        
        sqlQuery = "INSERT INTO {} ('timestamp', {}) VALUES(datetime('now', 'localtime'), {})".format(tableName, tableName, data)
        self.cursor(sqlQuery)
        self.connection.commit()



