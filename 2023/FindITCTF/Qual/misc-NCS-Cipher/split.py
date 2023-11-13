from pydub import AudioSegment


# Load the music file
audio = AudioSegment.from_file("flag.mp3")


# Define the segment duration in milliseconds (5 seconds = 5000 milliseconds)
segment_duration = 5000


# Split the audio into segments of the defined duration
segments = [audio[i:i+segment_duration] for i in range(0, len(audio), segment_duration)]


# Export each segment to individual files
for i, segment in enumerate(segments):
   segment.export(f"segment_{i+1}.mp3", format="mp3")