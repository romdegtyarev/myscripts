#!/bin/sh

TYPE="${1}"
INPUTDIR="${2}"

echo Input: $INPUTDIR
echo Type: $TYPE

if [[ $TYPE == "-P" ]]; then
    echo "Print:"
    cd "${INPUTDIR}"
    find ./ -type f -name ".*"
elif [[ $TYPE == "-D" ]]; then
    echo "Delete:"
    cd "${INPUTDIR}"
    find ./ -type f -name ".*" -exec rm -f {} \;
fi

echo "Done"