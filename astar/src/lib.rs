extern crate cpython;

mod native;

use std::collections::HashSet;

use cpython::{Python, PyList, PyResult, py_module_initializer, py_fn, PyTuple, PyErr, exc, ToPyObject};

py_module_initializer!(astar, |py, m| {
    m.add(py, "__doc__", "ABOBUS")?;
    m.add(py, "pathfind", py_fn!(py, pathfind_py(game_map: PyList, start: PyTuple, target: PyTuple)))?;
    Ok(())
});

fn pathfind_py(py: Python, game_map_py: PyList, start_py: PyTuple, target_py: PyTuple) -> PyResult<PyList> {
    let mut list = PyList::new(py, &[]);
    if start_py.len(py) != 2 || target_py.len(py) != 2 ||
        start_py.get_item(py, 0).extract::<usize>(py).is_err() ||
        start_py.get_item(py, 1).extract::<usize>(py).is_err() ||
        target_py.get_item(py, 0).extract::<usize>(py).is_err() ||
        target_py.get_item(py, 1).extract::<usize>(py).is_err()
    {
        return Err(PyErr::new::<exc::TypeError, _>(py, "start and target must be points (int, int)"));
    }
    let start = (start_py.get_item(py, 0).extract::<usize>(py).unwrap(), start_py.get_item(py, 1).extract::<usize>(py).unwrap());
    let target = (target_py.get_item(py, 0).extract::<usize>(py).unwrap(), target_py.get_item(py, 1).extract::<usize>(py).unwrap());

    let mut obstacles: HashSet<(usize, usize)> = HashSet::new();
    for i in 0..game_map_py.len(py) {
        for j in 0..game_map_py.get_item(py, 0).extract::<PyList>(py).unwrap().len(py) {
            if game_map_py.get_item(py, i).extract::<PyList>(py).unwrap().get_item(py, j).extract::<bool>(py).unwrap() {
                obstacles.insert((j, i));
            }
        }
    }

    let game_map = native::GameMap::new(obstacles, game_map_py.get_item(py, 0).extract::<PyList>(py).unwrap().len(py), game_map_py.len(py));
    if let Some(path) = native::pathfind(&game_map, start, target) {
        list = path.to_py_object(py);
    }

    Ok(list)
}
