# from sqlalchemy import desc
from db import db

# The Column.default and Column.onupdate keyword 
# arguments also accept Python functions. 
# These functions are invoked at the time of 
# insert or update if no other value for 
# that column is supplied, and the value returned 
# is used for the column’s value.

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80), index=True, nullable=False)

    price = db.Column(db.Float(precision=2), nullable=False)

    description = db.Column(db.String)

    store_id = db.Column(db.Integer, 
                        db.ForeignKey('stores.id'), 
                        nullable=False
                )

    store= db.relationship("StoreModel", back_populates='items')

    tags = db.relationship(
        'TagModel', 
        back_populates='items', 
        secondary='items_tags',
    )

    __table_args__ = (
        db.UniqueConstraint('name', 'store_id', name="item_name_store_id_uc"),
    )

    def add_item_data_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_item_by_name(cls, name):
        return cls.query.filter(ItemModel.name == name).first()

    @classmethod
    def get_item_by_id(cls, item_id: int):
        # return cls.query.get(item_id);
        return cls.query.get_or_404(item_id, 
        
        description=f"No Data Found for ID: {item_id}")

    @classmethod
    def get_all_items_in_db(cls):
        return cls.query.all()

    def update_item_in_db(self, name: str, price: float):
        self.name = name
        self.price = price

        db.session.commit()

    def delete_item_from_db(self):
        db.session.delete(self)
        db.session.commit()

