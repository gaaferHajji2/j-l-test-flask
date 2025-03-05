from flask import Flask;

from flask_sqlalchemy import SQLAlchemy;

app = Flask(__name__);
db = SQLAlchemy();

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/test?charset=utf8';

class Test1(db.Model):
    __tablename__ = "Test-G-01";

    id = db.Column(db.Integer, primary_key=True);

    t_type = db.Column(db.String(50), nullable=False);

    def __init__(self, t_type):
        self.t_type = t_type;

    def add(self):
        db.session.add(self);
        db.session.commit();

    def __str__(self):
        return self.t_type;

db.init_app(app=app);

with app.app_context():
    print("-"*15, "   TABLE CREATED   ", '-'*15);
    db.create_all();
    print("-"*15, "   TABLE CREATED   ", '-'*15);

    t1 = Test1(t_type="Gaafer 1 is Normal User");
    t1.add();

    t1.t_type = "Jafar Loka 01 is Admin User";
    db.session.commit();

    t1 = Test1(t_type="Jafar Loka 02  Admin User");
    t1.add();

    t1 = Test1(t_type="Jafar Loka 03  is Comapny User");
    t1.add();

    data = Test1.query.first();
    print(data);
    
    t2 = db.session.query(Test1).order_by(Test1.id.desc()).first();
    print(t2);