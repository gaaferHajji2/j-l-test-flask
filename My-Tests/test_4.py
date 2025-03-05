from flask import Flask;
from flask_sqlalchemy import SQLAlchemy;

from sqlalchemy.dialects.mysql import FLOAT;

app = Flask(__name__);

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/test?charset=utf8';

db  = SQLAlchemy();

class TestFloat(db.Model):
    __tablename__ = 'test_floats';

    id = db.Column(db.Integer, primary_key=True);

    floatValue = db.Column(db.Float, nullable=False, default=1.0);
    name = db.Column(db.String(25), nullable=False);

    def __init__(self, floatValue, name):
        self.name = name;
        self.floatValue = floatValue;

    def add(self):
        db.session.add(self);
        db.session.commit();

    def __str__(self):
        return "The Name is: {0} For Float Value is: {1}".format(self.floatValue, self.name);

db.init_app(app);

with app.app_context():

    db.create_all();

    a = TestFloat(floatValue=25.23, name='Jafar Hajji');
    a.add();

    print(db);
    print(a);