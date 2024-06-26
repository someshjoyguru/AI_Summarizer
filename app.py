from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['http://localhost:5173', 'https://nitjsr-cp-portal.vercel.app'], supports_credentials=True)

load_dotenv()  # Load environment variables

# Configure Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_text)
    return response.text

@app.route("/", methods=['GET'])
def home():
    return "Nice working"

@app.route('/evaluate', methods=['POST'])
def evaluate_resume():
    try:
        data = request.json
        text_input = data.get('text')
        response = get_gemini_response(text_input)
        summary = response.strip()
        return jsonify({"summary": summary}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)