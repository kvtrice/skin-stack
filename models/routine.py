from setup import db, ma
from marshmallow import fields
from datetime import datetime

class Routine(db.Model):
    __tablename__ = 'routines'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.Date(), default=datetime.now().strftime('%Y-%m-%d'))
    day_of_week = db.Column(db.String(20), nullable=False)
    time_of_day = db.Column(db.String(10))
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='routines')

class RoutineSchema(ma.Schema):
    user = fields.Nested('UserSchema', exclude=['password'])

    class Meta:
        fields = ('id', 'created_at', 'day_of_week', 'time_of_day', 'user')