use regex::Regex;

const INPUT: &str = include_str!("../input");
const Y_INTERSECT: i32 = 2_000_000;

#[derive(Debug, PartialEq)]
struct Coord {
    x: i32,
    y: i32,
}

struct Sensor {
    location: Coord,
    beacon: Coord,
    reach: i32,
}

impl Coord {
    fn distance(&self, other: &Self) -> i32 {
        (self.x - other.x).abs() + (self.y - other.y).abs()
    }
}

#[derive(Clone, Copy, Debug, PartialEq, PartialOrd)]
struct SimpleRange {
    start: i32,
    end: i32,
}

impl SimpleRange {
    fn new(start: i32, end: i32) -> Self {
        SimpleRange { start, end }
    }

    fn width(&self) -> i32 {
        self.end - self.start
    }
}

fn point_within(c: &Coord, s: &Sensor) -> bool {
    c.distance(&s.location) <= s.reach
}

fn horizontal_intersection_coord(y: i32, s: &Sensor) -> Option<Coord> {
    let c = Coord { x: s.location.x, y };
    if c.distance(&s.location) <= s.reach {
        Some(c)
    } else {
        None
    }
}

fn horizontal_intersection(y: i32, s: &Sensor) -> Option<SimpleRange> {
    let c = horizontal_intersection_coord(y, s)?;
    let d = c.distance(&s.location);

    let difference_delta = s.reach - d;

    Some(SimpleRange {
        start: (s.location.x - difference_delta),
        end: (s.location.x + difference_delta),
    })
}

fn merge_ranges(left: &SimpleRange, right: &SimpleRange) -> Option<SimpleRange> {
    if left.start > right.start {
        panic!("left and right must be ordered by start");
    }
    if right.start < left.end {
        Some(SimpleRange {
            start: left.start,
            end: right.end.max(left.end),
        })
    } else {
        None
    }
}

fn merge_ranges_iter(ranges: Vec<SimpleRange>) -> Vec<SimpleRange> {
    let mut sorted_ranges = ranges.clone();
    sorted_ranges.sort_by(|a, b| a.start.cmp(&b.start));

    sorted_ranges.iter().fold(Vec::new(), |accum, item| {
        let mut r = accum.clone();
        let left = accum.last();

        dbg!(&accum, item);

        if left.is_none() {
            r.push(*item);
            return r;
        }

        match merge_ranges(left.unwrap(), item) {
            Some(new_range) => {
                r.pop();
                r.push(new_range);
            }
            None => r.push(*item),
        }
        r
    })
}

fn parse_input(lines: &str) -> Vec<Sensor> {
    let number: Regex = Regex::new(r"-?\d+").unwrap();
    let mut sensors = Vec::new();

    // Sensor at x=2, y=18: closest beacon is at x=-2, y=15
    for line in lines.lines() {
        if line.starts_with('#') {
            continue;
        }

        let coords: Vec<_> = number.find_iter(line).collect();

        let x = coords.get(0).unwrap().as_str().parse::<i32>().unwrap();
        let y = coords.get(1).unwrap().as_str().parse::<i32>().unwrap();
        let bx = coords.get(2).unwrap().as_str().parse::<i32>().unwrap();
        let by = coords.get(3).unwrap().as_str().parse::<i32>().unwrap();

        let s = Coord { x, y };
        let b = Coord { x: bx, y: by };

        let d = s.distance(&b);

        sensors.push(Sensor {
            location: s,
            beacon: b,
            reach: d,
        });
    }

    sensors
}

fn part1(sensors: &[Sensor], y: i32) -> i32 {
    let intersections = sensors.iter().filter_map(|s| horizontal_intersection(y, s));

    let ranges = merge_ranges_iter(intersections.collect());

    ranges.iter().map(|r| r.width()).sum()
}

fn main() {
    let sensors = parse_input(INPUT);

    println!("Part 1: {}", part1(&sensors, Y_INTERSECT));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_point_within() {
        let c = Coord { x: 10, y: 10 };
        let s = Sensor {
            location: Coord { x: 5, y: 5 },
            beacon: Coord { x: 15, y: 15 },
            reach: 20,
        };
        assert!(point_within(&c, &s));
    }

    #[test]
    fn test_horizontal_intersection_coord() {
        let s = Sensor {
            location: Coord { x: 5, y: 5 },
            beacon: Coord { x: 15, y: 15 },
            reach: 20,
        };
        let s2 = Sensor {
            location: Coord { x: 5, y: 5 },
            beacon: Coord { x: 6, y: 6 },
            reach: 2,
        };

        assert_eq!(
            horizontal_intersection_coord(10, &s).unwrap(),
            Coord { x: 5, y: 10 }
        );
        assert_eq!(horizontal_intersection_coord(10, &s2), None);
    }

    #[test]
    fn test_horizontal_intersection() {
        let s = Sensor {
            location: Coord { x: 5, y: 5 },
            beacon: Coord { x: 15, y: 15 },
            reach: 20,
        };
        let s2 = Sensor {
            location: Coord { x: 5, y: 5 },
            beacon: Coord { x: 6, y: 6 },
            reach: 2,
        };

        assert_eq!(
            horizontal_intersection(10, &s).unwrap(),
            SimpleRange {
                start: -10,
                end: 20
            }
        );
        assert_eq!(horizontal_intersection(10, &s2), None);
    }

    #[test]
    fn test_merge_ranges() {
        assert_eq!(
            merge_ranges(&SimpleRange::new(0, 10), &SimpleRange::new(5, 15)).unwrap(),
            SimpleRange::new(0, 15)
        );
        assert_eq!(
            merge_ranges(&SimpleRange::new(0, 20), &SimpleRange::new(5, 15)).unwrap(),
            SimpleRange::new(0, 20)
        );
        assert_eq!(
            merge_ranges(&SimpleRange::new(-5, 0), &SimpleRange::new(100, 115)),
            None
        );
    }

    #[test]
    #[should_panic]
    fn test_merge_ranges_invalid() {
        merge_ranges(&SimpleRange::new(5, 10), &SimpleRange::new(0, 115));
    }

    #[test]
    fn test_merge_ranges_iter() {
        let ranges = vec![
            SimpleRange::new(0, 5),
            SimpleRange::new(4, 10),
            SimpleRange::new(15, 20),
            SimpleRange::new(18, 25),
            SimpleRange::new(30, 40),
        ];

        let expected = vec![
            SimpleRange::new(0, 10),
            SimpleRange::new(15, 25),
            SimpleRange::new(30, 40),
        ];

        assert_eq!(merge_ranges_iter(ranges), expected);
    }
}
