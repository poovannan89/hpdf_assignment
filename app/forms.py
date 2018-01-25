from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField
from wtforms.validators import DataRequired

class CheckoutForm(FlaskForm):
    amount = DecimalField('amount', validators=[DataRequired()])        
    submit = SubmitField('Paynow')