#!/bin/bash

eth=$1
RXpre=$(cat /proc/net/dev | grep $eth | tr : " " | awk '{print $2}')
TXpre=$(cat /proc/net/dev | grep $eth | tr : " " | awk '{print $10}')
sleep 1
RXnext=$(cat /proc/net/dev | grep $eth | tr : " " | awk '{print $2}')
TXnext=$(cat /proc/net/dev | grep $eth | tr : " " | awk '{print $10}')
clear
echo  -e  "\t RX `date +%k:%M:%S` TX"
RX=$((${RXnext}-${RXpre}))
TX=$((${TXnext}-${TXpre}))
 
#if [[ $RX -lt 1024 ]];then
RX="${RX}B/s"
#elif [[ $RX -gt 1048576 ]];then
RX=$(echo $RX | awk '{print $1/1048576 }')
#else
#RX=$(echo $RX | awk '{print $1/1048576 "MB/s"}')
#fi
 
#if [[ $TX -lt 1024 ]];then
TX="${TX}B/s"
#elif [[ $TX -gt 1048576 ]];then
#TX=$(echo $TX | awk '{print $1/1048576 "MB/s"}')
#else
TX=$(echo $TX | awk '{print $1/1048576 }')
#fi
 
echo -e " $RX "
echo -e " $TX "

