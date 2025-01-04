import os
from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
from flask_cors import CORS

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Enable Cross-Origin Resource Sharing
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for debugging; restrict in production

# MindsDB Configuration
MINDSDB_HOST = 'https://cloud.mindsdb.com'
MINDSDB_API_KEY = os.environ.get('MINDSDB_API_KEY')

# Initialize MindsDB LLM Client
client = OpenAI(
    api_key=MINDSDB_API_KEY,
    base_url="https://llm.mdb.ai/"
)

@app.route('/generate_journal', methods=['POST'])
def generate_journal():
    try:
        # Retrieve the JSON payload
        data = request.json
        user_entry = data.get('journal_entry', '')

        # Check if the journal entry is empty
        if not user_entry.strip():
            return jsonify({'error': 'Journal entry is empty'}), 400

        # Create completion using MindsDB's LLM endpoint
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """You are a mindful journaling assistant helping with manifestation and personal growth. 
                    For each journal entry, provide:
                    1. A thoughtful reflection on the emotions and intentions expressed
                    2. Two powerful affirmations related to their goals
                    3. A gentle suggestion for deepening their manifestation practice"""
                },
                {"role": "user", "content": user_entry}
            ],
            stream=False
        )
        
        # Extract the content from the LLM response
        suggestions = completion.choices[0].message.content

        return jsonify({'suggestions': suggestions})

    except Exception as e:
        print(f"Error generating journal suggestions: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Fetch the Render-assigned PORT and bind the app to it
    port = int(os.environ.get('PORT', 5000)) 
    app.run(debug=True, host='0.0.0.0', port=port)  
