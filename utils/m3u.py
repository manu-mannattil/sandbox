#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ------------  ---------------------------------------------------------
#         file  m3u
#  description  Generate M3U playlists by "fuzzy matching" metadata
#      created  2012-11-XX XX:XX IST
#     modified  2015-11-21 21:50 IST
# ------------  ---------------------------------------------------------
#
# Usage: m3u [-q] [-i FILE] [-o FILE] [-p PATTERN] DIRECTORY ...
#
# Options:
#     -q          quick search
#     -i FILE     input file name
#     -o FILE     output file name
#     -p PATTERN  search pattern
#
# Examples:
#     m3u -i top_100_songs.txt -o top_100_songs.m3u ~/music
#     w3m <url> | m3u -q ~/music > playlist.m3u
#
# I started writing this in November, 2012 while returning home from IIT
# Kanpur.  I used it for a while, but never really maintained it.
#

import os
import codecs
import getopt
import re
import sys
import unicodedata
from difflib import SequenceMatcher
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from string import Template

audio_file = lambda name: os.path.splitext(name)[1] in ('.mp3', '.flac')


class MetadataError(Exception):
    """Raised when mutagen fails to extract metadata from a track."""

    pass


def simple(string):
    """Return a simpler representation of string."""
    string = string.strip()
    string = unicodedata.normalize('NFKD', string).encode('ascii', 'ignore')
    string = re.sub(r'[([{].*$', '', string)
    string = re.sub(r'\W', '', string)

    return string.lower()


def metadata(path):
    """Return metadata dictionary of audio file at path."""
    ext = os.path.splitext(path)[1]

    try:
        if ext == '.flac':
            audio = FLAC(path)
        elif ext == '.mp3':
            audio = EasyID3(path)

        track = {
            'album': '',
            'artist': '',
            'comment': '',
            'date': '',
            'genre': '',
            'length': '',
            'path': path,
            'title': '',
            'tracknumber': ''
        }

        for key, value in track.iteritems():
            if key in audio:
                track.update({key: audio[key][0]})

        return track
    except:
        raise MetadataError


def diff(string1, string2, quick):
    """Fuzzy match string1 and string2"""
    if quick:
        return SequenceMatcher(None, string1, string2).quick_ratio()
    else:
        return SequenceMatcher(None, string1, string2).ratio()


def generate(quick, pattern, inp, out, folders):
    """Generate M3U playlist by scanning each folders recursively and fuzzy
    matching each line of the input file.  The generated playlist is written to
    the output file."""
    # scan the folders
    library = []
    for folder in folders:
        for root, dirs, files in os.walk(folder):
            for name in filter(audio_file, files):
                try:
                    path = os.path.join(root, name)
                    track = metadata(os.path.abspath(path))
                    library.append(track)
                except MetadataError:
                    pass

    # generate playlist
    for line in inp:
        rank = lambda track: diff(
            simple(line),
            simple(Template(pattern).safe_substitute(track)),
            quick
        )

        # XXX: using max() to find the best track makes things slower!
        matches = sorted(library, key=rank, reverse=True)
        best = rank(matches[0])

        for track in matches:
            if rank(track) == best:
                out.write(u'%s\n' % track['path'])
            else:
                break


def main():
    """Mainly argument parsing."""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "qp:i:o:")
    except getopt.GetoptError:
        sys.exit(__doc__)

    # default values
    quick = False
    pattern = u'$artist $title'
    inp = codecs.getreader('utf-8')(sys.stdin)
    out = codecs.getwriter('utf-8')(sys.stdout)

    if len(args) == 0:
        folders = [os.path.curdir.decode('utf-8')]
    else:
        folders = [arg.decode('utf-8') for arg in args]

    for opt, val in opts:
        if opt == '-q':
            quick = True
        elif opt == '-p':
            pattern = val.decode('utf-8')
        elif opt == '-i':
            inp = codecs.open(val.decode('utf-8'), 'r', encoding='utf-8')
        elif opt == '-o':
            out = codecs.open(val.decode('utf-8'), 'w', encoding='utf-8')
        else:
            sys.exit(__doc__)

    generate(quick, pattern, inp, out, folders)

if __name__ == '__main__':
    sys.exit(main())
