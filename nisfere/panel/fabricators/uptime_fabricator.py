from utils.helpers import get_current_uptime
from fabric.core import Fabricator

uptime_fabricator = Fabricator(
    poll_from=lambda _: get_current_uptime(),
)