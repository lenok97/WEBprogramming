from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table, Column
#импортируем необходимые типы
from sqlalchemy import Integer, String, DateTime, ForeignKey, Unicode, UnicodeText, ForeignKeyConstraint
#task 2 (слайд 13 / 20)
engine = create_engine("sqlite:///some.db")
metadata = MetaData()

#конструкторы таблиц по шаблону:
network_table = Table('network', metadata,
                      Column('network_id', Integer, primary_key=True),
                      Column('name', String(100), nullable=False),
                      Column('created_at', DateTime, nullable=False),
                      Column('owner_id', ForeignKey('user.id'))
                      )

user_table = Table('user', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('name', String),
                   Column('fullname', String)
                   )

story_table = Table('story', metadata,
                    Column('story_id', Integer, primary_key=True),
                    Column('version_id', Integer, primary_key=True),
                    Column('headline', Unicode(100), nullable=False),
                    Column('body', UnicodeText)
                    )

published_table = Table('published', metadata,
                        Column('pub_id', Integer, primary_key=True),
                        Column('pub_timestamp', DateTime, nullable=False),
                        Column('story_id', Integer),
                        Column('version_id', Integer),
                        ForeignKeyConstraint(['story_id', 'version_id'],['story.story_id', 'story.version_id'])
                        )

metadata.create_all(engine)

#task 2 (слайд 20 / 20)
from sqlalchemy import inspect 

metadata2 = MetaData()
network_reflected = Table('network', metadata2, autoload=True, autoload_with=engine)

inspector = inspect(engine)

#находим таблицы, содержащие колнки story_id
for table in  inspector.get_table_names():
    for column in inspector.get_columns(table):
        if column ['name'] == 'story_id':
            print (table)

#результат: https://github.com/lenok97/WEBprogramming/blob/master/lab%205%20sql/2.png


