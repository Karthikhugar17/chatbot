from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure the Generative AI API key securely
api_key = "AIzaSyD1Ei3I894KYJxctTE6ulMrVszP2qKdPVg"
if not api_key:
    raise ValueError("API key not found. Please provide a valid API key.")
genai.configure(api_key=api_key)

# Initialize the generative AI model
try:
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    raise RuntimeError(f"Failed to initialize the generative model: {e}")

conversation_history = []

@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages."""
    try:
        # Validate input
        user_input = request.json.get('message')
        if not user_input:
            return jsonify({"error": "Message is required."}), 400

        # Update conversation history
        conversation_history.append(f"User: {user_input}")
        
        # Limit conversation history to prevent memory overuse
        max_history_length = 10
        if len(conversation_history) > max_history_length:
            conversation_history.pop(0)

        # Generate AI response
        prompt = "\n".join(conversation_history)
        response = model.generate_content(prompt)
        ai_response = response.text if hasattr(response, 'text') else "Sorry, I couldn't generate a response."

        conversation_history.append(f"AI: {ai_response}")

        return jsonify({"response": ai_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
