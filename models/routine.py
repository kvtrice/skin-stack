from setup import db, ma
from marshmallow import fields
from datetime import datetime
from marshmallow.validate import OneOf

VALID_TIMES = ('AM', 'PM')
VALID_DAYS = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')

class Routine(db.Model):
    __tablename__ = 'routines'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.Date(), default=datetime.now().strftime('%Y-%m-%d'))
    day_of_week = db.Column(db.String(20), nullable=False)
    time_of_day = db.Column(db.String(10))
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='routines')

    routine_products = db.relationship('RoutineProduct', back_populates='routines')


class RoutineSchema(ma.Schema):
    user = fields.Nested('UserSchema', exclude=['password'])
    time_of_day = fields.String(validate=OneOf(VALID_TIMES))
    day_of_week = fields.String(validate=OneOf(VALID_DAYS))

    class Meta:
        fields = ('id', 'created_at', 'day_of_week', 'time_of_day', 'user')
