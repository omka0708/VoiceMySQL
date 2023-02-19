import pymysql.cursors

host = "localhost"
user = "root"
port = 3306
password = "omka2061"
database = "db"

limit_rows = 1000

try:
    connection = pymysql.connect(
        host=host, user=user, password=password, database=None, port=port, cursorclass=pymysql.cursors.DictCursor
    )
    print(f"Соединение установлено ...")

    while True:
        request = input('\nВведите SQL-запрос (или \'exit\' для остановки):\n\n')
        if request == 'exit':
            break
        try:
            with connection.cursor() as cursor:
                affected_rows = cursor.execute(request)
                print(f'Количество использованных строк: {affected_rows}')
                connection.commit()
                rows = cursor.fetchmany(limit_rows)
                print(*rows, sep='\n')
        except Exception as e:
            print(f'Ошибка в запросе ... \n{e}')

except Exception as e:
    print(f"Соединение разорвано ... \n{e}")
