from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table, Column
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy import select
from sqlalchemy import func
import os


#(18 / 46)
metaData = MetaData()
engine = create_engine("sqlite:///some.db")
user_table = Table('user', metaData,
                   Column('id', Integer, primary_key=True),
                   Column('username', String(50)),
                   Column('fullname', String(50))
                   )

metaData.create_all(engine)

print(user_table.c.fullname == 'ed')
print((user_table.c.fullname == 'ed') & (user_table.c.id > 5))
print((user_table.c.username == 'edward') | ((user_table.c.fullname == 'ed') & (user_table.c.id > 5)))
#результат:  https://github.com/lenok97/WEBprogramming/blob/master/lab%205%20sql/3.1.png

#(27 / 46)
add = user_table.insert().values(username='dilbert', fullname='Dilbert Jones')
connection = engine.connect()
result = connection.execute(add)
print(result)

sel=select([user_table.c.id, user_table.c.username, user_table.c.fullname]).\
    where((user_table.c.username == 'wendy')|(user_table.c.username == 'dilbert')).\
    order_by(user_table.c.fullname)

result=engine.execute(sel)
print(result.fetchall())
#результат: https://github.com/lenok97/WEBprogramming/blob/master/lab%205%20sql/3.2.png


#(38 / 46)
#таблица адресов
address_table = Table("address", metaData,
                      Column('id', Integer, primary_key=True),
                      Column('user_id', Integer, ForeignKey('user.id'), nullable=False),
                      Column('email_address', String(100), nullable=False)
                      )
metaData.create_all(engine)

#данные для проверки запроса
engine.execute(user_table.insert().values(username='ed', fullname='Ed Jones'))
engine.execute(address_table.insert().values(user_id='2', email_address='ed@ed.com'))
engine.execute(address_table.insert().values(user_id='2', email_address='jack@yahoo.com'))

#запрос
sel=select([user_table.c.fullname, address_table.c.email_address]).select_from(user_table.join(address_table)).\
    where(user_table.c.username == 'ed').order_by(address_table.c.email_address)
result=engine.execute(sel)
print(result.fetchall())
#результат: https://github.com/lenok97/WEBprogramming/blob/master/lab%205%20sql/3.3.png

#(46 / 46)
#устанавливаем новое значение fullname для username ed
result=engine.execute(user_table.update().values(fullname="Ed Jones").where(user_table.c.username == "ed"))
print("Обновлено колонок: ", result.rowcount)

sel_address = select([address_table.c.email_address]).\
    where(user_table.c.id == address_table.c.user_id)

result =select([user_table.c.username, sel_address.as_scalar().where(user_table.c.username.in_(['jack', 'wendy']))])
print(engine.execute(result).fetchall())
#результат: https://github.com/lenok97/WEBprogramming/blob/master/lab%205%20sql/3.4.png