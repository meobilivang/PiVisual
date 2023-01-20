import os

from typing import Tuple, Dict


def collect_cpu_usage() -> float:
    f = open("/proc/stat", "r")

    # extract 1st line, exclude 1st column
    cpu_info = [float(col) for col in f.readline().strip().split()[1:]]
    f.close()

    # Read more:
    # https://stackoverflow.com/questions/9229333/how-to-get-overall-cpu-usage-e-g-57-on-linux
    # https://www.kgoettler.com/post/proc-stat/
    (user, system, idle) = (cpu_info[0], cpu_info[2], cpu_info[3])

    current_cpu_usage = 100 * (user + system) / (user + system + idle)

    return current_cpu_usage


def collect_system_load() -> Tuple[float, float, float]:
    avg_one_min, avg_five_min, avg_fifteen_min = [
        float(elem[:-1]) for elem in os.popen("/usr/bin/uptime").read().split()[-3:]
    ]

    return avg_one_min, avg_five_min, avg_fifteen_min


def collect_system_up() -> str:
    up_duration = os.popen("/usr/bin/uptime -p").read().strip()
    up_since = os.popen("/usr/bin/uptime -s").read().strip()

    return up_duration, up_since


def collect_memory() -> Dict[str, int]:
    """
    Unit: kB
    """
    mem_info = {}
    selected_mem_metrics = {
        "MemTotal",
        "MemFree",
        "MemAvailable",
        "Buffers",
        "Cached",
        "SReclaimable",
        "Shmem",
        "SwapTotal",
        "SwapFree",
    }

    f = open("/proc/meminfo", "r")

    for line in f.readlines():
        metric_name, val = line.split()[:2]
        if metric_name[:-1] in selected_mem_metrics:
            mem_info[metric_name[:-1]] = int(val)

    # https://stackoverflow.com/questions/41224738/how-to-calculate-system-memory-usage-from-proc-meminfo-like-htop
    mem_used = mem_info["MemTotal"] - mem_info["MemFree"]
    cached_mem = mem_info["Cached"] + mem_info["SReclaimable"] + mem_info["Shmem"]
    swap = mem_info["SwapTotal"] - mem_info["SwapFree"]
    non_cached_mem = mem_used - (mem_info["Buffers"] + cached_mem)

    return mem_used, cached_mem, non_cached_mem, swap, mem_info["Buffers"]


def aggregate_metrics() -> Dict:
    mem_used, cached_mem, non_cached_mem, swap, buffers = collect_memory()
    cpu_usage = collect_cpu_usage()
    system_up_duration, system_up_since = collect_system_up()
    avg_load_one_min, avg_load_five_min, avg_load_fifteen_min = collect_system_load()

    return {
        "mem_used": mem_used,
        "cached_mem": cached_mem,
        "non_cached_mem": non_cached_mem,
        "swap": swap,
        "buffers": buffers,
        "cpu_usage": cpu_usage,
        "system_up_duration": system_up_duration,
        "system_up_since": system_up_since,
        "avg_load_one_min": avg_load_one_min,
        "avg_load_five_min": avg_load_five_min,
        "avg_load_fifteen_min": avg_load_fifteen_min,
    }
