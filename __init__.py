from os.path import dirname, join

from adapt.intent import IntentBuilder
from note_skill.api import *
from note_skill.index import note
from onyx.skills.core import OnyxSkill
from flask import current_app as app
from onyx.api.assets import Json
from onyx.util.log import getLogger

import requests

__author__ = ''

json = Json()
note_api = Note()

LOGGER = getLogger(__name__)

class NoteSkill(OnyxSkill):
    def __init__(self):
        super(NoteSkill, self).__init__(name="NoteSkill")

    def get_blueprint(self):
        return note

    def initialize(self):
        LOGGER.info("Note Skill initialize")

        self.load_data_files(dirname(__file__))
        self.init_dialog(dirname(__file__)) 
        self.load_regex_files(join(dirname(__file__), 'regex', self.lang))

        note_intent = IntentBuilder("NoteIntent")\
            .require("NoteKeyword")\
            .require("NoteText")\
            .build()

        self.register_intent(note_intent, self._handle_add)

    def _handle_add(self, message):
        user = message.data.get("user")
        text = message.data.get("NoteText")
        title = text.split(" ")[0]
        
        result = requests.post("http://localhost:5000/api/note/add", data={'title':title, 'content':text}, headers={'Authorization': 'Bearer ' + user})

        if result.json().get("status") == "success":
            self.speak_dialog("note.create", lang=self.lang)
        else:
            self.speak_dialog("note.create.error", lang=self.lang)

    def stop(self):
        pass

def create_skill():
    return NoteSkill()
