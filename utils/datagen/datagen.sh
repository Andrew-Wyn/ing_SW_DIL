#!/bin/sh
# Usage: datagen.sh number name surname face

numb="$1"
name="$2"
surn="$3"
face="$4"

#name 60 1036 256 62
#surn 57 1145 324 64
#numb 1446 793 596 60
#face 1480 51 577 677

numbgeom=x85+1446+793
namegeom=x85+60+1036
surngeom=x85+60+1145
#facegeom=x62+60+1036

gentext () {
    output="$(mktemp tmp.XXXXXXXXXX.png)"
    magick -background transparent -fill black -font /usr/share/fonts/TTF/times.ttf -pointsize 72 label:"$1" "$output"
    echo "$output"
}

composite () {
    output="$(mktemp tmp.XXXXXXXXXX.png)"
    magick composite -compose src-atop -geometry "$1" "$2" "$3" "$output"
    echo "$output"
}

numbt="$(gentext "Matricola $1")"
comp1="$(composite "$numbgeom" "$numbt" "template.png")"

echo "$numbt"
echo "$comp1"
