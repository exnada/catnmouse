#!/bin/bash
cd pics/

HEIGHT=${1}
WIDTH=${2}
FM=${3}
NBRSNAKES=${4}
RANDSEED=${5}

SOURCE=.
ORIGS=processed_originals
TARGET=processed_20x

mkdir -p ${ORIGS}/
mkdir -p ${TARGET}/
rm -f ${TARGET}/mazer_${HEIGHT}x${WIDTH}_r${RANDSEED}_s${NBRSNAKES}_f${FM}_*.png

echo "Processing images"
counter=0
# for i in `ls mazer_${HEIGHT}x${WIDTH}_*.png | grep -v network` ;
for i in `ls mazer_*.png | grep -v network` ;
do
	((counter++))
	echo -n '.'
	if [ "$((counter % 100 ))" -eq "0" ];
	then
		echo "  processed ${counter} images"
	fi
	j=`echo -n $i | sed -e 's/\.png/_20x.png/'`
	convert -scale 2000% ${SOURCE}/${i} ${TARGET}/${j}
	mv ${SOURCE}/${i} ${ORIGS}/${i}
done
echo "  processed ${counter} images"
echo "Image processing complete."

