#!/usr/bin/env bash
set -e

 function upload() {
    sum=$(sha512sum -b "$1" | cut -f 1 -d ' '  )
    mod=$(stat -c "%Y" "$1")
    gsutil  -h "x-goog-meta-modtime:${mod}" -h "x-goog-meta-sha512:${sum}" cp "$1" "gs://judd-rogers-music/$1";
 }

for dir in "${@}"; do
  find "${dir}" -type f | while read file; do
    upload "$file"
  done
done
