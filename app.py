# app.py
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from brain import ask_question, initialize_brain
import os

app = Flask(__name__)

# Initialize the AI brain when the app starts
initialize_brain()

@app.route("/sms", methods=['POST'])
def sms_reply():
    # 1. Get the message the user sent via SMS
    incoming_msg = request.values.get('Body', '').strip()
    
    # 2. Ask our AI Brain
    print(f"User asked: {incoming_msg}")
    answer = ask_question(incoming_msg)
    
    # 3. Package the response for Twilio
    resp = MessagingResponse()
    resp.message(answer)
    
    return str(resp)

if __name__ == "__main__":
    app.run(port=5000)