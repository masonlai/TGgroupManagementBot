import sqlite3


def connect():
    con = sqlite3.connect('tg.db')
    # cur = con.cursor()
    return con


def disconnect(con):
    con.commit()
    con.close()


def updatelist(id):
    con = connect()
    cur = con.cursor()
    insertSQL = 'insert into callList VALUES ({});'.format(id)
    cur.execute(insertSQL)
    disconnect(con)

def updateApprover(id):
    con = connect()
    cur = con.cursor()
    insertSQL = 'insert into approver VALUES ({});'.format(id)
    cur.execute(insertSQL)
    disconnect(con)


def deleteCallList(id):
    con = connect()
    cur = con.cursor()
    insertSQL = 'delete from callList where id == {};'.format(id)
    cur.execute(insertSQL)
    disconnect(con)


def deleteApproveList(id):
    con = connect()
    cur = con.cursor()
    insertSQL = 'delete from approver where id == {};'.format(id)
    cur.execute(insertSQL)
    disconnect(con)


def getCallList():
    con = connect()
    cur = con.cursor()

    cur.execute("SELECT * FROM callList")

    rows = cur.fetchall()

    returnList =[]
    for i in rows:
        returnList.append(i[0])

    return returnList

def getApprovers():
    con = connect()
    cur = con.cursor()

    cur.execute("SELECT * FROM approver")

    rows = cur.fetchall()
    returnList =[]
    for i in rows:
        returnList.append(i[0])

    return returnList
