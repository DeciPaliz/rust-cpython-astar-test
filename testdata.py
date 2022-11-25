game_map = []

_f = open('map.txt', 'r')
_s = _f.read()
_f.close()
_s = _s.split()
while '' in _s:
    _s.remove('')
for i in range(len(_s)):
    game_map.append([])
    for c in _s[i]:
        game_map[i].append(c == '#')


def print_map(path):
    for i in range(len(game_map)):
        for j in range(len(game_map[i])):
            c = '#' if game_map[i][j] else '.'
            if (j, i) in path:
                c = '\033[91m*\033[0m'
            print(c, end='')
        print('')


def random_positions(amount=1000):
    from random import choice
    res = []
    for i in range(amount):
        start = None
        target = None
        while True:
            x, y = choice(range(len(game_map[0]))), choice(range(len(game_map)))
            if not game_map[y][x]:
                start = (x, y)
                break
        while True:
            x, y = choice(range(len(game_map[0]))), choice(range(len(game_map)))
            if not game_map[y][x]:
                target = (x, y)
                break
        res.append((start, target))
    return res
