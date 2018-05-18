#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Xray CLI"""

import argparse
import sys
import logging

from xraypy.xrayapi import XrayApiClient

from xraypy import __version__

__author__ = "João Galego"
__copyright__ = "João Galego"
__license__ = "mit"

LOGGER = logging.getLogger(__name__)

def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="XrayPy CLI")
    parser.add_argument(
        '--version',
        action='version',
        version='XrayPy {ver}'.format(ver=__version__))
    parser.add_argument(
        dest="xray_properties",
        help="Xray properties file",
        type=str,
        metavar="STRING")
    parser.add_argument(
        dest="xray_command",
        help="Xray command",
        type=str,
        metavar="STRING")
    parser.add_argument(
        '-v',
        '--verbose',
        dest="loglevel",
        help="set loglevel to INFO",
        action='store_const',
        const=logging.INFO)
    parser.add_argument(
        '-vv',
        '--very-verbose',
        dest="loglevel",
        help="set loglevel to DEBUG",
        action='store_const',
        const=logging.DEBUG)
    return parser.parse_args(args)

def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s %(name)s %(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")

def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging(args.loglevel)

    # Initialize Xray REST API client
    LOGGER.debug("Starting XrayPy...")
    xray = XrayApiClient(args.xray_properties)

    # Import JUnit results
    if args.xray_command == 'junit':
        # Get arguments
        junit_xml_report = input('JUnit XML report: ')
        project_key = input('Project Key: ')
        test_plan_key = input('Test Plan Key: ')
        test_environments = input('Test Environments: ')
        revision = input('Revision: ')
        fix_version = input('Fix Version: ')

        # Make request
        xray.import_junit_results(junit_xml_report, \
                                  project_key, \
                                  test_plan_key=test_plan_key, \
                                  test_environments=test_environments, \
                                  revision=revision, \
                                  fix_version=fix_version)

def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])

if __name__ == "__main__":
    run()
