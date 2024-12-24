from flask import Flask, render_template, request, jsonify
import os
import requests
import logging
import random
from dotenv import load_dotenv
import groq as Groq

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
IMGFLIP_USERNAME = os.getenv("IMGFLIP_USERNAME")
IMGFLIP_PASSWORD = os.getenv("IMGFLIP_PASSWORD")

# Initialize Flask app
app = Flask(__name__, template_folder="templates", static_folder="static")

# Initialize Groq client
groq_client = Groq.Client(api_key=GROQ_API_KEY)


# Sentiment Analysis Function with Improved Prompt
def analyze_sentiment(text):
    prompt = (
        f"Analyze the sentiment of the following text: \"{text}\". "
        "Classify it as one of the following emotions: Happy, Sad, Angry, Disgusted, Surprised, Fearful, or Neutral. "
        "Look for emotional cues, keywords, and the tone of the message. "
        "For example, words like 'amazing' or 'joyful' indicate happiness, 'gross' or 'ew' indicate disgust, "
        "'angry' or 'furious' indicate anger, and so on. "
        "Respond with only the emotion name."
    )
    try:
        response = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Groq API Error: {e}")
        return "Neutral"  # Default sentiment on error


# Post-processing sentiment based on keywords
def post_process_sentiment(sentiment, text):
    disgust_keywords = ["gross", "ew", "yuck", "disgusting", "nasty"]
    happy_keywords = ["amazing", "joy", "happy", "excited", "great"]
    sad_keywords = ["sad", "down", "unhappy", "depressed", "lonely"]
    angry_keywords = ["angry", "furious", "rage", "irritated", "mad"]
    
    # Check if certain keywords appear in the text, adjusting sentiment accordingly
    if any(keyword in text.lower() for keyword in disgust_keywords) and sentiment != "Disgusted":
        return "Disgusted"
    elif any(keyword in text.lower() for keyword in happy_keywords) and sentiment != "Happy":
        return "Happy"
    elif any(keyword in text.lower() for keyword in sad_keywords) and sentiment != "Sad":
        return "Sad"
    elif any(keyword in text.lower() for keyword in angry_keywords) and sentiment != "Angry":
        return "Angry"
    
    # If no keyword is found, return the sentiment as is
    return sentiment


# Generate Meme using Imgflip API with Randomized Templates
def get_imgflip_meme(sentiment):
    meme_templates = {
        "Happy": [
            "102156234", "61520", "101511", "1367068", "61544",  # Success Kid, Doge, etc.
            "87743020", "21604242", "134398632", "101511", "100777631",  # More happy memes
            "170064501", "177142476"
        ],
        "Sad": [
            "61579", "80707627", "61580", "438680", "123999232",  # Sad Frog, Crying Jordan, etc.
            "101501", "129242436", "8874528", "195557", "24524376",  # More sad memes
            "54528559", "126768765"
        ],
        "Angry": [
            "181913649", "195389", "55311130", "61546", "108785202",  # Drake, Gru, etc.
            "16791970", "53613629", "512469", "124120185", "212014606",  # More angry memes
            "101513", "1045787"
        ],
        "Disgusted": [
            "101470", "129242436", "188390779", "61556", "222403160",  # Disgusted face, etc.
            "114786225", "743193", "306758052", "183418922", "157826504",  # More disgusted memes
            "149430817", "53884553"
        ],
        "Surprised": [
            "155067746", "4173692", "129139038", "17496002", "61582",  # Pikachu, etc.
            "106973319", "287799544", "12418045", "130687708", "5977616",  # More surprised memes
            "178147410", "107028244"
        ],
        "Fearful": [
            "442575", "112126428", "259237855", "13767816", "65489615",  # Scared memes
            "106746504", "159970062", "142520575", "75983867", "10157337",  # More fearful memes
            "178195093", "54189002"
        ],
        "Neutral": [
            "16464531", "21735", "347390", "718432", "131940431",  # Neutral, Meh, etc.
            "63690228", "106067193", "154145564", "32881814", "128644734",  # More neutral memes
            "133632364", "56829925"
        ],
    }

    if sentiment not in meme_templates:
        sentiment = "Neutral"  # Default fallback

    # Select a random template ID
    template_id = random.choice(meme_templates[sentiment])
    url = "https://api.imgflip.com/caption_image"

    # Generate caption text dynamically based on sentiment
    captions = {
        "Happy": ["Feeling awesome!", "Life is great!", "Best day ever!", "I'm on top of the world!", "This is pure joy!"],
        "Sad": ["This is so sad...", "Why me?", "I'm feeling down...", "Everything is falling apart.", "Tears are real."],
        "Angry": ["I'm furious!", "How dare they!", "This is so infuriating!", "I can't take this anymore!", "Enough is enough!"],
        "Disgusted": ["Ew, gross!", "That's disgusting!", "Yuck!", "I can't stand it.", "Please stop!"],
        "Surprised": ["Wow, really?", "I can't believe it!", "No way!", "I'm shocked!", "This is insane!"],
        "Fearful": ["Oh no!", "This is terrifying!", "I'm scared!", "What’s happening?", "I can’t handle this!"],
        "Neutral": ["Meh.", "It's just okay.", "I guess it's fine.", "Not bad, not good.", "Just another day."],
    }
    caption_texts = captions.get(sentiment, ["Meh."])
    top_text = caption_texts[0]
    bottom_text = caption_texts[1]

    payload = {
        "template_id": template_id,
        "username": IMGFLIP_USERNAME,
        "password": IMGFLIP_PASSWORD,
        "text0": top_text,
        "text1": bottom_text,
    }

    try:
        response = requests.post(url, data=payload)
        data = response.json()
        if data.get("success"):
            return data["data"]["url"]
        else:
            logging.error(f"Imgflip API Error: {data.get('error_message', 'Unknown error')}")
            return "https://i.imgflip.com/7f0mne.jpg"  # Default meme
    except Exception as e:
        logging.error(f"Error connecting to Imgflip API: {e}")
        return "https://i.imgflip.com/7f0mne.jpg"  # Default meme


# Routes
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    sentiment = analyze_sentiment(text)
    sentiment = post_process_sentiment(sentiment, text)  # Apply post-processing
    meme_url = get_imgflip_meme(sentiment)

    return jsonify({"sentiment": sentiment, "meme_url": meme_url})


if __name__ == "__main__":
    app.run(debug=True)
