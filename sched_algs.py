#!/usr/bin/env python3

"""
Definitions for scheduling algorithms like First Come First Served (FCFS) scheduling,
Shortest Job First (preemptive) / Shortest Remaining Time First scheduling, Priority
Scheduling (preemptive) and Round Robin Scheduling (preemptive).
"""

from typing import Callable, List, Tuple

from sortedcontainers import SortedKeyList


def fcfs_schedule(tasks: List[dict]):
    """
    Schedule tasks according to FCFS algorithm and set waiting and turnaround times.
    """

    timer = tasks[0]["arrival_time"]

    for task in tasks:
        # Set waiting and turnaround time of process
        task["waiting_time"] = timer - task["arrival_time"]
        task["turnaround_time"] = task["waiting_time"] + task["burst_time"]

        timer += task["burst_time"]


def _schedule_key(
    tasks: List[dict], quantum: int, key: Callable[[dict], Tuple[int, int, int]]
):
    """
    Schedule tasks according to algorithm determined by the key and set waiting and
    turnaround times.
    """

    tasks_sorted = SortedKeyList(key=key)
    tasks_sorted.add(tasks[0])
    end = 1
    timer = tasks[0]["arrival_time"]

    while (num := len(tasks_sorted)) > 0:
        # Add tasks that have arrived after previous iteration
        for task in tasks[end:]:
            if task["arrival_time"] <= timer:
                task["waiting_time"] = timer - task["arrival_time"]
                task["turnaround_time"] = task["waiting_time"]
                tasks_sorted.add(task)
                num += 1
                end += 1

        min_task = tasks_sorted[0]
        t_rem = min_task["burst_time"] - min_task["exec_time"]
        time = min([quantum, t_rem])

        # Increment waiting and turnaround time of all other processes
        for i in range(1, num):
            tasks_sorted[i]["waiting_time"] += time
            tasks_sorted[i]["turnaround_time"] += time

        # Remove process and execute process
        task = tasks_sorted.pop(0)
        task["exec_time"] += time
        task["turnaround_time"] += time
        timer += time

        # Insert only if execution time is left
        if task["exec_time"] < task["burst_time"]:
            tasks_sorted.add(task)


def rr_schedule(tasks: List[dict], quantum: int):
    """
    Schedule tasks according to preemptive Round Robin algorithm and set waiting and
    turnaround times.
    """

    tasks_queued = []
    tasks_queued.append(tasks[0])
    end = 1
    timer = tasks[0]["arrival_time"]

    while (num := len(tasks_queued)) > 0:
        # Add tasks that have arrived after previous iteration
        for task in tasks[end:]:
            if task["arrival_time"] <= timer:
                task["waiting_time"] = timer - task["arrival_time"]
                task["turnaround_time"] = task["waiting_time"]
                tasks_queued.append(task)
                num += 1
                end += 1

        t_rem = tasks_queued[0]["burst_time"] - tasks_queued[0]["exec_time"]
        time = min([quantum, t_rem])

        # Increment waiting and turnaround time of all other processes
        for i in range(1, num):
            tasks_queued[i]["waiting_time"] += time
            tasks_queued[i]["turnaround_time"] += time

        # Remove process and execute process
        task = tasks_queued.pop(0)
        task["exec_time"] += time
        task["turnaround_time"] += time
        timer += time

        # Insert only if execution time is left
        if task["exec_time"] < task["burst_time"]:
            tasks_queued.append(task)


def sjf_schedule(tasks: List[dict], quantum: int):
    """
    Schedule tasks according to preemptive SJF algorithm and set waiting and turnaround
    times.
    """

    get_remaining_exec_time: Callable[[dict], Tuple[int, int, int]] = lambda task: (
        task["burst_time"] - task["exec_time"],
        task["arrival_time"],
        tasks.index(task),
    )

    _schedule_key(tasks, quantum, get_remaining_exec_time)


def priority_schedule(tasks: List[dict], quantum: int):
    """
    Schedule tasks according to preemptive priority scheduling algorithm and set waiting
    and turnaround times.
    """

    get_nice: Callable[[dict], Tuple[int, int, int]] = lambda task: (
        task["nice"],
        task["arrival_time"],
        tasks.index(task),
    )

    _schedule_key(tasks, quantum, get_nice)
