from flask import Flask;
from flask_sqlalchemy import SQLAlchemy;
from sqlalchemy.dialects.mysql import TINYINT;

app = Flask(__name__);
db  = SQLAlchemy();

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost:3306/test?charset=utf8';

class a(db.Model):
    __tablename__ = 'a';
    id = db.Column(db.Integer, primary_key=True);
    tinyint = db.Column(TINYINT, nullable=False);
    text_data = db.Column(db.TEXT(collation='utf8mb4_unicode_ci'), nullable=False);
    string_here = db.Column(db.String(250, collation='utf8mb4_unicode_ci'), nullable=False);

    def __init__(self, tiny, text, string_h):
        self.tinyint=tiny;
        self.text_data = text;
        self.string_here = string_h;

    def add(self):
        with app.app_context():
            db.session.add(self);
            db.session.commit();

db.init_app(app);

@app.before_first_request
def create_all_tables():
    print("---- CREATE ALL TABLES ----");
    db.create_all();

with app.app_context():
    create_all_tables();
    
    test1= a(1, "Small Text Here", "جعفر حجي 1");
    test1.add();

    test2= a(3, "تم التغيير الآن", "جعفر حجي 2");
    test2.add();

    print(db);

# app.run(port=5000, debug=True);


