# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
"""
from onyx.api.exceptions import *
from onyx.extensions import db
from note_skill.models import NoteModel
from onyx.api.assets import Json
from onyx.util.log import getLogger

logger = getLogger('Note')
json = Json()


class Note:

    def __init__(self):
        self.id = None
        self.user = None
        self.text = ""
        self.title = "Undefined"
        self.folder = None

    def add(self):
        try:
            query = NoteModel.Note(user=self.user,\
                                           title=self.title,\
                                           text=self.text,\
                                           folder=self.folder)
            db.session.add(query)
            db.session.commit()
            logger.info('Note ' + self.title + ' added successfully')

            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('Note added error : ' + str(e))

    def get_all(self):
        try:
            query = NoteModel.Note.query.filter(NoteModel.Note.user.endswith(self.user)).all()
            
            notes = []

            for fetch in query:
                e = {}
                e['id'] = fetch.id
                e['title'] = fetch.title
                e['text'] = fetch.text
                e['folder'] = fetch.folder
                notes.append(e)

            return json.encode(notes)
        except Exception as e:
            logger.error('Getting notes error : ' + str(e))

    def get(self):
        try:
            query = NoteModel.Note.query.filter_by(id=self.id,user=self.user).first()
            note = {}

            note['id'] = query.id
            note['title'] = query.title
            note['text'] = query.text
            note['folder'] = query.folder

            return json.encode(note)
        except Exception as e:
            logger.error('Getting note error : ' + str(e))

    def delete(self):
        try:
            delete = NoteModel.Note.query.filter_by(id=self.id,user=self.user).first()

            db.session.delete(delete)
            db.session.commit()
            return json.encode({'status':'success'})
        except:
            return json.encode({'status':'error'})

    def update_note(self):
        try:
            update = NoteModel.Note.query.filter_by(id=self.id,user=self.user).first()
            update.title = self.title
            update.text = self.text
            update.folder = self.folder

            db.session.add(update)
            db.session.commit()
            logger.info('Note ' + update.title + ' updated')
            return json.encode({'status':'success'})

        except Exception as e:
            logger.error('Note update error : ' + str(e))
