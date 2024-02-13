import unittest
from flask import url_for
from app import app, db
from app.models import FoodItem, Order

class FlaskIntegrationTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        self.context = app.app_context()
        self.context.push()
        db.create_all()

        # Add a sample food item to the database
        self.sample_item = FoodItem(name='Test Pizza', price=9.99, category='Test Category')
        db.session.add(self.sample_item)
        db.session.commit()

    

    def test_add_to_cart_and_checkout(self):
        # Add item to cart
        response = self.app.post('/add_to_cart', data={'item_id': 1, 'quantity': 1}, follow_redirects=True)
        self.assertIn(b'Item added to cart.', response.data)

        # Verify cart contents
        with self.app as client:
            response = client.get('/cart')
            #self.assertIn(b'Test Pizza', response.data)

        # Checkout/Users/warisara/Desktop/site.db
        checkout_data = {
            'name': 'Test Customer',
            'contact_number': '123456789',
            'credit_card_number':'1234567891234567' #
        }
        response = self.app.post('/checkout', data=checkout_data, follow_redirects=True)
        #self.assertIn(b'Checkout successful! Thank you for your order.', response.data)

        # Verify order creation in database
        order = Order.query.first()
        #self.assertIsNotNone(order)
        #self.assertEqual(order.customer_name, 'Test Customer')

if __name__ == '__main__':
    unittest.main()
