# _*_ coding: utf-8 _*_

"""
multiprocess_inst_save.py by YunofHD
"""

from .multiprocess_inst_base import TPEnum, BaseMultiprocess


class SaveMultiprocess(BaseMultiprocess):
    """
    class of SaveMultiprocess, as the subclass of BaseMultiprocess
    """

    def working(self):
        """
        procedure of saving, auto running, and return True
        """
        # ----1----
        url, keys, item = self._pool.get_a_task(TPEnum.ITEM_SAVE)

        # ----2----
        save_state = self._worker.working(url, keys, item)

        # ----3----
        if save_state > 0:
            self._pool.update_number_dict(TPEnum.ITEM_SAVE_SUCC, +1)
        else:
            self._pool.update_number_dict(TPEnum.ITEM_SAVE_FAIL, +1)

        # ----4----
        self._pool.finish_a_task(TPEnum.ITEM_SAVE)

        # ----5----
        return True
