from flask import Flask;
from flask_sqlalchemy import SQLAlchemy;

app = Flask(__name__);

db  = SQLAlchemy();

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/test';

class MakeTransactions1(db.Model):
    __tablename__ = 'table_1';
    
    id = db.Column(db.Integer, primary_key = True);

    name1 = db.Column(db.String(25), nullable=False);

    def __init__(self, name1):
        self.name1 = name1;

class MakeTransactions2(db.Model):
    __tablename__ = 'table_2';
    
    id = db.Column(db.Integer, primary_key = True);

    name1 = db.Column(db.String(25), nullable=False);

    def __init__(self, name1):
        self.name1 = name1;

db.init_app(app);

with app.app_context():
    db.create_all();

    t1 = MakeTransactions1(name1 = 'G1');
    t2 = MakeTransactions2(name1 = 'G2');

    db.session.add(t1);
    db.session.add(t2);

    db.session.commit();
    print(db);

    # db.drop_all();