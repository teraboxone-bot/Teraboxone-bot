import os
import requests
from flask import Flask, request

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

app = Flask(__name__)

def terabox_direct(url):
    api_key = os.getenv("API_KEY")  # TeraBox API
    try:
        r = requests.get(f"https://teraboxapi.com/api?key={api_key}&link={url}").json()
        return r.get("direct_link", "Error: Invalid link or API key")
    except:
        return "Server error"

@app.route("/", methods=["POST"])
def bot():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        direct = terabox_direct(text)

        requests.post(API_URL, json={"chat_id": chat_id, "text": direct})

    return "OK"

@app.route("/")
def home():
    return "Bot is running!"
