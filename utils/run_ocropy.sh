#!/bin/bash
FILE_NAME=$1
FILE_PATH=$2

if [ "$FILE_PATH" == "" ]; then
	FULL_PATH="$FILE_NAME"
else
	FULL_PATH="$FILE_PATH"/"$FILE_NAME"
fi


mkdir -p $FULL_PATH

cd $FULL_PATH
	convert -density 300 "$FULL_PATH".pdf "$FILE_NAME".png
	ls . | xargs -I % cp % $FILE_NAME
	ls . > "$FULL_PATH".html
cd ..
rm -rf $FULL_PATH




