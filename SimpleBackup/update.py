#!/usr/bin/python
import sys
import os
import hashlib
import fileinput
import time
import json

from google.cloud import storage


stor = storage.Client()
music_bucket = stor.lookup_bucket('judd-rogers-music')
metadata_bucket = stor.lookup_bucket('judd-rogers-music-metadata')


BLOCKSIZE = 65536

def do_blob_upload(method):
    # Possible to time out when uploading
    uploadTries = 0
    uploadedSuccessfully = False
    while not uploadedSuccessfully:
        try:
            uploadTries += 1
            result = method
            uploadedSuccessfully = True
        except ConnectionError as ce:
            uploadedSuccessfully = false
            if uploadTries > 5:
                raise ce
            time.sleep(0.25)
    time.sleep(0.25)

def visitFile(fileName):
    hasher = hashlib.sha512()

    with open(fileName, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    st = os.stat(fileName)
    return { "path":fileName, "mtime":int(st.st_mtime), "size":int(st.st_size), "sha512": hasher.hexdigest() }

for directory in sys.argv:
  for root, dirs, files in os.walk(directory):
     for name in files:
        path = os.path.join(root,name)
        metadata = visitFile(path)
        blob = music_bucket.get_blob(path)
        if None == blob:
            blob = music_bucket.blob(path)
        if None == blob.metadata:
            blob.metadata = {}
        if "sha512" in blob.metadata and blob.metadata["sha512"] == metadata["sha512"] and blob.size == metadata["size"]:
            print(path + " same as on disk; skipping")
            continue
        print(path + " upload needed")
        blob.metadata = { "mtime":metadata["mtime"], "sha512":metadata["sha512"]}
        do_blob_upload(blob.upload_from_filename(path))
        path = metadata["sha512"]
        metadata_blob = metadata_bucket.get_blob("sha512/" + path)
        if None == metadata_blob:
            metadata_blob = metadata_bucket.blob("sha512/" + path)
        do_blob_upload(metadata_blob.upload_from_string(json.dumps(metadata)))
