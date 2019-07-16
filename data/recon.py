#!/usr/bin/env python3

import mongoengine

class Recon(mongoengine.Document):
    '''
    Takes in recon information and puts it into the database
    '''
    _id = mongoengine.StringField()
    session_id = mongoengine.StringField()
    ip_address = mongoengine.StringField()
    defaultgateway = mongoengine.StringField()
    dns = mongoengine.StringField()
    whoami = mongoengine.StringField()
    isAdmin = mongoengine.BooleanField()
    whoIsAdmin = mongoengine.ListField()
    pwd = mongoengine.ListField()

    meta = {
        'db_alias': 'core',
        'collection': 'Reconnaissance'
    }
