from utils.helpers import get_cpu_usage, get_ram_usage, get_disk_usage
from fabric.core import Fabricator

psutil_fabricator = Fabricator(
    poll_from= lambda _: {
        "cpu_usage": get_cpu_usage(),
        "ram_usage": get_ram_usage(),
        "disk_usage": get_disk_usage()
    }
)