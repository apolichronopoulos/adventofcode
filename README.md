# adventofcode

Personal repository for advent of code challenges

## [2024](https://adventofcode.com/2024)

[1](https://adventofcode.com/2024/day/1) - [2](https://adventofcode.com/2024/day/2) - [3](https://adventofcode.com/2024/day/3) - [4](https://adventofcode.com/2024/day/4) - [5](https://adventofcode.com/2024/day/5) - [6](https://adventofcode.com/2024/day/6) - [7](https://adventofcode.com/2024/day/7) - [8](https://adventofcode.com/2024/day/8) - [9](https://adventofcode.com/2024/day/9) - [10](https://adventofcode.com/2024/day/10) - [11](https://adventofcode.com/2024/day/11) - [12](https://adventofcode.com/2024/day/12) - [13](https://adventofcode.com/2024/day/13) - [14](https://adventofcode.com/2024/day/14) - [15](https://adventofcode.com/2024/day/15) - [16](https://adventofcode.com/2024/day/16) - [17](https://adventofcode.com/2024/day/17) - [18](https://adventofcode.com/2024/day/18) - [19](https://adventofcode.com/2024/day/19) - [20](https://adventofcode.com/2024/day/20) - [21](https://adventofcode.com/2024/day/21) - [22](https://adventofcode.com/2024/day/22) - [23](https://adventofcode.com/2024/day/23) - [24](https://adventofcode.com/2024/day/24) - [25](https://adventofcode.com/2024/day/25)

## [2023](https://adventofcode.com/2023)

[1](https://adventofcode.com/2023/day/1) - [2](https://adventofcode.com/2023/day/2) - [3](https://adventofcode.com/2023/day/3) - [4](https://adventofcode.com/2023/day/4) - [5](https://adventofcode.com/2023/day/5) - [6](https://adventofcode.com/2023/day/6) - [7](https://adventofcode.com/2023/day/7) - [8](https://adventofcode.com/2023/day/8) - [9](https://adventofcode.com/2023/day/9) - [10](https://adventofcode.com/2023/day/10) - [11](https://adventofcode.com/2023/day/11) - [12](https://adventofcode.com/2023/day/12) - [13](https://adventofcode.com/2023/day/13) - [14](https://adventofcode.com/2023/day/14) - [15](https://adventofcode.com/2023/day/15) - [16](https://adventofcode.com/2023/day/16) - [17](https://adventofcode.com/2023/day/17) - [18](https://adventofcode.com/2023/day/18) - [19](https://adventofcode.com/2023/day/19) - [20](https://adventofcode.com/2023/day/20) - [21](https://adventofcode.com/2023/day/21) - [22](https://adventofcode.com/2023/day/22) - [23](https://adventofcode.com/2023/day/23) - [24](https://adventofcode.com/2023/day/24) - [25](https://adventofcode.com/2023/day/25)

## Python

Create a venv with custom requirements

```bash
cd ./python
rm -rf venv
python3.11 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
pip install --upgrade pip
```

## Run puzzles

Use venv (or any other python env you want)

```bash
. ./python/venv/bin/activate
```

Run as module

```bash
cd ./python
python -m 2024.puzzle_2024_01 ../puzzles
python -m 2024.puzzle_2024_02 ../puzzles
python -m 2024.puzzle_2024_03 ../puzzles
python -m 2024.puzzle_2024_04 ../puzzles
python -m 2024.puzzle_2024_05 ../puzzles
python -m 2024.puzzle_2024_06 ../puzzles
python -m 2024.puzzle_2024_07 ../puzzles
python -m 2024.puzzle_2024_08 ../puzzles
```

or include path, to use utils

```bash
cd ./python
export PYTHONPATH=$(pwd)
python ./2024/puzzle_2024_01.py ../puzzles
python ./2024/puzzle_2024_02.py ../puzzles
python ./2024/puzzle_2024_03.py ../puzzles
python ./2024/puzzle_2024_04.py ../puzzles
```

# aoc-cli

Download puzzle description using [aoc-cli](https://github.com/scarvalhojr/aoc-cli)

```bash
current_year=$(date +%Y)
for day in {01..25}
do
  mkdir ./puzzles/$current_year/$day/
  aoc -y $current_year -d $day > ./puzzles/$current_year/$day/puzzle.md
done
```
