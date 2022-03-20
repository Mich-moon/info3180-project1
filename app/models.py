from . import db


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prop_title = db.Column(db.String(100), nullable=False, unique=True)
    prop_desc = db.Column(db.String(300), nullable=False)
    prop_room_count = db.Column(db.Integer, nullable=False)
    prop_bathroom_count = db.Column(db.Float, nullable=False)
    prop_price = db.Column(db.Float, nullable=False)
    prop_type = db.Column(db.String(10), nullable=False)
    prop_location = db.Column(db.String(100), nullable=False)
    prop_photo = db.Column(db.String(500), nullable=False)

    def __init__(self, prop_title, prop_desc, prop_room_count, prop_bathroom_count, prop_price, prop_type, prop_location, prop_photo):
        self.prop_title = prop_title
        self.prop_desc = prop_desc
        self.prop_room_count = prop_room_count
        self.prop_bathroom_count = prop_bathroom_count
        self.prop_price = prop_price
        self.prop_type = prop_type
        self.prop_location = prop_location
        self.prop_photo = prop_photo

    def __repr__(self):
        return '<Property %r>' % self.prop_title
