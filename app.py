from flask import Flask, render_template, request, jsonify
import random
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

app = Flask(__name__)

# Download required nltk data (run this once to download)
nltk.download('punkt')
nltk.download('stopwords')

# Predefined data for products with image paths
products = {
    'laptop': {'price': 1000, 'discount': 10, 'image': 'images/laptop.jpg'},
    'phone': {'price': 500, 'discount': 5, 'image': 'images/phone.jpg'},
    'tablet': {'price': 300, 'discount': 8, 'image': 'images/tablet.jpg'}
}

greetings = ["hello", "hi", "greetings", "sup", "what's up", "hey"]
responses = ["Hello! How can I help you?", "Hi there! What would you like to negotiate on?"]

def greet(sentence):
    for word in sentence.split():
        if word.lower() in greetings:
            return random.choice(responses)
    return None

def price_negotiation(product, user_offer):
    base_price = products[product]['price']
    discount = products[product]['discount']
    min_price = base_price * (1 - discount / 100)

    if user_offer >= base_price:
        return f"The price for the {product} is ${base_price}. No negotiation needed!"
    elif user_offer < min_price:
        return f"Sorry, we can't go below ${min_price:.2f}. The best price I can offer for the {product} is ${min_price:.2f}."
    else:
        return f"Great! We can settle for ${user_offer}. It's a deal!"

def get_product_from_sentence(sentence):
    for product in products.keys():
        if product in sentence.lower():
            return product
    return None

def tokenize(sentence):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(sentence.lower())
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    return filtered_sentence

def chatbot_response(user_input):
    user_input = user_input.lower()
    greeting_response = greet(user_input)
    if greeting_response:
        return greeting_response

    tokens = tokenize(user_input)
    product = get_product_from_sentence(user_input)

    if product:
        try:
            user_offer = int([token for token in tokens if token.isdigit()][0])
            return price_negotiation(product, user_offer)
        except IndexError:
            return f"How much would you like to offer for the {product}?"

    return "I'm sorry, I didn't understand that. Can you please rephrase?"

@app.route('/')
def index():
    return render_template('index.html', products=products)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    response = chatbot_response(user_input)
    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(debug=True)
