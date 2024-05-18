from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

app = Flask(__name__)

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_text)
    return response.text

input_prompt = "Summarize the following text in 3 sentences:\n\n{text}"

@app.route('/evaluate', methods=['POST'])
def evaluate_resume():
    try:

        text_input = request.form['text']        
        formatted_prompt = input_prompt.format(text=text_input)
        
        response = get_gemini_response(formatted_prompt)
        
        summary = response.strip()
        
        return jsonify({"summary": summary}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
