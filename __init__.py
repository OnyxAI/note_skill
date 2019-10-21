from os.path import dirname, join

from note_skill.index import note
from onyx.skills.core import OnyxSkill
from onyx.util.log import getLogger

__author__ = ''

LOGGER = getLogger(__name__)

class NoteSkill(OnyxSkill):
    def __init__(self):
        super(NoteSkill, self).__init__(name="NoteSkill")

    def get_blueprint(self):
        return note

    def initialize(self):
        LOGGER.info("Note Skill initialize")

    def stop(self):
        pass

def create_skill():
    return NoteSkill()
