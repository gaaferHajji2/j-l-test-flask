from flask import Flask;

from flask_sqlalchemy import SQLAlchemy;

from sqlalchemy.dialects.mysql import INTEGER, TINYINT, FLOAT;

app = Flask(__name__);

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/test';

db = SQLAlchemy();

"""
Unsigned is a special mysql extension to integers. To use it with sqlalchemy 
/ flask-sqlalchemy you have to import it from the mysql dialect extension.

from sqlalchemy.dialects.mysql import BIGINT

db.Column(BIGINT(unsigned=True))
"""

class TestUnsignedInteger(db.Model):
    __tablename__ = 'test-12';

    id = db.Column(db.Integer, primary_key= True);

    col1 = db.Column(INTEGER(unsigned=True), nullable=False);
    col2 = db.Column(TINYINT(unsigned=True), nullable=False);
    col3 = db.Column(FLOAT(unsigned=True), nullable=False);
    col4 = db.Column(db.Date, nullable=False);
    col5 = db.Column(db.Time, nullable=False);
    name = db.Column(db.String(25), nullable=False);

    def __init__(self, col1, col2, col3, col4, col5, name):
        self.col1 = col1;
        self.col2 = col2;
        self.col3 = col3;
        self.col4 = col4;
        self.col5 = col5;
        self.name = name;

    def add(self):
        db.session.add(self);
        db.session.commit();

db.init_app(app);

with app.app_context():
    db.create_all();

    a = TestUnsignedInteger(col1= 300000000, col2=250, col3=25.95, col4='2023-12-12', col5='05:30', name='JafarLoka');
    a.add();

    print(a);
    print(db);

