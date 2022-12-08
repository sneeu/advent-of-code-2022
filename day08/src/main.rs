type Tree = i32;
type Forest = Vec<Vec<Tree>>;

const INPUT: &str = include_str!("../input");

fn parse_grid(input: &str) -> Forest {
    let mut rows = Vec::new();

    for line in input.trim().split("\n") {
        let mut row = Vec::new();

        for char in line.chars() {
            row.push(char.to_digit(10).unwrap() as i32);
        }

        rows.push(row);
    }

    rows
}

fn visible(forest: &Forest, x: usize, y: usize) -> bool {
    let tree = forest[x][y];

    let row = &forest[x];
    let column: Vec<i32> = forest.iter().map(|row| row[y]).collect();

    let left = if y > 0 {
        *row[0..y].iter().max().unwrap()
    } else {
        -1
    };
    let right = if (y + 1) < row.len() {
        *row[(y + 1)..].iter().max().unwrap()
    } else {
        -1
    };

    let above = if x > 0 {
        *column[0..x].iter().max().unwrap()
    } else {
        -1
    };

    let below = if (x + 1) < column.len() {
        *column[(x + 1)..].iter().max().unwrap()
    } else {
        -1
    };

    left < tree || right < tree || above < tree || below < tree
}

fn visible_from(forest: &Forest, x: usize, y: usize) -> u32 {
    let tree = forest[x][y];

    let row = &forest[x];
    let column: Vec<i32> = forest.iter().map(|row| row[y]).collect();

    let mut left = 0;
    for yy in (0..y).rev() {
        left += 1;
        if row[yy] >= tree {
            break
        }
    }

    let mut right = 0;
    for yy in (y + 1)..row.len() {
        right += 1;
        if row[yy] >= tree {
            break
        }
    }

    let mut above = 0;
    for xx in (0..x).rev() {
        above += 1;
        if column[xx] >= tree {
            break
        }
    }

    let mut below = 0;
    for xx in (x + 1)..column.len() {
        below += 1;
        if column[xx] >= tree {
            break;
        }
    }

    left * right * above * below
}

fn part1(forest: &Forest) -> i32 {
    // Naïve …
    let mut visible_count = 0;

    let width = forest.len();
    let height = forest[0].len();

    for x in 0..width {
        for y in 0..height {
            let is_visible = visible(&forest, x, y);
            if is_visible {
                visible_count += 1;
            }
        }
    }

    visible_count
}

fn part2(forest: &Forest) -> u32 {
    let mut max_view = 0;

    let width = forest.len();
    let height = forest[0].len();

    for x in 0..width {
        for y in 0..height {
            max_view = max_view.max(visible_from(&forest, x, y));
        }
    }
    
    max_view
}

fn main() {
    let tree_grid: Vec<Vec<i32>> = parse_grid(INPUT);

    println!("Part 1: {}", part1(&tree_grid));
    println!("Part 2: {}", part2(&tree_grid));
}

#[test]
fn test_tiny_forest() {
    let forest = vec![vec![0]];
    assert!(visible(&forest, 0, 0));
}

#[test]
fn test_large_forest() {
    let forest = vec![
        vec![3, 0, 3, 7, 3],
        vec![2, 5, 5, 1, 2],
        vec![6, 5, 3, 3, 2],
        vec![3, 3, 5, 4, 9],
        vec![3, 5, 3, 9, 0],
    ];

    assert!(visible(&forest, 1, 1));
    assert!(visible(&forest, 1, 2));
    assert!(!visible(&forest, 1, 3));
    assert!(visible(&forest, 2, 1));
    assert!(!visible(&forest, 2, 2));
    assert!(visible(&forest, 2, 3));
    assert!(!visible(&forest, 3, 1));
    assert!(visible(&forest, 3, 2));
    assert!(!visible(&forest, 3, 3));
}

#[test]
fn test_tiny_forest_visible_from() {
    let forest = vec![vec![0]];
    assert_eq!(visible_from(&forest, 0, 0), 0);
}

#[test]
fn test_small_forest_visible_from() {
    let forest = vec![
        vec![0, 0, 0],
        vec![0, 1, 0],
        vec![0, 0, 0],
    ];
    assert_eq!(visible_from(&forest, 1, 1), 1);
}

#[test]
fn test_medium_forest_visible_from() {
    let forest = vec![
        vec![0, 0, 0, 0, 0],
        vec![2, 1, 0, 0, 0],
        vec![0, 5, 3, 0, 0],
        vec![0, 0, 2, 0, 0],
        vec![0, 0, 0, 0, 0],
    ];
    assert_eq!(visible_from(&forest, 2, 2), 8);
}

#[test]
fn test_large_forest_visible_from() {
    let forest = vec![
        vec![3, 0, 3, 7, 3],
        vec![2, 5, 5, 1, 2],
        vec![6, 5, 3, 3, 2],
        vec![3, 3, 5, 4, 9],
        vec![3, 5, 3, 9, 0],
    ];
    assert_eq!(visible_from(&forest, 3, 2), 8);
}