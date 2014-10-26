#!/usr/bin/env python
#import sys
import re
import os
import magic
import glob
import argparse
from mutagen.easyid3 import EasyID3
from mutagen.easymp4 import EasyMP4
import mutagen
import shutil

import pprint
pp = pprint.PrettyPrinter()

argp = argparse.ArgumentParser(description="Sort files from Android's LOST.DIR")
argp.add_argument('-s', '--source', required=True, type=str)
argp.add_argument('-d', '--destination', required=True, type=str)
args = argp.parse_args()

recover_dir = args.destination


#### Handlers
def handle_mp3(filename):
    mp3_dir = os.path.join(recover_dir, 'mp3')
    #mp3 = MP3(filename)
    try:
        id3 = EasyID3(filename)
    except mutagen.id3.ID3NoHeaderError:
        return None
    artist = (id3.get('artist', ['noartist']))[0]
    album = (id3.get('album', ['noalbum']))[0]
    title = (id3.get('title', ['notitle']))[0]
    try:
        tracknumber = id3['tracknumber'][0]
    except KeyError:
        tracknumber = 'XX'
    tracknumber = re.sub(r'/.*', '', tracknumber)
    try:
        tracknumber = '%02d' % int(tracknumber)
    except ValueError:
        pass

    track_file = ''.join([tracknumber, '-', title, '.mp3'])

    artist_dir = os.path.join(mp3_dir, artist)
    final_path = os.path.join(artist_dir, album, track_file)

    #os.renames(filename, final_path)
    if not os.path.isdir(os.path.dirname(final_path)):
        os.makedirs(os.path.dirname(final_path))
    shutil.copy(filename, final_path)
    print final_path


def handle_mp4(filename):
    mp4_dir = os.path.join(recover_dir, 'mp3')
    mp4 = EasyMP4(filename)
    artist = (mp4.get('artist', ['noartist']))[0]
    album = (mp4.get('album', ['noalbum']))[0]
    title = (mp4.get('title', ['notitle']))[0]
    try:
        tracknumber = mp4['tracknumber'][0]
    except KeyError:
        tracknumber = 'XX'
    tracknumber = re.sub(r'/.*', '', tracknumber)
    try:
        tracknumber = '%02d' % int(tracknumber)
    except ValueError:
        pass

    track_file = ''.join([tracknumber, '-', title, '.mp4'])

    artist_dir = os.path.join(mp4_dir, artist)
    final_path = os.path.join(artist_dir, album, track_file)

    #os.renames(filename, final_path)
    if not os.path.isdir(os.path.dirname(final_path)):
        os.makedirs(os.path.dirname(final_path))
    shutil.copy(filename, final_path)
    print final_path


def handle_mv(filename, dir):
    _fn = '%s.%s' % (os.path.basename(filename), dir)
    final_path = os.path.join(recover_dir, dir, _fn)
    #os.renames(filename, final_path)
    if not os.path.isdir(os.path.dirname(final_path)):
        os.makedirs(os.path.dirname(final_path))
    shutil.copy(filename, final_path)
    print "Renamed", filename, final_path


seen_types = {}
known_types = {'audio/mpeg': handle_mp3,
               'image/jpeg': lambda fn: handle_mv(fn, 'jpg'),
               'application/ogg': lambda fn: handle_mv(fn, 'ogg'),
               'audio/mp4': handle_mp4,
               'audio/x-wav': lambda fn: handle_mv(fn, 'wav'),
               'image/png': lambda fn: handle_mv(fn, 'png'),
               'video/mp4': lambda fn: handle_mv(fn, 'mp4'),
               'text/plain': lambda fn: handle_mv(fn, 'txt'),
               'application/octet-stream': handle_mp3,
               }


c = 0
with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as m:
    for file in glob.glob(os.path.join(args.source, '*')):
        c += 1
        type = m.id_filename(file)
        seen_types[type] = seen_types.get(type, 0) + 1
        if type in known_types:
            known_types[type](file)

print "Saw", c, "files"
pp.pprint(seen_types)
