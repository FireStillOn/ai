from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
import requests

app = Flask(__name__)
load_dotenv("api_keys.env")

@app.route("/", methods=["GET", "POST"])
def index():
    video_path = None
    if request.method == "POST":
        prompt = request.form["prompt"]
        script = generate_script(prompt)
        voice_path = generate_voice(script)
        video_path = "static/final_output.mp4"  # Placeholder for combined video
        # Combine with ffmpeg here (voice + video + music + branding)
    return render_template("index.html", video_path=video_path)

def generate_script(prompt):
    openai_key = os.getenv("OPENAI_API_KEY")
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {openai_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": f"Write a short viral YouTube Short script on: {prompt}"}],
            "temperature": 0.7
        }
    )
    return response.json()["choices"][0]["message"]["content"]

def generate_voice(script):
    voice_path = "static/voice.mp3"
    eleven_key = os.getenv("ELEVENLABS_API_KEY")
    response = requests.post(
        "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM",
        headers={
            "xi-api-key": eleven_key,
            "Content-Type": "application/json"
        },
        json={
            "text": script,
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}
        }
    )
    with open(voice_path, "wb") as f:
        f.write(response.content)
    return voice_path

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=81)