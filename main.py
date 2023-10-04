import os
import logging
from gptapi import get_gpt_response
from texttospeech import text_to_speech
from wordstamp import wordstamp
from movie import merge_captions_with_video

logging.basicConfig(level=logging.INFO)

def clean_up(files):
    """Remove temporary files after processing."""
    for file in files:
        try:
            os.remove(file)
            logging.info(f"Deleted {file}")
        except Exception as e:
            logging.error(f"Error deleting {file}: {e}")

def main():
    logging.info("Starting the program...")
    query = input("What is the subject? ")
    
    try:
        response = get_gpt_response(query)
        logging.info("Received response from GPT.")
        
        output_filename = 'Files/output.mp3'
        text_to_speech(response, output_filename)
        logging.info(f"Converted response to speech: {output_filename}")
        
        wordstamp(output_filename)
        logging.info("Word stamping completed.")
        
        video_file = "Files/mc.mp4"
        srt_file = "Files/output.srt"
        merge_captions_with_video(video_file, output_filename, srt_file)
        logging.info(f"Video merged with captions: {video_file}")
        
        clean_up([srt_file, output_filename])
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
