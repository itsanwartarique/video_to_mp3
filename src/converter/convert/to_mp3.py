import sqlite3,tempfile
from moviepy.editor import VideoFileClip

def convert_video_to_mp3(input_video, output_audio):
    video_clip = VideoFileClip(input_video)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(output_audio)

def to_mp3(video_id):
    # connect with db
    conn = sqlite3.connect("../db/storage.db")
    cursor = conn.cursor()

    cursor.execute('''
        SELECT filename,video_data FROM videos WHERE id = ?
    ''',(video_id,))
    res = cursor.fetchone()
    conn.close()
    if res:
        
        with open(f"{res[0]}","wb") as file:
            file.write(res[1])

        convert_video_to_mp3(f"{res[0]}",f"{res[0]}.mp3")

        with open(f"{res[0]}.mp3","rb") as file:
            mp3_data = file.read()

        conn = sqlite3.connect("../db/audio.db")
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO mp3 (filename,mp3_data) VALUES (?,?)
        ''',(res[0],mp3_data,))
        conn.commit()
        mp3_id = cursor.lastrowid
        conn.close()
        return mp3_id,None
        # publish mp3 id to mp3 queue   
    else:
        return None , "failed to convert"