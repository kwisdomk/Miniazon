from flask import Flask, render_template, request, jsonify
import sqlite3
from data_structures.search_index import SearchIndex
from data_structures.shopping_cart import ShoppingCart
from data_structures.recommendations import ProductGraph

app = Flask(__name__)

# start our DS
search_index = SearchIndex()
shopping_cart = ShoppingCart()
product_graph = ProductGraph()

@app.route('/')
def home():
    """Homepage - show all products"""
    conn = sqlite3.connect('miniazon.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return render_template('index.html' , products=products)

@app.route('/search')
def search():
    """Search products using inverted index"""
    query = request.args.get('q', '')
    if query:
        product_ids = search_index.search(query)
# conv. set to list for db query
        placeholders = ','.join('?' * len(product_ids))
        conn = sqlite3.connect('miniazon.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM products WHERE id IN ({placeholders})", list(product_ids))
        results = cursor.fetchall()
        conn.close()
    else:
        results = []
    return render_template('search.html', results=results, query=query)
    
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Show product details and recommendations"""
    conn = sqlite3.connect('miniazon.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()

#get recs
    recommendations_ids = product_graph.get_recommendations(product_id)
    if recommendations_ids:
        placeholders = ','.join('?' * len(recommendations_ids))
        cursor.execute(f"SELECT * FROM products WHERE id IN ({placeholders})", list(recommendations_ids))
        recommendations = cursor.fetchall()
    else:
        recommendations = []

        conn.close()
        return render_template('product.html', product=product, recommendations=recommendations)
    
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    """Addo item-desu to shopping carto"""
    user_id = "erosenpai_1337" # demo creds"
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))
        
    shopping_cart.add_item(user_id, product_id, quantity)
    return jsonify({"success":True, "message": "ka-ching!! Item-desu addedo to carto"})
                        
@app.route('/cart')
def view_cart():
    """Display shoppingi carto-desu"""
    user_id = "erosenpai_1337"
    cart_items = shopping_cart.get_cart(user_id)

    # Fetch product details for items in cart
    conn = sqlite3.connect('miniazon.db')
    cursor = conn.cursor()
    cart_products = []
    total = 0

for product_id, quantity in cart_items.items():
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    if product:
        item_total = product[3] * quantinty # price * quantity
        total += item_total
        cart_products.append({
            'id': product[0],
            'name': product[1],
            'price': product[3],
            'quantity': quantity,
            'total': item_total
        })

    conn.close()
    return render_template('cart.html', cart_items=cart_products, total=total)

if __name__ == '__main__':
    app.run(debug=True)