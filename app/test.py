import pymssql
from app.util import *

class SQL_Server():
    def __init__(self, server='(local)', user='sa', password='18340014', database='bookstore', autocommit=True):
        # self.host = host
        self.server = server
        self.user = user
        self.password = password
        self.database = database
        self.autocommit = autocommit

        self.tableList = None
        self.attributeList = None

    def connection(self):
        connect = pymssql.connect(user=self.user, password=self.password, database=self.database,
                               autocommit=self.autocommit)
        return connect

    def tableDetect(self, tablename):
        # update table and attribute
        self.getTAList()

        if tablename in self.tableList:
            return True
        return False

    def getTableList(self):
        # get table list
        connect = self.connection()
        cursor = connect.cursor()
        cursor.execute("SELECT Name FROM SysObjects WHERE XType='U' ORDER BY Name")
        self.tableList = cursor.fetchall()
        for i in range(len(self.tableList)):
            self.tableList[i] = self.tableList[i][0]
        cursor.close()
        connect.close()

    def getAttributeList(self):
        # get attribute list for each table
        connect = self.connection()
        cursor = connect.cursor()
        self.attributeList = []
        for table in self.tableList:
            cursor.execute("SELECT column_name FROM information_schema.COLUMNS WHERE table_name='" + table + "'")
            temp = cursor.fetchall()
            for i in range(len(temp)):
                temp[i] = temp[i][0]
            self.attributeList.append(temp)
        cursor.close()
        connect.close()

    def getAttributeListOfTable(self, table):
        index = getIndex(table, self.tableList)
        return self.attributeList[index]

    def getAttributeListForSelectShow(self, table, attribute):
        if attribute == '*':
            return self.getAttributeListOfTable(table)
        return [attribute]

    def getTAList(self):
        # get table list
        self.getTableList()

        # get attribute list for each table
        self.getAttributeList()

    def ifManager(self, username, password):
        connect = self.connection()
        cursor = connect.cursor()
        username = "'" + username + "'"
        password = "'" + password + "'"
        cursor.execute('SELECT * FROM BSUSER WHERE Username = ' + username + ' and Password = ' + password + ';')
        results = cursor.fetchall()[0]
        return results[3]

    def loginDetect(self, username, password):
        connect = self.connection()
        cursor = connect.cursor()
        username = "'" + username + "'"
        password = "'" + password + "'"
        cursor.execute('SELECT * FROM BSUSER WHERE Username = ' + username + ' and Password = ' + password + ';')
        results = cursor.fetchall()
        cursor.close()
        connect.close()
        return results

    def register(self, username, password, address):
        # try to insert (username, password) into USERTABLE
        connect = self.connection()
        cursor = connect.cursor()
        username = "'" + username + "'"
        password = "'" + password + "'"
        address = "'" + address + "'"
        statement = '(' + username + ', ' + password + ',' + address + ',' + '0 )'
        cursor.close()
        connect.close()
        return self.insertIntoTable('BSUSER', statement)

    def selectFromTable(self, table, toBeSelected):
        # 'toBeSelected' in form of '*' or '(XXXX,....)'
        # update table and attribute
        self.getTAList()

        statement = toBeSelected

        connect = self.connection()
        cursor = connect.cursor()
        try:
            # if table == 'MAKE' or table == 'ASSEMBLE':
            #     cursor.execute('SELECT ' + attribute + ' FROM ' + table + ' order by date desc')
            # else:
            cursor.execute('SELECT ' + statement + ' FROM ' + table)
            results = cursor.fetchall()
            print(results)
            return results
        except Exception as e:
            print('No such query, input again')
        else:
            index = getIndex(table, self.tableList)
            showResults(table, self.attributeList[index], attribute, results)
        finally:
            cursor.close()
            connect.close()

    def insertIntoTable(self, table, toBeInserted):
        # 'toBeInserted' in form of "('XXXX','XXX',...)"
        # update table and attribute
        self.getTAList()

        statement = toBeInserted

        connect = self.connection()
        cursor = connect.cursor()
        try:
            cursor.execute('INSERT INTO ' + table + ' VALUES ' + statement)
        except Exception as e:
            print('Something error')
            return '失败'
        else:
            print('Succeed')
            return '成功'
        finally:
            cursor.close()
            connect.close()

    def deleteFromUserTable(self, table, toBeDeleted):
        # 'toBeDeleted' in form of "XXXX='XXX'"
        # update table and attribute
        self.getTAList()

        statement = toBeDeleted

        connect = self.connection()
        cursor = connect.cursor()
        try:
            cursor.execute('DELETE FROM ' + table + ' WHERE ' + statement)
        except Exception as e:
            print('Something error, please input again')
            return '失败'
        else:
            print('Succeed or no such value')
            return '成功'
        finally:
            cursor.close()
            connect.close()

    def updateTable(self, table, toBeUpdated, pending):
        # 'toBeUpdated' in form of
        # update table and attribute
        self.getTAList()

        statement1 = toBeUpdated
        statement2 = pending

        connect = self.connection()
        cursor = connect.cursor()
        try:
            cursor.execute('UPDATE ' + table + ' SET ' + statement1 + ' WHERE ' + pending)
        except Exception as e:
            print('Something error')
            return '失败'
        else:
            print('Succeed')
            return '成功'
        finally:
            cursor.close()
            connect.close()

    def dropTable(self, table):
        # update table and attribute
        self.getTAList()

        connect = self.connection()
        cursor = connect.cursor()
        try:
            cursor.execute('DROP TABLE ' + table)
        except Exception as e:
            print('Something error, please input again')
            return '失败'
        else:
            print('Succeed')
            return '成功'
        finally:
            cursor.close()
            connect.close()

    # def getAuthorID(self):
    #     results = self.selectFromTable('AUTHOR', 'AuthorID')
    #     id = []
    #     for res in results:
    #         id.append(res[0])
    #     return id
    #
    # def getUserID(self):
    #     results = self.selectFromTable('BSUSER', 'Username')
    #     id = []
    #     for res in results:
    #         id.append(res[0])
    #     return id
    #
    # def getBookID(self):
    #     results = self.selectFromTable('BOOK', 'ISBN')
    #     id = []
    #     for res in results:
    #         id.append(res[0])
    #     return id

def main():
    sql = SQL_Server()
    sql.insertIntoTable('AUTHOR', "('1834001405','Chen')")
    sql.insertIntoTable('AUTHOR', "('1834001414','Ning')")
    sql.selectFromTable('AUTHOR', '*')
    sql.updateTable('AUTHOR', "Authorname='Jia'", "AuthorID='1834001405'")
    sql.selectFromTable('AUTHOR', '*')
    sql.deleteFromUserTable('AUTHOR', "AuthorID='1834001405'")
    sql.selectFromTable('AUTHOR', '*')
    sql.deleteFromUserTable('AUTHOR', "AuthorID='1834001414'")
    sql.selectFromTable('AUTHOR', '*')


if __name__ == '__main__':
    main()