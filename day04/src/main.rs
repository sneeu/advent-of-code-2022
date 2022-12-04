use std::ops::Range;

fn covers(left: &Range<i32>, right: &Range<i32>) -> bool {
    left.start <= right.start && left.end >= right.end
}

fn between(x: i32, r: &Range<i32>) -> bool {
    x >= r.start && x <= r.end
}

fn overlaps(left: &Range<i32>, right: &Range<i32>) -> bool {
    between(right.start, left) || between(right.end, left)
}

fn parse_line(line: &str) -> (Range<i32>, Range<i32>) {
    let (left, right) = line.split_once(",").unwrap();
    let (ls, le) = left.split_once("-").unwrap();
    let (rs, re) = right.split_once("-").unwrap();

    (
        Range {
            start: ls.parse::<i32>().unwrap(),
            end: le.parse::<i32>().unwrap(),
        },
        Range {
            start: rs.parse::<i32>().unwrap(),
            end: re.parse::<i32>().unwrap(),
        },
    )
}

fn main() {
    const INPUT: &str = include_str!("../input");

    let ranges = INPUT.split("\n").filter(|l| l.len() > 0).map(parse_line);

    println!(
        "Part 1:  {}",
        ranges
            .clone()
            .filter(|(l, r)| { covers(l, r) || covers(r, l) })
            .collect::<Vec<(Range<i32>, Range<i32>)>>()
            .len()
    );

    println!(
        "Part 2:  {}",
        ranges
            .clone()
            .filter(|(l, r)| { overlaps(l, r) || overlaps(r, l) })
            .collect::<Vec<(Range<i32>, Range<i32>)>>()
            .len()
    );
}
