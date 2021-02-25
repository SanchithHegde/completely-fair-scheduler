# Completely Fair Scheduler (CFS)

The process scheduler used in Linux kernel (since version 2.6.23), simulated
using Python. The only change is that it uses SortedKeyList instead of a
red-black tree, but has the same time complexity of operations.

## Installing Dependencies

- Install [`poetry`](https://python-poetry.org/docs/).
- Install requirements:

  ```shell
  poetry install --no-root
  ```

- Activate the environment:

  ```shell
  poetry shell
  ```

## Running

`python3 cfs.py`

## License

[MIT](LICENSE)
