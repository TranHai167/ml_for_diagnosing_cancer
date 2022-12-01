import math

import MySQLdb
import pandas as pd


def get_columns_name(path):
    name = []

    # Get data from excel file
    df = pd.read_excel(r"" + path)
    for i in df.columns:
        name.append(i)
    return name, df


# Get query to create table in mysql with above columns
def query_create_table_sql(path):
    command = 'DROP TABLE IF EXISTS data; CREATE TABLE data (ID INT AUTO_INCREMENT PRIMARY KEY'
    field, df = get_columns_name(path)
    for i in range(len(field)):
        if i <= 20:
            string = field[i] + " TEXT"
        else:
            string = field[i] + " TEXT"
        command = command + ', ' + string
    command += ')  ENGINE = InnoDB CHARSET=utf8mb4 COLLATE utf8mb4_vietnamese_ci;'
    print(command)
    return command, df


# Get query to insert data to table in mysql with above columns
def query_insert_table_sql(path):
    command = 'INSERT INTO data ('
    field, df = get_columns_name(path)
    for i in range(len(field)):
        command = command + field[i]
        if i != len(field) - 1:
            command = command + ', '
    command += ') VALUES ('
    for i in range(len(field)):
        command = command + '%s'
        if i != len(field) - 1:
            command = command + ', '
    command += ')'
    return [command, df]


# Insert to database!
# def transfer_data_to_database():

# Get data in each row and insert it to database:
# Simultaneously get data from 'dienbienngaycuoi' field
def insert_data_to_db(cursor, db, path):
    command, df = query_insert_table_sql(path)
    print(command)
    for r in range(len(df)):
        data = []
        for i in range(len(df.columns)):
            nul = False
            try:
                nul = math.isnan(float(df.iloc[r, i]))
            except:
                data.append(str(df.iloc[r, i]))
                continue
            if nul == True:
                data.append('null')
            else:
                data.append(str(df.iloc[r, i]))

        # Assign values from each row
        values = tuple(data)
        # Execute sql query
        try:
            cursor.execute(command, values)
        except:
            continue


# Get field need to be analysed
def get_data(cursor):
    db_ngay_cuoi = []
    command_get_data = "SELECT dienbiengaydautien FROM data"
    cursor.execute(command_get_data)
    # get all records
    records = cursor.fetchall()
    for row in records:
        db_ngay_cuoi.append(row[0])
    return db_ngay_cuoi


if __name__ == "__main__":
    # This Python file uses the following encoding: utf-8
    database = MySQLdb.connect(host='localhost', user='TranHai', passwd='16072002', db='test')
    mycursor = database.cursor()
    mycursor.execute("DROP TABLE IF EXISTS data")

    path = "C:\\Users\\TRAN NGOC HAI\\PycharmProjects\\pythonProject\\Data.xlsx"

    # Query to create table
    create, df = query_create_table_sql(path)
    mycursor.execute(create)
    mycursor.execute("ALTER TABLE data add UNIQUE(MABN, HOTEN, NGAYVK)")

    # Execute insert into table
    insert_data_to_db(mycursor, database, path)
    db = get_data(mycursor)
    mycursor.close()

    # Commit transaction
    database.commit()

    # Close the db connection
    database.close()
    print("Loaded data to database")
    print("DONE!")
