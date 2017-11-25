from sqlalchemy import create_engine

engine = create_engine("sqlite:///some.db")

engine.execute("""DROP TABLE employee """)
#создание таблицы employee
engine.execute("""CREATE TABLE employee (
    emp_id integer primary key,
    emp_name varchar(30)
    )""")
#INSERT, которая вставляет строку с emp_name = 'dilbert'; 
#первичный ключ не указываем - он генерируется автоматически
engine.execute("""INSERT into employee(emp_name) values ('dilbert')""")

#выбираем все строки и столбцы таблицы
result = engine.execute("SELECT * from employee")
#вывод результата 
print(result.fetchall)

