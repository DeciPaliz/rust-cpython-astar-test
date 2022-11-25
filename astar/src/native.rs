use std::collections::{HashSet, HashMap, BinaryHeap};

macro_rules! add_usizes {
    ($cell:expr, $d:expr) => {
        if $d < 0 { $cell - (-$d as usize) } else { $cell + ($d as usize) }
    };
}

macro_rules! movement {
    ($cell:expr, $dx:expr, $dy:expr) => {
        (add_usizes!($cell.0, $dx), add_usizes!($cell.1, $dy))
    };
}

#[derive(Clone, Copy, PartialEq, Eq)]
struct TreeNode {
    priority: usize,
    point: (usize, usize)
}

impl PartialOrd for TreeNode {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        match self.priority.partial_cmp(&other.priority) {
            Some(std::cmp::Ordering::Less) => Some(std::cmp::Ordering::Greater),
            Some(std::cmp::Ordering::Greater) => Some(std::cmp::Ordering::Less),
            Some(std::cmp::Ordering::Equal) => Some(std::cmp::Ordering::Equal),
            None => None,
        }
    }
}

impl Ord for TreeNode {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        self.partial_cmp(other).unwrap()
    }
}

impl TreeNode {
    pub fn new(point: (usize, usize), priority: usize) -> TreeNode {
        TreeNode { point, priority }
    }

    pub fn get_point(&self) -> (usize, usize) {
        self.point
    }
}

pub struct GameMap {
    pub obstacles: HashSet<(usize, usize)>,
    pub width: usize,
    pub height: usize
}

impl GameMap {
    pub fn new(obstacles: HashSet<(usize, usize)>, width: usize, height: usize) -> GameMap {
        GameMap { obstacles, width, height }
    }
}

fn heuristic(from: (usize, usize), to: (usize, usize)) -> usize {
    let mut x = from.0.abs_diff(to.0);
    let mut y = from.1.abs_diff(to.1);
    let diag = x.min(y);
    x -= diag;
    y -= diag;

    diag * 14 + x * 10 + y * 10
}

fn is_legal(game_map: &GameMap, cell: (usize, usize), dx: i8, dy: i8) -> bool {
    if dx == 0 && dy == 0 { return false; }
    if (dx < 0 && (-dx as usize) > cell.0) || (dy < 0 && (-dy as usize) > cell.1) {
        return false;
    }
    let x: usize = add_usizes!(cell.0, dx);
    let y: usize = add_usizes!(cell.1, dy);
    !(
        x >= game_map.width.try_into().unwrap() ||
        y >= game_map.height.try_into().unwrap() ||
        game_map.obstacles.contains(&(x, y)) ||
        (
            (dx != 0 && dy != 0) &&
            (game_map.obstacles.contains(&(cell.0, y)) && game_map.obstacles.contains(&(x, cell.1)))
        )
    )
}

fn reconstruct(came_from: HashMap<(usize, usize), (usize, usize)>, current: (usize, usize)) -> Vec<(usize, usize)> {
    let mut path = vec![current];
    let mut current = current;
    while let Some(&cell) = came_from.get(&current) {
        current = cell;
        path.push(cell);
    }
    path.reverse();
    path
}

pub fn pathfind(game_map: &GameMap, start: (usize, usize), target: (usize, usize)) -> Option<Vec<(usize, usize)>> {
    let mut open_heap = BinaryHeap::<TreeNode>::new();
    let mut open_set = HashSet::<(usize, usize)>::new();
    let mut came_from = HashMap::<(usize, usize), (usize, usize)>::new();
    let mut g_scores = HashMap::<(usize, usize), usize>::new();
    let mut f_scores = HashMap::<(usize, usize), usize>::new();

    g_scores.insert(start, 0);
    f_scores.insert(start, heuristic(start, target));
    open_heap.push(TreeNode::new(start, *f_scores.get(&start).unwrap()));
    open_set.insert(start);

    while open_set.len() != 0 {
        let current = open_heap.pop().unwrap().get_point();
        open_set.remove(&current);
        if current == target {
            return Some(reconstruct(came_from, current));
        }
        let mut neighbours = Vec::<((usize, usize), i8, i8)>::new();
        for dx in -1..2 as i8 {
            for dy in -1..2 as i8 {
                if is_legal(game_map, current, dx, dy) {
                    neighbours.push((movement!(current, dx, dy), dx, dy));
                }
            }
        }

        for (neighbour, dx, dy) in neighbours {
            let d: usize = if dx != 0 && dy != 0 { 14 } else { 10 };
            let tentative_g_score = g_scores.get(&current).unwrap() + d;
            if g_scores.get(&neighbour).is_none() || tentative_g_score < *g_scores.get(&neighbour).unwrap() {
                came_from.insert(neighbour, current);
                g_scores.insert(neighbour, tentative_g_score);
                let f = tentative_g_score + heuristic(neighbour, target);
                f_scores.insert(neighbour, f);
                if !open_set.contains(&neighbour) {
                    open_set.insert(neighbour);
                    open_heap.push(TreeNode::new(neighbour, f));
                }
            }
        }
    }

    None
}
