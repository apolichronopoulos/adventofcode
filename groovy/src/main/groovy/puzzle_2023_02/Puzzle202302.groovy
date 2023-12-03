static def puzzle1(filename, maxColors) {
    def file = new File(filename)
    def sum = 0

    file.eachLine { line ->
        println(line)
        def x = line.split(":")
        def game = Integer.parseInt(x[0].trim().split()[1])
        def possible = true

        x[1].split(";").each { round ->
            round.split(",").each { color ->
                def n = Integer.parseInt(color.trim().split()[0])
                def c = color.trim().split()[1][0]

                if (maxColors[c] < n) {
                    possible = false
                }
            }
        }

        if (possible) {
            sum += game
        }
    }

    println("result: $sum")
}

static def puzzle2(filename) {
    def file = new File(filename)
    def sum = 0

    file.eachLine { line ->
        println(line)
        def x = line.split(":")
        def maxColors = ['r': 0, 'g': 0, 'b': 0]

        x[1].split(";").each { round ->
            round.split(",").each { color ->
                def n = Integer.parseInt(color.trim().split()[0])
                def c = color.trim().split()[1][0]

                if (maxColors[c] < n) {
                    maxColors[c] = n
                }
            }
        }

        def power = Math.max(maxColors['r'], 1) * Math.max(maxColors['g'], 1) * Math.max(maxColors['b'], 1)

        println("maxColors $maxColors\n")
        println("power $power\n")

        sum += power
    }

    println("result: $sum")
}

static void main(String[] args) {
    println "Hello world!"

// Uncomment the lines below to run the script
//    puzzle1('example.txt', [r: 12, g: 13, b: 14])  // result -> 8
// puzzle1('input.txt', [r: 12, g: 13, b: 14])  // result -> 2169
// puzzle2('example.txt')  // result -> 2286
 puzzle2('input.txt')  // correct -> 60948

}
