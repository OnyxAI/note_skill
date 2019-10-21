# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
"""
from onyx.api.exceptions import *
import logging

logger = logging.getLogger()

class Note:

    def __init__(self):
        self.id = None
