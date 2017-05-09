#############################################################################################################
# This small utility uses a commandline tool named youtube-dl to download youtube videos
# It downloads the links listed in d:\Tal - Work Related\Python\PycharmProjects\youtube-dl\youtube_links.txt
# currently it only supports mp3/avi/mp4
# it downloads the videos to the specified location in 'downloaded_location'.
# for formats transformation it uses ffmpeg
# the youtube-dl exe and formatting utilities all located in d:\Tal - Work Related\VideoDownloadAndConvertEXE\
# these utilities also added to the sys Path variable so it can be called from anywhere
#############################################################################################################

import threading
from subprocess import check_output
import time
import sys


youtube_links_list=[]

def parseVideosFile (filePath):
    fr = open(filePath,'r')
    for line in fr.readlines():
        a,b = line.split(",")
        youtube_links_list.append([a,b.strip()])   # stripping the \n
    fr.close()

download_location = './DownloadedClips/%(title)s.%(ext)s '   # this is the location to download.
parseVideosFile("d:\Tal - Work Related\Python\PycharmProjects\youtube-dl\youtube_links.txt")
print("Downloading a total of " + str(len(youtube_links_list)) + " videos")

def convert(command):
    check_output(command, shell=True)

threads=[]
for youtube_link_and_format in youtube_links_list:

    #youtube_link = input("Please enter the youtube link: ")
    #format = input("Please enter the format wanted (mp3/mp4/avi): ")

    youtube_link = youtube_link_and_format[0]
    format = youtube_link_and_format[1]

    cmd_command = ""
    if (format == "mp3"):
        cmd_command = 'youtube-dl.exe -x --extract-audio --audio-format mp3 ' + download_location + youtube_link
    elif (format == "mp4"):
        cmd_command = 'youtube-dl.exe -f bestvideo[ext=mp4] ' + '-o ' + download_location + youtube_link  #-o is for the location
    elif (format == "avi" ):
        cmd_command = 'youtube-dl.exe --recode-video ' + format + ' ' + youtube_link

    t = threading.Thread(target=convert,args=(cmd_command,))
    threads.append(t)

for t in threads:
    t.start()

def is_any_thread_alive():
    answer = True
    for t in threads:
        if (not t.is_alive()):
            answer = False
    return answer

# printing dots while the threads are converting
s = '.'
sys.stdout.write( 'working' )
while is_any_thread_alive():
        sys.stdout.write( s )
        sys.stdout.flush()
        time.sleep(0.5)


for t in threads:
    t.join()

print("\nfinished")

