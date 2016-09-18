# -*- coding: utf-8 -*-
#
# @author: Daemon Wang
# Created on 2016-03-02
#


import logging
import os,pdb

from tornado.options import parse_command_line, options, define


def parse_config_file(path):
    """Rewrite tornado default parse_config_file.

    Parses and loads the Python config file at the given path.

    This version allow customize new options which are not defined before
    from a configuration file.
    """
    config = {}
    execfile(path, config, config)
    for name in config:
        if name in options:
            options[name].set(config[name])
        else:
            define(name, config[name])


def parse_options():
    _root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    _settings = os.path.join(_root, "settings.py")
    #_settings_local = os.path.join(_root, "settings_local.py")

    try:
        parse_config_file(_settings)
        logging.info("Using settings.py as default settings.")
    except Exception, e:
        logging.error("No any default settings, are you sure? Exception: %s" % e)
    '''
    try:
        parse_config_file(_settings_local)
        logging.info("Override some settings with local settings.")
    except Exception, e:
        logging.error("No local settings. Exception: %s" % e)
    '''
    parse_command_line()
