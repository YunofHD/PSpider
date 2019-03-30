# _*_ coding: utf-8 _*_

"""
define multiprocess_instances of url_fetch, htm_parse, item_save and proxies for multiprocess_pool
"""

from .multiprocess_inst_base import TPEnum, MonitorProcess
from .multiprocess_inst_fetch import FetchMultiprocess
from .multiprocess_inst_parse import ParseMultiprocess
from .multiprocess_inst_save import SaveMultiprocess
from .multiprocess_inst_proxies import ProxiesMultiprocess