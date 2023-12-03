package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func puzzle1(filename string, maxColors map[byte]int) {
	file, err := os.Open(filename)
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	sum := 0

	for scanner.Scan() {
		line := scanner.Text()
		fmt.Println(line)
		x := strings.Split(line, ":")
		game, err := strconv.Atoi(strings.Fields(x[0])[1])
		if err != nil {
			fmt.Println("Error converting game value:", err)
			return
		}
		possible := true

		for _, round := range strings.Split(x[1], ";") {
			for _, color := range strings.Split(round, ",") {
				fields := strings.Fields(color)
				n, err := strconv.Atoi(fields[0])
				if err != nil {
					fmt.Println("Error converting n value:", err)
					return
				}
				c := fields[1][0]
				if maxColors[c] < n {
					possible = false
				}
			}
		}

		if possible {
			sum += game
		}
	}

	if err := scanner.Err(); err != nil {
		fmt.Println("Error reading file:", err)
		return
	}

	fmt.Printf("result: %d\n", sum)
}

func puzzle2(filename string) {
	file, err := os.Open(filename)
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	sum := 0

	for scanner.Scan() {
		line := scanner.Text()
		fmt.Println(line)
		x := strings.Split(line, ":")
		maxColors := map[byte]int{'r': 0, 'g': 0, 'b': 0}

		for _, round := range strings.Split(x[1], ";") {
			for _, color := range strings.Split(round, ",") {
				fields := strings.Fields(color)
				n, err := strconv.Atoi(fields[0])
				if err != nil {
					fmt.Println("Error converting n value:", err)
					return
				}
				c := fields[1][0]
				if maxColors[c] < n {
					maxColors[c] = n
				}
			}
		}

		power := max(maxColors['r'], 1) * max(maxColors['g'], 1) * max(maxColors['b'], 1)

		fmt.Printf("maxColors %v\n", maxColors)
		fmt.Printf("power %d\n", power)

		sum += power
	}

	if err := scanner.Err(); err != nil {
		fmt.Println("Error reading file:", err)
		return
	}

	fmt.Printf("result: %d\n", sum)
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func main() {
	// Uncomment the lines below to run the script
	puzzle1("../puzzles/2023/02/example.txt", map[byte]int{'r': 12, 'g': 13, 'b': 14}) // result -> 8
	puzzle1("../puzzles/2023/02/input.txt", map[byte]int{'r': 12, 'g': 13, 'b': 14})   // result -> 2169
	puzzle2("../puzzles/2023/02/example.txt")                                          // result -> 2286
	puzzle2("../puzzles/2023/02/input.txt")                                            // correct -> 60948
}
