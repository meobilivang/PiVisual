import os

from typing import Tuple, Dict
from time import sleep


class MetricsUtils:
    def __init__(self) -> None:
        pass

    def collect_cpu_usage(self) -> float:
        # Read more:
        # https://stackoverflow.com/questions/9229333/how-to-get-overall-cpu-usage-e-g-57-on-linux
        # https://www.kgoettler.com/post/proc-stat/
        # https://rosettacode.org/wiki/Linux_CPU_utilization
        cpu_usage = float(
            os.popen(
                "/usr/bin/top -b -n1 | /usr/bin/grep 'Cpu(s)' | awk '{print $2 + $4}'"
            )
            .read()
            .strip()
        )

        return cpu_usage

    def collect_system_load(self) -> Tuple[float, float, float]:
        avg_one_min, avg_five_min, avg_fifteen_min = [
            float(elem[:-1]) for elem in os.popen("/usr/bin/uptime").read().split()[-3:]
        ]

        return avg_one_min, avg_five_min, avg_fifteen_min

    def collect_system_up(self) -> str:
        up_duration = os.popen("/usr/bin/uptime -p").read().strip()
        up_since = os.popen("/usr/bin/uptime -s").read().strip()

        return up_duration, up_since

    def collect_memory(self) -> Dict[str, int]:
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

        return (
            mem_used,
            cached_mem,
            non_cached_mem,
            swap,
            mem_info["Buffers"],
            mem_info["MemTotal"],
        )

    def disk_usage(self) -> list[Dict]:
        """Shows disk usage per drive (in Mb)"""

        # Filesystem 1M-blocks  Used  Available  Use%  Mounted on
        raw = [
            item.strip().split()
            for item in os.popen("/usr/bin/df -hm").read().splitlines()[1:]
        ]

        disk_usage_per_drive = []
        for item in raw:
            curr_disk_usage = {}

            curr_disk_usage["fs"] = item[0]
            curr_disk_usage["1M_blocks"] = item[1]
            curr_disk_usage["used"] = item[2]
            curr_disk_usage["available"] = item[3]
            curr_disk_usage["percent_use"] = item[4]
            curr_disk_usage["mounted_point"] = item[5]

            disk_usage_per_drive.append(curr_disk_usage)

        return disk_usage_per_drive

    def aggregate_metrics(self) -> Dict:
        (
            mem_used,
            cached_mem,
            non_cached_mem,
            swap,
            buffers,
            total_mem,
        ) = self.collect_memory()
        cpu_usage = self.collect_cpu_usage()
        system_up_duration, system_up_since = self.collect_system_up()
        (
            avg_load_one_min,
            avg_load_five_min,
            avg_load_fifteen_min,
        ) = self.collect_system_load()

        disk_usage_per_drive = self.disk_usage()

        return {
            "mem_used": mem_used,
            "cached_mem": cached_mem,
            "non_cached_mem": non_cached_mem,
            "swap": swap,
            "buffers": buffers,
            "total_mem": total_mem,
            "cpu_usage": cpu_usage,
            "system_up_duration": system_up_duration,
            "system_up_since": system_up_since,
            "avg_load_one_min": avg_load_one_min,
            "avg_load_five_min": avg_load_five_min,
            "avg_load_fifteen_min": avg_load_fifteen_min,
            "disk_usage": disk_usage_per_drive,
        }

    def collect_machine_info(self) -> Dict:
        model = os.popen("/usr/bin/cat /sys/class/dmi/id/product_name").read()
        host_name = os.popen("/usr/bin/cat /proc/sys/kernel/hostname").read()

        return {"model": model, "hostname": host_name}
