#!/bin/sh

INPUTDIR="${1}"
echo Input: $INPUTDIR
cd "${INPUTDIR}"
echo Cur dir: $PWD

find . -maxdepth 10 -type d -print0 | while read -d '' -r dir; do
	num=$(find $dir -ls | wc -l);
	printf "%s - %5d files in directory\n" "$dir" "$num";
done

