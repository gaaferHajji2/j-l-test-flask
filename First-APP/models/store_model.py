from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80), unique=True, nullable=False, index=True)

    items = db.relationship("ItemModel", back_populates='store', lazy='dynamic')

    tags = db.relationship("TagModel", back_populates='store', lazy='dynamic')

    def add_store_data_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_store_by_name(cls, name: str):
        return cls.query.filter(StoreModel.name == name).first()

    @classmethod
    def get_store_by_id(cls, store_id: int):
        return cls.query.get_or_404(store_id, description=f"No Data Found for store With store_id: {store_id}")

    @classmethod
    def get_all_stores_from_db(cls):
        return cls.query.all()

    def delete_store_from_db(self):
        db.session.delete(self)
        db.session.commit()