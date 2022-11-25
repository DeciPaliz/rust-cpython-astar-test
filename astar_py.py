def parent(i):
    return (i - 1) // 2


def left_child(i):
    return ((2 * i) + 1)


def right_child(i):
    return ((2 * i) + 2)


class MinHeap:
    def __init__(self):
        self.contents = []

    def _heapify(self, i):
        left = left_child(i)
        right = right_child(i)
        size = len(self.contents)
        largest = i
        if left < size and self.contents[left][1] > self.contents[largest][1]:
            largest = left
        if right < size and self.contents[right][1] > self.contents[largest][1]:
            largest = right
        if largest != i:
            self.contents[i], self.contents[largest] = self.contents[largest], self.contents[i]
            self._heapify(largest)

    def insert(self, data, p):
        i = len(self.contents)
        self.contents.append((data, p))
        while self.contents[parent(i)][1] >= p and i > 0:
            self.contents[parent(i)], self.contents[i] = self.contents[i], self.contents[parent(i)]
            i = parent(i)

    def pop(self):
        self.contents[0], self.contents[-1] = self.contents[-1], self.contents[0]
        res = self.contents.pop()[0]
        self._heapify(0)
        return res

    def contains(self, data):
        return data in [x for x, _ in self.contents]

    def __len__(self):
        return len(self.contents)


def heuristic(start, target):
    x = abs(target[0] - start[0])
    y = abs(target[1] - start[1])
    diag = min(x, y)
    x -= diag
    y -= diag
    return diag * 14 + x * 10 + y * 10


def is_legal(game_map, cell, dx, dy):
    return not (
        cell[0] + dx < 0 or
        cell[1] + dy < 0 or
        cell[0] + dx >= len(game_map[0]) or
        cell[1] + dy >= len(game_map) or
        game_map[cell[1] + dy][cell[0] + dx] or
        (
            (dx != 0 and dy != 0) and
            (game_map[cell[1]][cell[0] + dx] and game_map[cell[1] + dy][cell[0]])
        )
    )


def reconstruct(cameFrom, current):
    total_path = [current]
    while cameFrom[current[1]][current[0]] is not None:
        current = cameFrom[current[1]][current[0]]
        total_path.insert(0, current)
    return total_path


def pathfind(game_map, start, target):
    height = len(game_map)
    width = len(game_map[0])

    openHeap = MinHeap()
    cameFrom = []
    for i in range(height):
        cameFrom.append([None] * width)

    gScore = []
    for i in range(height):
        gScore.append([-1] * width)
    gScore[start[1]][start[0]] = 0

    fScore = []
    for i in range(height):
        fScore.append([-1] * width)
    fScore[start[1]][start[0]] = heuristic(start, target)
    openHeap.insert(start, fScore[start[1]][start[0]])

    while len(openHeap) != 0:
        current = openHeap.pop()
        if current == target:
            return reconstruct(cameFrom, current)

        links = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1)
        ]
        for neighbour_x, neighbour_y, dx, dy in [(current[0] + dx, current[1] + dy, dx, dy) for dx, dy in links if is_legal(game_map, current, dx, dy)]:
            neighbour = (neighbour_x, neighbour_y)
            d = 14 if dx != 0 and dy != 0 else 10
            tentative_gScore = gScore[current[1]][current[0]] + d
            if tentative_gScore < gScore[neighbour[1]][neighbour[0]] or gScore[neighbour[1]][neighbour[0]] == -1:
                cameFrom[neighbour[1]][neighbour[0]] = current
                gScore[neighbour[1]][neighbour[0]] = tentative_gScore
                f = tentative_gScore + heuristic(neighbour, target)
                fScore[neighbour[1]][neighbour[0]] = f
                if not openHeap.contains(neighbour):
                    openHeap.insert(neighbour, f)

    return None
