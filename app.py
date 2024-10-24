from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = '49'  

# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('Sweets.db')
    conn.row_factory = sqlite3.Row
    return conn


# Homepage route
@app.route('/')
def home():
    conn = get_db_connection()
    milkshakes = conn.execute('SELECT * FROM Milkshakes').fetchall()  # Fetching milkshakes from the database
    conn.close()
    return render_template('Home.html', milkshakes=milkshakes)

# Customization route for users to build their milkshakes
@app.route('/customize', methods=['GET', 'POST'])
def customize():
    conn = sqlite3.connect('Sweets.db')
    cur = conn.cursor()  

    if request.method == 'POST':
        base = request.form['Base']
        milk = request.form['Milk']
        topping_1 = request.form['Topping_1']
        topping_2 = request.form['Topping_2']
        topping_3 = request.form['Topping_3']
        size = request.form['Size']
        name = request.form['Name']



        conn = sqlite3.connect('Sweets.db')
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO Customize (Base, Milk, Topping_1, Topping_2, Topping_3, Size, Name) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (base, milk, topping_1, topping_2, topping_3, size, name))
        conn.commit()
        # Save the order to the database using the function we defined above
        

        # Logic to handle customization
        flash(f'Order placed! Base: {base}, Milk: {milk}, Topping_1: {topping_1}, Topping_2: {topping_2}, Topping_3: {topping_3}, Size: {size},', 'success')
        conn.close()
        return redirect(url_for('customize'))
    
    

    return render_template('customize.html')



# Route for handling milkshake orders
@app.route('/check_order', methods=['GET', 'POST'])
def check_order():
    custom_order = None
    customer_name = None  # Initialize the variable to avoid UnboundLocalError
    customer_searched = False
    
    if request.method == 'POST':
        customer_name = request.form.get('Name')  # Safely get the form value
        conn = get_db_connection()

        # Fetch the custom order based on customer name from the 'Customize' table
        custom_order = conn.execute('''
            SELECT Base, Milk, Topping_1, Topping_2, Topping_3, Size 
            FROM Customize 
            WHERE Name = ?
        ''', (customer_name,)).fetchone()
        conn.close()

        customer_searched = True

        # Flash message for success or error
        if custom_order:
            flash(f"Custom order found for {customer_name}!", 'success')
        else:
            flash('No custom order found for that customer.', 'error')

    return render_template('check_order.html', custom_order=custom_order, customer_searched=customer_searched, customer_name=customer_name)

@app.route('/menu')
def Menu():
    return render_template('menu.html')


# Run the application
if __name__ == '__main__':
    app.run(debug=True)
