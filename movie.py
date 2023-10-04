from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip, TextClip
import pysrt

# def style_captions(caption_text):
#     return caption_text.upper()

def extract_captions_from_srt(srt_filename):
    """Reads an .srt file and returns a list of tuples (text, start_time, end_time)."""
    subs = pysrt.open(srt_filename)
    captions = []
    for sub in subs:
        start_time = sub.start.ordinal / 1000  # Convert from milliseconds to seconds
        end_time = sub.end.ordinal / 1000
        captions.append((sub.text, start_time, end_time))
    return captions

def merge_captions_with_video(video_filename, audio_filename, srt_filename, output_filename="Files/output.mp4"):
    video = VideoFileClip(video_filename)
    audio = AudioFileClip(audio_filename)

    # Mute the video
    video = video.without_audio()

    # If the video is shorter than the audio, loop the video
    while video.duration < audio.duration:
        video = concatenate_videoclips([video, video])

    # Cut the looped video to the length of the audio
    video = video.subclip(0, audio.duration)

    # Attach the TTS audio
    video = video.set_audio(audio)

    captions = extract_captions_from_srt(srt_filename)
    caption_clips = []

    for text, start_time, end_time in captions:
        # Style the caption
        
        txt_clip = (TextClip(text, font="./CoolveticaRg-Regular.ttf", fontsize=35, color="white", stroke_color= 'black',stroke_width=.2 )
                    .set_pos(('center', 'center'))
                    .set_duration(end_time - start_time)
                    .set_start(start_time)
                    .set_end(end_time))
        
        caption_clips.append(txt_clip)

    # Composite the captions on top of the video
    final_video = CompositeVideoClip([video] + caption_clips)

    # Write to output
    final_video.write_videofile(output_filename)

