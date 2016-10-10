#!/usr/bin/env bash
IFS=$'\n'
i=0
j=0
k=0

for line in `ps aux`

do
    ((i++))
    if [ $i -gt 3 ]
    then
        j=`echo $line |awk '{print $3}'`
        k=$(bc <<< $j+$k )
        #echo $j
    fi
 
done
echo $k
