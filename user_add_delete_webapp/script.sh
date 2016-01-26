#!/bin/bash
#file=/etc/passwd
file=$1
# set the Internal Field Separator to :
counter=0
IFS=':'
while read -r a b c d
do
  counter=`expr $c + $counter`
done < "$file"
echo $counter
