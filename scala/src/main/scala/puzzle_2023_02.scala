import scala.io.Source

object puzzle_2023_02 {
  def puzzle1(filename: String, maxColors: Map[Char, Int]): Unit = {
    val file = Source.fromFile(filename)
    var sum = 0

    for (line <- file.getLines()) {
      println(line)
      val x = line.split(":")
      val game = x(0).trim.split(" ")(1).toInt
      var possible = true

      for (round <- x(1).split(";")) {
        for (color <- round.split(",")) {
          val Array(n, c) = color.trim.split(" ")
          if (maxColors(c.charAt(0)) < n.toInt) {
            possible = false
          }
        }
      }

      if (possible) {
        sum += game
      }
    }

    file.close()
    println(s"result: $sum")
  }

  def puzzle2(filename: String): Unit = {
    val file = Source.fromFile(filename)
    var sum = 0

    for (line <- file.getLines()) {
      println(line)
      val x = line.split(":")
      var maxColors = Map('r' -> 0, 'g' -> 0, 'b' -> 0)

      for (round <- x(1).split(";")) {
        for (color <- round.split(",")) {
          val Array(n, c) = color.trim.split(" ")
          if (maxColors(c.charAt(0)) < n.toInt) {
            maxColors += (c.charAt(0) -> n.toInt)
          }
        }
      }

      val power = Math.max(maxColors('r'), 1) * Math.max(maxColors('g'), 1) * Math.max(maxColors('b'), 1)

      println(s"maxColors $maxColors\n")
      println(s"power $power\n")

      sum += power
    }

    file.close()
    println(s"result: $sum")
  }

  def main(args: Array[String]): Unit = {
    // Uncomment the lines below to run the script
    puzzle1("puzzles/2023/02/example.txt", Map('r' -> 12, 'g' -> 13, 'b' -> 14)) // result -> 8
    puzzle1("puzzles/2023/02/input.txt", Map('r' -> 12, 'g' -> 13, 'b' -> 14)) // result -> 2169
    puzzle2("puzzles/2023/02/example.txt") // result -> 2286
    puzzle2("puzzles/2023/02/input.txt") // correct -> 60948
  }
}
