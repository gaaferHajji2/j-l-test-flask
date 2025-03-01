from db import db;

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=True, nullable=False)

    password = db.Column(db.String(256), nullable=False)

    @classmethod
    def get_user_by_username(cls, username):
        return cls.query.filter(UserModel.username == username).first()

    @classmethod
    def get_user_by_id(cls, user_id):
        return cls.query.get_or_404(
            user_id,
            description=f"No user Found With ID: {user_id}",
        )

    def save_user_data_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_user_data_by_id(self):
        db.session.delete(self)
        db.session.commit()