# Completely Fair Scheduler (CFS)

The process scheduler used in Linux kernel (since version 2.6.23), simulated 
using Python. The only change is that it uses SortedKeyList instead of a 
red-black tree, but has the same time complexity of operations.

## Installing Dependencies

Run `pip3 install -r requirements.txt` to install the dependencies, with the 
`--user` flag if required.

## Running
```python3 cfs.py```
