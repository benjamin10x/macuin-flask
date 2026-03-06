from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class AutoparteForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    categoria = StringField('Categoría', validators=[DataRequired()])
    precio = FloatField('Precio', validators=[DataRequired(), NumberRange(min=0)])
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0)])
    descripcion = TextAreaField('Descripción')
    submit = SubmitField('Guardar')