from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

carts = {}

@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    cart = carts.get(user_id, {})
    cart_info = []
    total_price = 0.0
    for product_id, quantity in cart.items():
        product = requests.get(f"https://saas-assignement2-product.onrender.com/products/{product_id}").json()
        if product:
            product_total_price = product['price'] * quantity
            total_price += product_total_price
            cart_info.append({
                'id': product_id,
                'name': product['name'],
                'quantity': quantity,
                'total_price': product_total_price
            })
    
    return jsonify({
        'cart': cart_info,
        'total_price': total_price
    })

@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def add_to_cart(user_id, product_id):
    quantity = request.json.get("quantity")
    product = requests.get(f"https://saas-assignement2-product.onrender.com/products/{product_id}").json()
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    if user_id not in carts:
        carts[user_id] = {}
    cart = carts[user_id]

    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity

    return jsonify({
        'message': f'Added {quantity} of {product["name"]} to the cart.',
        'cart': cart
    })

@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(user_id, product_id):
    quantity = request.json.get("quantity")
    cart = carts.get(user_id)
    
    if product_id not in cart:
        return jsonify({'error': 'Product not found in the cart'}), 404

    if cart[product_id] <= quantity:
        del cart[product_id]
    else:
        cart[product_id] -= quantity

    return jsonify({
        'message': f'Removed {quantity} from the cart.',
        'cart': cart
    })

if __name__ == '__main__':
    app.run(debug=True)
