import unittest
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from app import app, db
from app.models import FoodItem, Order
from app.forms import CheckoutForm

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            # Populate the test DB with necessary initial data
            # For example, add some FoodItem entries
    
    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        


    def test_add_to_cart(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['cart'] = {}
            response = client.post('/add_to_cart', data={'item_id': '1', 'quantity': '1'})
            self.assertIn('cart', session)
            self.assertEqual(session['cart']['1']['quantity'], 1)
    
    def test_add_to_cart(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['cart'] = {}
            response = client.post('/add_to_cart', data={'item_id': '1', 'quantity': '1'})
            self.assertIn('cart', session)
            self.assertEqual(session['cart']['1']['quantity'], 1)

    def test_product_detail(self):
        response = self.app.get('/product/1')  # Assuming an item with ID 1 exists
        self.assertEqual(response.status_code, 200)
    
    def test_cart_empty(self):
        with self.app as client:
            response = client.get('/cart')
            self.assertIn(b'Your cart is empty', response.data)

    def test_cart_with_items(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['cart'] = {'1': {'quantity': 1, 'name': 'Test Item', 'price': 10}}
            response = client.get('/cart')
            self.assertIn(b'Test Item', response.data)

    def test_remove_from_cart(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['cart'] = {'1': {'quantity': 1, 'name': 'Test Item', 'price': 10}}
            response = client.post('/remove_from_cart', data={'item_id': '1'}, follow_redirects=True)
            self.assertNotIn('1', session['cart'])


if __name__ == '__main__':
    unittest.main()
