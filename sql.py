import mysql.connector
# from flask_mysqldb import MySQL,MySQLdb

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="vhos"
)

# * working properly ✅
def fetchall(query):
    mycursor = mydb.cursor()
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    mycursor.close()
    return myresult

# * working properly ✅
def fetchall_dict(query):
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    mycursor.close()
    return myresult

def update(statement):
    cs = mydb.cursor()
    cs.execute(statement)
    mydb.commit()
    cs.close()

def insert(q, v):
  mycursor = mydb.cursor()
  sql = q
  val = v
  mycursor.execute(sql, val)
  mydb.commit()


def del_service_db(asp, name):
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='vhos',
                                            user='root')
        cursor = connection.cursor()

        # Delete a record
        sql_Delete_query = f"delete from services where asp_id = '{asp}' AND service_name = '{name}'"
        cursor.execute(sql_Delete_query)
        connection.commit()
        print('number of rows deleted', cursor.rowcount)


    except mysql.connector.Error as error:
        print("Failed to delete record from table: {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def del_asp_db(asp):
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='vhos',
                                            user='root')
        cursor = connection.cursor()

        # Delete a record
        sql_Delete_query = f"delete from asp_data where asp_id = '{asp}'"
        print(sql_Delete_query)
        cursor.execute(sql_Delete_query)
        connection.commit()
        print('number of rows deleted', cursor.rowcount)


    except mysql.connector.Error as error:
        print("Failed to delete record from table: {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def del_vo_db(vo):
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='vhos',
                                            user='root')
        cursor = connection.cursor()

        # Delete a record
        sql_Delete_query = f"delete from owner where email = '{vo}'"
        print(sql_Delete_query)
        cursor.execute(sql_Delete_query)
        connection.commit()
        print('number of rows deleted', cursor.rowcount)


    except mysql.connector.Error as error:
        print("Failed to delete record from table: {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")




def sql(query):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database = "vhos"
    )
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    ret = cursor.fetchall()
    return ret


def sql_data(query):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database = "vhos"
    )
    cursor = db.cursor()
    cursor.execute(query)
    ret = cursor.fetchall()
    return ret


def sql_dict(query):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database = "vhos"
    )
    cursor = db.cursor(dictionary=True)
    cursor.execute(query)
    ret = cursor.fetchall()
    return ret


# ✅ WOrking
def asp_all_requests(query):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database = "vhos"
    )
    cursor = db.cursor(dictionary=True)
    cursor.execute(query)
    ret = cursor.fetchall()
    return ret


def asp_update_services(query):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database = "vhos"
    )

    cursor = db.cursor(dictionary=True)
    cursor.execute(query)
    ret = cursor.fetchall()
    return ret

