#!/usr/bin/env python3

import mongoengine

class Recon(mongoengine.Document):
    _id = mongoengine.StringField()
    session_id = mongoengine.StringField()
    ip_address = mongoengine.StringField()
    defaultgateway = mongoengine.StringField()
    dns = mongoengine.StringField()
    whoami = mongoengine.StringField()
    isAdmin = mongoengine.BooleanField()
    whoIsAdmin = mongoengine.ListField()

    meta = {
        'db_alias': 'core',
        'collection': 'Reconnaissance'
    }
