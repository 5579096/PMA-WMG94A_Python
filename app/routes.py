from flask import render_template, redirect, url_for, flash, request, session
from app import app, db
from app.models import FoodItem, Order
from app.forms import CheckoutForm, AdminLoginForm, FoodItemForm
import uuid
import json  # Used for serializing cart details into a JSON string

# Route for the home page, optionally filtered by category
@app.route('/', defaults={'category': None})
@app.route('/<category>')
def index(category):

    # Filter items by category if specified and not 'all'
    if category and category != 'all':
        items = FoodItem.query.filter_by(category=category).all()
    else:
        # Fetch all items if no specific category is requested
        items = FoodItem.query.all()
    # Retrieve distinct categories for filtering options
    categories = FoodItem.query.with_entities(FoodItem.category).distinct()
    # Render the index page with items and categories
    return render_template('index.html', items=items, categories=categories, current_category=category)


# Add item to shopping cart
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item_id = request.form.get('item_id')
    quantity = int(request.form.get('quantity', 1))  # Default to 1 if not provided
    item = FoodItem.query.get(item_id)

    item_id_str = str(item_id)  # Ensure the item_id is a string if it's not already
    quantity = int(quantity)  # Assuming quantity is the number to add
    
    if not item:
        flash('Item not found.', 'danger')
        return redirect(url_for('index'))
    
     # Prepare the cart item and add/update it in the session cart
    cart_item = {
        'id': item.id,
        'name': item.name,
        'price': item.price,
        'quantity': quantity
    }
    if 'cart' not in session:
        session['cart'] = {} # Initialize as an empty dictionary
    
    if item_id_str in session['cart']:
        # Update quantity for existing item
        session['cart'][item_id_str]['quantity'] += quantity # Add/update the item in the cart
    else:
        # Add new item to cart
        session['cart'][item_id_str] = cart_item

    session.modified = True  # Mark the session as modified to ensure it gets saved
    flash('Item added to cart.', 'success')
    return redirect(url_for('cart'))

# Display product details
@app.route('/product/<int:item_id>')
def product_detail(item_id):
    item = FoodItem.query.get_or_404(item_id)
    return render_template('product_detail.html', item=item)

# Display the shopping cart contents
@app.route('/cart')
def cart():
    # Check if 'cart' is in session and it has items
    if 'cart' not in session or not session['cart']:
        # Pass a message to the template indicating the cart is empty
        empty_message = "Your cart is empty. Start adding items now!"
    else:
        empty_message = None

    return render_template('cart.html', empty_message=empty_message)

# Remove an item from the shopping cart
@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    item_id = request.form.get('item_id')
    if item_id in session['cart']:
        del session['cart'][item_id]
        session.modified = True  # Ensure the session is marked as modified
        flash('Item removed from cart.', 'success')
    else:
        flash('Item not found in cart.', 'error')
    return redirect(url_for('cart'))

# Checkout process: collect user info and place the order
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    form = CheckoutForm()
    if form.validate_on_submit():
        # Check if 'cart' exists in session and it has items
        if 'cart' not in session or not session['cart']:
            # If the cart is empty or not set, redirect to the cart page with an error message
            flash('Your cart is empty. Please add items before proceeding to checkout.', 'error')
            return redirect(url_for('cart'))

        # Generate a unique order number
        order_number = uuid.uuid4().hex[:6].upper()

        # Serialize cart details
        cart_details = json.dumps(session['cart'])

        # Create and save the order
        order = Order(
            order_number=order_number,
            customer_name=form.name.data,
            contact_number=form.contact_number.data,
            details=cart_details  # Store serialized cart items
        )
        db.session.add(order)
        db.session.commit()

        # Clear the cart from the session after successful checkout
        del session['cart']

        #flash('Checkout successful! Thank you for your order.', 'success')
        # Redirect to the thank you page with the order number
        return redirect(url_for('thank_you', order_number=order_number))
    
    return render_template('checkout.html', title='Checkout', form=form)

# Thank you page after placing an order
@app.route('/thank_you/<order_number>')
def thank_you(order_number):
    order = Order.query.filter_by(order_number=order_number).first_or_404()
    # Details are stored as a JSON string
    order_details = json.loads(order.details)  # Convert JSON string to Python dictionary or list
    return render_template('thank_you.html', order=order, order_details=order_details)

# Admin login route
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        # Example: Hardcoded check for simplicity
        if form.username.data == 'admin' and form.password.data == 'adminpass':
            session['is_admin'] = True
            flash('You have been logged in!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('admin_login.html', title='Admin Login', form=form)

# Admin dashboard route
@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('is_admin'):
        return redirect(url_for('admin_login'))
    # Fetch all FoodItems from the database
    food_items = FoodItem.query.all()
    return render_template('admin_dashboard.html', food_items=food_items)

@app.route('/admin/add_food_item', methods=['GET', 'POST'])
def add_food_item():
    form = FoodItemForm()
    if form.validate_on_submit():
        food_item = FoodItem(name=form.name.data, price=form.price.data,category=form.category.data, image_filename=form.image_filename.data)
        db.session.add(food_item)
        db.session.commit()
        flash('Food item added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('add_edit_food_item.html', form=form, title="Add Food Item")

@app.route('/admin/edit_food_item/<int:item_id>', methods=['GET', 'POST'])
def edit_food_item(item_id):
    food_item = FoodItem.query.get_or_404(item_id)
    form = FoodItemForm(obj=food_item)
    if form.validate_on_submit():
        food_item.name = form.name.data
        food_item.price = form.price.data
        food_item.image_filename = form.image_filename.data
        food_item.category = form.category.data
        food_item.description = form.description.data
        db.session.commit()
        flash('Food item updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('add_edit_food_item.html', form=form, title="Edit Food Item", food_item=food_item)


@app.route('/admin/delete_food_item/<int:item_id>', methods=['POST'])
def delete_food_item(item_id):
    food_item = FoodItem.query.get_or_404(item_id)
    db.session.delete(food_item)
    db.session.commit()
    flash('Food item deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))



@app.route('/update_cart_item', methods=['POST'])
def update_cart_item():
    item_id = request.form.get('item_id')
    new_quantity = request.form.get('quantity', type=int)

    if item_id in session.get('cart', {}):
        if 1 <= new_quantity <= 10:  # Validates the quantity is within the allowed range
            session['cart'][item_id]['quantity'] = new_quantity
            flash('Quantity updated successfully.', 'success')
        else:
            flash('Invalid quantity selected.', 'danger')
    else:
        flash('Item not found in cart.', 'danger')

    return redirect(url_for('cart'))

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('is_admin', None)  # To match the admin session key
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))
