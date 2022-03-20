from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, DecimalField, SelectField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired


class PropertyForm(FlaskForm):
    title = StringField('Property Title', validators=[
                        DataRequired(), Length(1, 100)])
    desc = TextAreaField('Description', validators=[
                         DataRequired(), Length(1, 300)])
    room_count = IntegerField('No. of Rooms', validators=[DataRequired()])
    bathroom_count = DecimalField(
        'No. of Bathrooms', places=2, validators=[DataRequired()])
    price = DecimalField('Price', places=2, validators=[DataRequired()])
    type = SelectField('Property Type', choices=[
                       'House', 'Apartment'], validators=[DataRequired()])
    location = StringField('Location', validators=[
                           DataRequired(), Length(1, 100)])
    photo = FileField('Photo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
