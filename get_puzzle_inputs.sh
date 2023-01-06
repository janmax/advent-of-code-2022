#!/usr/bin/env bash

session=$1

for i in {1..25}
do
	echo $i
	curl -s "https://adventofcode.com/2022/day/$i/input" -X GET -H "Cookie: session=$session" > $(printf "%02d" $i)/puzzle.in
done
