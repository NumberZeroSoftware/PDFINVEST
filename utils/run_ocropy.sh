#!/bin/bash
FILE_NAME=$1
FILE_PATH=$2

if [ "$FILE_PATH" == "" ]; then
	FULL_PATH="$FILE_NAME"
else
	FULL_PATH="$FILE_PATH"/"$FILE_NAME"
fi

mkdir -p "$FULL_PATH"
echo "Starting Processing: $FULL_PATH.pdf"

cd "$FULL_PATH"
	convert -density 300 "$FULL_PATH".pdf "$FILE_NAME".png
	ls | grep "$FILE_NAME" > images.txt
	ocropus-nlbin $(cat images.txt) -o temp
	ocropus-gpageseg 'temp/????.bin.png'
	ocropus-rpred -n 'temp/????/??????.bin.png'
	ocropus-hocr 'temp/????.bin.png' -o temp.html
	cp temp.html ../"$FILE_NAME".html
cd ..
#rm -rf "$FULL_PATH"

echo "Done Processing: $FULL_PATH.pdf"




