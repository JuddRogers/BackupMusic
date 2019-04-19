Two versions of simple backup to Google Cloud Storage.

The shell script `upload.sh` works so long as all files have boring names.
Few classical music files have such names.

The python script `update.py` computes the metadata (sha512 and modification
time) and adds them as metadata on the blob. It also creates an object in a
second bucket which maps the sha512 to a path.
