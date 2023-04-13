from sched import scheduler
from typing import Callable
from apscheduler.schedulers.background import BackgroundScheduler

class EventsScheduler(scheduler):
    """General purpose event scheduler"""

    def call_regular_interval(
            self,
            delay: float,
            action: Callable,
            args: tuple = (),
            kwargs: dict = {}
    ):
        """register action interval"""
        def repeat(*interval_args, **interval_kwargs):
            action(*interval_args, **interval_kwargs)

            self.enter(delay, 1, repeat, interval_args, interval_kwargs)

        self.enter(delay, 1, repeat, args, kwargs)

scheduler = BackgroundScheduler()
