from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Corrected the relationship name to 'reviews' (plural)
    reviews = relationship('Review', back_populates='customer')
    items = association_proxy('reviews', 'item')

    _serialization_rules = {
        'reviews': {'exclude': ['customer']}
    }

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'
    
class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    # Corrected the relationship name to 'reviews' (plural)
    reviews = relationship('Review', back_populates='item')

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    customer_id = db.Column(db.Integer, ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, ForeignKey('items.id'))

    # Corrected the back references to 'reviews' (plural)
    customer = relationship('Customer', back_populates='reviews')
    item = relationship('Item', back_populates='reviews')

    def __repr__(self):
        return f'<Review {self.id}, Customer {self.customer_id}, Item {self.item_id}>'
    
