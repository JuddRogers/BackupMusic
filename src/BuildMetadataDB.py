import os
import json
from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3

from pymongo import MongoClient
mongo = MongoClient()
db = mongo.music

# Set the directory you want to start from
for rootDir in ('/Music/Magnatune', '/Music/cd'):
    for dirName, subdirList, fileList in os.walk(rootDir):
        print('Found directory: %s' % dirName)
        for fname in fileList:
            metadata['path'] = os.path.join(dirName, fname)
            if fname.endswith(".flac"):
                f = FLAC(os.path.join(dirName, fname))
                for key in ( 'comment', 'artist', 'album', 'track', 'tracknumber', 'title', 'genre' ):
                    metadata[key] = f[key]
            else if fname.endswith(".mp3"):
            	e = EasyID3(os.path.join(dirName, fname))
            	for key in ( 'album', 'artist', 'title', 'genre', 'date', 'tracknumber', "discnumber"):
            		metadata[key] = e[key]
            db.metadata.insert_one(json.dumps(metadata))
