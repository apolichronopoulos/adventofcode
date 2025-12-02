#!/bin/bash

year=${AOC_YEAR:-$(date -v -11m +%Y)}
days=${AOC_DAYS:-12}

for day in $(seq -w 1 $days)
do
  mkdir -p ./puzzles/$year/$day/
  aoc download -y $year -d $day -o -P -p ./puzzles/$year/$day/puzzle.md
  aoc download -y $year -d $day -o -I -i ./puzzles/$year/$day/input.txt
  echo '' >> ./puzzles/$year/$day/example.txt
done
pre-commit run --files ./puzzles/**/*
