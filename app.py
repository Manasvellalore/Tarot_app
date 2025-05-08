from flask import Flask, render_template, jsonify, request
import random
from tarot_cards import tarot_deck

app = Flask(__name__)

# Helper function to adjust card meaning based on the user's question
def adjust_meaning_for_question(deep_meaning, question):
    if "love" in question.lower():
        return f"Love-related interpretation: {deep_meaning} This suggests that in your romantic life, the card represents a key aspect of your relationship dynamics or potential future."
    elif "career" in question.lower():
        return f"Career-focused meaning: {deep_meaning} In a career context, the card might indicate growth, challenges, or decisions you need to make regarding your job or professional life."
    elif "money" in question.lower():
        return f"Financial perspective: {deep_meaning} If related to finances, this card is advising on how to approach money-related matters or the potential changes in your financial situation."
    else:
        return f"General interpretation: {deep_meaning} In general, this card speaks to the deeper aspects of your life journey, regardless of the specific question."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/draw', methods=['GET'])
def draw_cards():
    question = request.args.get('question', '')
    # Randomly draw 3 cards from the deck
    drawn_cards = random.sample(tarot_deck, 10)
    
    # Prepare card data for the response
    cards_data = []
    for card in drawn_cards:
        orientation = random.choice(['Upright', 'Reversed'])
        meaning = card['upright'] if orientation == 'Upright' else card['reversed']
        deep_meaning = card['deep_meaning']['upright'] if orientation == 'Upright' else card['deep_meaning']['reversed']
        
        personalized_meaning = adjust_meaning_for_question(deep_meaning, question)
        
        cards_data.append({
            'name': card['name'],
            'orientation': orientation,
            'meaning': meaning,
            'deep_meaning': deep_meaning,
            'personalized_meaning': personalized_meaning
        })

    return jsonify({'question': question, 'cards': cards_data})

if __name__ == '__main__':
    app.run(debug=True)
