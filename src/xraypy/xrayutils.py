#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Xray Utils Module
"""

import sys
import logging

__author__ = "João Galego"
__copyright__ = "João Galego"
__license__ = "mit"

# General

def setup_logging(loglevel):
    """Setup basic logging

    :param loglevel (int) minimum loglevel for emitting messages
    """

    logformat = "[%(asctime)s] %(levelname)s %(name)s %(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")

# Xray

def setup_test_run_info(test_key, start_date, finish_date, status, comment):
    """Returns the test run info JSON ready for processing

    :param test_key (str) test key
    :param start_date (str) start date of the test run
    :param finish_date (str) finish date of the test run
    :param status (str) test run status e.g. PASS, FAIL
    :param comment (str) string comment
    """
    return {'testKey': test_key, \
            'start': start_date, \
            'finish': finish_date, \
            'comment': comment, \
            'status': status}

class XrayApiClientException(Exception):
    """XrayApiClient Exception"""
    pass
