#!/bin/bash
#This sorts for files based on time for a particular day and prints
#desired header params as set in quick_look.py
#
check(){
cd $FLD$DT$OBS 
i=1
while [ $i -lt $lim ]
do
	FLT=$TYP$i
	echo $FLT  `ls *"$FLT"* | sort -t "T" -k 3 -u | wc -l`
	for file in `ls *"$FLT"* | sort -t "T" -k 3 -u`
	do
		python3 $QL -P $file
	done
	i=$((i+1))
done
}

FLD=/home/janmejoyarch/sftp_drive/suit_data/level0fits/
OBS=/engg4
QL=/home/janmejoyarch/Dropbox/Janmejoy_SUIT_Dropbox/scripts/quick_look.py
DAY=10

while [ $DAY -lt 13 ]
do
	DT=2024/02/$DAY
	echo $DT
	TYP=NB0
	lim=9
	check

	lim=4
	TYP=BB0
	check
	
	DAY=$((DAY+1))
done

