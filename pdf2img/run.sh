#!/bin/bash

REBUILD=0

if [ "$1" == "--rebuild" ]; then
    REBUILD=1
    shift
fi

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 [--rebuild] <pdf_file> <page_number> <image_name>"
    exit 1
fi

PDF_FILE=$1
PAGE_NUMBER=$2
IMAGE_NAME=$3

IMAGE_NAME_DOCKER="pdf2img"

if [ $REBUILD -eq 1 ] || ! docker image inspect $IMAGE_NAME_DOCKER >/dev/null 2>&1; then
    echo "Building Docker image..."
    docker build -t $IMAGE_NAME_DOCKER .
fi

docker run --rm -v "$(pwd)":/app $IMAGE_NAME_DOCKER "$PDF_FILE" "$PAGE_NUMBER" "$IMAGE_NAME"
