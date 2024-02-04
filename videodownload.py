from pytube import YouTube

yt = YouTube('https://www.youtube.com/watch?v=a5B8Xx1RPSc')

highresvideo = yt.streams.get_highest_resolution()
highresvideo.download()

# a me non funziona ma se a te si teniamolo
