from flask import Flask;
from flask_sqlalchemy import SQLAlchemy;
from sqlalchemy.dialects.mysql import JSON;

from sqlalchemy import or_;

app = Flask(__name__);
db = SQLAlchemy();

# db.session.query(Example).\
#    filter(Example.json_field['id'].astext.cast(Integer) == 1)
"""
The same applies to all types that cannot be directly cast from json. SQLAlchemy 
used to offer a shortcut for the combination of astext and cast(), but it has 
been removed in version 1.1 and above:

Changed in version 1.1: The ColumnElement.cast() operator on JSON objects now requires 
that the JSON.Comparator.astext modifier be called explicitly, 
if the cast works only from a textual string.

https://stackoverflow.com/questions/53264047/sqlalchemy-filter-by-json-field
"""

# filter(or_(User.name == v for v in ('Alice', 'Bob', 'Carl')))

# If you already have a collection then you should use the in_ operator like this: 
# filter(User.name.in_(['Alice', 'Bob', 'Carl']))

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root@localhost:3306/test?charset=utf8";

class TestColumns(db.Model):
    __tablename__ = 'test_columns';

    id = db.Column(db.Integer, primary_key = True);
    name = db.Column(db.String(20), nullable=False);
    col1_test = db.Column(JSON, nullable=False);

    def __init__(self, name, col1_test):
        self.name = name;
        self.col1_test = col1_test;

    def add(self):
        db.session.add(self);
        db.session.commit();

    def __str__(self):
        return "<Data Of Column is>{0} is: {1}".format(self.name, self.col1_test);

db.init_app(app);


with app.app_context():
    db.create_all();
    # a = TestColumns(name='Jafar Hajji', col1_test={'from': 'a', 'to': 'b'});
    # b = TestColumns(name='Jafar Hajji', col1_test={'from': 'c', 'to': 'd'});
    # c = TestColumns(name='Jafar Hajji', col1_test={'from': 'e', 'to': 'f'});
    # a.add();
    # b.add();
    # c.add();

    # This is Like And Operation.
    data = db.session.query(TestColumns).filter(
        TestColumns.col1_test['from'] == 'a', 
    );
    print(data.first());

    data = db.session.query(TestColumns).filter(
        or_(
            TestColumns.col1_test['from'] == 'a',
            TestColumns.col1_test['to'] == 'd'
        )
    );

    print('-'*15);

    for res in data.all():
        print(res);
# print(db);