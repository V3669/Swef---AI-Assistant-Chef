from flask import Flask, jsonify, request
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# Set the secret key for the Flask app
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Root route
@app.route('/', methods=['GET'])
def home():
    try:
        with open('data/fridge.json') as f:
            fridge_data = json.load(f)
        
        # Extracting items with their quantities
        fridge_items = {item['name']: item['quantity'] for item in fridge_data['items']}
        return jsonify({
            "message": "Welcome to the Swef API! Use /get_fridge_items to fetch fridge items.",
            "fridge_items": fridge_items
        })
    except Exception as e:
        print(f"Error in home route: {e}")  # Log the error
        return jsonify({"error": "Internal Server Error"}), 500

# Route to fetch fridge items
@app.route('/get_fridge_items', methods=['GET'])
def get_fridge_items():
    try:
        with open('data/fridge.json') as f:
            fridge_data = json.load(f)
        
        # Extracting items with their quantities
        fridge_items = {item['name']: item['quantity'] for item in fridge_data['items']}
        return jsonify(fridge_items)
    except Exception as e:
        print(f"Error in get_fridge_items route: {e}")  # Log the error
        return jsonify({"error": "Internal Server Error"}), 500

# Function to call the AI/ML API
def get_recipes_from_ai(ingredients, budget):
    api_key = os.getenv('AI_API_KEY')
    api_url = os.getenv('AI_API_URL')

    # Construct the prompt based on budget
    if budget == "budget":
        prompt = f"Suggest budget-friendly recipes using the following ingredients: {', '.join(ingredients)}. Minimize extra ingredients."
    else:
        prompt = f"Suggest various dishes using the following ingredients: {', '.join(ingredients)}. Include extra ingredients if necessary."

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'gpt-4o-mini',
        'prompt': prompt,
        'max_tokens': 150  # Adjust as needed
    }

    response = requests.post(api_url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()  # Assuming the response contains recipes
    else:
        return {"error": "Failed to fetch recipes from AI/ML API"}

# Route to get recipes based on ingredients and budget
@app.route('/get_recipes', methods=['POST'])
def get_recipes():
    data = request.json
    ingredients = data.get('ingredients', [])
    budget = data.get('budget', 'splurge')  # Default to 'splurge' if not specified

    # Call the AI/ML API to get recipes
    recipes_response = get_recipes_from_ai(ingredients, budget)
    return jsonify(recipes_response)

# Route to get missing ingredients
@app.route('/get_missing_ingredients', methods=['POST'])
def get_missing_ingredients():
    data = request.json
    required_ingredients = data.get('required_ingredients', [])
    available_ingredients = data.get('available_ingredients', [])
    
    missing_ingredients = [item for item in required_ingredients if item not in available_ingredients]
    return jsonify({"missing_ingredients": missing_ingredients})

# Test route to check JSON loading
@app.route('/test_json', methods=['GET'])
def test_json():
    try:
        with open('data/fridge.json') as f:
            fridge_data = json.load(f)  # Load JSON directly
        return jsonify(fridge_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)