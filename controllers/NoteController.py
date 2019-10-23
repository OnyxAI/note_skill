# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
"""

from note_skill.index import note
from flask_login import login_required, current_user
from flask import render_template, g, request, redirect, url_for
from onyx.api.assets import Json
from note_skill.api import *

notes_api = Note()
json = Json()


@note.route('/' , methods=['GET','POST'])
@login_required
def index():
    notes_api.user = current_user.id
    json.json = notes_api.get_all()
    notes = json.decode()

    return render_template('note/index.html', notes=notes)

@note.route('/<int:_id>' , methods=['GET','POST'])
@login_required
def display(_id):
    notes_api.user = current_user.id
    notes_api.id = _id

    json.json = notes_api.get()
    note = json.decode()

    json.json = notes_api.get_all()
    notes = json.decode()

    return render_template('note/index.html', note=note, notes=notes)

@note.route('/add' , methods=['GET','POST'])
@login_required
def add():
    if request.method == 'POST':
        notes_api.user = current_user.id
        notes_api.title = request.form['title']
        notes_api.text = request.form['content']

        notes_api.add()
        return redirect(url_for('note.index'))

@note.route('/edit/<int:_id>' , methods=['GET','POST'])
@login_required
def edit(_id):
    if request.method == 'POST': 
        notes_api.user = current_user.id
        notes_api.id = _id

        notes_api.title = request.form['title']
        notes_api.text = request.form['content']

        notes_api.update_note()
        return redirect(url_for('note.display', _id=_id))

@note.route('/delete/<int:_id>' , methods=['GET','POST'])
@login_required
def delete(_id):
    if request.method == 'GET':
        notes_api.user = current_user.id
        notes_api.id = _id

        notes_api.delete()
        return redirect(url_for('note.index'))



@note.route('/config' , methods=['GET','POST'])
@login_required
def config():
    return render_template('note/config.html')

@note.route('/widget')
@login_required
def widget():
    return render_template('note/widget.html')
