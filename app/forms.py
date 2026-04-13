from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    FloatField as _FloatField,
    IntegerField as _IntegerField,
    TextAreaField,
    SubmitField,
)
from wtforms.validators import DataRequired, InputRequired, NumberRange, Length


class FloatField(_FloatField):
    """FloatField con mensaje de error en español."""
    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = float(valuelist[0].replace(',', '.'))
            except (ValueError, TypeError):
                self.data = None
                raise ValueError('Ingrese un número válido (ej. 99.99).')


class IntegerField(_IntegerField):
    """IntegerField con mensaje de error en español."""
    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = int(valuelist[0])
            except (ValueError, TypeError):
                self.data = None
                raise ValueError('Ingrese un número entero válido.')

class AutoparteForm(FlaskForm):
    nombre = StringField(
        'Nombre',
        validators=[
            DataRequired(message='El nombre es obligatorio.'),
            Length(min=2, max=200, message='El nombre debe tener entre 2 y 200 caracteres.'),
        ],
    )
    categoria = StringField(
        'Categoría',
        validators=[
            DataRequired(message='La categoría es obligatoria.'),
            Length(max=100, message='La categoría no debe exceder 100 caracteres.'),
        ],
    )
    precio = FloatField(
        'Precio',
        validators=[
            InputRequired(message='El precio es obligatorio.'),
            NumberRange(min=0, message='El precio debe ser un valor mayor o igual a 0.'),
        ],
    )
    stock = IntegerField(
        'Stock',
        validators=[
            InputRequired(message='El stock es obligatorio.'),
            NumberRange(min=0, message='El stock no puede ser negativo.'),
        ],
    )
    descripcion = TextAreaField('Descripción')
    submit = SubmitField('Guardar')