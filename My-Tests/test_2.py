#### NOTE VERY IMPORTANT ###
#### we should be careful when define and set db.init_app(flask_app);
#### db.init_app() can't be set with app.app_context().

from flask import Flask;

from flask_sqlalchemy import SQLAlchemy;

app = Flask(__name__);
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root@localhost:3306/test?charset=utf8";

db = SQLAlchemy();

class UserModel(db.Model):
    __tablename__= 'users_2';

    id = db.Column(db.Integer, primary_key=True);
    
    name = db.Column(db.String(25, collation='utf8mb4_unicode_ci'), nullable=False);

    profile = db.relationship('ProfileModel', uselist=False);

    def __init__(self, name):
        self.name=name;

    def add(self):
        db.session.add(self);
        db.session.commit();
    

class ProfileModel(db.Model):
    __tablename__ = 'profiles';
    
    id = db.Column(db.Integer, primary_key=True);
    bio = db.Column(db.TEXT(collation='utf8mb4_unicode_ci'), nullable=False);
    
    user_id = db.Column(db.Integer, db.ForeignKey('users_2.id'));
    user = db.relationship('UserModel', uselist=False);

    def __init__(self, bio):
        self.bio = bio;

    def add(self):
        db.session.add(self);
        db.session.commit();

db.init_app(app);

@app.before_first_request
def create_all_tables():
    print("---- Create All Tables ---");
    db.create_all();

with app.app_context():
    create_all_tables();
    user = UserModel(name='Jafar Hajji');
    profile = ProfileModel(bio='جعفر حجي هنا');

    user.profile = profile;

    profile.add();
    user.add();

    temp1 = db.session.get(UserModel, 1);
    print(temp1);
    print(temp1.profile.bio);

    temp2 = db.session.get(ProfileModel, 1);
    print(temp2);
    print(temp2.user.name);


# print(db);

# app.run(port=5000, debug=True);
    
    
