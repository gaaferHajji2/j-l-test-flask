from db import db

class TagModel(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80), nullable=False, unique=True)

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=True)
    
    store = db.relationship('StoreModel', back_populates='tags')

    items = db.relationship(
        'ItemModel', 
        back_populates='tags', 
        secondary='items_tags',
    )

    __table_args__ = (
        db.UniqueConstraint('name', 'store_id', name="tag_name_store_id_uc"),
    )


    @classmethod
    def get_tag_by_name(cls, name: str):
        return cls.query.filter(TagModel.name == name).first()

    @classmethod
    def get_tag_by_name_and_store_if(cls, name: str, store_id: int):
        return cls.query.filter(TagModel.name == name, TagModel.store_id == store_id).first()

    @classmethod
    def get_tag_by_id(cls, id: int):
        return cls.query.get_or_404(
            id, 
            description=f"No tag With Id: {id}"
        )

    def save_tag_to_db(self):
        db.session.add(self)
        db.session.commit()