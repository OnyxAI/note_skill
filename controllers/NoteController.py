# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
"""

from note_skill.index import note
from flask_login import login_required
from flask import render_template

from note_skill.api import *


@note.route('/' , methods=['GET','POST'])
@login_required
def index():
    return render_template('note/index.html')

@note.route('/config' , methods=['GET','POST'])
@login_required
def config():
    return render_template('note/config.html')

@note.route('/widget')
@login_required
def widget():
    return render_template('note/widget.html')
