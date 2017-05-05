"""
CMB - Discord Breencast

A Discord bot by Emzi0767. Designed to provide 24/7 Breencast in my guild.
"""

__name__ = "cmb"
__author__ = "Emzi0767"
__version__ = "1.0.1"
__license__ = "Apache License 2.0"
__copyright__ = "Copyright 2017 Emzi0767"

version_info = tuple(__version__.split("."))

# core modules
from .cmbbot import CmbBot
from .cmbbotcmd import CmbBotCommands

# utilities
from .utils import log
from .utils import logex
