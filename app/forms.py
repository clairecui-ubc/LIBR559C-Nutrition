from flask_wtf import Form
from wtforms import StringField, BooleanField,IntegerField, TextField, SubmitField,RadioField
from wtforms import validators,ValidationError
from wtforms.validators import DataRequired, NumberRange,Optional


class IndexNumber(Form):
    index1 = IntegerField('index1',[validators.DataRequired(),validators.NumberRange(min=1,max=122)])
    index2 = IntegerField('index2',[validators.Optional(),validators.NumberRange(min=1,max=122)])
    index3 = IntegerField('index3',[validators.Optional(),validators.NumberRange(min=1,max=122)])
    index4 = IntegerField('index4',[validators.Optional(),validators.NumberRange(min=1,max=122)])
    index5 = IntegerField('index5',[validators.Optional(),validators.NumberRange(min=1,max=122)])
    submit = SubmitField("Calculate")
    gender = RadioField('gender',choices=[('male','male'),('female','female')])

class Recommendation(Form):
    submit=SubmitField('Recommendation')