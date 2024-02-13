from app import db  # Import the SQLAlchemy instance from Flask app
from datetime import datetime  # Import datetime module to use for timestamping

# Define the FoodItem model to represent food items in the database
class FoodItem(db.Model):
    # Define the columns for the FoodItem table
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each food item
    name = db.Column(db.String(100), nullable=False)  # Name of the food item, cannot be null
    description = db.Column(db.String(250), nullable=True)  # Optional description of the food item
    price = db.Column(db.Float, nullable=False)  # Price of the food item, cannot be null
    category = db.Column(db.String(100), nullable=False)  # Category of the food item, cannot be null
    image_filename = db.Column(db.String(100), nullable=True)  # Optional filename for an image of the food item

# Define the Order model to represent customer orders in the database
class Order(db.Model):
    # Define the columns for the Order table
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each order
    order_number = db.Column(db.String(120), unique=True, nullable=False)  # Unique order number, cannot be null
    customer_name = db.Column(db.String(100), nullable=False)  # Name of the customer, cannot be null
    contact_number = db.Column(db.String(20), nullable=False)  # Contact number for the customer, cannot be null
    details = db.Column(db.Text, nullable=False)  # Details of the order, stored as JSON string, cannot be null
    order_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Timestamp when the order was placed, defaulting to the current time

    def __repr__(self):
        # Define a __repr__ method to return a string representation of the Order
        # Useful for debugging and logging purposes
        return f'<Order {self.order_number}>'
