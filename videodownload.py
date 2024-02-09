from pytube import YouTube
import os

yt = YouTube('https://www.youtube.com/watch?v=a5B8Xx1RPSc')

highresvideo = yt.streams.get_highest_resolution()
highresvideo.download()


