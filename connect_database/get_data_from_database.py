import mysql.connector


if __name__ == '__main__':

    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='test',
                                            user='TranHai',
                                            password='16072002')

        sql_select_Query = "select 'dienbienngaydautien' from data"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)

        records = cursor.fetchall()
        co = 0

    except mysql.connector.Error as e:
        print('Error reading data from MySQL table', e)
    finally:
        if connection.is_connected():
            connection.close()
            cursor.close()
            print("MySQL connection is closed")