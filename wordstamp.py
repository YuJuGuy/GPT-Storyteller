import os
import whisper


def format_srt_time(seconds):
    """
    Format time in seconds to SRT time format (HH:MM:SS,mmm).
    """
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    srt_format = "{:02}:{:02}:{:02},{:03}".format(int(hours), int(minutes), int(seconds), milliseconds)
    return srt_format

def wordstamp(audio):
    model = whisper.load_model("base")  # Change this to your desired model
    print("Whisper model loaded.")
    transcribe = model.transcribe(audio, word_timestamps=True)
    segments = transcribe['segments']

    segmentId = 0
    for segment in segments:
        for word in segment['words']:
            startTime = format_srt_time(word['start'])
            endTime = format_srt_time(word['end'])
            text = word['word']
            segmentId += 1
            segment_str = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"

            srtFilename = os.path.join("Files", f"output.srt")
            with open(srtFilename, 'a', encoding='utf-8') as srtFile:
                srtFile.write(segment_str)
