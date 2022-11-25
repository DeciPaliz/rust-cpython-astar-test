# rust-cpython-astar-test
A pseudo-benchmark created to compare performance of the A* algorithm written in Rust and in Python.

Thanks to [Greenstick](https://stackoverflow.com/users/2206251/greenstick) for the code for the progress bar ([stackoverflow answer](https://stackoverflow.com/a/34325723)).

## How to use

Rust needs to be installed on your system. 

To build the library, `cd` into the `astar` directory and run `cargo build --release`. In order for `test.py` to import the library, the file `astar/target/release/libastar.so` (or `libastar.dylib` if you're on Mac, or `libastar.dll` if you're on Windows) needs to be renamed to `astar.so` (or `astar.dll` if you're on Windows).

Then run `python test.py`.
