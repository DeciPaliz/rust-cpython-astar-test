import testdata
import sys
from progressbar import printProgressBar
from time import time

from astar_py import pathfind as pathfind_py
from astar.target.release.astar import pathfind as pathfind_rust

N = int(input('Enter the amount of tests: '))

rp = testdata.random_positions(N)

times_py = []
times_rust = []

printProgressBar(0, N*2, 'Progress:', length=20)

for i in range(N):
    start = rp[i][0]
    target = rp[i][1]

    printProgressBar(2*i, N*2, 'Progress:', length=20)
    s_py = time()
    pathfind_py(testdata.game_map, start, target)
    e_py = time()

    printProgressBar(2*i+1, N*2, 'Progress:', length=20)
    s_rust = time()
    pathfind_rust(testdata.game_map, start, target)
    e_rust = time()
    times_py.append(e_py - s_py)
    times_rust.append(e_rust - s_rust)

printProgressBar(N*2, N*2, 'Progress:', length=20)
sys.stdout.flush()

print('\n')

print('=== PYTHON ===')
print(f'avg: {sum(times_py)/N}')
print(f'max: {max(times_py)}')
print(f'min: {min(times_py)}')
print('')
print('==== RUST ====')
print(f'avg: {sum(times_rust)/N}')
print(f'max: {max(times_rust)}')
print(f'min: {min(times_rust)}')
