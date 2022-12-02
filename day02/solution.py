ROCK_PAPER_SCISSORS = {
    "A": "rock",
    "B": "paper",
    "C": "scissors",
    "X": "rock",
    "Y": "paper",
    "Z": "scissors",
}

POSITIONS = {
    "rock": 0,
    "paper": 1,
    "scissors": 2,
}

RPS_SCORE = {
    "rock": 1,
    "paper": 2,
    "scissors": 3,
}

POINTS = {
    "win": 6,
    "loss": 0,
    "tie": 3,
}


def compare(left, right):
    if left == right:
        return "tie"
    elif (left + 1) % 3 == right:
        return "win"
    return "loss"


def line_result(line):
    left, right = line[0], line[2]
    left = ROCK_PAPER_SCISSORS[left]
    right = ROCK_PAPER_SCISSORS[right]
    left_pos = POSITIONS[left]
    right_pos = POSITIONS[right]
    result = compare(left_pos, right_pos)

    return POINTS[result] + RPS_SCORE[right]


def part1(lines):
    return sum(line_result(line) for line in lines)


# There's a lot of machinery in Part 1 but there's only 9 possible lines.
PART2_SCORES = {
    "A X": POINTS["loss"] + RPS_SCORE["scissors"], # Lose to rock
    "A Y": POINTS["tie"] + RPS_SCORE["rock"], # Tie to rock
    "A Z": POINTS["win"] + RPS_SCORE["paper"], # Win to rock
    "B X": POINTS["loss"] + RPS_SCORE["rock"], # Lose to paper
    "B Y": POINTS["tie"] + RPS_SCORE["paper"],
    "B Z": POINTS["win"] + RPS_SCORE["scissors"],
    "C X": POINTS["loss"] + RPS_SCORE["paper"], # Lose to scissors
    "C Y": POINTS["tie"] + RPS_SCORE["scissors"],
    "C Z": POINTS["win"] + RPS_SCORE["rock"],
}


def part2(lines):
    return sum(PART2_SCORES[line.strip()] for line in lines)


def main():
    with open("input") as f:
        lines = f.readlines()

    print("Part 1: ", part1(list(lines)))
    print("Part 2: ", part2(list(lines)))


if __name__ == "__main__":
    main()