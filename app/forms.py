from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired
from app.models import *

class editTreeForm(FlaskForm):
    # id = IntegerField('TreeID', validators=[DataRequired()])
    chieucao = IntegerField('Height of tree', validators=[DataRequired()])
    loaicay = StringField('Kind of tree', validators=[DataRequired()])
    submit = SubmitField('Save')

class editBuildingForm(FlaskForm):
    # id = IntegerField('BuildingID', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    floor = IntegerField('Floors', validators=[DataRequired()])
    addr_house = StringField('Address', validators=[DataRequired()])
    typehouse = StringField('Type house', validators=[DataRequired()])
    square = FloatField('Square',validators=[DataRequired()])
    submit = SubmitField('Save')

