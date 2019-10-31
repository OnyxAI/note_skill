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
from flask import render_template, g, request, redirect, url_for, session, Response
from flask_jwt_extended import get_jwt_identity, decode_token
from onyx.decorators import api_required
from onyx.api.assets import Json
from onyx.core.controllers.api import api
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

@api.route('/note/get_all' , methods=['GET','POST'])
@api_required
def get_all():
    try:
        try:
            current_user = decode_token(session['token'])['identity']
        except:	
            current_user = get_jwt_identity()

        notes_api.user = current_user['id']

        return Response(notes_api.get_all(), mimetype='application/json')
    except Exception as e:
        print(str(e))
        return Response(json.encode({"status": "error"}), mimetype='application/json')

@note.route('/<int:_id>/<token>' , methods=['GET','POST'])
def edit_webview(_id, token):
    try:
        if decode_token(token):
            current_user = decode_token(token)['identity']

            notes_api.user = current_user['id']
            notes_api.id = _id
        
            note = json.decode(notes_api.get())

            return render_template('note/webview.html', note=note, edit=True, token=token)
        else:
            return "Invalid Token."
    except Exception as e:
        print(str(e))
        return "An error has appear. Please Reload"

@note.route('/view/<int:_id>/<token>' , methods=['GET','POST'])
def display_webview(_id, token):
    try:
        if decode_token(token):
            current_user = decode_token(token)['identity']

            notes_api.user = current_user['id']
            notes_api.id = _id
        
            note = json.decode(notes_api.get())

            return render_template('note/webview.html', note=note, edit=False, token=token)
        else:
            return "Invalid Token."
    except Exception as e:
        print(str(e))
        return "An error has appear. Please Reload"

@note.route('/edit/<int:_id>/<token>' , methods=['GET','POST'])
def edit_webview_post(_id, token):
    try:
        if request.method == 'POST': 
            
            if decode_token(token):
                
                current_user = decode_token(token)['identity']

                notes_api.user = current_user['id']
                notes_api.id = _id

                notes_api.title = request.form['title']
                notes_api.text = request.form['content']
                

                notes_api.update_note()

                return redirect(url_for('note.edit_webview', _id=_id, token=token))
            else:
                return "Invalid Token."
    except Exception as e:
        print(str(e))
        return "An error has appear. Please Reload"

@note.route('/add/<token>' , methods=['GET','POST'])
def add_webview(token):
    try:
        if decode_token(token):
            if request.method == 'GET':
                
                return render_template('note/add_webview.html', token=token)
            elif request.method == 'POST': 
                    
                current_user = decode_token(token)['identity']

                notes_api.user = current_user['id']

                notes_api.title = request.form['title']
                notes_api.text = request.form['content']
                    

                notes_api.add()

                return redirect(url_for('note.add_webview', token=token))
        else:
            return "Invalid Token."
    except Exception as e:
        print(str(e))
        return "An error has appear. Please Reload"

        
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

@api.route('/note/add' , methods=['GET','POST'])
@api_required
def add_api():
    if request.method == 'POST':
        try:
            current_user = decode_token(session['token'])['identity']
        except:	
            current_user = get_jwt_identity()

        notes_api.user = current_user['id']
        notes_api.title = request.form['title']
        notes_api.text = request.form['content']

        return notes_api.add()

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
