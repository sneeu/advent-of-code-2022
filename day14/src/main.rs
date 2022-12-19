use std::collections::HashSet;

const INPUT: &str = include_str!("../input");
const MOVES: [(i32, i32); 3] = [(0, -1), (-1, -1), (1, -1)];

#[derive(Clone, Copy, PartialEq, Eq, Hash)]
struct Coord {
    x: i32,
    y: i32,
}

fn generate_rocks(from: &Coord, to: &Coord) -> Vec<Coord> {
    let mut sx = from.x.min(to.x);
    let ex = from.x.max(to.x);

    let mut sy = from.y.min(to.y);
    let ey = from.y.max(to.y);

    let dx = if sx == ex { 0 } else { 1 };
    let dy = if sy == ey { 0 } else { 1 };

    let mut coords = vec![];

    while sx < ex || sy < ey {
        sx += dx;
        sy += dy;

        coords.push(Coord { x: sx, y: sy });
    }

    coords
}

fn parse_coord(coord_str: &str) -> Coord {
    let mut xy = coord_str.split(",").map(|c| c.parse::<i32>().unwrap());

    Coord {
        x: xy.next().unwrap(),
        y: xy.next().unwrap(),
    }
}

fn parse_line(line: &str) -> Vec<Coord> {
    let mut r = Vec::new();

    for coord in line.split("->") {
        r.push(parse_coord(coord));
    }

    r
}

fn parse_rocks(input: &str) -> HashSet<Coord> {
    // 529,71 -> 529,72 -> 539,72 -> 539,71
    let mut rocks = HashSet::new();

    let lines = input.lines().map(parse_line).collect::<Vec<_>>();

    for line in lines {
        for w in line.windows(2) {
            for r in generate_rocks(&w[0], &w[1]) {
                rocks.insert(r);
            }
        }
    }

    rocks
}

fn bounds(rocks: HashSet<Coord>) -> (Coord, Coord) {
    let bottom_left = rocks.iter().reduce(|accum, value| { &Coord { x: accum.x.min(value.x), y: accum.x.min(value.x) }}).unwrap();
    let top_right = rocks.iter().reduce(|accum, value| { &Coord { x: accum.x.max(value.x), y: accum.x.max(value.x) }}).unwrap();

    (*bottom_left, *top_right)
}

fn out_of_bounds(c: Coord, bottom: i32) -> bool {
    c.y < bottom
}

fn part1(rocks: HashSet<Coord>) -> u32 {
    let starting_position = Coord { x: 500, y: 0 };
    let (Coord { x: bottom, y: _}, _) = bounds(rocks);

    let mut sand = starting_position.clone();

    while !out_of_bounds(sand, bottom) {
        for (mx, my) in MOVES {
            let option = Coord { x: sand.x + mx, y: sand.y + my };
            if !rocks.contains(&option) {
                rocks.insert(option);
                break;
            }
        }
    }

    0
}

fn main() {
    let coords = parse_rocks(INPUT);
    println!("Part 1: {}", part1(coords));
}
