from flask import Flask, request, jsonify, render_template
import sqlite3

def create_db():
    conn = sqlite3.connect('chocolate_house.db')
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS Flavors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        season TEXT NOT NULL,
        available_from DATE,
        available_until DATE
    );
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS Ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        quantity INTEGER NOT NULL
    );
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS CustomerSuggestions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flavor_suggestion TEXT NOT NULL,
        allergies TEXT
    );
    ''')

    conn.commit()
    conn.close()

create_db()

app = Flask(__name__)

def get_flavors():
    conn = sqlite3.connect('chocolate_house.db')
    c = conn.cursor()
    c.execute('SELECT * FROM Flavors')
    flavors = c.fetchall()
    conn.close()
    return flavors

def add_flavor(name, season, available_from, available_until):
    conn = sqlite3.connect('chocolate_house.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO Flavors (name, season, available_from, available_until)
        VALUES (?, ?, ?, ?)
    ''', (name, season, available_from, available_until))
    conn.commit()
    conn.close()

def get_ingredients():
    conn = sqlite3.connect('chocolate_house.db')
    c = conn.cursor()
    c.execute('SELECT * FROM Ingredients')
    ingredients = c.fetchall()
    conn.close()
    return ingredients

def add_ingredient(name, quantity):
    conn = sqlite3.connect('chocolate_house.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO Ingredients (name, quantity)
        VALUES (?, ?)
    ''', (name, quantity))
    conn.commit()
    conn.close()

def add_suggestion(flavor_suggestion, allergies):
    conn = sqlite3.connect('chocolate_house.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO CustomerSuggestions (flavor_suggestion, allergies)
        VALUES (?, ?)
    ''', (flavor_suggestion, allergies))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_flavors', methods=['GET'])
def flavors():
    flavors = get_flavors()
    return jsonify({"flavors": flavors})

@app.route('/get_ingredients', methods=['GET'])
def ingredients():
    ingredients = get_ingredients()
    return jsonify({"ingredients": ingredients})

@app.route('/add_flavor', methods=['POST'])
def add_flavor_route():
    data = request.get_json()
    add_flavor(data['name'], data['season'], data['available_from'], data['available_until'])
    return jsonify({"message": "Flavor added successfully!"})

@app.route('/add_ingredient', methods=['POST'])
def add_ingredient_route():
    data = request.get_json()
    add_ingredient(data['name'], data['quantity'])
    return jsonify({"message": "Ingredient added successfully!"})

@app.route('/add_suggestion', methods=['POST'])
def add_suggestion_route():
    data = request.get_json()
    add_suggestion(data['flavor_suggestion'], data['allergies'])
    return jsonify({"message": "Suggestion submitted successfully!"})

@app.route('/add_flavor', methods=['GET'])
def add_flavor_page():
    return render_template('add_flavor.html')

@app.route('/delete_flavor/<int:flavor_id>', methods=['DELETE'])
def delete_flavor(flavor_id):
    try:
        # Delete 
        conn = sqlite3.connect('chocolate_house.db')
        c = conn.cursor()
        c.execute('DELETE FROM Flavors WHERE id = ?', (flavor_id,))
        conn.commit()
        conn.close()

        return jsonify({"message": f"Flavor with ID {flavor_id} deleted successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
