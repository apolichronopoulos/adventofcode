# adventofcode

Personal repository for advent of code challenges

## [2025](https://adventofcode.com/2025)

Starting this year, there will be 12 days of puzzles each December.

[1](https://adventofcode.com/2025/day/1) - [2](https://adventofcode.com/2025/day/2) - [3](https://adventofcode.com/2025/day/3) - [4](https://adventofcode.com/2025/day/4) - [5](https://adventofcode.com/2025/day/5) - [6](https://adventofcode.com/2025/day/6) - [7](https://adventofcode.com/2025/day/7) - [8](https://adventofcode.com/2025/day/8) - [9](https://adventofcode.com/2025/day/9) - [10](https://adventofcode.com/2025/day/10) - [11](https://adventofcode.com/2025/day/11) - [12](https://adventofcode.com/2025/day/12)

## [2024](https://adventofcode.com/2024)

[1](https://adventofcode.com/2024/day/1) - [2](https://adventofcode.com/2024/day/2) - [3](https://adventofcode.com/2024/day/3) - [4](https://adventofcode.com/2024/day/4) - [5](https://adventofcode.com/2024/day/5) - [6](https://adventofcode.com/2024/day/6) - [7](https://adventofcode.com/2024/day/7) - [8](https://adventofcode.com/2024/day/8) - [9](https://adventofcode.com/2024/day/9) - [10](https://adventofcode.com/2024/day/10) - [11](https://adventofcode.com/2024/day/11) - [12](https://adventofcode.com/2024/day/12) - [13](https://adventofcode.com/2024/day/13) - [14](https://adventofcode.com/2024/day/14) - [15](https://adventofcode.com/2024/day/15) - [16](https://adventofcode.com/2024/day/16) - [17](https://adventofcode.com/2024/day/17) - [18](https://adventofcode.com/2024/day/18) - [19](https://adventofcode.com/2024/day/19) - [20](https://adventofcode.com/2024/day/20) - [21](https://adventofcode.com/2024/day/21) - [22](https://adventofcode.com/2024/day/22) - [23](https://adventofcode.com/2024/day/23) - [24](https://adventofcode.com/2024/day/24) - [25](https://adventofcode.com/2024/day/25)

## [2023](https://adventofcode.com/2023)

[1](https://adventofcode.com/2023/day/1) - [2](https://adventofcode.com/2023/day/2) - [3](https://adventofcode.com/2023/day/3) - [4](https://adventofcode.com/2023/day/4) - [5](https://adventofcode.com/2023/day/5) - [6](https://adventofcode.com/2023/day/6) - [7](https://adventofcode.com/2023/day/7) - [8](https://adventofcode.com/2023/day/8) - [9](https://adventofcode.com/2023/day/9) - [10](https://adventofcode.com/2023/day/10) - [11](https://adventofcode.com/2023/day/11) - [12](https://adventofcode.com/2023/day/12) - [13](https://adventofcode.com/2023/day/13) - [14](https://adventofcode.com/2023/day/14) - [15](https://adventofcode.com/2023/day/15) - [16](https://adventofcode.com/2023/day/16) - [17](https://adventofcode.com/2023/day/17) - [18](https://adventofcode.com/2023/day/18) - [19](https://adventofcode.com/2023/day/19) - [20](https://adventofcode.com/2023/day/20) - [21](https://adventofcode.com/2023/day/21) - [22](https://adventofcode.com/2023/day/22) - [23](https://adventofcode.com/2023/day/23) - [24](https://adventofcode.com/2023/day/24) - [25](https://adventofcode.com/2023/day/25)

## Development Setup

```bash
brew install pyenv pyenv-virtualenv pre-commit scarvalhojr/tap/aoc-cli
```

## Python

Create a pyenv with custom requirements

```bash
pyenv virtualenv 3.12 aoc
pyenv local aoc
```

Update requirements

```bash
cd ./python
pip install -r requirements.txt
pip install --upgrade pip
```

## Run puzzles

Use pyenv (or any other python env you want)

```bash
pyenv local aoc
```

### Run specific puzzle

```bash
cd ./python && year=2024 && day=01
python -m ${year}.puzzle_${year}_${day} ../puzzles
```

### Run all puzzles

Run as module

```bash
cd ./python
year=$(date -v -11m +%Y)
for day in {01..25}
do
  python -m ${year}.puzzle_${year}_${day} ../puzzles
done
```

or include path, to use utils

```bash
cd ./python
export PYTHONPATH=$(pwd)
year=$(date -v -11m +%Y)
for day in {01..25}
do
  python ./${year}/puzzle_${year}_${day}.py ../puzzles
done
```

# aoc-cli

Download puzzle description and/or input using [aoc-cli](https://github.com/scarvalhojr/aoc-cli)

_Note: to use authenticated requests put your session token in `~/.adventofcode.session`_

```bash
AOC_YEAR=2025 AOC_DAYS=12 ./scripts/download-aoc-files.sh
```
