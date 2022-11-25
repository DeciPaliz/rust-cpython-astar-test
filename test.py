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

py_avg = sum(times_py)/N
py_max = max(times_py)
py_min = min(times_py)
rust_avg = sum(times_rust)/N
rust_max = max(times_rust)
rust_min = min(times_rust)


print('=== PYTHON ===')
print(f'avg: {py_avg}')
print(f'max: {py_max}')
print(f'min: {py_min}')
print('')
print('==== RUST ====')
print(f'avg: {rust_avg}')
print(f'max: {rust_max}')
print(f'min: {rust_min}')
print('')
print('==============')
print('Rust is better than Python by:')
print(f'  {py_avg/rust_avg*100 if py_avg > rust_avg else -rust_avg/py_avg*100}% (avg)')
print(f'  {py_max/rust_max*100 if py_max > rust_max else -rust_max/py_max*100}% (max)')
print(f'  {py_min/rust_min*100 if py_min > rust_min else -rust_min/py_min*100}% (min)')
