import os
from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

MINDSDB_HOST = 'https://cloud.mindsdb.com'
MINDSDB_API_KEY = os.environ.get('MINDSDB_API_KEY')

client = OpenAI(
    api_key=MINDSDB_API_KEY,
    base_url="https://llm.mdb.ai/"
)

@app.route('/')
def index():
    return "Welcome to the Journaling Assistant Backend! The service is running."

@app.route('/generate_journal', methods=['POST'])
def generate_journal():
    try:
        data = request.json
        user_entry = data.get('journal_entry', '')
        
        if not user_entry.strip():
            return jsonify({'error': 'Journal entry is empty'}), 400

        # Create completion using MindsDB's LLM endpoint
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": """You are a mindful journaling assistant helping with manifestation and personal growth.
                For each journal entry, provide:
                1. A thoughtful reflection on the emotions and intentions expressed
                2. Two powerful affirmations related to their goals
                3. A gentle suggestion for deepening their manifestation practice"""
            },
            {"role": "user", "content": user_entry}]
        )
        
        suggestion = completion.choices[0].message.content
        return jsonify({'suggestions': suggestion})

    except Exception as e:
        print(f"Error generating suggestion: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use the PORT environment variable from Render
    app.run(debug=False, host='0.0.0.0', port=port)
