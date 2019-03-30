# _*_ coding: utf-8 _*_

"""
multiprocess_inst_fetch.py by YunofHD
"""

import time
import logging
from .multiprocess_inst_base import TPEnum, BaseMultiprocess


class FetchMultiprocess(BaseMultiprocess):
    """
    class of FetchMultiprocess, as the subclass of BaseMultiprocess
    """

    def __init__(self, name, worker, pool, max_count=500, daemon=None):  # name线程名称，模块名称，pool是multiorocess_pool，
        """
        constructor
        """
        BaseMultiprocess.__init__(self, name, worker, pool, daemon)
        self._max_count = max_count
        self._proxies = None
        return

    def working(self):
        """
        procedure of fetching, auto running, and return True
        """
        # ----*----
        if self._pool.get_proxies_flag() and (not self._proxies):
            self._proxies = self._pool.get_a_task(TPEnum.PROXIES)

        # ----1----
        priority, counter, url, keys, deep, repeat = self._pool.get_a_task(TPEnum.URL_FETCH)

        # ----2----
        fetch_state, fetch_result, proxies_state = self._worker.working(priority, url, keys, deep, repeat, proxies=self._proxies)

        # ----3----
        if fetch_state > 0:
            self._pool.update_number_dict(TPEnum.URL_FETCH_SUCC, +1)
            self._pool.add_a_task(TPEnum.HTM_PARSE, (priority, counter, url, keys, deep, fetch_result))
        elif fetch_state == 0:
            self._pool.add_a_task(TPEnum.URL_FETCH, (priority, counter, url, keys, deep, repeat+1))
        else:
            self._pool.update_number_dict(TPEnum.URL_FETCH_FAIL, +1)

        # ----*----
        if self._proxies and (proxies_state <= 0):
            if proxies_state == 0:
                self._pool.add_a_task(TPEnum.PROXIES, self._proxies)
            else:
                self._pool.update_number_dict(TPEnum.PROXIES_FAIL, +1)
            self._pool.finish_a_task(TPEnum.PROXIES)
            self._proxies = None

        # ----4----
        self._pool.finish_a_task(TPEnum.URL_FETCH)

        # ----*----
        while (self._pool.get_number_dict(TPEnum.HTM_PARSE_NOT) >= self._max_count) or (self._pool.get_number_dict(TPEnum.ITEM_SAVE_NOT) >= self._max_count):
            logging.debug("%s[%s] sleep 5 seconds because of too many 'HTM_PARSE_NOT' or 'ITEM_SAVE_NOT'...", self.__class__.__name__, self.getName())
            time.sleep(5)

        # ----5----
        return True
