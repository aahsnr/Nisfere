from fabric.core import Fabricator
import time

date_fabricator = Fabricator(
    poll_from= lambda _: time
)