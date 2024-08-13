#!/bin/bash

HEIGHT=${1}
WIDTH=${2}
FM=${3}
NBRSNAKES=${4}
RANDSEED=${5}
FPS=${6}
MOVIEFILENAME=${7}
SOURCE=../pics/processed_20x

cd mpeg/
echo "Compiling movie ${MOVIEFILENAME}"

ffmpeg -y -loglevel 0 -r ${FPS} -i ${SOURCE}/mazer_${HEIGHT}x${WIDTH}_r${RANDSEED}_f${FM}_s${NBRSNAKES}_t%05d_20x.png -c:v libx264 -vcodec libx264 -crf 22 -pix_fmt yuv420p ${MOVIEFILENAME}
