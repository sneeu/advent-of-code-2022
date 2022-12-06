use std::collections::VecDeque;

const INPUT: &str = include_str!("../input");

fn unique(buff: &VecDeque<char>) -> bool {
    let buffer_length = buff.len();

    for i in 0..buffer_length {
        for j in (i + 1)..buffer_length {
            if buff[i] == buff[j] {
                return false;
            }
        }
    }

    return true;
}

fn part_x(input: &str, unique_length: usize) -> Option<usize> {
    let mut buffer = VecDeque::with_capacity(4);
    let mut length = 0;

    for c in input.chars() {
        if buffer.len() == unique_length {
            buffer.pop_back();
        }

        buffer.push_front(c);
        length += 1;

        if length >= unique_length && unique(&buffer) {
            return Some(length);
        }
    }

    None
}

fn main() {
    println!("Part 1:  {}", part_x(INPUT, 4).unwrap());
    println!("Part 2:  {}", part_x(INPUT, 14).unwrap());
}
