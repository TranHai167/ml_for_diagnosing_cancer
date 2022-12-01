import mysql.connector

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='test',
                                         user='TranHai',
                                         password='16072002')

    sql_select_Query = 'select username from php_databse'
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)

    # get all records
    records = cursor.fetchall()

    print('Total number of rows in table: ', cursor.rowcount)
    print('\nPrinting each row')
    for row in records:
        print('name: ', row[0])


except mysql.connector.Error as e:
    print('Error reading data from MySQL table', e)
finally:
    if connection.is_connected():
        connection.close()
        cursor.close()
        print("MySQL connection is closed")