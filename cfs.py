#!/usr/bin/env python3

""" Program to simulate Completely Fair Scheduler (CFS). """

import sys
import random
from math import floor
from typing import Callable, List
from sortedcontainers import SortedKeyList
import numpy
from tabulate import tabulate
import sched_algs


def cfs_schedule(tasks: List[dict], quantum: int):
    """ Schedule tasks according to CFS algorithm and set waiting and
        turnaround times. """
    get_vruntime: Callable[[dict], int] = lambda task: task["vruntime"]
    get_nice: Callable[[dict], int] = lambda task: task["nice"]

    tasks_sorted = SortedKeyList(key=get_vruntime)
    tasks_sorted.add(tasks[0])
    end = 1
    timer = tasks[0]["arrival_time"]
    min_vruntime = 0

    while (num := len(tasks_sorted)) > 0:
        # Add tasks that have arrived after previous iteration
        for task in tasks[end:]:
            if task["arrival_time"] <= timer:
                task["waiting_time"] = timer - task["arrival_time"]
                task["turnaround_time"] = task["waiting_time"]
                task["vruntime"] = min_vruntime
                tasks_sorted.add(task)
                num += 1
                end += 1

        timeslice = floor(quantum / num)  # Dynamic timeslice
        min_task = tasks_sorted[0]

        # Time remaining for smallest task
        t_rem = min_task["burst_time"] - min_task["exec_time"]

        # Time of execution of smallest task
        time = min([timeslice, t_rem])
        min_vruntime = get_vruntime(min_task)
        min_nice = get_nice(min_task)

        # display_tasks(tasks_sorted)
        # print(f'Executing task {min_task["pid"]} for {time} seconds\n')

        # Execute process
        vruntime = min_vruntime + time * min_nice
        min_task["exec_time"] += time
        min_task["turnaround_time"] += time
        timer += time

        # Increment waiting and turnaround time of all other processes
        for i in range(1, num):
            tasks_sorted[i]["waiting_time"] += time
            tasks_sorted[i]["turnaround_time"] += time

        # Remove from sorted list and update vruntime
        task = tasks_sorted.pop(0)
        task["vruntime"] = vruntime

        # Insert only if execution time is left
        if min_task["exec_time"] < min_task["burst_time"]:
            tasks_sorted.add(task)


def display_tasks(tasks: List[dict]):
    """ Print all tasks' information in a table. """
    headers = [
        "ID",
        "Arrival Time",
        "Burst Time",
        "Nice",
        "Waiting Time",
        "Turnaround Time",
    ]
    tasks_mat = []
    for task in tasks:
        tasks_mat.append(
            [
                task["pid"],
                f"{task['arrival_time'] / 1000}",
                f"{task['burst_time'] / 1000}",
                task["nice"],
                f"{task['waiting_time'] / 1000}",
                f"{task['turnaround_time'] / 1000}",
            ]
        )
    print(
        "\n"
        + tabulate(tasks_mat, headers=headers, tablefmt="fancy_grid", floatfmt=".3f")
    )
    # print('\n' + tabulate(tasks, headers='keys', tablefmt='fancy_grid'))


def find_avg_time(tasks: List[dict]):
    """ Find average waiting and turnaround time. """
    waiting_times = []
    total_wt = 0
    total_tat = 0
    num = len(tasks)
    for task in tasks:
        waiting_times.append(task["waiting_time"])
        total_wt += task["waiting_time"]
        total_tat += task["turnaround_time"]

    print(f"\nAverage waiting time: {total_wt / (num * 1000): .3f} seconds")
    print(f"Average turnaround time: {total_tat / (num * 1000): .3f} seconds")
    print(
        "Standard deviation in waiting time: "
        f"{numpy.std(waiting_times) / 1000: .3f} seconds"
    )


def reset_tasks(tasks: List[dict]):
    """ Reset task execution details. """
    for task in tasks:
        task["vruntime"] = 0
        task["exec_time"] = 0
        task["waiting_time"] = 0
        task["turnaround_time"] = 0


if __name__ == "__main__":
    MIN_VERSION = (3, 8)
    if not sys.version_info >= MIN_VERSION:
        raise EnvironmentError(
            "Python version too low, required at least "
            f'{".".join(str(n) for n in MIN_VERSION)}'
        )

    QUANTUM = 200  # Time quantum in ms
    MAX_ARRIVAL_TIME = 20_000
    MAX_BURST_TIME = 50_000
    MAX_NICE_VALUE = 10

    N = int(input("Enter number of tasks: "))
    TASKS = []

    # print('Enter ID, arrival time, burst time, nice value of processes:')
    # print('(Times should be in milliseconds)')
    for _ in range(N):
        # pid, at, bt, nice = tuple(int(x) for x in input().split())
        pid, at, bt, nice = (
            random.randint(1, N * N),
            random.randint(0, MAX_ARRIVAL_TIME),
            random.randint(0, MAX_BURST_TIME),
            random.randint(1, MAX_NICE_VALUE),
        )
        TASKS.append(
            {
                "pid": pid,
                "arrival_time": at,
                "burst_time": bt,
                "nice": nice,
                "vruntime": 0,
                "exec_time": 0,
                "waiting_time": 0,
                "turnaround_time": 0,
            }
        )

    # Sort tasks by arrival time
    TASKS_SORTED = SortedKeyList(TASKS, key=lambda task: task["arrival_time"])

    # Schedule tasks according to CFS algorithm and print average times
    reset_tasks(TASKS_SORTED)
    cfs_schedule(TASKS_SORTED, QUANTUM)
    print("\n**************** CFS SCHEDULING ****************")
    display_tasks(TASKS)
    find_avg_time(TASKS)

    # Schedule tasks according to FCFS algorithm and print average times
    reset_tasks(TASKS_SORTED)
    sched_algs.fcfs_schedule(TASKS_SORTED)
    print("\n**************** FCFS SCHEDULING ****************")
    # display_tasks(TASKS)
    find_avg_time(TASKS)

    # Schedule tasks according to SJF algorithm and print average times
    reset_tasks(TASKS_SORTED)
    sched_algs.sjf_schedule(TASKS_SORTED, QUANTUM)
    print("\n**************** SJF SCHEDULING ****************")
    # display_tasks(TASKS)
    find_avg_time(TASKS)

    # Schedule tasks according to priority algorithm and print average times
    reset_tasks(TASKS_SORTED)
    sched_algs.priority_schedule(TASKS_SORTED, QUANTUM)
    print("\n**************** PRIORITY SCHEDULING ****************")
    # display_tasks(TASKS)
    find_avg_time(TASKS)

    # Schedule tasks according to round robin algorithm and print average times
    reset_tasks(TASKS_SORTED)
    sched_algs.rr_schedule(TASKS_SORTED, QUANTUM)
    print("\n**************** ROUND ROBIN SCHEDULING ****************")
    # display_tasks(TASKS)
    find_avg_time(TASKS)
