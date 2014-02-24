#!/usr/bin/env python

import re
from subprocess import Popen, PIPE


def get_file_name(url):
    args = 'youtube-dl '
    args += '--get-filename -o "%(title)s.%(ext)s" ' + url

    process = Popen(args, stdout=PIPE, shell=True)
    name = process.communicate()[0][:-1]

    return name.decode('UTF-8')


def download_song(name, url):
    command = 'youtube-dl -c -o "%s" -f 35/18 %s' % (name, url)
    return Popen(command, shell=True).wait()


def convert_songs(song, pattern=None):
    song_name = pattern.sub('.mp3', song)
    command = 'ffmpeg -i "%s" -vn -c:a libmp3lame -b:a 320k -f mp3 "%s"' % \
              (song, song_name)

    return Popen(command, shell=True).wait()


if __name__ == '__main__':
    try:
        p = re.compile(r'[.]\w+$')
        with open('songs') as f:
            lines = f.readlines()
            for url in lines:
                url = url[:-1]
                file_name = get_file_name(url)
                print('Song: "%s" - from: "%s"' % (file_name, url))
                download_song(file_name, url)
                convert_songs(file_name, p)
    except Exception as e:
        pass
