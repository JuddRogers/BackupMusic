# BackupMusic
Backing up Music is different from other files. This project will backup to S3 Glacier and manage changes to metadata.

Music files tend to not change. Sometimes the metadata (ID3 tags and such) change but the audio does not often change. 

Thus, backing up is different from backing up documents.

This project will backup music files to some inexpensive remote storage and watch for changes
to the metadata and store those changes separately from the original file. The goal is to keep costs down
while ensuring a reliable if not fast backup.

## Design

Some way to store configuration.

### Change Monitor

A small module to watch for changes to directory trees where music is found. This will write the paths
to the files which change plus the type of change to a persistent queue.

### Metadata Extractor

Another module will be started when there is work in the queue to do the initial processing. This is delayed after the
modifications start to reduce the chance the file will be backed up only to change again. This just extracts the
metadata in the various formats and then queues the file(s) for upload.

### File Backup

Does the actual copy of the changed file to the remote store. Deals with throttled writes to the store.

Also saves a copy of the extracted metadata.