#!/bin/bash
ffmpeg -i $1.m4a -acodec pcm_s16le -ac 1 -ar 16000 $1.wav  
~/Documents/Git/whisper.cpp/main -m /Users/neelredkar/Documents/Git/whisper.cpp/models/ggml-medium.en.bin -f $1.wav -otxt -of $1
rm $1.wav
python transcribe.py $1.txt
latexmk -pdf $1.tex
latexmk -c