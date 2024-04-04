#!/bin/zsh
ffmpeg -i $1.m4a -acodec pcm_s16le -ac 1 -ar 16000 $1.wav  
~/Documents/Git/whisper.cpp/main -m /Users/neelredkar/Documents/Git/whisper.cpp/models/ggml-medium.en.bin -f $1.wav -otxt -of $1
rm $1.wav
python transcribe.py $1.txt
latexmk -pdf $1.tex
latexmk -c
mkdir $1
mv $1*(.) $1

# ask for name of folder to move to
echo "Enter the name of the folder you want to move to: "
read folder
mv -r $1 $folder

git add .
git commit -m "Transcribed notes for $1"