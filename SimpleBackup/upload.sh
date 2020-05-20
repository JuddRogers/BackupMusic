#!/usr/bin/env bash
set -e

# gs://<name>
bucket_name="judd-rogers-music"

 function upload() {
    sum=$(sha512sum -b "$1" | cut -f 1 -d ' '  )
    mod=$(stat -c "%Y" "$1")
    # gsutil cp will validate using this MD5 and if the uploaded bytes don't match, not update the file.
    # yes, the output has a leading tab.
    md5=$(gsutil hash -m "$1"|grep md5 | cut -f4)
    gsutil -h "Content-MD5:${md5}" -h "x-goog-meta-modtime:${mod}" -h "x-goog-meta-sha512:${sum}" cp "$1" "gs://${bucket_name}/$1";
 }

for dir in "${@}"; do
  find "${dir}" -type f | while read file; do
    upload "$file"
  done
done
