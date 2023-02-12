import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
import os
import smtplib
from pydub import AudioSegment
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.audio import MIMEAudio
from moviepy.audio.io import AudioFileClip
import streamlit as st
import requests
import re
import urllib.request
import os
from pytube import YouTube
import os
from moviepy.editor import *
from moviepy.audio.io import AudioFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip

# def get_links(query):
#     query = query.replace(' ', '+')
#     url = f"https://www.youtube.com/results?search_query={query}"
#     response = requests.get(url)
#     html = response.text
#     links = re.findall('"/watch\?v=(.{11})"', html)
#     return [f"https://www.youtube.com/watch?v={link}" for link in links]

# singer = input("Enter the name of a singer: ")
# num_links = int(input("Enter the number of links: "))
# links= get_links(singer)[:num_links]

# print("YouTube links:")
# for link in links:
#     print(link)

# def download_video(link, folder):
#     yt = YouTube(link)
#     stream = yt.streams.first()
#     stream.download(folder)
#     print("Video downloaded successfully")



    # Send GET request and parse HTML content


    # Extract video URLs and durations
    # video_urls = re.findall(r'href="\/watch\?v=(.{11})', html_content)
    # video_durations = re.findall(r'data-duration="(\d+)', html_content)
    # video_urls = ["https://www.youtube.com/watch?v=" + url for url in video_urls]

    # # Filter videos with duration less than 5 minutes
    # videos = [(url, int(duration)) for url, duration in zip(video_urls, video_durations) if int(duration) < 300]

    # Write video URLs to a file
    # with open("videos.txt", "w") as f:
    #     for i, video in enumerate(videos):
    #         url, duration = video
    #         f.write(f"{i+1}: {url} ({duration}s)\n")
# def download_files(x,n):
#     html = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + str(x))
#     video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
#     video_durations = re.findall(r'data-duration="(\d+)', html.read().decode())
#     video_ids = ["https://www.youtube.com/watch?v=" + url for url in video_ids]
#     videos = [(url, int(duration)) for url, duration in zip(video_ids, video_durations) if int(duration) < 300]
#     for i ,video in enumerate(videos):
#         yt = YouTube(video) 
#         print("Songs are downloading "+str(i+1)+" .......")
#         mp4files = yt.streams.filter(only_audio=True).first().download(filename='song-'+str(i)+'.mp3')


def download_files(x,n):
    html = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + str(x))
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    i = 0
    while(i<n):
        yt = YouTube("https://www.youtube.com/watch?v=" + video_ids[i])
        duration = yt.length 
        
        if duration <= 300:
            print("Song "+str(i+1)+" is downloading .......")
            mp4files = yt.streams.filter(only_audio=True).first().download(filename='song-'+str(i)+'.mp3')
            i += 1

            
# def merge_sound(n,y):
#     if os.path.isfile("song-0.mp3"):
#         try:
#             fin_sound = AudioSegment.from_file("song-0.mp3")[0:y*1000]
#         except:
#             fin_sound = AudioSegment.from_file("song-0.mp3",format="mp4")[0:y*1000]
#     for i in range(1,n):
#         aud_file = str(os.getcwd()) + "/song-"+str(i)+".mp3"
#         try:
#             f = AudioSegment.from_file(aud_file)
#             fin_sound = fin_sound.append(f[0:y*1000],crossfade=1000)
#         except:
#             f = AudioSegment.from_file(aud_file,format="mp4")
#             fin_sound = fin_sound.append(f[0:y*1000],crossfade=1000)
        
#     return fin_sound

# def convert_to_audio(folder):
#     for filename in os.listdir(folder):
#         if filename.endswith(".3gpp"):
#             video = VideoFileClip(os.path.join(folder, filename))
#             audio = video.audio
#             audio.write_audiofile(os.path.join(folder, filename.split(".")[0] + ".mp3"))
#             print("Converted {} to audio successfully".format(filename))
            
def cut_audio(folder, seconds):
    print(folder)
    for audio_file in os.listdir(folder):
        if audio_file.endswith(".mp3"):
            audio_path = os.path.join(folder, audio_file)
            cut_audio_path = os.path.join(folder, audio_file)

        # Load the audio file
            audio = AudioFileClip(audio_path)

        # Cut the audio to the specified duration
            #cut_audio = audio.subclip(seconds, audio.duration)
            cut_audio = audio.subclip(0,seconds)

        # Save the cut audio to a file
            cut_audio.write_audiofile(cut_audio_path)
            # return cut_audio_path
            print(cut_audio_path)
            
def merge_audio(folder, output_filename):
    audio_clips = []
    for filename in os.listdir(folder):
        if filename.endswith(".mp3") or filename.endswith(".wav"):
            audio_clips.append(AudioFileClip(os.path.join(folder, filename)))
    final_audio = concatenate_audioclips(audio_clips)
    final_audio.write_audiofile(output_filename)
    print("Merged all audio files in the folder successfully")
    return output_filename


def send_email(to, audio_filename):

    from_email = "sanjoliagarwal123@gmail.com"
    from_password = "kudwnrbnlsdcjizc"
    subject = "Audio file"
    message = "Attached is the audio file."

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    with open(audio_filename, "rb") as f:
        audio = MIMEAudio(f.read(),_subtype='wav')
    audio.add_header("Content-Disposition", "attachment", filename=audio_filename)
    msg.attach(audio)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(from_email, from_password)
    server.sendmail(from_email, to, msg.as_string())
    server.quit()

# def folder1(folder,links):
#     if not os.path.isdir(folder):
#         os.makedirs(folder)
#     for link in links:
#         download_video(link, folder)


def main():
    st.title("Mashup")
    st.write("Enter the name of the singer, the number of seconds to cut, and your email address")
    # folder = "vid"
    singer = st.text_input("Singer name: ")
    seconds = st.number_input("Number of seconds to cut: ")
    num = st.number_input("Number of videos: ",min_value=2, max_value=50, step=1)
    start_or_end = "start"
    to = st.text_input("Email address: ")

    if st.button("Submit"):
        # links= get_links(singer)[:num]
        # folder1(folder,links)
        # convert_to_audio(folder)
        # cut_audio(folder, seconds)
        # output_filename=merge_audio(folder, "outfile.mp3")
        download_files(singer,num)
        # fin_sound = merge_sound(num,seconds)
        folder = os.getcwd()
        cut_audio(folder, seconds)
        output_filename=merge_audio(folder, "outfile.mp3")
        output_name="outfile.mp3"
        # fin_sound.export(output_name, format="mp3")
        if output_name:
            send_email(to, output_name)
            st.success("Audio file sent to your email address successfully")
            # return 0
            exit(1)
        else:
            st.error("No audio file found for the singer")

if __name__ == "__main__":
    main()
