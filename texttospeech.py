import requests
import os
from dotenv import load_dotenv

load_dotenv()


def text_to_speech(text, output_filename='Files/output.mp3'):
    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB"
    headers = {
      "Accept": "audio/mpeg",
      "Content-Type": "application/json",
      "xi-api-key": os.getenv('ELEVEN_LABS_API_KEY')  # Replace '--' with your actual API key
    }

    data = {
      "text": text,
      "model_id": "eleven_multilingual_v2",
      "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.5
      }
    }

    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        with open(output_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
        print(f"Audio saved to {output_filename}")
    else:
        print(f"Error: {response.status_code}, {response.text}")

# Example usage:

