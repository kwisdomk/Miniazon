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
    results = [] # FIX 1: Initialize this here so it doesn't crash if no results found

    if query:
        product_ids = search_index.search(query)
        # conv. set to list for db query
        if product_ids:
            placeholders = ','.join('?' * len(product_ids))
            conn = sqlite3.connect('miniazon.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM products WHERE id IN ({placeholders})", list(product_ids))
            results = cursor.fetchall()
            conn.close()
    
    return render_template('search.html', results=results, query=query)
    
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Show product details and recommendations"""
    conn = sqlite3.connect('miniazon.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()

    #get recs
    recommendations = []
    recommendations_ids = product_graph.get_recommendations(product_id)
    if recommendations_ids:
        placeholders = ','.join('?' * len(recommendations_ids))
        cursor.execute(f"SELECT * FROM products WHERE id IN ({placeholders})", list(recommendations_ids))
        recommendations = cursor.fetchall()
    else:
        recommendations = []

    conn.close() # FIX 2: Unindented these so page loads even if no recs
    return render_template('product.html', product=product, recommendations=recommendations)
    
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    """Addo item-desu to shopping carto"""
    user_id = "erosenpai_1337" # demo creds"
    
    # FIX 3: Convert ID to int, or it won't match the database keys
    product_id = request.form.get('product_id')
    if product_id:
        product_id = int(product_id)
        
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

    # FIX 4: Indented this whole block so it belongs to the function!
    for product_id, quantity in cart_items.items():
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product = cursor.fetchone()
        if product:
            item_total = product[3] * quantity # price * quantity
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

# making the search bar and recco work by populating the memory
conn = sqlite3.connect('miniazon.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM products")
products = cursor.fetchall()

for product in products:
    product_id, name, description, price, category = product
    search_index.add_product(product_id, name, description)

# create a mock .ship
# 1 is for laptop
# 2 -> mouse
# 3 -> keyboard
# 4 -> monitor
# 5 -> headpones
product_graph.add_relationship(1,2)
product_graph.add_relationship(1,3)
product_graph.add_relationship(1,4)
product_graph.add_relationship(2,3)
product_graph.add_relationship(3,5)

conn.close()

if __name__ == '__main__':
    app.run(debug=True)