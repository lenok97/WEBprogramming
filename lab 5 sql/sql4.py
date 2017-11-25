from sqlalchemy import create_engine, func, select
from sqlalchemy import MetaData,Column
from sqlalchemy import Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import aliased
import os

metaData = MetaData()
engine = create_engine("sqlite:///some.db")
base = declarative_base()

#класс для таблицы network
class Network(base):
    __tablename__ = 'network'
    network_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    def __repr__(self):
        return "<Network(%r)>" % (self.name)

#класс для таблицы user
class User(base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    def __repr__(self):
        return "<User(%r, %r)>" % (self.name, self.fullname)

#класс для таблицы address
class Address(base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", backref="addresses")
    def __repr__(self):
        return "<Address(%r)>" % self.email_address

#класс для таблицы account
class Account(base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    owner = Column(String(50), nullable = False)
    balance = Column(Numeric, default=0)
    def __repr__(self):
        return "<Account(%r, %r)>" % (self.owner, self.balance)


#класс для таблицы transaction
class Transaction(base):
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key=True)
    amount = Column(Numeric, nullable=False)
    account_id = Column(Integer, ForeignKey(Account.__tablename__ + '.id'), nullable=False)
    account = relationship('Account', backref="transactions")
    def __repr__(self):
        return "Transaction: %r" % (self.amount)


#создание таблицы network в some.db
base.metadata.create_all(engine)


#(25 / 72)
session = Session(bind=engine)
session.add_all([
    Network(name='net1'),
    Network(name='net2')
])
session.commit()

#(43 / 72)
session.add_all([
    User(name='wendy', fullname='Wendy Weathersmith'),
    User(name='mary', fullname='Mary Contrary'),
    User(name='fred', fullname='Fred Flinstone'),
    User(name='ed', fullname='Ed Jones')
])
session.commit()

#запрос который возвращает все значения fullname в алфавитном порядке
query = session.query(User.fullname).order_by(User.fullname)
print("the list of 'fullname' values for all User objects in alphabetical order: \n", query.all())

#запрос, который возвращает только пользователей с именем "mary" или "ed"
query = query.filter(User.name.in_(['mary','ed']))
print("only User rows with the name 'mary' or 'ed'", query.all())
#вывести 2ую строку последнего запроса
print("#2: ", query[1])

#(62 / 72)
#добавим данные для теста запросов
jack = User(name='jack', fullname='Jack Bean')
jack.addresses = [Address(email_address='jack@gmail.com'),
                  Address(email_address='j25@yahoo.com'),
                  Address(email_address='jack@hotmail.com')]
session.add(jack)
session.commit()

query = session.query(User.name, Address.email_address).join(Address).filter(Address.email_address=="j25@yahoo.com")
print ("join: \n",query.all())

user_alias1 = aliased(User)
user_alias2 = aliased(User)

query=engine.execute(select([user_alias1.name, user_alias2.name]).distinct().where(user_alias1.name < user_alias2.name))
print ("Select all pairs of distinct user names: \n", query.fetchall())

#результаты https://github.com/lenok97/WEBprogramming/blob/master/lab%205%20sql/4.png

#(72 / 72)
account1=Account(owner = "Jack Jones", balance = 5000)
account2=Account(owner="Ed Rendell", balance=10000)
session.add_all([
    account1,
    account2,
    Transaction(amount=500, account=account1),
    Transaction(amount=4500, account=account1),
    Transaction(amount=6000, account=account2),
    Transaction(amount=4000, account=account2)])
session.commit()


for account in session.query(Account).all():
    print(account.owner)
    print(account.balance)
    sum = 0
    for acc in account.transactions:
        sum += acc.amount
    print(sum)

#результаты https://github.com/lenok97/WEBprogramming/blob/master/lab%205%20sql/4ex.png

session.close()
os.remove("some.db")