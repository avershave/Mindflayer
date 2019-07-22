#!/usr/bin/env python3

import mongoengine

class ReconFiles(mongoengine.EmbeddedDocument):
    '''
    Takes in pwd files and stores them into the database
    Tracks the filesystem in the unit
    '''
    dir_name = mongoengine.StringField() # the _id will be the pwd of the dir
    files = mongoengine.ListField()
    gathered = mongoengine.BooleanField(default=False)

class Recon(mongoengine.Document):
    '''
    Takes in recon information and puts it into the database
    '''
    _id = mongoengine.StringField() # the id will be the session ID
    session_id = mongoengine.StringField()
    ip_address = mongoengine.StringField()
    defaultgateway = mongoengine.StringField()
    dns = mongoengine.StringField()
    whoami = mongoengine.StringField()
    isAdmin = mongoengine.BooleanField()
    whoIsAdmin = mongoengine.ListField()
    pwd = mongoengine.StringField()
    installedprg = mongoengine.ListField()

    directory = mongoengine.EmbeddedDocumentListField(ReconFiles)

    meta = {
        'db_alias': 'core',
        'collection': 'Reconnaissance'
    }