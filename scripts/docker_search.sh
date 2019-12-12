#!/bin/bash

i_1=$(ls ./api/*.py)
i_2=$(ls ./api/authentication/*.py)
i_3=$(ls ./api/ext_news/*.py)
i_4=$(ls ./api/int_news/*.py)



for a in $i_1
do
    grep -l "print" $a
    grep -n "print" $a
done

for a in $i_2
do
    grep -l "print" $a
    grep -n "print" $a
done

for a in $i_3
do
    grep -l "print" $a
    grep -n "print" $a
done

for a in $i_4
do
    grep -l "print" $a
    grep -n "print" $a
done




