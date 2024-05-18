from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

app = Flask(__name__)

load_dotenv()  # Load environment variables

# Configure Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_text)
    return response.text

input_prompt = "Summarize the following text in 3 sentences:\n\n{text}"

@app.route('/evaluate', methods=['POST'])
def evaluate_resume():
    try:
        # Extract data from the request
        if 'text' not in request.form:
            return jsonify({"error": "Text input is required"}), 400
        
        text_input = request.form['text']
        
        # Format the prompt with the input text
        formatted_prompt = input_prompt.format(text=text_input)
        
        # Get the AI response
        response = get_gemini_response(formatted_prompt)
        
        # Parse the response (assuming the response is already in a string format)
        summary = response.strip()  # Here, you might want to handle any specific formatting
        
        return jsonify({"summary": summary}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
