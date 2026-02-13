import sys
import os
import yt_dlp
from pydub import AudioSegment

def download_audio(singer, num):
    os.makedirs("downloads", exist_ok=True)

    opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s'
    }

    search = f"ytsearch{num}:{singer}"

    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([search])

def trim_audio(duration):
    trimmed = []

    for file in os.listdir("downloads"):
        path = os.path.join("downloads", file)
        audio = AudioSegment.from_file(path)

        cut = audio[:duration * 1000]
        name = "cut_" + file.split('.')[0] + ".mp3"
        cut.export(name, format="mp3")

        trimmed.append(name)

    return trimmed

def merge_audio(files, output):
    final = AudioSegment.empty()
    renamed_files = []

    # rename files to short safe names
    for i, f in enumerate(files):
        new_name = f"song{i}.mp3"
        os.rename(f, new_name)
        renamed_files.append(new_name)

    # merge safely
    for f in renamed_files:
        audio = AudioSegment.from_mp3(f)
        final += audio

    final.export(output, format="mp3")


def main():
    singer = sys.argv[1]
    num = int(sys.argv[2])
    duration = int(sys.argv[3])
    output = sys.argv[4]

    download_audio(singer, num)
    files = trim_audio(duration)
    merge_audio(files, output)

    print("Mashup created:", output)

if __name__ == "__main__":
    main()
