
#!/usr/bin/python3
#mysql_adc.py
import sqlite3
import datetime
import data_local as dataDevice
import time
import os

DEBUG=True
SHOWSQL=True
CLEARDATA=False
VAL0=0;VAL1=1;VAL2=2;VAL3=3 #Set data order
FORMATBODY="%5s %8s %14s %12s %16s"
FORMATLIST="%5s %12s %10s %16s %7s"
DATEBASE_DIR="/var/databases/datasite/"
DATEBASE=DATEBASE_DIR+"mydatabase.db"
TABLE="recordeddata"
DELAY=1 #approximate seconds between samples

def captureSamples(cursor):
    if(CLEARDATA):cursor.execute("DELETE FROM %s" %(TABLE))
    myData = dataDevice.device()
    myDataNames=myData.getName()

    if(DEBUG):print(FORMATBODY%("##",myDataNames[VAL0],
                                myDataNames[VAL1],myDataNames[VAL2],
                                myDataNames[VAL3]))
    for x in range(10):
        data=myData.getNew()
        for i,dataName in enumerate(myDataNames):
            sqlquery = "INSERT INTO %s (itm_name, itm_value) " %(TABLE) + \
                       "VALUES('%s', %s)" \
                        %(str(dataName),str(data[i]))
            if (SHOWSQL):print(sqlquery)
            cursor.execute(sqlquery)
#            cursor.execute("INSERT INTO ? (itm_name, itm_value) VALUES('?', ?)",
#                        (TABLE,str(dataName),data[i]))
#            cursor.execute("INSERT INTO ? (itm_name, itm_value) VALUES('?', ?)",
#                        (str(TABLE),str(dataName),str(data[i])))
##            sqlquery = "INSERT INTO %s (itm_name, itm_value) VALUES(?, ?)" %(TABLE)
#           sqlquery = "INSERT INTO ? (itm_name, itm_value) VALUES(?, ?)"
##            cursor.execute(sqlquery,(str(dataName),str(data[i])))

        if(DEBUG):print(FORMATBODY%(x,
                                    data[VAL0],data[VAL1],
                                    data[VAL2],data[VAL3]))
        time.sleep(DELAY)
    cursor.commit()

def displayAll(connect):
    sqlquery="SELECT * FROM %s" %(TABLE)
    if (SHOWSQL):print(sqlquery)
    cursor = connect.execute (sqlquery)
    print(FORMATLIST%("","Date","Time","Name","Value"))

    for x,column in enumerate(cursor.fetchall()):
       print(FORMATLIST%(x,str(column[0]),str(column[1]),
                         str(column[2]),str(column[3])))

def createTable(cursor):
    print("Create a new table: %s" %(TABLE))
    sqlquery="CREATE TABLE %s (" %(TABLE) + \
             "itm_date DEFAULT (date('now','localtime')), " + \
             "itm_time DEFAULT (time('now','localtime')), " + \
             "itm_name, itm_value)" 
    if (SHOWSQL):print(sqlquery)
    cursor.execute(sqlquery)
    cursor.commit()

def openTable(cursor):
    try:
        displayAll(cursor)
    except sqlite3.OperationalError:
        print("Table does not exist in database")
        createTable(cursor)
    finally:
        captureSamples(cursor)
        displayAll(cursor)

try:
    if not os.path.exists(DATEBASE_DIR):
        os.makedirs(DATEBASE_DIR)
    connection = sqlite3.connect(DATEBASE)
    try:
        openTable(connection)
    finally:
        connection.close()
except sqlite3.OperationalError:
    print("Unable to open Database")
finally:
    print("Done")

#End
