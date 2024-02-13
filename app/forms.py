# Import necessary components from Flask-WTF and WTForms to create form classes
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length

# Define a form for the checkout process
class CheckoutForm(FlaskForm):
    # Customer's name field with validation for data presence and length constraints
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    # Contact number field with validation for data presence and length constraints
    contact_number = StringField('Contact Number', validators=[DataRequired(), Length(min=10, max=15)])
    # Dummy payment field to simulate entering a credit card number, with length validation
    credit_card_number = StringField('Credit Card Number', validators=[DataRequired(), Length(min=16, max=16)], description="Enter a 16-digit mock credit card number.")
    # Submit button for completing the checkout process
    submit = SubmitField('Complete Checkout')

# Define a form for the admin login process
class AdminLoginForm(FlaskForm):
    # Admin username field with validation for data presence
    username = StringField('Username', validators=[DataRequired()])
    # Admin password field with validation for data presence
    password = PasswordField('Password', validators=[DataRequired()])
    # Submit button for the login form
    submit = SubmitField('Log In')

# Define a form for adding or editing food items by the admin
class FoodItemForm(FlaskForm):
    # Food item's name field with validation for data presence
    name = StringField('Name', validators=[DataRequired()])
    # Food item's price field with validation for data presence
    price = FloatField('Price', validators=[DataRequired()])
    # Optional description field for the food item
    description = TextAreaField('Description') 
    # Field for uploading an image filename associated with the food item
    image_filename = StringField('Images', validators=[DataRequired()])
    # Category selection for the food item, with predefined choices
    category = SelectField('Category', choices=[
        ('Drinks', 'Drinks'),
        ('Sweet', 'Sweet'),
        ('Foods', 'Foods'),
        ('Extras', 'Extras')
    ], validators=[DataRequired()])
    # Submit button for the food item form
    submit = SubmitField('Submit')
