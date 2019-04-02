# _*_ coding: utf-8 _*_

"""
threads_inst_proxies.py by xianhu
"""

import time
import logging
from .multiprocess_inst_base import TPEnum, BaseMultiprocess


class ProxiesMultiprocess(BaseMultiprocess):
    """
    class of ProxiesMultiprocess, as the subclass of BaseMultiprocess
    """

    def __init__(self, name, worker, pool, max_count=100, daemon=None):
        """
        constructor
        """
        BaseMultiprocess.__init__(self, name, worker, pool, daemon)
        self._max_count = max_count
        return

    def working(self):
        """
        procedure of proxies, auto running, and return False if you need stop process
        """
        # ----2----
        proxies_state, proxies_list = self._worker.working()

        # ----3----
        for proxies in proxies_list:
            self._pool.add_a_task(TPEnum.PROXIES, proxies)

        # ----*----
        while (not self._pool.is_all_tasks_done()) and (self._pool.get_number_dict(TPEnum.PROXIES_LEFT) >= self._max_count):
            logging.debug("%s[%s] sleep 5 seconds because of too many 'PROXIES_LEFT'...", self.__class__.__name__, self.getName())
            time.sleep(5)

        # ----*----
        while self._pool.is_all_tasks_done() and (not self._pool.get_thread_stop_flag()):
            logging.debug("%s[%s] sleep 5 seconds because all tasks are done but not stop process...", self.__class__.__name__, self.getName())
            time.sleep(5)

        # ----5----
        return not (self._pool.is_all_tasks_done() and self._pool.get_thread_stop_flag())
