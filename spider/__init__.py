# _*_ coding: utf-8 _*_

"""
define WebSpider, and also define utilities and instances for web_spider
"""

__version__ = "1.6.2"

from .utilities import *
from .concurrent import TPEnum, WebSpider
from .multiprocess import MultiprocessWebSpider
from .instances import Fetcher, Parser, Saver, Proxieser
